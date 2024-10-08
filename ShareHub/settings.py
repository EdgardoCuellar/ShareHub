"""
Django settings for ShareHub project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from datetime import datetime
import os
from storages.backends.s3boto3 import S3Boto3Storage


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# KEY CHANGED FOR THE PRODUCTION VERSION ON THE SERVER THIS ONE IS FOR TESTING PURPOSES
# get the secret key from ./private/secret_key.txt
SECRET_KEY = ""
with open(os.path.join(BASE_DIR, 'private/django_secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

DATABASE_PASSWORD = ""
with open(os.path.join(BASE_DIR, 'private/database_password.txt')) as f:
    DATABASE_PASSWORD = f.read().strip()

EMAIL_API_KEY = ""
with open(os.path.join(BASE_DIR, 'private/email_api_key.txt')) as f:
    EMAIL_API_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DATABASE_SQLITE = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', "nedgardo.pythonanywhere.com", "64.227.73.236", "sharehub.social", "www.sharehub.social"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'storages',
    'anymail',
    'apscheduler'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'ShareHub.urls'

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

WSGI_APPLICATION = 'ShareHub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if DATABASE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'sharehub',
            'USER': 'sharehubadmin',
            'PASSWORD': DATABASE_PASSWORD, # get the password from ./private/database_password.txt
            'HOST': 'localhost',  # Set your database host if it's not on localhost
            'PORT': '5432',          # Leave empty to use the default PostgreSQL port (5432)
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr-BE'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) # STATICFILES_DIRS
AWS_ACCESS_KEY_ID = 'DO00TJGG8YYLMU2KPXGZ'
AWS_SECRET_ACCESS_KEY = 'your-spaces-secret-access-key'
with open(os.path.join(BASE_DIR, 'private/aws_secret_access_key.txt')) as f:
    AWS_SECRET_ACCESS_KEY = f.read().strip()
AWS_STORAGE_BUCKET_NAME = 'sharehub'
AWS_S3_ENDPOINT_URL = 'https://ams3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read' # This will make sure that the uploaded files are public and can be accessed without any authentication.
AWS_QUERYSTRING_AUTH = False # This will make sure that the file URL does not have unnecessary parameters like your access key.

AWS_STATIC_LOCATION = 'static'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, AWS_STATIC_LOCATION),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_STATIC_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

AWS_MEDIA_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_MEDIA_LOCATION) 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Email settings
ANYMAIL = {
    "MAILGUN_API_KEY": EMAIL_API_KEY,
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
    "MAILGUN_SENDER_DOMAIN": "sharehub.social",
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = 'ShareHub <no-reply@sharehub.social>' 
# SERVER_EMAIL = 'postmaster@sharehub.social'


# CACHE PERFORMANCES TO DO IT TIME
# if DEBUG:
#     CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
#         "LOCATION": "127.0.0.1:11211",
#         }
#     }

# else:
#     CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
#         "LOCATION": [
#             "172.19.26.240:11211",
#             "172.19.26.242:11211",
#         ],
#         }
#     }


# settings.py

# Set the logging configuration
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

log_file_name = datetime.now().strftime('%d%m%Y_%H%M%S') + '_error.log'
log_file_path = os.path.join(LOGGING_DIR, log_file_name)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': log_file_path,
        },
        # Add other handlers if needed
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

