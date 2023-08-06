from enum import Enum
import logging

MQ_RUNTIME_EXCHANGE = 'runtime'
MQ_RUNTIME_EXCHANGE_TYPE: str = 'topic'
MQ_RUNTIME_COLLECTOR_REDIS_QUEUE = 'micropipes.runtime_collector.redis'

MQ_RUNTIME_LOGS_ADD = 'runtime.logs.add'
MQ_RUNTIME_STATS_ADD = 'runtime.stats.add'

MQ_RUNTIME_BINDINGS = [MQ_RUNTIME_LOGS_ADD, MQ_RUNTIME_STATS_ADD]


_levelToName = {
    logging.DEBUG: 'DEBUG',
    logging.INFO: 'INFO',
    logging.WARNING: 'WARNING',
    logging.ERROR: 'ERROR',
    logging.CRITICAL: 'CRITICAL'
}

_nameToLevel = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @staticmethod
    def from_str(level:str):
        return _nameToLevel[level.upper()]

    @staticmethod
    def to_str(level):
        return _levelToName[level]
