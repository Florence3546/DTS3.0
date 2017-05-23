# coding=UTF-8
from __future__ import unicode_literals

from common import constant


# ==================================================
# 注册审核
# ==================================================


def has_bind_user(task):
    return hasattr(task, 'process') and hasattr(task.process, 'user')


def be_personal_user(task):
    return has_bind_user(task) and (
        task.process.user.enterprise is None
    )


def be_enterprise_user(task):
    return has_bind_user(task) and task.process.user.enterprise


# ==================================================
# 订单发货
# ==================================================


def has_bind_order(task):
    return hasattr(task, 'process') and hasattr(task.process, 'order')


def order_not_paid(task):
    return has_bind_order(task) and (
        task.process.order.pay_status == constant.NOT_PAID and
        task.process.order.trade_state == constant.ORDER_NOT_PAID
    )


def order_paid_valid(task):
    return has_bind_order(task) and (
        task.process.order.pay_status == constant.HAS_PAID and
        task.process.order.verify_state == constant.VALID
    )


def order_can_pay(task):
    return order_not_paid(task) and (
        task.process.order.change_price_state != constant.REVIEWING
    )


def order_can_change_price(task):
    return order_not_paid(task) and (
        task.process.order.change_price_state == constant.NO_APPLY
    )


def order_is_changing_price(task):
    return order_not_paid(task) and (
        task.process.order.change_price_state == constant.REVIEWING
    )


def order_can_refund(task):
    return has_bind_order(task) and (
        task.process.order.pay_status == constant.HAS_PAID and
        task.process.order.trade_state in [
            constant.ORDER_HAS_PAID, constant.ORDER_IS_PICKING, constant.ORDER_IS_SHIPPING, constant.ORDER_FINISHED
        ]
    )


def order_can_pick(task):
    return order_paid_valid(task) and (
        task.process.order.trade_state == constant.ORDER_HAS_PAID
    )


def order_is_reviewing(task):
    return has_bind_order(task) and (
        task.process.order.verify_state == constant.REVIEWING and
        task.process.order.trade_state < constant.ORDER_IS_PICKING
    )


def order_can_close(task):
    return order_not_paid(task) or (
        task.process.order.pay_status == constant.HAS_REFUND and
        task.process.order.trade_state == constant.ORDER_IS_REFUNDING
    )


def order_can_ship(task):
    return order_paid_valid(task) and (
        task.process.order.trade_state == constant.ORDER_IS_PICKING
    )


def order_can_receive(task):
    return order_paid_valid(task) and (
        task.process.order.trade_state == constant.ORDER_IS_SHIPPING
    )


# ==================================================
# 退款退货
# ==================================================


def has_bind_refund(task):
    return hasattr(task, 'process') and hasattr(task.process, 'refundrecord')


def refund_is_handling(task):
    return has_bind_refund(task) and (
        task.process.refundrecord.refund_status == constant.REFUND_HANDLING and
        # task.process.refundrecord.order.trade_state == constant.ORDER_IS_REFUNDING
        task.process.refundrecord.order.trade_state not in [constant.ORDER_NOT_PAID, constant.ORDER_CLOSED]
    )


def refund_is_reviewing(task):
    return has_bind_refund(task) and (
        task.process.refundrecord.refund_status == constant.REFUND_REVIEWING
    )


def refund_is_returning(task):
    return has_bind_refund(task) and (
        task.process.refundrecord.refund_status == constant.REFUND_RETURNING and
        len(task.process.refundrecord.waybill_no.strip()) > 0
    )


def refund_can_finish(task):
    if has_bind_refund(task):
        refundrecord = task.process.refundrecord
        order = refundrecord.order
        if order.pay_status == constant.HAS_PAID and order.trade_state in [
            constant.ORDER_HAS_PAID,
            constant.ORDER_IS_PICKING,
            constant.ORDER_IS_SHIPPING,
            constant.ORDER_FINISHED,
            constant.ORDER_IS_REFUNDING,
        ]:
            if refundrecord.refund_status == constant.REFUND_HANDLING:
                if order.verify_state != constant.VALID:
                    return True
                else:
                    return False
            elif refundrecord.refund_status == constant.REFUND_REVIEWING:
                if refundrecord.refund_type == constant.REFUND:
                    return True
                else:
                    return False
            elif refundrecord.refund_status == constant.REFUND_RECEIVING:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def refund_can_close(task):
    return has_bind_refund(task) and (
        task.process.refundrecord.refund_status in [
            constant.REFUND_HANDLING,
            constant.REFUND_REVIEWING,
            constant.REFUND_RECEIVING,
        ]
    )


