import logging

from devbooster.log.CollectorLogger import CollectorLoggerCounter, CollectorLogger

logging.setLoggerClass(CollectorLogger)

logging.basicConfig(level=logging.DEBUG, force=True)

l = logging.getLogger("TEST_LOGGER")


def test_exc():
    print()

    try:
        "abc"[3]
    except Exception:
        l.exception("exception message")
    assert CollectorLoggerCounter().exceptions.get("TEST_LOGGER")[0]["msg"] == "exception message"


def test_warnings():
    print()

    l.warning("AAA")
    assert CollectorLoggerCounter().warnings.get("TEST_LOGGER")[0]["msg"] == "AAA"


def test_errors():
    print()

    l.error("AAA")
    assert CollectorLoggerCounter().errors.get("TEST_LOGGER")[0]["msg"] == "AAA"


def test_criticals():
    print()

    l.critical("AAA")
    assert CollectorLoggerCounter().criticals.get("TEST_LOGGER")[0]["msg"] == "AAA"
