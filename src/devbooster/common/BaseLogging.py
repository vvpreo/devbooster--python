import logging


class BaseLogging:
    __logger_name__ = 'XXX'

    def __init__(self):
        self.logger = logging.getLogger(self.__logger_name__)
