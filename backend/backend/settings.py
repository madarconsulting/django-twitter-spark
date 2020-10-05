"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import platform
from configparser import RawConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Loading settings.ini file with PostgreSQL database credentials
config = RawConfigParser()
config.read(BASE_DIR + '/settings.ini')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y21d7$0uroh@zaen$5k#h38ivnpy_safw#gp-+m0)z5ms1amf6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'accounts',
    'users',
    'api',
    'udf',
    'rest_framework',
    'drf_yasg'
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config.get('postgresdbConf', 'DB_ENGINE'),
        'NAME': config.get('postgresdbConf', 'DB_NAME'),
        'USER': config.get('postgresdbConf', 'DB_USER'),
        'PASSWORD': config.get('postgresdbConf', 'DB_PASS'),
        'HOST': config.get('postgresdbConf', 'DB_HOST'),
        'PORT': config.get('postgresdbConf', 'DB_PORT'),
    }
}

AUTH_USER_MODEL = 'users.CustomUser'


###################################################################
##### Tweepy CONFIG
###################################################################

CONSUMER_KEY = config.get('tweepyConf', 'CONSUMER_KEY') 
CONSUMER_SECRET = config.get('tweepyConf', 'CONSUMER_SECRET') 
ACCESS_TOKEN = config.get('tweepyConf', 'ACCESS_TOKEN') 
ACCESS_TOKEN_SECRET = config.get('tweepyConf', 'ACCESS_TOKEN_SECRET') 

###################################################################
##### Spark CONFIG
###################################################################

SPARK_WORKERS = config.get('sparkConf', 'SPARK_WORKERS')
SPARK_UDF_FILE = BASE_DIR + config.get('sparkConf', 'SPARK_UDF_FILE')
SPARK_EXECUTOR_MEMORY = str(config.get('sparkConf', 'SPARK_EXECUTOR_MEMORY'))
SPARK_EXECUTOR_CORES = str(config.get('sparkConf', 'SPARK_EXECUTOR_CORES'))
SPARK_CORE_MAX = str(config.get('sparkConf', 'SPARK_CORE_MAX'))
SPARK_DRIVER_MEMORY = str(config.get('sparkConf', 'SPARK_DRIVER_MEMORY'))

###################################################################
##### TASS CONFIG
###################################################################

TASS_FILES_LIST = config.get('tassConf', 'TASS_FILES_LIST')

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config.get('timeZone', 'TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
if(platform.system() == 'Windows'):
    STATICFILES_DIRS = (BASE_DIR + '/static'),
elif(platform.system() == 'Linux'):
    STATICFILES_DIRS = (BASE_DIR + STATIC_URL),

###################################################################
##### LOGGING CONFIG 
###################################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'standard': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/logs/default.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'debug_file': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/logs/debug.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'warning_file': {
            'level':'WARNING',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/logs/warning.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'info_file': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/logs/info.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'error_file': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/logs/error.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'emails': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/logs/emails.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'debug_logger': {
            'handlers': ['debug_file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'info_logger': {
            'handlers': ['info_file'],
            'level': 'INFO',
            'propagate': True
        },
        'error_logger': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.request': {
            'handlers': ['default', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'emails': {
            'handlers': ['emails'],
            'level': 'DEBUG',
            'propagate': True
        },

    }
}

###################################################################
##### REST_FRAMEWORK CONFIG 
###################################################################

REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.coreapi.AutoSchema' }

'''
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
    )
    ],
}
'''

###################################################################
##### Simplejwt CONFIG
###################################################################

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

###################################################################
##### Simplejwt CONFIG
###################################################################


# Frontend client port
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]