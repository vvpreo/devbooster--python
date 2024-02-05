import logging
from functools import wraps

from devbooster.common import now_ts
from devbooster.log.settings import DEVBOOSTER_LOGGING_TIMER_LEVEL

time_logger = logging.getLogger("timer")

if DEVBOOSTER_LOGGING_TIMER_LEVEL is None:
    level = logging.INFO
else:
    level = int(DEVBOOSTER_LOGGING_TIMER_LEVEL)


def log_time(func):
    """This decorator logs execution time for decorated functions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = now_ts()
        result = func(*args, **kwargs)
        end = now_ts()
        t = round((end - start) * 1000, 3)
        time_logger.log(level, f"{func.__name__}, ({t}), with {args=}, {kwargs=}")
        return result

    return wrapper
