# coding=UTF-8

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dts',
        'USER': 'root',
        'PASSWORD': 'zxcvbnhy6',
        'HOST': '192.168.0.99',
        'PORT': '3306',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '192.168.0.99:11211',
    },
}
