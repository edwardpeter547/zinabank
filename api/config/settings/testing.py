from os import getenv, path
from dotenv import load_dotenv
from .base import * #noqa
from .base import BASE_DIR
from loguru import logger
from common import get_database_config
from common.startup import get_stdout_logger_config

test_env_file = path.join(BASE_DIR, "envs", ".env.test")

if path.isfile(test_env_file):
    load_dotenv(test_env_file)

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



SECRET_KEY = getenv("SECRET_KEY")

DEBUG = True

SITE_NAME = "test site"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = "test@example.com"
DOMAIN = "testserver"

DATABASES = {
    'default': get_database_config(BASE_DIR)
}

LOGGER_CONFIG = get_stdout_logger_config()

logger.configure(**LOGGER_CONFIG)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"loguru": {"class": "interceptor.InterceptHandler"}},
    "root": {"handlers": ["loguru"], "level": "ERROR"},
}
