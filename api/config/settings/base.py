
import sys
from datetime import timedelta, date
from pathlib import Path
from dotenv import load_dotenv
from os import path
from common import get_database_config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


APPS_DIR = BASE_DIR / "core_apps"


local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
    "phonenumber_field",
    "drf_spectacular",
    "corsheaders",
    "djoser",
    "cloudinary",
    "django_filters",
    "djcelery_email",
    "django_celery_beat",

]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.user_auth",
    "core_apps.user_profile",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core_apps.user_auth.middleware.CustomHeaderMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': get_database_config(BASE_DIR)
}

BANK_NAME = "Zina Bank"

ADMIN_URL = "testurl/"

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "user_auth.User"

DEFAULT_BIRTH_DATE = date(1900, 1, 1)
DEFAULT_DATE = date(2000, 1, 1)
DEFAULT_EXPIRY_DATE = date(2025, 1, 1)
DEFAULT_COUNTRY = "GB"
DEFAULT_PHONE_NUMBER = "+447788643944"
MAX_DIGITS = 12
DECIMAL_PLACES = 2
DEFAULT_AMOUNT = "0.00"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core_apps.common.cookie_auth.CookieAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": [
        "rest_framework.pagination.PageNumberPagination",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "50/day",
        "user": "100/day"
    }
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Zina Bank API",
    "DESCRIPTION": "An API built for a banking system",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "LICENSE": {
        "name": "MIT License",
        "url": "https://opensource.org/license/mit",
    }
}

LOGGING_CONFIG = None

MAX_UPLOAD_SIZE = 1 * 1024 * 1024

LOCKOUT_DURATION = timedelta(minutes=1)

LOGIN_ATTEMPTS = 3

OPT_EXPIRATION  = timedelta(minutes=1)