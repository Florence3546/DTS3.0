# coding=UTF-8
from __future__ import unicode_literals

from django.db import models

from bpmn.models import Process
from common.constant import (
    # CONTRACT_STATUS_CHOICES,
    # LOGISTICS_STATUS_CHOICES,
    PAY_TYPE_CHOICES,
    # LOGISTICS_WAITING,
    SHIPPING_TYPE_CHOICES,
    PAY_STATUS_CHOICES,
    NOT_PAID,
    REVIEWING,
    # CHANGE_PRICE_STATE,              # 改价状态
    # INVOICE_STATE_CHOICES,           # 开票状态
    REVIEW_STATUS_CHOICES,           # 审核状态
    TRADE_STATE_CHOICES,       # 交易状态
    REFUND_TYPE_CHOICES,       # 退款类型
    REFUND_STATUS_CHOICES,       # 退款状态
    REFUND_HANDLING,
    TRADE_TYPE_CHOICES,     # 交易类型
)
from dtsauth.models import Enterprise, User
from good.models import Good
from promotion.models import GoodPromotion

import datetime


class Order(models.Model):
    """订单"""
    order_no = models.CharField('订单编号', max_length=50)  # YYYYmmddHHMMSS + buyerid+
    buyer = models.ForeignKey(User, verbose_name='下单人', on_delete=models.PROTECT, related_name='orders_submit')
    purchaser = models.ForeignKey(Enterprise, verbose_name='采购方', blank=True, null=True)
    receiving_address = models.ForeignKey('ReceivingAddress', verbose_name='收货地址', blank=True, null=True)
    # address = models.TextField('收货地址')  # JSON格式
    payment_method = models.ForeignKey('PaymentMethod', verbose_name='支付方式', blank=True, null=True, on_delete=models.PROTECT)
    shipping_method = models.ForeignKey('ShippingMethod', verbose_name='配送方式', blank=True, null=True, on_delete=models.PROTECT)
    is_purchasea_greement = models.BooleanField('是否是协议客户', default=False, blank=True)
    pay_status = models.IntegerField('付款状态', choices=PAY_STATUS_CHOICES, default=NOT_PAID)
    total_price = models.IntegerField('商品价格总计')  # 订单金额 单位：分
    real_price = models.IntegerField('实付价格总计', blank=True, null=True)  # 订单金额 单位：分
    # logi_status = models.IntegerField('物流状态', choices=LOGISTICS_STATUS_CHOICES, default=LOGISTICS_WAITING)
    ord_time = models.DateTimeField('下单时间', auto_now_add=True)
    pay_time = models.DateTimeField('付款时间', blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人', on_delete=models.PROTECT, related_name='orders_review')
    proc_delivery = models.OneToOneField(Process, verbose_name='发货流程')

    need_invoice = models.BooleanField('是否需要开票', default=False)
    invoice_no = models.CharField('发票号码', max_length=30, blank=True)  # 12位分类发票代码 + 8位发票号码 开票状态
    change_price_state = models.IntegerField('改价状态', choices=REVIEW_STATUS_CHOICES, default=0, blank=True, null=True)
    verify_state = models.IntegerField('审核状态', choices=REVIEW_STATUS_CHOICES, default=0, blank=True, null=True)
    trade_state = models.IntegerField('交易状态', choices=TRADE_STATE_CHOICES, default=0, blank=True, null=True)
    trade_type = models.IntegerField('交易类型', choices=TRADE_TYPE_CHOICES, default=1, blank=True, null=True)
    fail_reason = models.TextField('失败原因', blank=True)
    note = models.TextField('买家留言', blank=True)
    waybill_no = models.CharField('物流单号', max_length=50, blank=True)
    order_source = models.CharField('订单来源', max_length=100, blank=True)  # pc 手机

    def __unicode__(self):
        return self.order_no


class QuicklyOrder(models.Model):
    """快速下单"""
    user = models.ForeignKey(User, verbose_name='下单人', on_delete=models.PROTECT, related_name='user_quickly_order')
    good = models.ForeignKey(Good, verbose_name='产品', on_delete=models.PROTECT)
    quantity = models.IntegerField('产品数量')


class ChangePriceRecord(models.Model):
    """改价审批列表"""
    apply_discount = models.IntegerField('申请优惠')  # 申请优惠 单位：分
    real_discount = models.IntegerField('实际优惠', blank=True, null=True)  # 实际优惠 单位：分
    order_item = models.OneToOneField('OrderItem', verbose_name='订单商品', on_delete=models.CASCADE)
    change_price_state = models.IntegerField('改价状态', choices=REVIEW_STATUS_CHOICES, default=REVIEWING)
    starff = models.ForeignKey(User, verbose_name='申请人', on_delete=models.PROTECT, related_name='change_price_applied')
    leader = models.ForeignKey(User, verbose_name='审核人', on_delete=models.PROTECT, related_name='change_price_replied',
                               null=True, blank=True)
    apply_time = models.DateTimeField('申请时间', default=datetime.datetime.now)
    reply_time = models.DateTimeField('审批时间', blank=True, null=True)


class ReceivingAddress(models.Model):
    """收货地址"""
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    people = models.CharField('收货人', max_length=50)
    telephone = models.CharField('收货人电话', max_length=50)
    region = models.CharField('所在地区', max_length=50)  # 省市区 三级
    address = models.TextField('收货地址')  # 详细地址
    email = models.CharField('邮箱', blank=True, max_length=100)
    # zip = models.CharField('邮编', blank=True, max_length=100)
    is_default = models.BooleanField('是否是默认地址', default=False)

    def __unicode__(self):
        return self.people


class OrderItem(models.Model):
    """订单商品"""
    order = models.ForeignKey(Order, verbose_name='订单', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, verbose_name='产品', on_delete=models.PROTECT)
    price = models.IntegerField('产品单价')  # 单位：分
    real_price = models.IntegerField('实付单价', blank=True, null=True)  # 单位：分
    quantity = models.IntegerField('产品数量')
    batch_no = models.CharField('产品批号', max_length=30, blank=True)
    expired = models.DateField('到期日期', blank=True, null=True)
    # review_status = models.IntegerField('审核状态', blank=True)
    stock_status = models.IntegerField('库存状态', blank=True, null=True)
    promotion = models.ForeignKey(GoodPromotion, verbose_name='促销活动', blank=True, null=True)


class PaymentMethod(models.Model):
    """支付方式"""
    name_cn = models.CharField('中文名称', max_length=30, blank=True, null=True)
    pay_type = models.IntegerField('支付类型', choices=PAY_TYPE_CHOICES)
    # logo = models.ImageField('LOGO', upload_to='logo/payment_method/', blank=True)
    logo = models.CharField('LOGO', max_length=100, blank=True, null=True)
    order_no = models.IntegerField('显示排序', blank=True, null=True)
    is_active = models.BooleanField('状态', default=False, blank=True)
    api_args = models.TextField('API参数')  # JSON
    reserved_1 = models.CharField('备用字段1', max_length=50, blank=True)
    reserved_2 = models.CharField('备用字段2', max_length=50, blank=True)
    reserved_3 = models.CharField('备用字段3', max_length=50, blank=True)

    def __unicode__(self):
        return self.name_cn


class ShippingMethod(models.Model):
    """配送方式"""
    name_cn = models.CharField('中文名称', max_length=30, blank=True, null=True)
    shipping_type = models.IntegerField('配送类型', choices=SHIPPING_TYPE_CHOICES)
    logo = models.ImageField('LOGO', upload_to='logo/shipping_method/', blank=True)
    website = models.CharField('查询网址', max_length=80, blank=True, null=True)
    order_no = models.IntegerField('显示排序', blank=True, null=True)
    is_active = models.BooleanField('状态', blank=True)
    reserved_1 = models.CharField('备用字段1', max_length=50, blank=True)
    reserved_2 = models.CharField('备用字段2', max_length=50, blank=True)
    reserved_3 = models.CharField('备用字段3', max_length=50, blank=True)

    def __unicode__(self):
        return self.name_cn


class ShoppingCartItem(models.Model):
    """购物车清单"""
    buyer = models.ForeignKey(User, verbose_name='购买人', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, verbose_name='产品', on_delete=models.CASCADE)
    quantity = models.IntegerField('产品数量')
    created = models.DateTimeField('创建时间', default=datetime.datetime.now)


class MyFavorites(models.Model):
    """用户收藏"""
    coll_user = models.ForeignKey(User, verbose_name='收藏用户', on_delete=models.CASCADE)
    coll_good = models.ForeignKey(Good, verbose_name='收藏产品', on_delete=models.CASCADE)
    created = models.DateTimeField('创建时间', default=datetime.datetime.now)


class RefundRecord(models.Model):
    """退款/退货记录"""
    order = models.ForeignKey(Order, verbose_name='订单', on_delete=models.PROTECT)
    refund = models.IntegerField('退款金额')           # 订单金额 单位：分
    applicant = models.ForeignKey(User, verbose_name='申请人', on_delete=models.PROTECT, related_name='apply_refund_records')
    refund_type = models.IntegerField('退款类型', choices=REFUND_TYPE_CHOICES)
    consult = models.ForeignKey(User, verbose_name='客服', on_delete=models.PROTECT, related_name='handle_refund_records', blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审批者', on_delete=models.PROTECT, related_name='review_refund_records', blank=True, null=True)
    created = models.DateTimeField('创建时间', default=datetime.datetime.now)
    refund_status = models.IntegerField('退款状态', choices=REFUND_STATUS_CHOICES, default=REFUND_HANDLING)
    proc_refund = models.OneToOneField(Process, verbose_name='退款流程')
    shipping_method = models.CharField('配送方式', max_length=30, blank=True)
    waybill_no = models.CharField('物流单号', max_length=50, blank=True)
    refund_desc = models.TextField('退款说明', blank=True)


class Invoice(models.Model):
    """发票内容"""
    order = models.ForeignKey(Order, verbose_name='订单', on_delete=models.CASCADE)
    company_name = models.CharField('公司名称', max_length=40)
    taxpayer_no = models.CharField('纳税人识别号', max_length=50)
    address_phone = models.CharField('地址、电话', max_length=50)
    bank_account = models.CharField('开户行及账户', max_length=50)