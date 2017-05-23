# coding=UTF-8
from __future__ import unicode_literals

from bpmn import conditions, handlers
from bpmn.models import Process, Task

# 基础退货流程
BASE_REFUND = {
    Process.START_TASK: 'init_refund',
    Process.END_TASK_LIST: ['mark_refund_finished', 'mark_refund_closed'],
    'init_refund': {
        'name_cn': '发起退款/退货',
        'note': '用户订单支付后，提交退款或退货，客服进行处理',
        'transit_type': Task.AUTO_TRANSIT,
        'condition_list': [conditions.refund_is_handling],
        'run': handlers.init_refund,
        'mutex': [],
        'target_list': ['mark_refund_finished', 'mark_refund_reviewing', 'mark_refund_closed'],
    },
    'mark_refund_reviewing': {
        'name_cn': '提交审核',
        'note': '客服处理退款/退货申请，点击【通过】，进入退款审核',
        'transit_type': Task.MANUAL_TRANSIT,
        'condition_list': [conditions.refund_is_handling],
        'run': handlers.mark_refund_reviewing,
        'mutex': [],
        'target_list': ['mark_refund_returning', 'mark_refund_finished', 'mark_refund_closed'],
    },
    'mark_refund_returning': {
        'name_cn': '退款审核通过',
        'note': '主管审核退款申请，点击【通过】，等待买家发货',
        'transit_type': Task.MANUAL_TRANSIT,
        'condition_list': [conditions.refund_is_reviewing],
        'run': handlers.mark_refund_returning,
        'mutex': [],
        'target_list': ['mark_refund_receiving'],
    },
    'mark_refund_receiving': {
        'name_cn': '已发货',
        'note': '买家发货后，点击【已发货】，录入物流单号，等待卖家收货',
        'transit_type': Task.MANUAL_TRANSIT,
        'condition_list': [conditions.refund_is_returning],
        'run': handlers.mark_refund_receiving,
        'mutex': [],
        'target_list': ['mark_refund_closed'],
    },
    'mark_refund_finished': {
        'name_cn': '退款完成',
        'note': '卖家收货检验后，点击【确认收货并退款】，退款完成',
        'transit_type': Task.MANUAL_TRANSIT,
        'condition_list': [conditions.refund_can_finish],
        'run': handlers.mark_refund_finished,
        'mutex': [],
        'target_list': [],
    },
    'mark_refund_closed': {
        'name_cn': '退款关闭',
        'note': '卖家检验后存在争议，退款失败，点击【拒绝退款并关闭】',
        'transit_type': Task.MANUAL_TRANSIT,
        'condition_list': [conditions.refund_can_close],
        'run': handlers.mark_refund_closed,
        'mutex': [],
        'target_list': [],
    },
}
