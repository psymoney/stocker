from .base import *


# Turn DEBUG mod
DEBUG = True

ALLOWED_HOSTS = []

logger_setting = {
    "handlers": ["console"],
    "level": "DEBUG",
}

LOGGING["loggers"].setdefault("apps", logger_setting)
