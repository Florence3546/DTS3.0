# coding=UTF-8
from __future__ import unicode_literals

from django.apps import AppConfig


class BpmnConfig(AppConfig):
    name = 'bpmn'
    verbose_name = u'bpmn业务流程建模标注模块'

    def ready(self):
        from .models import Process
        from .configs import PROCESS_TYPE_DICT, PROCESS_CONFIG_DICT
        Process.register_type_dict(PROCESS_TYPE_DICT)
        Process.register_config_dict(PROCESS_CONFIG_DICT)
