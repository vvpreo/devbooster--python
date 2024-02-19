import time

from devbooster.common.idle import get_proc_busy


def test_proc_idle():
    time.sleep(1)
    print()
    print(get_proc_busy()) # this one must be very small: 0.00xxxx
    print(get_proc_busy()) # this one must be close to 1.0
