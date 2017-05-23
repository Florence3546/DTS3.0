# coding=UTF-8
from __future__ import unicode_literals

from django.db import models

from common.constant import DISCOUNT_TYPE_CHOICES, PROMOTION_TYPE_CHOICES
from dtsauth.models import Enterprise
import datetime


class PromotionRule(models.Model):
    """促销活动规则"""
    name = models.CharField('规则名', max_length=80)  # 如：会员9折，满100打9折
    prom_type = models.IntegerField('促销类型', choices=PROMOTION_TYPE_CHOICES)
    prom_value = models.IntegerField('促销类型值', default=0)
    disc_type = models.IntegerField('折扣类型', choices=DISCOUNT_TYPE_CHOICES)
    disc_value = models.IntegerField('折扣值')  # 根据折扣类型，折扣值的单位为 百分比 或者 分


class GoodPromotion(models.Model):
    """促销活动"""
    prom_price = models.IntegerField('促销价')  # 单位为 分
    prom_rule = models.ForeignKey(PromotionRule, verbose_name='促销规则', on_delete=models.PROTECT)  # 必须是 is_template=False 的规则
    created = models.DateTimeField('创建时间', default=datetime.datetime.now)
    start_date = models.DateField('生效日期')
    end_date = models.DateField('终止日期', blank=True, null=True)  # 终止日期当天协议就已失效


class PurchaseAgreement(models.Model):
    """采购协议"""
    purchaser = models.ForeignKey(Enterprise, verbose_name='采购方', on_delete=models.PROTECT)
    created = models.DateTimeField('创建时间', default=datetime.datetime.now)
    start_date = models.DateField('生效日期')
    end_date = models.DateField('终止日期', blank=True, null=True)  # 终止日期当天协议就已失效
    note = models.TextField('备注', blank=True)
    photo0 = models.ImageField('协议图片0', upload_to='purchace_agreement/%Y/%m/%d/', blank=True)
    photo1 = models.ImageField('协议图片1', upload_to='purchace_agreement/%Y/%m/%d/', blank=True)
    photo2 = models.ImageField('协议图片2', upload_to='purchace_agreement/%Y/%m/%d/', blank=True)
    photo3 = models.ImageField('协议图片3', upload_to='purchace_agreement/%Y/%m/%d/', blank=True)
    photo4 = models.ImageField('协议图片4', upload_to='purchace_agreement/%Y/%m/%d/', blank=True)
