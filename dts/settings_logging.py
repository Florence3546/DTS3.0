import logging.handlers

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(process)d][%(thread)d][%(levelname)-5s][%(filename)s:%(lineno)d][%(funcName)s]: %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
        'simple': {
            'format': '[%(asctime)s][%(levelname)s] %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'socket': {
            'level': 'INFO',
            'class': 'logging.handlers.SocketHandler',
            'formatter': 'verbose',
            'host': 'localhost',
            'port': logging.handlers.DEFAULT_TCP_LOGGING_PORT,
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'dts': {
            'handlers': ['console', 'socket'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'socket'],
            'level': 'DEBUG',
        },
    },
}
