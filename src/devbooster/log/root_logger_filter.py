import json
import logging
import threading
from typing import Any, Dict

from devbooster.common import now_ts
from devbooster.common.MetaSingleton import MetaSingleton
from devbooster.log import context_vars
from devbooster.log.settings import DEVBOOSTER_LOGGING_JSONED_DEFAULT, DEVBOOSTER_LOGGING_EXCLUDE_PROCESSES


class JsonEncoderUnknownToString(json.JSONEncoder):
    def default(self, obj):
        return str(obj)


class DevboosterRootLoggerFilter(logging.Filter, metaclass=MetaSingleton):
    ticker_thread_id = None
    last_msg_ts: float = 0.0

    def __init__(self):
        super().__init__()
        self.setup_done = False

    def setup(self):
        """
        Переопределение базового фильтра для добавления дополнительных элементов
        :return: None
        """
        if not self.setup_done:
            old_get_logger = logging.getLogger

            def getLogger(name: str = None) -> logging.Logger:
                logger = old_get_logger(name)
                logger.addFilter(self)
                return logger

            logging.getLogger = getLogger

    def filter(self, record: logging.LogRecord) -> bool:
        # Check if log for given process:
        if record.processName in DEVBOOSTER_LOGGING_EXCLUDE_PROCESSES:
            return False

        # Set context if any
        for name, foo in context_vars.items():
            setattr(record, name, foo())

        # Check if it is ticker
        if DevboosterRootLoggerFilter.ticker_thread_id != threading.current_thread().native_id:
            DevboosterRootLoggerFilter.last_msg_ts = now_ts()

        # Check if needed to jsonyfy
        if DEVBOOSTER_LOGGING_JSONED_DEFAULT:
            record.jsoned = json.dumps(self._get_dicted(record), ensure_ascii=False, cls=JsonEncoderUnknownToString)

        return True

    def _get_dicted(self, record: logging.LogRecord) -> Dict[str, Any]:
        d = {
            "name": str(record.name),
            "msg": str(record.msg),
            "args": str(record.args),
            "levelname": record.levelname,
            "levelno": record.levelno,
            "pathname": record.pathname,
            "filename": record.filename,
            "module": record.module,
            "exc_info": str(record.exc_info),
            "exc_text": str(record.exc_text),
            "stack_info": str(record.stack_info),
            "lineno": record.lineno,
            "funcName": record.funcName,
            "created": record.created,
            "msecs": record.msecs,
            "relativeCreated": record.relativeCreated,
            "thread": record.thread,
            "threadName": record.threadName,
            "processName": record.processName,
            "process": record.process,
        }
        for name in context_vars.keys():
            d[name] = getattr(record, name)
        return d
