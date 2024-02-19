import devbooster.log

devbooster.log.settings.DEVBOOSTER_LOGGING_JSONED_DEFAULT = True
devbooster.log.settings.DEVBOOSTER_LOGGING_CONTEXT_VARS = ["context_var_1:v1", "context_var_2:v2"]

devbooster.log.setup()

import logging

l = logging.getLogger("TEST_LOGGER")


def test():
    print()

    l.debug("TEST DEBUG OK")
    l.info("TEST INFO OK")
    l.warning("TEST WARNING OK")
    l.error("TEST ERROR OK")
    l.critical("TEST CRITITCAL OK")
