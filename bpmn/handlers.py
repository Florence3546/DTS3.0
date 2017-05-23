# coding=UTF-8
from __future__ import unicode_literals

from common import constant

from .models import Task


# ==================================================
# 注册审核
# ==================================================


def init_review_status(task, **reverse):
    """初始化企业账号审核状态"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        is_active = reverse['is_active']
        review_status = reverse['review_status']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        is_active = False
        review_status = constant.REVIEWING
    user = task.process.user
    enter = user.enterprise
    org_kwargs = {
        'is_active': user.is_active,
        'review_status': enter.review_status,
    }
    if user.is_active != is_active:
        user.is_active = is_active
        user.save()
    if enter.review_status != review_status:
        enter.review_status = review_status
        enter.save()
    return state, msg, org_kwargs


def valid_enterprise(task, **reverse):
    """企业账号审核通过"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        review_status = reverse['review_status']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        review_status = constant.VALID
    enter = task.process.user.enterprise
    org_kwargs = {'review_status': enter.review_status}
    if enter.review_status != review_status:
        enter.review_status = review_status
        enter.save()
    return state, msg, org_kwargs


def invalid_enterprise(task, **reverse):
    """企业账号审核不通过"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        review_status = reverse['review_status']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        review_status = constant.INVALID
    enter = task.process.user.enterprise
    org_kwargs = {'review_status': enter.review_status}
    if enter.review_status != review_status:
        enter.review_status = review_status
        enter.save()
    return state, msg, org_kwargs


def active_user(task, **reverse):
    """激活账号"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        is_active = reverse['is_active']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        is_active = True
    user = task.process.user
    org_kwargs = {'is_active': user.is_active}
    if user.is_active != is_active:
        user.is_active = is_active
        user.save()
    return state, msg, org_kwargs


# ==================================================
# 订单发货
# ==================================================


def mark_order_paid(task, **reverse):
    """标记已付款"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        pay_status = reverse['pay_status']
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        pay_status = constant.HAS_PAID
        trade_state = constant.ORDER_HAS_PAID
    order = task.process.order
    org_kwargs = {
        'pay_status': order.pay_status,
        'trade_state': order.trade_state,
    }
    if order.pay_status != pay_status or order.trade_state != trade_state:
        order.pay_status = pay_status
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs


def order_apply_change_price(task, **reverse):
    """订单申请改价"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        change_price_state = reverse['change_price_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        change_price_state = constant.REVIEWING
    order = task.process.order
    org_kwargs = {
        'change_price_state': order.change_price_state,
    }
    if order.change_price_state != change_price_state:
        order.change_price_state = change_price_state
        order.save()
    return state, msg, org_kwargs


def order_change_price_valid(task, **reverse):
    """订单改价通过"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        change_price_state = reverse['change_price_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        change_price_state = constant.VALID
    order = task.process.order
    org_kwargs = {
        'change_price_state': order.change_price_state,
    }
    if order.change_price_state != change_price_state:
        order.change_price_state = change_price_state
        order.save()
    return state, msg, org_kwargs


def order_change_price_invalid(task, **reverse):
    """订单改价不通过"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        change_price_state = reverse['change_price_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        change_price_state = constant.INVALID
    order = task.process.order
    org_kwargs = {
        'change_price_state': order.change_price_state,
    }
    if order.change_price_state != change_price_state:
        order.change_price_state = change_price_state
        order.save()
    return state, msg, org_kwargs


def mark_order_reviewing(task, **reverse):
    """标记审核中"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        verify_state = reverse['verify_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        verify_state = constant.REVIEWING
    order = task.process.order
    org_kwargs = {
        'verify_state': order.verify_state,
    }
    if order.verify_state != verify_state:
        order.verify_state = verify_state
        order.save()
    return state, msg, org_kwargs


def mark_order_refunding(task, **reverse):
    """标记退款"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        trade_state = constant.ORDER_IS_REFUNDING
    order = task.process.order
    org_kwargs = {
        'trade_state': order.trade_state,
    }
    if order.trade_state != trade_state:
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs


def mark_order_valid(task, **reverse):
    """订单审核通过"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        verify_state = reverse['verify_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        verify_state = constant.VALID
    order = task.process.order
    org_kwargs = {
        'verify_state': order.verify_state,
    }
    if order.verify_state != verify_state:
        order.verify_state = verify_state
        order.save()
    return state, msg, org_kwargs


def mark_order_invalid(task, **reverse):
    """订单审核不通过"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        verify_state = reverse['verify_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        verify_state = constant.INVALID
    order = task.process.order
    org_kwargs = {
        'verify_state': order.verify_state,
    }
    if order.verify_state != verify_state:
        order.verify_state = verify_state
        order.save()
    return state, msg, org_kwargs


