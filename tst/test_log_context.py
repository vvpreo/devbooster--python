from devbooster import log
from devbooster.log import context_vars

log.settings.DEVBOOSTER_LOGGING_CONTEXT_VARS=["context_var_1:HELLO", "context_var_2:WORLD"]
log.settings.DEVBOOSTER_LOGGING_BASE_FORMAT = '%(asctime)s - %(levelname)8s - %(threadName)s - %(name)s - %(message)s - %(context_var_1)s - %(context_var_2)s'
log.setup()

import logging

l = logging.getLogger("TEST_LOGGER")


def test():
    print()
    l.critical("msg")
    context_vars["context_var_1"] = lambda : "GOODBYE"
    l.critical("msg")
