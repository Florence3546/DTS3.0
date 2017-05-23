# coding=UTF-8
from __future__ import unicode_literals

from django.apps import AppConfig


class DtsauthConfig(AppConfig):
    name = 'dtsauth'
    verbose_name = u'DTS用户认证和授权系统'

    permission_json = [
        {'codename': 'dtsauth', 'name': '账号认证与授权', 'children': [
            {'codename': 'dtsauth.user_manage', 'name': '用户管理', 'children': []},
            {'codename': 'dtsauth.enterprise_manage', 'name': '企业管理', 'children': []},
            {'codename': 'dtsauth.role_manage', 'name': '角色管理', 'children': []},
        ]}
    ]
