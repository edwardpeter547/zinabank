from os import getenv, path
from dotenv import load_dotenv
from .base import * # noqa
from .base import BASE_DIR
from loguru import logger
from common import get_database_config
from common.startup import get_file_logger_config
import cloudinary

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': get_database_config(BASE_DIR)
}


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-vmz)cr6m%ix@08@=l2of=7ji2k$f$ju!__el34u5llgz^te#)*'
SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")

SITE_NAME = getenv("SITE_NAME")

BANK_NAME = getenv("BANK_NAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

ADMIN_URL = getenv("ADMIN_URL")

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

# SIMPLE_JWT CONFIG
SIMPLE_JWT = {
    "SIGNING_KEY": getenv("SIGNING_KEY"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# CONFIGURE DJOSER
DJOSER = {
    "USER_ID_FIELD": "id",
    "LOGIN_FIELD": "email",
    "TOKEN_MODEL": None,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",
    "SERIALIZERS": {
        "user_create": "core_apps.user_auth.serializers.UserCreateSerializer",
    }
}


# Add Celery Configuration 
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_WORKER_SEND_TASK_EVENTS = True

# Cloudinary Configuration
cloudinary.config(
    cloud_name=getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=getenv("CLOUDINARY_API_KEY"),
    api_secret=getenv("CLOUDINARY_API_SECRET")
)

COOKIE_NAME = 'access'

COOKIE_SAMESITE = 'Lax'

COOKIE_PATH = "/"

COOKIE_HTTPONLY = True

COOKIE_SECURE = getenv("COOKIE_SECURE", "True") == "True"

LOGS_DIR = path.join(BASE_DIR, "logs")

LOGGER_CONFIG = get_file_logger_config(log_directory=LOGS_DIR)

logger.configure(**LOGGER_CONFIG)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"loguru": {"class": "interceptor.InterceptHandler"}},
    "root": {"handlers": ["loguru"], "level": "DEBUG"},
}