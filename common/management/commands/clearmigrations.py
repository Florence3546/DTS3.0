# coding=UTF-8
from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = '清空根目录所有一级子目录中 migrations 目录下的迁移记录'

    def handle(self, *args, **options):
        for name in os.listdir(settings.BASE_DIR):
            m_dir = os.path.join(name, 'migrations')
            if os.path.isdir(m_dir):
                for m_name in os.listdir(m_dir):
                    m_path = os.path.join(m_dir, m_name)
                    if os.path.isfile(m_path) and m_name != '__init__.py':
                        os.remove(m_path)
                        self.stdout.write(self.style.SUCCESS(u'已删除文件 "%s"' % m_path))
        self.stdout.write(self.style.SUCCESS(u'清理完成'))
