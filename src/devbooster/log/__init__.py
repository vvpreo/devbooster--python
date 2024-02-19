import os
from typing import Optional, Dict, Any

import yaml

from devbooster.common import get_proc_name
from devbooster.log.settings import \
    DEVBOOSTER_LOGGING_FOLDER, \
    DEVBOOSTER_LOGGING_LEVEL, \
    DEVBOOSTER_LOGGING_CONFIG_FILE, \
    DEVBOOSTER_LOGGING_LOGGER_CLASS


def get_config() -> Optional[Dict[str, Any]]:
    if DEVBOOSTER_LOGGING_CONFIG_FILE is None:
        return get_custom_config()
    else:
        with open(DEVBOOSTER_LOGGING_CONFIG_FILE, 'rt', encoding='utf8') as f:
            log_config = yaml.safe_load(f)
        return log_config


def get_custom_config() -> Optional[Dict[str, Any]]:
    return None


def _get_config_default() -> dict:
    from .settings import DEVBOOSTER_LOGGING_BASE_FORMAT, DEVBOOSTER_LOGGING_JSONED_DEFAULT
    return {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': DEVBOOSTER_LOGGING_BASE_FORMAT \
                    if not DEVBOOSTER_LOGGING_JSONED_DEFAULT else '%(jsoned)s',
            },
            'jsoned': {
                'format': '%(jsoned)s'
            },
        },
        'handlers': {
            'stderr': {
                'level': DEVBOOSTER_LOGGING_LEVEL,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                # 'stream': 'ext://sys.stdout',
                'stream': 'ext://sys.stderr',
            },
            'proc_rollover': {
                'level': DEVBOOSTER_LOGGING_LEVEL,
                'formatter': 'jsoned',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': "/".join([DEVBOOSTER_LOGGING_FOLDER, f"{get_proc_name()}_log.yml"]),
                'when': 'h',
                'interval': 1,
                'backupCount': 7 * 24,
            },

        },
        'loggers': {
            '': {  # root logger
                'handlers': ['stderr'],
                'level': DEVBOOSTER_LOGGING_LEVEL,
                'propagate': False
            },
        }
    }


context_vars: Dict[str, Any] = {}


def setup():
    """
    DO NOT FORGET THAT YOU MUST SETUP LOGGING MODULE FIRST IN EACH PYTHON PROCESS YOU RUN
    :return:
    """
    print()
    from devbooster.log.root_logger_filter import DevboosterRootLoggerFilter
    root_logger = DevboosterRootLoggerFilter

    os.makedirs(os.path.join(DEVBOOSTER_LOGGING_FOLDER), exist_ok=True)

    for var in settings.DEVBOOSTER_LOGGING_CONTEXT_VARS:
        splitted = var.split(":")
        nm = splitted[0]

        def first_val_foo(fv: str = splitted[1]):
            return fv

        context_vars.update({nm: first_val_foo})
        setattr(root_logger, var, property(context_vars.get(var)))

    from logging import config

    config.dictConfig(get_config() or _get_config_default())

    import logging
    logging.setLoggerClass(DEVBOOSTER_LOGGING_LOGGER_CLASS)

    root_logger().setup()

    logger = logging.getLogger("lg")
    logger.info("Realtalk Logger setup DONE")
