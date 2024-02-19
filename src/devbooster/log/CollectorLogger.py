import datetime
import logging
import threading
import traceback
from types import TracebackType
from typing import Union, Tuple, Type, Optional, Dict

from devbooster.common.MetaSingleton import MetaSingleton

_SysExcInfoType = Union[Tuple[Type[BaseException], BaseException, Optional[TracebackType]], Tuple[None, None, None]]
_ExcInfoType = Union[None, bool, _SysExcInfoType, BaseException]


class CollectorLoggerCounter(metaclass=MetaSingleton):
    def __init__(self):
        self.exceptions: Dict[str, list] = dict()
        self.errors: Dict[str, list] = dict()
        self.warnings: Dict[str, list] = dict()
        self.criticals: Dict[str, list] = dict()
        self.countLock = threading.Lock()

    def as_dict(self):
        return {
            "criticals": {k: v for k, v in self.criticals.items() if len(v) > 0},
            "errors": {k: v for k, v in self.errors.items() if len(v) > 0},
            "warnings": {k: v for k, v in self.warnings.items() if len(v) > 0},
            "exceptions": {k: v for k, v in self.exceptions.items() if len(v) > 0},
        }

    @staticmethod
    def synchro(f):
        def wrapper(*args, **kwargs):
            CollectorLoggerCounter().countLock.acquire()
            f(*args, **kwargs)
            CollectorLoggerCounter().countLock.release()

        return wrapper


class CollectorLogger(logging.Logger):

    @staticmethod
    def _now_str(frmt="%Y%m%d-%H:%M:%S.%f") -> str:
        return datetime.datetime.now().strftime(frmt)

    def __init__(self, name, level=logging.NOTSET):
        CollectorLoggerCounter().exceptions.update({name: list()})
        CollectorLoggerCounter().errors.update({name: list()})
        CollectorLoggerCounter().warnings.update({name: list()})
        CollectorLoggerCounter().criticals.update({name: list()})
        super(CollectorLogger, self).__init__(name, level)

    @CollectorLoggerCounter.synchro
    def exception(self, msg: object, *args, **kwargs):
        trc = [row.strip() for row in traceback.format_exc().split("\n")]
        CollectorLoggerCounter().exceptions.get(self.name).append({"msg": msg, "trace": trc, "ts": self._now_str()})
        return super(CollectorLogger, self).error(msg, *args, exc_info=True, **kwargs)

    @CollectorLoggerCounter.synchro
    def critical(self, msg: object, *args, **kwargs):
        CollectorLoggerCounter().criticals.get(self.name).append({"msg": msg, "ts": self._now_str()})
        return super(CollectorLogger, self).critical(msg, *args, **kwargs)

    @CollectorLoggerCounter.synchro
    def error(self, msg: object, *args, **kwargs):
        CollectorLoggerCounter().errors.get(self.name).append({"msg": msg, "ts": self._now_str()})
        return super(CollectorLogger, self).error(msg, *args, **kwargs)

    @CollectorLoggerCounter.synchro
    def warning(self, msg: object, *args, **kwargs):
        CollectorLoggerCounter().warnings.get(self.name).append({"msg": msg, "ts": self._now_str()})
        return super(CollectorLogger, self).warning(msg, *args, **kwargs)

    @CollectorLoggerCounter.synchro
    def warn(self, msg: object, *args, **kwargs):
        CollectorLoggerCounter().warnings.get(self.name).append({"msg": msg, "ts": self._now_str()})
        return super(CollectorLogger, self).warning(msg, *args, **kwargs)