def mark_order_picking(task, **reverse):
    """订单拣配"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        trade_state = constant.ORDER_IS_PICKING
    order = task.process.order
    org_kwargs = {
        'trade_state': order.trade_state,
    }
    if order.trade_state != trade_state:
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs


def close_order(task, **reverse):
    """订单关闭"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        trade_state = constant.ORDER_CLOSED
    order = task.process.order
    org_kwargs = {
        'trade_state': order.trade_state,
    }
    if order.trade_state != trade_state:
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs


def mark_order_shipping(task, **reverse):
    """标记已发货"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        trade_state = constant.ORDER_IS_SHIPPING
    order = task.process.order
    org_kwargs = {
        'trade_state': order.trade_state,
    }
    if order.trade_state != trade_state:
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs


def mark_order_received(task, **reverse):
    """确认收货"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        trade_state = constant.ORDER_FINISHED
    order = task.process.order
    org_kwargs = {
        'trade_state': order.trade_state,
    }
    if order.trade_state != trade_state:
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs


# ==================================================
# 退款退货
# ==================================================


def init_refund(task, **reverse):
    """客户发起退款/退货"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        trade_state = constant.ORDER_IS_REFUNDING
    order = task.process.refundrecord.order
    org_kwargs = {
        'trade_state': order.trade_state,
    }
    if order.trade_state != trade_state:
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs


def mark_refund_reviewing(task, **reverse):
    """标记退款/退货审核中"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        refund_status = reverse['refund_status']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        refund_status = constant.REFUND_REVIEWING
    refundrecord = task.process.refundrecord
    org_kwargs = {
        'refund_status': refundrecord.refund_status,
    }
    if refundrecord.refund_status != refund_status:
        refundrecord.refund_status = refund_status
        refundrecord.save()
    return state, msg, org_kwargs


def mark_refund_returning(task, **reverse):
    """标记待退货"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        refund_status = reverse['refund_status']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        refund_status = constant.REFUND_RETURNING
    refundrecord = task.process.refundrecord
    org_kwargs = {
        'refund_status': refundrecord.refund_status,
    }
    if refundrecord.refund_status != refund_status:
        refundrecord.refund_status = refund_status
        refundrecord.save()
    return state, msg, org_kwargs


def mark_refund_receiving(task, **reverse):
    """标记待收货"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        refund_status = reverse['refund_status']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        refund_status = constant.REFUND_RECEIVING
    refundrecord = task.process.refundrecord
    org_kwargs = {
        'refund_status': refundrecord.refund_status,
    }
    if refundrecord.refund_status != refund_status:
        refundrecord.refund_status = refund_status
        refundrecord.save()
    return state, msg, org_kwargs


def mark_refund_finished(task, **reverse):
    """标记退款完成"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        refund_status = reverse['refund_status']
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        refund_status = constant.REFUND_FINISHED
        trade_state = constant.ORDER_CLOSED
    refundrecord = task.process.refundrecord
    order = refundrecord.order
    org_kwargs = {
        'refund_status': refundrecord.refund_status,
        'trade_state': order.trade_state,
    }
    if refundrecord.refund_status != refund_status:
        refundrecord.refund_status = refund_status
        refundrecord.save()
    if order.trade_state != trade_state:
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs


def mark_refund_closed(task, **reverse):
    """标记退款关闭"""
    if reverse:
        state, msg = Task.TASK_IN_ORDER, '撤销成功'
        refund_status = reverse['refund_status']
        trade_state = reverse['trade_state']
    else:
        state, msg = Task.TASK_SUCCEED, '设置成功'
        refund_status = constant.REFUND_CLOSED
        trade_state = constant.ORDER_FINISHED
    refundrecord = task.process.refundrecord
    order = refundrecord.order
    org_kwargs = {
        'refund_status': refundrecord.refund_status,
        'trade_state': order.trade_state,
    }
    if refundrecord.refund_status != refund_status:
        refundrecord.refund_status = refund_status
        refundrecord.save()
    if order.trade_state != trade_state:
        order.trade_state = trade_state
        order.save()
    return state, msg, org_kwargs

