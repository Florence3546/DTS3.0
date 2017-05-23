# coding=UTF-8
from __future__ import unicode_literals

from django.forms import ModelForm
from order.models import Order, OrderItem, PaymentMethod, ShippingMethod, ShoppingCartItem, ReceivingAddress, Invoice


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class PaymentMethodForm(ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class ShippingMethodForm(ModelForm):
    class Meta:
        model = ShippingMethod
        fields = ['name_cn', 'website', 'shipping_type', 'order_no', 'is_active']


class ReceivingAddressForm(ModelForm):
    class Meta:
        model = ReceivingAddress
        # fields = '__all__'
        fields = ['user', 'people', 'telephone', 'region', 'address', 'email']


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
