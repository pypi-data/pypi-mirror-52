import threading
import queue
import json
import time
import pika.exceptions as exceptions
from micropipes.shared.utils import LOG, create_mq_connection, close_mq_connection
from micropipes.shared.constants_runtime import *

MAX_BATCH_ENTRIES = 200
DEFAULT_SEND_DELAY = 10

class RuntimeClient(threading.Thread):

    def __init__(self, send_delay = DEFAULT_SEND_DELAY):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.should_work = True
        self.connection = None
        self.channel = None
        self.send_delay = send_delay
        self.logs_que = queue.Queue()
        self.stats_que = queue.Queue()

    def isReady(self):
        return (self.channel is not None)

    def run(self):
        LOG.info('Starting RuntimeClient')
        self.connection = create_mq_connection()
        if not self.connection:
            LOG.error('Failed to create mq connection - exiting')
            return
        self.prepareChannel()
        last_sent = time.time()
        while self.should_work:
            try:
                self.connection.process_data_events()
                delta = time.time() - last_sent
                if delta < self.send_delay:
                    time.sleep(0.05)
                    continue
                # logs
                entries = []
                try:
                    while self.logs_que.qsize() > 0 and len(entries) < MAX_BATCH_ENTRIES:
                        log_entry = self.logs_que.get_nowait()
                        entries.append(log_entry)
                        self.logs_que.task_done()
                except queue.Empty:
                    pass
                if len(entries) > 0:
                    self._publish_log_entries(json.dumps(entries))
                # metrics
                m_entries = []
                try:
                    while self.stats_que.qsize() > 0 and len(m_entries) < MAX_BATCH_ENTRIES:
                        m_entry = self.stats_que.get_nowait()
                        m_entries.append(m_entry)
                        self.stats_que.task_done()
                except queue.Empty:
                    pass
                if len(m_entries) > 0:
                    self._publish_stats_entries(json.dumps(m_entries))
                last_sent = time.time()
            except Exception as e:
                LOG.error(e, exc_info=True)
                if not self.channel or (self.channel.is_closed and isinstance(self.channel._closing_reason,
                                                 exceptions.ChannelClosedByBroker)):
                    self.prepareChannel()

        LOG.info('Finishing RuntimeClient')

    def _stop(self):
        try:
            LOG.debug('Trying to stop RuntimeClient')
            self.should_work = False
            self.channel = None
            close_mq_connection(self.connection)
        except Exception as e:
            LOG.error(e, exc_info=True)

    def prepareChannel(self):
        LOG.debug('RuntimeClient preparing channel')
        if self.connection and self.connection.is_closed:
            LOG.warning('Reconnecting')
            self.connection = create_mq_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=MQ_RUNTIME_EXCHANGE, exchange_type=MQ_RUNTIME_EXCHANGE_TYPE)

    def _publish_log_entries(self , entry):
        try:
            self.channel.basic_publish(
                exchange=MQ_RUNTIME_EXCHANGE, routing_key=MQ_RUNTIME_LOGS_ADD,
                body=entry)
        except Exception as e:
            LOG.error(e, exc_info=True)

    def _publish_stats_entries(self , entry):
        try:
            self.channel.basic_publish(
                exchange=MQ_RUNTIME_EXCHANGE, routing_key=MQ_RUNTIME_STATS_ADD,
                body=entry)
        except Exception as e:
            LOG.error(e, exc_info=True)

    def thread_safe_stop(self):
        try:
            if self.connection:
                self.connection.add_callback_threadsafe(self._stop)
        except Exception as e:
            LOG.error(e, exc_info=True)

    def add_log(self, worker_type, worker_id, customer_id, job_id, log_level:LogLevel, log_message):
        if not isinstance(log_level, LogLevel):
            raise TypeError('log_level must be an instance of LogLevel Enum')
        log = {
           'time': time.time(),
           'worker_type': worker_type,
           'worker_id': worker_id,
           'customer_id': customer_id,
           'job_id': job_id,
           'log_level': log_level.value,
           'message': log_message
        }
        self.logs_que.put_nowait(log)

    def add_stats(self, worker_type, worker_id, customer_id, job_id, stats_name, stats_value):
        met = {
           'time': time.time(),
           'worker_type': worker_type,
           'worker_id': worker_id,
           'customer_id': customer_id,
           'job_id': job_id,
           'stats_name': stats_name,
           'stats_value': stats_value
        }
        self.stats_que.put_nowait(met)