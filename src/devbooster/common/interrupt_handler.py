import signal
from typing import Set


class InterruptHandler:

    def __init__(self):
        self._interrupted = False
        _add_handler(self)

    def _sigint_handler(self, frame):
        # print(f'{self} caught SIGINT')
        self._interrupted = True

    def not_interrupted(self) -> bool:
        return not self._interrupted

    def interrupted(self) -> bool:
        return self._interrupted


_handlers: Set[InterruptHandler] = set()


def _add_handler(handler: InterruptHandler):
    _handlers.add(handler)


def _signal_dispatcher(signum, frame):
    signame = signal.Signals(signum).name
    if signum == signal.SIGINT:
        for handler in _handlers:
            handler._sigint_handler(frame)
    else:
        raise ValueError(f'Unhandled signal {signame} ({signum})')


signal.signal(signal.SIGINT, _signal_dispatcher)
# signal.signal(signal.SIGKILL, _signal_dispatcher)
