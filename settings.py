import os
import pathlib

DEBUG = bool(os.environ.get("DEBUG", False))
SQL_DEBUG = os.environ.get("SQL_DEBUG", DEBUG)

BASE_PATH = pathlib.Path(__file__).parent

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", 1414))
APP_TITLE = "GodMode 2"
APP_LOGO = "<strong>God</strong>Mode 2"
APP_DSN = "sqlite:///godmode/database/godmode.sqlite"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simpleFormatter": {
            "format": "%(asctime)s %(levelname)-8s %(module)s : %(message)s"
        },
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "formatter": "simpleFormatter",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["consoleHandler"]
        },
    }
}

CONNECTION_STRING = ""
TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""
TELEGRAM_CHANNEL_ID = ""

try:
    from local_settings import *
except ImportError:
    pass
