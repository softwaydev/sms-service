import os
import os
import logging
from colorlog import ColoredFormatter

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '123'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
STATIC_URL = '/static/'

AUTH_SERVICE_CHECK_TOKEN_URL = 'http://127.0.0.1:8001/check_token/'
AUTH_SERVICE_CHECK_PERM_URL = 'http://127.0.0.1:8001/check_perm/'
AUTH_TOKEN = '123'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'sw_rest_auth.authentication.TokenServiceAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


REQUEST_LOGGING_ENABLE_COLORIZE = str2bool(os.getenv("ENABLE_COLORIZE", "False"))
DEFAULT_LOG_HANDLER = os.getenv("DEFAULT_LOG_HANDLER", "console")


class ColoredFormatter(ColoredFormatter):
    def format(self, record):
        dummy = logging.LogRecord(None, None, None, None, None, None, None)
        extra_txt = ''
        for k, v in record.__dict__.items():
            if k not in dummy.__dict__:
                extra_txt += '\n{}={}'.format(k, v)
        message = super().format(record)
        return message + extra_txt


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": "log_request_id.filters.RequestIDFilter"},
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "formatters": {
        "dev": {
            "fmt": "%(levelname)s %(asctime)s %(request_id)s %(name)s  %(pathname)s %(funcName)s %(message)s"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(levelname)s %(asctime)s %(request_id)s %(name)s  %(pathname)s %(funcName)s %(message)s",
            "json_ensure_ascii": False,
        },
        "sql": {
            "()": ColoredFormatter,
            "format": "[%(duration).3f] %(statement)s",
        },
    },
    "handlers": {
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "json",
            "filters": ["request_id"],
        },
        "dev": {
            "class": "logging.StreamHandler",
            "filters": ["request_id"],
            "formatter": "dev",
        },
    },
    "loggers": {
        "": {
            "handlers": [DEFAULT_LOG_HANDLER],
            "level": "INFO",
            "propagate": False
        },
    },
}

DEVINO_LOGIN = 'tester'
DEVINO_PASSWORD = '123'


try:
    from project.local_settings import *
except ImportError:
    print("Warning: no local_settings.py")
