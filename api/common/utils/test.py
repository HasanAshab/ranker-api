import os
from unittest.mock import Mock
from contextlib import contextmanager
from django.conf import settings


def fake_file(name, mode="rb"):
    return open(
        os.path.join(
            settings.STATIC_ROOT,
            "test",
            name,
        ),
        mode=mode,
    )


@contextmanager
def catch_signal(signal):
    handler = Mock()
    signal.connect(handler)
    yield handler
    signal.disconnect(handler)
