# coding=UTF-8
from __future__ import unicode_literals

from .register import BASE_REGISTER
from .delivery import BASE_DELIVERY
from .refund import BASE_REFUND


REGISTER = 'REGISTER'  # 注册审核
DELIVERY = 'DELIVERY'  # 发货
REFUND = 'REFUND'  # 退货

# 流程类型字典
PROCESS_TYPE_DICT = {
    REGISTER: {
        'name_cn': '注册审核',
        'using': 'BASE_REGISTER',
    },
    DELIVERY: {
        'name_cn': '发货',
        'using': 'BASE_DELIVERY',
    },
    REFUND: {
        'name_cn': '退货',
        'using': 'BASE_REFUND',
    }
}


# 流程配置字典
PROCESS_CONFIG_DICT = {
    'BASE_REGISTER': {
        'name_cn': '基础注册审核',
        'config': BASE_REGISTER,
    },
    'BASE_DELIVERY': {
        'name_cn': '基础发货',
        'config': BASE_DELIVERY,
    },
    'BASE_REFUND': {
        'name_cn': '基础退货',
        'config': BASE_REFUND,
    },
}
