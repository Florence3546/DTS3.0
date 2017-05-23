# coding=UTF-8
from __future__ import unicode_literals

from django.db import models


class GoodStock(models.Model):
    """商品库存中间表 库存管理系统 -> 中间表 -> 电商系统"""
    good = models.CharField('商品名', max_length=80)  # 如：百服咛
    manufacturer = models.CharField('生产企业', max_length=80)
    quantity = models.IntegerField('实际库存数量', default=0)
    virtual_quantity = models.IntegerField('虚拟库存数量', default=0)
    estimate_time = models.DateTimeField('途中商品预计送达时间', blank=True, null=True)
    latest_modified = models.DateTimeField('最后修改时间', auto_now_add=True, help_text='线下系统最后一次修改的时间')
    latest_sync = models.DateTimeField('最后同步时间', blank=True, null=True, help_text='线上系统最后一次同步的时间')


class Order(models.Model):
    """订单 电商系统 -> 中间表 -> 库存管理系统"""
    order_no = models.IntegerField('订单编号')
    purchaser = models.CharField('采购方', max_length=80)
    address = models.TextField('收货地址')
    latest_modified = models.DateTimeField('最后修改时间', auto_now_add=True, help_text='线上系统最后一次修改的时间')
    latest_sync = models.DateTimeField('最后同步时间', blank=True, null=True, help_text='线下系统最后一次同步的时间')


class OrderItem(models.Model):
    """订单清单 电商系统 -> 中间表 -> 库存管理系统"""
    good = models.CharField('商品名', max_length=80)  # 如：百服咛
    quantity = models.IntegerField('下单数量', default=0)
    order_no = models.IntegerField('订单编号')
    latest_modified = models.DateTimeField('最后修改时间', auto_now_add=True, help_text='线上系统最后一次修改的时间')
    latest_sync = models.DateTimeField('最后同步时间', blank=True, null=True, help_text='线下系统最后一次同步的时间')
