from devbooster import log

log.setup()

from devbooster.log import settings, ticker

import logging
from time import sleep

l = logging.getLogger("TEST_LOGGER")


def test():
    print()
    settings.RT_LOGGING_TICKER_ON = True
    ticker.Ticker().start()
    sleep(1)
    l.info("One sec passed")
    sleep(1)
    l.info("Another one sec passed")
