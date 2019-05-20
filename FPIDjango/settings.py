"""
Django settings for FPIDjango project.

----

Unfortunately, the modified import statement of

..

    from FPIDjango.private.settings_private import *

is required for the PyCharm Python Console and the PyCharm manage.py to
work properly.  It obviously knows better than I do.  It cannot pay
attention to some silly environment variable that I set in Preferences
like we were able to do in the run settings.

This will work -- and not reveal our credentials -- as long as the
**private** directory is included in our **.gitignore** file.

----

(Comments autogenerated by Django )
Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import psycopg2.extensions

from FPIDjango.private.settings_private import *

"""
Original import of dummy values:
from .settings_public import *
"""

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = MY_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', DB_HOST]


# Application definition

INSTALLED_APPS = [

    # Application app(s)
    'fpiweb.apps.FpiwebConfig',

    # Django supplied apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third party apps
    'bootstrap4',
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

ROOT_URLCONF = 'FPIDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'fpiweb/')
        ],

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

WSGI_APPLICATION = 'FPIDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
            'ENGINE': DB_ENGINE,
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PSWD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# URL to allow a user to authenticate herself.  This becomes the default
# used whenever Django detects someone trying to do something requiring
# authentication.
LOGIN_URL = 'fpiweb:login/'


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# django-bootstrap4 settings
# Default settings
BOOTSTRAP4 = {

    # The complete URL to the Bootstrap CSS file
    # Note that a URL can be either a string,
    # e.g. "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap
    # .min.css",
    # or a dict like the default value below.
    "css_url": {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css"
                "/bootstrap.min.css",
        "integrity": "sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId"
                     "/iRN3ewGhXQFZCSftd1LZCfmhktB",
        "crossorigin": "anonymous",
    },

    # The complete URL to the Bootstrap JavaScript file
    "javascript_url": {
        "url": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js"
               "/bootstrap.min.js",
        "integrity": "sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB"
                     "/pTJ0euyQp0Mk8ck+5T",
        "crossorigin": "anonymous",
    },

    # The complete URL to the Bootstrap CSS file (None means no theme)
    "theme_url": None,

    # The URL to the jQuery JavaScript file (full)
    "jquery_url": {"url": "https://code.jquery.com/jquery-3.3.1.min.js",
        "integrity": "sha384-tsQFqpEReu7ZLhBV2VZlAu7zcOV+rXbYlF2cqB8txI"
                     "/8aZajjp4Bqd+V6D5IgvKT",
        "crossorigin": "anonymous",
                   },

    # The URL to the jQuery JavaScript file (slim)
    "jquery_slim_url": {
        "url": "https://code.jquery.com/jquery-3.3.1.slim.min.js",
        "integrity":
            "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH"
            "+8abtTE1Pi6jizo",
        "crossorigin": "anonymous",
    },

    # The URL to the Popper.js JavaScript file (slim)
    "popper_url": {
        "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd"
               "/popper.min.js",
        "integrity":
            "sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK"
            "/l8WvCWPIPm49",
        "crossorigin": "anonymous",
    },

    # Put JavaScript in the HEAD section of the HTML document (only relevant
    # if you use bootstrap4.html)
    'javascript_in_head': False,

    # Include jQuery with Bootstrap JavaScript False|falsy|slim|full (
    # default=False)
    # False - means tag bootstrap_javascript use default value - `falsy` and
    # does not include jQuery)
    'include_jquery': False,

    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-3',

    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-9',

    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,

    # Class to indicate required (better to set this in your Django form)
    'required_css_class': '',

    # Class to indicate error (better to set this in your Django form)
    'error_css_class': 'is-invalid',

    # Class to indicate success, meaning the field has valid input (better
    # to set this in your Django form)
    'success_css_class': 'is-valid',

    # Renderers (only set these if you have studied the source and
    # understand the inner workings)
    'formset_renderers': {
        'default': 'bootstrap4.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap4.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap4.renderers.FieldRenderer',
        'inline': 'bootstrap4.renderers.InlineFieldRenderer',
    },
}
