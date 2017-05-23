# coding=UTF-8

from django.core.cache import cache
from django.db import models
from django.core.mail import mail_admins
from django.core import serializers
from common.constant import (
    SETTINGS_BASIC,
    SETTINGS_FRONT_SITE,
    SETTINGS_ADMIN_LOGO,
    SETTINGS_CONSULT_SETTING,
    SETTINGS_AUTH_SETTING,
    SETTINGS_REMIND_SETTING,
)
import simplejson as json
import datetime


class SettingsType(models.Model):
    """设置类型"""
    code = models.CharField('类型码', max_length=30, unique=True)
    name = models.CharField('类型名', max_length=30, unique=True)
    note = models.TextField('备注', blank=True)

    CACHE_KEY = 'SETTINGS_%s'

    def __unicode__(self):
        return self.code

    @classmethod
    def get_item_dict(cls, code):
        """根据类型码获取设置项字典"""
        cache_key = cls.CACHE_KEY % code
        item_dict = cache.get(cache_key)
        if item_dict is None:
            self = cls.objects.filter(code=code).first()
            if self:
                item_dict = {item.name: item for item in self.item_set.all()}
            else:
                item_dict = {}
            cache.set(cache_key, item_dict)
        return item_dict

    @classmethod
    def get_item_list(cls, code):
        """根据类型码获取设置项列表"""
        item_dict = cls.get_item_dict(code)
        item_list = item_dict.values()
        item_list.sort(lambda x, y: cmp(x.value, y.value))
        return item_list

    @classmethod
    def get_basic_settings(cls, key):
        """基础信息"""
        item_dict = cls.get_item_dict(SETTINGS_BASIC)
        item = item_dict.get(key)
        if item:
            return json.loads(item.note)
        else:
            return {}

    @classmethod
    def get_front_site_settings(cls):
        """基础信息 - 前台网站"""
        return cls.get_basic_settings(SETTINGS_FRONT_SITE)

    @classmethod
    def get_admin_logo_settings(cls):
        """基础信息 - 后台Logo"""
        return cls.get_basic_settings(SETTINGS_ADMIN_LOGO)

    @classmethod
    def get_consult_settings(cls):
        """基础信息 - 客服设置"""
        return cls.get_basic_settings(SETTINGS_CONSULT_SETTING)

    @classmethod
    def get_auth_settings(cls):
        """基础信息 - 登录验证"""
        return cls.get_basic_settings(SETTINGS_AUTH_SETTING)

    @classmethod
    def get_remind_settings(cls):
        """基础信息 - 信息提醒"""
        return cls.get_basic_settings(SETTINGS_REMIND_SETTING)

    @classmethod
    def get_item_choices(cls, code):
        """根据类型码获取设置项choices"""
        return [(item.value, item.name) for item in cls.get_item_list(code)]

    def delete_cache(self):
        """清除cache"""
        cache_key = self.CACHE_KEY % self.code
        cache.delete(cache_key)

    @staticmethod
    def post_save_callback(sender, **kwargs):
        """数据保存时发出的信号回调"""
        self = kwargs['instance']
        self.delete_cache()

    @staticmethod
    def post_delete_callback(sender, **kwargs):
        """数据删除时发出的信号回调"""
        self = kwargs['instance']
        self.delete_cache()


class SettingsItem(models.Model):
    """设置项"""
    name = models.CharField('设置名', max_length=30)
    value = models.CharField('值', max_length=200, blank=True)
    note = models.TextField('备注', blank=True)
    s_type = models.ForeignKey(SettingsType, on_delete=models.CASCADE, verbose_name='设置类型', related_name='item_set')

    class Meta:
        unique_together = (('name', 's_type'),)

    def __unicode__(self):
        return self.name

    def delete_cache(self):
        """清除cache"""
        self.s_type.delete_cache()

    @staticmethod
    def post_save_callback(sender, **kwargs):
        """数据保存时发出的信号回调"""
        self = kwargs['instance']
        self.delete_cache()

    @staticmethod
    def post_delete_callback(sender, **kwargs):
        """数据删除时发出的信号回调"""
        self = kwargs['instance']
        self.delete_cache()


class Region(models.Model):
    id = models.IntegerField('地区ID', primary_key=True, unique=True)
    region_code = models.CharField('行政代码', max_length=6, blank=True)
    region_name = models.CharField('行政名称', max_length=20, blank=True)
    parent_id = models.IntegerField('父级ID', blank=True, default=0)
    is_active = models.BooleanField('启用禁用', default=False)
    region_level = models.IntegerField('行政级别', blank=True)
    region_order = models.IntegerField('排序', blank=True)
    region_name_en = models.CharField('行政英文名', max_length=20, blank=True)
    region_shortname_en = models.CharField('行政英文缩写', max_length=5, blank=True)

    def __unicode__(self):
        return self.region_name


class GlobalConfig(models.Model):
    """全局配置"""
    name = models.CharField('配置名', max_length=20, unique=True)
    name_cn = models.CharField('中文', max_length=30)
    value = models.CharField('配置值', max_length=200)
    note = models.TextField('备注', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, to_field='name', verbose_name='父级配置', blank=True, null=True, related_name='children_set')
    is_reserved = models.BooleanField('不可删除', default=False)

    CACHE_KEY = 'GLOBAL_CONFIG_%s'



    def __unicode__(self):
        return self.name

    @classmethod
    def get_value(cls, name):
        """根据配置名获取配置值"""
        cache_key = cls.CACHE_KEY % name
        value = cache.get(cache_key)
        if value is None:
            children = cls.get_children(name)
            if len(children):
                value = {self.name: self.value for self in children}
            else:
                self = cls.objects.filter(name=name).first()
                value = self.value if self else ''
            cache.set(cache_key, value)
        return value

    @classmethod
    def get_children(cls, name):
        """根据配置名获取子配置项"""
        return cls.objects.filter(parent_id=name)

    def to_json(self):
        """对象序列化为json格式"""
        if not hasattr(self, '_json_cache'):
            self._json_cache = serializers.serialize('json', [self])
        return self._json_cache

    def delete_parent_cache(self):
        """清除父级cache"""
        cache_key = self.CACHE_KEY % self.parent_id
        cache.delete(cache_key)

    def set_cache(self):
        """设置cache"""
        cache_key = self.CACHE_KEY % self.name
        cache.set(cache_key, self.value)
        self.delete_parent_cache()

    def delete_cache(self):
        """清除cache"""
        cache_key = self.CACHE_KEY % self.name
        cache.delete(cache_key)
        self.delete_parent_cache()

    @staticmethod
    def post_save_callback(sender, **kwargs):
        """数据保存时发出的信号回调"""
        self = kwargs['instance']

        # 发送邮件通知管理员
        subject = u'%s 数据被修改' % sender.__name__
        message = self.to_json()
        mail_admins(subject, message)

        # 更新 memcache
        self.set_cache()

    @staticmethod
    def post_delete_callback(sender, **kwargs):
        """数据删除时发出的信号回调"""
        self = kwargs['instance']

        # 发送邮件通知管理员
        subject = u'%s 数据被删除' % sender.__name__
        message = self.to_json()
        mail_admins(subject, message)

        # 更新 memcache
        self.delete_cache()


def set_file_path(obj,filename):
    return u'admin_logo/%(date)s/%(filename)s' % {
        'date': datetime.date.today(),
        'filename': filename,
    }


class ImageModel(models.Model):
    """单张图片上传：后台网站logo"""
    photo = models.ImageField('图片', upload_to=set_file_path)
