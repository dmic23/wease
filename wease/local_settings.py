#import dj_database_url
from settings import BASE_DIR
import os
import sys

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

ADMINS = (
    ('Daniel Micaletti', 'danielmicaletti@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

UPLOAD_FILE_PATTERN = "uploads/%s_%s"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.

# URL prefix for static files. #header .logo img{margin-left:-30px;}

STATIC_URL = '/static/build/development/'

MEDIA_URL = '/static/build/development/media/'

MEDIA_ROOT = 'static/build/development/media/'

STATICFILES_DIRS = (
	# os.path.join(BASE_DIR, 'static/build/production'),
    os.path.join(BASE_DIR, 'static/build/development'),
)

from .email_info import EMAIL_BACKEND, EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT

SWAMP_DRAGON_CONNECTION = ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data')
DRAGON_URL = 'http://localhost:9999/'

BROKER_URL = 'redis://localhost:6379/0'

