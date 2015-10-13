"""
Django settings for wease project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#import dj_database_url
import urlparse
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Daniel Micaletti', 'danielmicaletti@gmail.com'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't(m_$z02(o_#3$=7y-w_j-053f4wvvp%qm_(%=piqy6*f!e47y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'storages',
    'boto',
    'rest_framework',
    'djcelery',
    'widget_tweaks', 
    'swampdragon',
    'eventlog',
    'authentication',
    'orders', 
    'messaging',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)



ROOT_URLCONF = 'wease.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
		'django.contrib.auth.context_processors.auth',
		'django.core.context_processors.request',
		"django.core.context_processors.debug",
		"django.core.context_processors.i18n",
		"django.core.context_processors.media",
		"django.core.context_processors.static",
		"django.core.context_processors.tz",
		"django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'wease.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wease',
	'USER': 'wease_admin',
	'PASSWORD': 'WeASeAdmin2015',
	'HOST': 'localhost',
	'PORT': '',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

LOGIN_URL = 'wease.fr'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/staticfiles/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

#MEDIA_URL = '/media/'

#MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles/media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

UPLOAD_FILE_PATTERN = 'uploads/%s_%s'

REST_FRAMEWORK = {
    'UPLOADED_FILES_USE_URL': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['wease.fr', 'wease.eu', '188.166.28.225',]

AUTH_USER_MODEL = 'authentication.Account'

try:
   from local_settings import *
except ImportError, e:
   print "error message=++ %s" % e.message
   pass

if not DEBUG:  
    AWS_ACCESS_KEY_ID = 'AKIAJ4NZ3DZXDBPNRZ6Q'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'weaseprod'
    AWS_PRELOAD_METADATA = True  
#    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
#    STATIC_URL = S3_URL
    MEDIA_URL = S3_URL
    # SwampDragon settings
    SWAMP_DRAGON_CONNECTION = ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data')
    DRAGON_URL = 'http://188.166.28.225:3000'
    SWAMP_DRAGON_HOST = '127.0.0.1'
    SWAMP_DRAGON_PORT = 9000

from .email_info import EMAIL_BACKEND, EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT
# For gmail and google apps
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = os.environ.get('EMAIL_PORT')
