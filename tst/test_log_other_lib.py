from devbooster import log

log.setup()

import logging

import requests


l = logging.getLogger("TEST_LOGGER")


def test():
    print()
    response = requests.get("http://yandex.ru")
    l.info(response.status_code)

