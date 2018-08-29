# Standard library imports.
import pathlib

# Local imports.
from .base import *

__author__ = 'Jason Parent'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PGDATABASE'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            pathlib.Path('../client-angular/dist/client-angular/'),
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

STATICFILES_DIRS = [
    pathlib.Path('../client-angular/dist/client-angular/'),
]

STATIC_ROOT = os.path.join(BASE_DIR, '../static')

MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

CORS_ORIGIN_ALLOW_ALL = True
