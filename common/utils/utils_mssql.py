# coding=UTF-8
from __future__ import unicode_literals
from django.conf import settings

import pymssql


def get_conn(using):
    return pymssql.connect(**(settings.MSSQL_DATABASES[using]))
