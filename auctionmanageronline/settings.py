"""
Django settings for auctionmanageronline project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

TEMPLATE_DEBUG = os.environ.get('TEMPLATE_DEBUG', False)


# SECURITY WARNING: keep the secret key used in production secret!

if not DEBUG:
    with open('/home/wildlife/secret_key.txt') as f:
        SECRET_KEY = f.read().strip()
else:
    SECRET_KEY = 'j4io2joidj90*)*#*#)()uf23j90)*&3}}{|%($^oijun'


ALLOWED_HOSTS = ['ec2-54-163-252-105.compute-1.amazonaws.com', 'wcvauction.lightcastletech.com']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'manager',
    'south',
    'django_extensions',
    'django_select2',
    'gunicorn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'auctionmanageronline.urls'

WSGI_APPLICATION = 'auctionmanageronline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if not DEBUG:
    with open('/home/wildlife/db_pass.txt') as f:
        DB_PASS = f.read().strip()
else:
    DB_PASS = 'wildlife'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auctionmanager',
        'USER': 'wildlife',
        'PASSWORD': DB_PASS,
        'HOST': 'localhost',
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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
LOGIN_URL = '/login/'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/auctionmanager.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'auction': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },

}




