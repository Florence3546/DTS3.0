# coding=UTF-8

import json
from django.core.serializers.json import DjangoJSONEncoder


class DTSjson(object):
    @staticmethod
    def dumps(data):
        return json.dumps(data, cls=DjangoJSONEncoder)

    @staticmethod
    def loads(data):
        return json.loads(data, cls=json.JSONDecoder)
