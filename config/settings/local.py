from .base import *
from .base import INSTALLED_APPS, MIDDLEWARE

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
