from time import sleep

from devbooster import log
from devbooster.common import get_proc_name
from devbooster.log import DEVBOOSTER_LOGGING_FOLDER

config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {'standard': {'format': '%(jsoned)s'}, 'jsoned': {'format': '%(jsoned)s'}, },
    'handlers': {
        'stderr': {
            'level': 0,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
        'proc_rollover': {
            'level': 0,
            'formatter': 'jsoned',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': "/".join([DEVBOOSTER_LOGGING_FOLDER, f"{get_proc_name()}_log.yml"]),
            'when': 's',
            'interval': 1,
            'backupCount': 10,
        },

    },
    'loggers': {'': {'handlers': ['stderr', 'proc_rollover'], 'propagate': False, 'level': 0}, }
}

log._get_config_default = lambda: config

log.setup()

import logging

l = logging.getLogger("TEST_LOGGER")


def test():
    print()

    for i in range(10):
        l.info(f"iteration # {i}")
        sleep(1)
