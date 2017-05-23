# coding=UTF-8
from __future__ import unicode_literals

from bpmn import conditions, handlers
from bpmn.models import Process, Task

# 基础注册审核
BASE_REGISTER = {
    Process.START_TASK: 'register_user',
    Process.END_TASK_LIST: ['active_user', 'invalid_enterprise'],
    'register_user': {
        'name_cn': '注册账号',
        'note': '用户在商城注册账号信息后，系统自动生成注册流程',
        'transit_type': Task.AUTO_TRANSIT,
        'condition_list': [],
        'run': None,
        'mutex': [],
        'target_list': ['be_enterprise', 'active_user'],
    },
    'be_personal': {
        'name_cn': '个人账号初始化',
        'note': '根据注册时的选择，初始化个人账号',
        'transit_type': Task.AUTO_TRANSIT,
        'condition_list': [conditions.be_personal_user],
        'run': None,
        'mutex': [],
        'target_list': ['active_user'],
    },
    'be_enterprise': {
        'name_cn': '企业账号初始化',
        'note': '根据注册时的选择，进入企业账号审核流程',
        'transit_type': Task.AUTO_TRANSIT,
        'condition_list': [conditions.be_enterprise_user],
        'run': handlers.init_review_status,
        'mutex': [],
        'target_list': ['valid_enterprise', 'invalid_enterprise'],
    },
    'valid_enterprise': {
        'name_cn': '企业账号审核通过',
        'note': '运营方的审核人员，审核过企业的资质后，点击【通过】',
        'transit_type': Task.MANUAL_TRANSIT,
        'condition_list': [],
        'run': handlers.valid_enterprise,
        'mutex': [],
        'target_list': ['active_user'],
    },
    'invalid_enterprise': {
        'name_cn': '企业账号审核不通过',
        'note': '运营方的审核人员，审核过企业的资质后，点击【不通过】',
        'transit_type': Task.MANUAL_TRANSIT,
        'condition_list': [],
        'run': handlers.invalid_enterprise,
        'mutex': [],
        'target_list': [],
    },
    'active_user': {
        'name_cn': '激活账号',
        'note': '系统自动激活账号',
        'transit_type': Task.AUTO_TRANSIT,
        'condition_list': [],
        'run': handlers.active_user,
        'mutex': [],
        'target_list': [],
    },
}
