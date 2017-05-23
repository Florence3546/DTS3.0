# coding=UTF-8
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from dtsauth.apps import DtsauthConfig
from dtsauth.models import Permission


class Command(BaseCommand):
    help = '加载权限配置数据'

    def get_permission_list(self, permission_json, result):
        for perm in permission_json:
            result.append(json.dumps({
                'codename': perm['codename'],
                'name': perm['name']
            }))
            if 'children' in perm and perm['children']:
                self.get_permission_list(perm['children'], result)
        return result

    def handle(self, *args, **options):
        permission_new = self.get_permission_list(DtsauthConfig.permission_json, [])
        permission_old = [json.dumps(perm) for perm in Permission.objects.values()]
        delete_list = [json.loads(perm_str) for perm_str in set(permission_old) - set(permission_new)]
        add_list = [json.loads(perm_str) for perm_str in set(permission_new) - set(permission_old)]

        with transaction.atomic():
            delete_codename_list = [perm['codename'] for perm in delete_list]
            Permission.objects.filter(codename__in=delete_codename_list).delete()
            Permission.objects.bulk_create([Permission(**perm) for perm in add_list])
            self.stdout.write(self.style.SUCCESS('Successfully load dts_permission: delete %s, add %s' %
                                                 (len(delete_list), len(add_list))))
