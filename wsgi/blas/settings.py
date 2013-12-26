"""
Django settings for openshift project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import imp

ON_OPENSHIFT = False
if 'OPENSHIFT_REPO_DIR' in os.environ:
    ON_OPENSHIFT = True

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
default_keys = { 'SECRET_KEY': 'tjy&7h%c=q01+c5i@_-t)&n2c+y*tn7v_)vbdksnlv@s5qh%e_' }
use_keys = default_keys
if ON_OPENSHIFT:
    imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)

SECRET_KEY = use_keys['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if ON_OPENSHIFT:
    #developer mode
    DEBUG = True
    #DEBUG = False
else:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
     os.path.join(BASE_DIR,'templates'),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if 'DJANGO_DB_ENGINE' in os.environ:
    print("DJANGO_DB_ENGINE detected")
    DB_ENGINE = os.environ['DJANGO_DB_ENGINE']
else:
    print("DJANGO_DB_ENGINE NOT detected")
    DB_ENGINE = 'sqlite'

if DB_ENGINE == 'sqlite':
    print("Using sqlite3 as DB engine.")
    DB_ENGINE = 'django.db.backends.sqlite3'
    DB_USER = ''
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_PORT = ''
    if ON_OPENSHIFT:
        DB_NAME = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'db.sqlite3')
    else:
        DB_NAME = os.path.join(BASE_DIR, 'db.sqlite3')
elif DB_ENGINE == 'postgresql':
    print("Using postgresql as DB engine.")
    DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
    if ON_OPENSHIFT:
        DB_NAME = os.environ['OPENSHIFT_APP_NAME']
        DB_USER = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
        DB_PASSWORD = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
        DB_HOST = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
        DB_PORT = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
    else:
        DB_NAME = 'development'
        DB_USER = 'postgres'
        DB_PASSWORD = 'postgres'
        DB_HOST = ''
        DB_PORT = ''


DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'