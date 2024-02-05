import logging
import threading
from threading import Thread
from time import sleep

from devbooster.common import now_ts
from devbooster.common.MetaSingleton import MetaSingleton
from devbooster.log.root_logger_filter import DevboosterRootLoggerFilter
from devbooster.log.settings import DEVBOOSTER_LOGGING_TICKER_ON, DEVBOOSTER_LOGGING_TICKER_SECS_INTERVAL


class Ticker(Thread, metaclass=MetaSingleton):
    """
    CLass to make easier debug applications where is important to track time for different events.
    It gives visual perception of delays between events
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("ticker")
        self.name = "ticker"
        self.tick_interval = DEVBOOSTER_LOGGING_TICKER_SECS_INTERVAL  # sec
        self.daemon = True
        self.enabled = DEVBOOSTER_LOGGING_TICKER_ON

    def run(self):
        DevboosterRootLoggerFilter.ticker_thread_id = threading.current_thread().native_id
        while True:
            ticked_so_far = now_ts() - DevboosterRootLoggerFilter.last_msg_ts
            ticked_so_far = round(ticked_so_far, 3)
            if ticked_so_far > self.tick_interval:
                self.logger.debug(f"TICKED secs: {ticked_so_far}")
            sleep(self.tick_interval)

    def start(self) -> None:
        self.logger.debug("Started")
        super(Ticker, self).start()
