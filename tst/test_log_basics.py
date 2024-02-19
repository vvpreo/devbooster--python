import logging

from devbooster import log

log.setup()

l = logging.getLogger("TEST_LOGGER")


def test():
    print()
    print(f"CURRENT LOG LEVEL: {log.DEVBOOSTER_LOGGING_LEVEL}")
    l.debug(f"TEST DEBUG OK {logging.DEBUG}")
    l.info(f"TEST INFO OK {logging.INFO}")
    l.warning(f"TEST WARNING OK {logging.WARNING}, {logging.WARN}")
    l.error(f"TEST ERROR OK {logging.ERROR}")
    l.critical(f"TEST CRITITCAL OK {logging.CRITICAL}")
