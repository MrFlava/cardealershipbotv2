import logging.config
from os import path

from botmanlib.utils import parse_environ_settings

PROJECT_ROOT = path.normpath(path.join(path.dirname(path.realpath(__file__)), '..'))
ADMINS = []
ADMIN_PASSWORD = "simplepassword"
MEDIA_FOLDER = path.join(PROJECT_ROOT, 'media')
RESOURCES_FOLDER = path.join(PROJECT_ROOT, 'resources')
SETTINGS_FILE = path.join(RESOURCES_FOLDER, 'settings.json')
JOBS_PATH = path.join(RESOURCES_FOLDER, 'jobs.dill')

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d,%H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        'deb_file': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8',
            'filename': path.join(PROJECT_ROOT, 'logs', 'app.log')
        },
        'err_file': {
            'level': 'ERROR',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8',
            'filename': path.join(PROJECT_ROOT, 'logs', 'error.log')
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'deb_file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
})

parse_environ_settings(locals())

try:
    from local_settings import *
except ImportError:
    pass
