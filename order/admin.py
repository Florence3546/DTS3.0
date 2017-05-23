from django.contrib import admin

# Register your models here.
from .models import (Order,
                     ReceivingAddress,
                     OrderItem,
                     PaymentMethod,
                     ShippingMethod,
                     ShoppingCartItem,
                     MyFavorites,
                     ChangePriceRecord,
                     RefundRecord,
                     QuicklyOrder,
                     Invoice
                     )

from bpmn.models import Process


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['good']


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_no', 'buyer', 'purchaser', 'receiving_address', 'payment_method', 'shipping_method', 'pay_status',
        'total_price',
        'verify_state', 'trade_state', 'change_price_state', 'pay_time', 'reviewer', 'proc_delivery')
    list_editable = ['total_price', 'verify_state', 'trade_state', 'change_price_state', 'payment_method']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)


class ReceivingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'people', 'telephone', 'region', 'address', 'email', 'is_default')


admin.site.register(ReceivingAddress, ReceivingAddressAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'good', 'quantity', 'batch_no', 'expired', 'stock_status')


admin.site.register(OrderItem, OrderItemAdmin)


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name_cn', 'pay_type', 'logo', 'order_no', 'is_active', 'reserved_1', 'reserved_2', 'reserved_3')


admin.site.register(PaymentMethod, PaymentMethodAdmin)


class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = (
        'name_cn', 'shipping_type', 'logo', 'website', 'order_no', 'is_active', 'reserved_1', 'reserved_2',
        'reserved_3')


admin.site.register(ShippingMethod, ShippingMethodAdmin)


class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'good', 'quantity', 'created')


admin.site.register(ShoppingCartItem, ShoppingCartItemAdmin)


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('proc_type', 'proc_conf', 'state_json', 'created', 'ended')


admin.site.register(Process, ProcessAdmin)


class MyFavoritesAdmin(admin.ModelAdmin):
    list_display = ('coll_user', 'coll_good', 'created')


admin.site.register(MyFavorites, MyFavoritesAdmin)


@admin.register(ChangePriceRecord)
class ChangePriceRecordAdmin(admin.ModelAdmin):
    list_display = ('apply_discount', 'real_discount', 'change_price_state', 'starff', 'leader', 'apply_time')


@admin.register(RefundRecord)
class RefundRecordAdmin(admin.ModelAdmin):
    list_display = ('order', 'applicant', 'refund_type', 'reviewer', 'refund_status', 'proc_refund', 'waybill_no')


@admin.register(QuicklyOrder)
class QuicklyOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'good', 'quantity')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'company_name', 'taxpayer_no', 'address_phone', 'bank_account')
