from unittest.mock import Mock
from contextlib import contextmanager


@contextmanager
def catch_signal(signal):
    handler = Mock()
    signal.connect(handler)
    yield handler
    signal.disconnect(handler)
