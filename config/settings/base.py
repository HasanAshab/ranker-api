"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import (
    default_headers,
)
from environ import Env
from command_scheduler.enums import ScheduleType
from command_scheduler.utils import args


SITE_ID = 1

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SILENCED_SYSTEM_CHECKS = ["rest_framework.W001"]

ENV_FILE = ".env"
Env.read_env(BASE_DIR / ENV_FILE)
env = Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1"]


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "notifications",
    "django_filters",
    "django_extensions",
    "phonenumber_field",
    "colorfield",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "drf_standardized_response",
    "drf_standardized_errors",
    "drf_pagination_meta_wrap",
    "knox",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.mfa",
    "allauth.headless",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.twitter",
]

LOCAL_APPS = [
    "command_scheduler",
    "ranker.common",
    "ranker.authentication",
    "ranker.accounts",
    "ranker.users",
    "ranker.recent_searches",
    "ranker.level_titles",
    "ranker.difficulties",
    "ranker.challenges",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Mail
DEFAULT_FROM_EMAIL = "ranker.noreply@gmail.com"

# User Model
AUTH_USER_MODEL = "users.UserModel"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"


# Log
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        #         "db_query": {
        #             "level": "DEBUG",
        #             "class": "logging.FileHandler",
        #             "filename": "tmp/logs/db_queries.log",
        #         },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = (
    *default_headers,
    "X-Session-Token",
    "location",
)

# Rest Framework
REST_FRAMEWORK = {
    # API Versioning
    "DEFAULT_VERSION": "v1",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    # Auth
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
    # Exception
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    # Response
    "DEFAULT_RENDERER_CLASSES": (
        "drf_standardized_response.renderers.StandardizedJSONRenderer",
    ),
    # Pagination
    "PAGE_SIZE": 15,
    # Test
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    # Docs
    "DEFAULT_SCHEMA_CLASS": "ranker.docs.openapi.AutoSchema",
}

# Api Docs
SPECTACULAR_SETTINGS = {
    "TITLE": "Ranker",
    "DESCRIPTION": "The api documentation of Ranker-API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "EXTERNAL_DOCS": {
        "url": "https://allauth.org/docs/draft-api",
        "description": "Authentication",
    },
    "SCHEMA_PATH_PREFIX": r"/api/",
    "ENUM_NAME_OVERRIDES": {
        "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices",
        "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices",
        "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices",
        "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices",
        "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices",
        "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices",
        "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices",
        "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices",
        "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices",
        "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices",
        "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices",
    },
    "POSTPROCESSING_HOOKS": (
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums",
    ),
}

# Knox (For Auth Token Management)
REST_KNOX = {
    "TOKEN_TTL": timedelta(days=20),
    "AUTH_HEADER_PREFIX": "Bearer",
}
KNOX_TOKEN_MODEL = "knox.AuthToken"


# All-Auth
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
MFA_TOTP_ISSUER = "Ranker"
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env("GOOGLE_CLIENT_ID"),
            "secret": env("GOOGLE_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": ["profile", "email", "name"],
    },
    "facebook": {
        "APP": {
            "client_id": env("FACEBOOK_CLIENT_ID"),
            "secret": env("FACEBOOK_CLIENT_SECRET"),
            "key": "",
        },
    },
    "twitter": {
        "APP": {
            "client_id": env("TWITTER_CLIENT_ID"),
            "secret": env("TWITTER_CLIENT_SECRET"),
            "key": "",
        },
    },
}
# All-Auth : Headless
FRONTEND_BASE_URL = "https://ranker.com"
HEADLESS_ONLY = True
HEADLESS_TOKEN_STRATEGY = "ranker.authentication.tokens.SessionTokenStrategy"
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": FRONTEND_BASE_URL + "/account/verify-email/{key}",
    "account_reset_password_from_key": FRONTEND_BASE_URL
    + "/account/password/reset/{key}",
}


# Command Scheduler

SCHEDULED_COMMANDS = [
    {
        "enabled": True,
        "schedule": ScheduleType.DAILY,
        "command": "update_ranking",
        "args": args(chunk=1000),
    },
    {
        "enabled": True,
        "schedule": ScheduleType.DAILY,
        "command": "reset_repeated_challenges",
        "args": args("D", chunk=1000),
    },
    {
        "enabled": True,
        "schedule": ScheduleType.WEEKLY,
        "task": "reset_repeated_challenges",
        "args": ["W"],
        "args": args("W", chunk=1000),
    },
    {
        "enabled": True,
        "schedule": ScheduleType.MONTHLY,
        "task": "reset_repeated_challenges",
        "args": args("M", chunk=1000),
    },
]

# Ranker

# ranker.authentication
TOKEN_LOGIN_SALT = env("TOKEN_LOGIN_SALT")
TOKEN_LOGIN_MAX_AGE = 5  # seconds

# ranker.common
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE_SID = env("TWILIO_VERIFY_SERVICE_SID")

GROQ_API_KEY = env("GROQ_API_KEY")

# ranker.users
USERNAME_MAX_LENGTH = 35
USERNAME_MAX_SUGGESTIONS = 3
USERNAME_GENERATION_MAX_ATTEMPTS = 10

XP_PER_LEVEL = 1000
