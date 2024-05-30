from ALGator.settings import *
import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME', 'algator'),
        'USER': os.getenv('DATABASE_USER', 'algator'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'algator'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', 3306),
    }
}

ALGATOR_SERVER = {
 'Hostname' : os.getenv('ALGATOR_HOST', 'localhost'),
 'Port'     : os.getenv('ALGATOR_PORT', 12321),
}

IS_PRODUCTION = bool(os.getenv('PROD', False))
