# coding=UTF-8
from __future__ import unicode_literals

from django.apps import AppConfig
# from common.utils import utils_mssql


class CommonConfig(AppConfig):
    name = 'common'
    verbose_name = u'通用模块'

    def ready(self):
        # 测试连接 sql server
        # conn = utils_mssql.get_conn('dingding')

        # 监听信号
        from django.db.models.signals import post_delete, post_save
        from .models import SettingsType, SettingsItem

        post_save.connect(SettingsType.post_save_callback, sender=SettingsType)
        post_delete.connect(SettingsType.post_delete_callback, sender=SettingsType)

        post_save.connect(SettingsItem.post_save_callback, sender=SettingsItem)
        post_delete.connect(SettingsItem.post_delete_callback, sender=SettingsItem)

