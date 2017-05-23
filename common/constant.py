# coding=UTF-8

USERTYPE_PURCHASER = 'Purchaser'
USERTYPE_SYSTEM = 'System'
USERTYPE_REGULATOR = 'Regulator'
USERTYPE_SUPPLIER = 'Supplier'
USERTYPE_MEMBER = 'Members'
# USERTYPE_OPERATOR = 'Operator'
# USERTYPE_MANUFACTURER = 'Manufacturer'
USERTYPE_CHOICES = [
    (USERTYPE_PURCHASER, '企业用户'),
    (USERTYPE_SYSTEM, '系统用户'),
    (USERTYPE_REGULATOR, '监管部门'),
    (USERTYPE_SUPPLIER, '供应商'),
    (USERTYPE_MEMBER, '个人用户'),
    # (USERTYPE_OPERATOR, '运营商'),
    # (USERTYPE_MANUFACTURER, '生产商'),
]

PAY_ONLINE = 0
PAY_OFFLINE = 1
PAY_ADVANCE = 2
PAY_COD = 3
PAY_TYPE_CHOICES = [
    (PAY_ONLINE, '线上支付'),
    (PAY_OFFLINE, '线下支付'),
    (PAY_ADVANCE, '预存款支付'),
    (PAY_COD, '货到付款'),
]

SHIPPING_HOME = 0
SHIPPING_TP = 1
SHIPPING_NONE = 2
SHIPPING_TYPE_CHOICES = [
    (SHIPPING_HOME, '快递'),
    (SHIPPING_TP, '物流'),
    (SHIPPING_NONE, '自提'),
]

# CONTRACT_INVALID = -1
# CONTRACT_REVIEWING = 0
# CONTRACT_VALID = 1
# CONTRACT_STATUS_CHOICES = [
#     (CONTRACT_REVIEWING, '审核中'),
#     (CONTRACT_VALID, '正式'),
#     (CONTRACT_INVALID, '作废'),
# ]

NO_APPLY = 0
REVIEWING = 1
VALID = 2
INVALID = 3
REVIEW_STATUS_CHOICES = [
    (NO_APPLY, '未申请'),
    (REVIEWING, '待审核'),
    (VALID, '通过'),
    (INVALID, '不通过'),
]

OUT_OF_STOCK = -1
UNKNOWN_STOCK = 0
IN_STOCK = 1
OUT_OF_STOCK = -1
STOCK_STATUS_CHOICES = [
    (UNKNOWN_STOCK, '未知'),
    (IN_STOCK, '有货'),
    (OUT_OF_STOCK, '缺货'),
]

ONLINE_READY = 0
ONLINE_YES = 1
ONLINE_UNDER = 2
ONLINE_CHOICES = [
    (ONLINE_READY, '未上架'),
    (ONLINE_YES, '上架'),
    (ONLINE_UNDER, '下架')
]
# LOGISTICS_TERMINATE = -1
# LOGISTICS_WAITING = 0
# LOGISTICS_CHECKING = 1
# LOGISTICS_PICKING = 2
# LOGISTICS_DELIVERED = 3
# LOGISTICS_ARRIVED = 4
# LOGISTICS_STATUS_CHOICES = [
#     (LOGISTICS_WAITING, '待处理'),
#     (LOGISTICS_CHECKING, '处理中'),
#     (LOGISTICS_PICKING, '拣配中'),
#     (LOGISTICS_TERMINATE, '已中止'),
#     (LOGISTICS_DELIVERED, '已发货'),
#     (LOGISTICS_ARRIVED, '已送达'),
# ]

OTC_A = 0
OTC_B = 1
OTC_C = 2
OTC_TYPE_CHOICES = [
    (OTC_A, '甲类'),  # 全部报销
    (OTC_B, '乙类'),  # 部分自费
    (OTC_C, '丙类'),  # 完全自费
]

PROMOTION_MEMBER = 0
PROMOTION_BULK = 1
PROMOTION_TYPE_CHOICES = [
    (PROMOTION_MEMBER, '会员'),
    (PROMOTION_BULK, '批发'),
]

DISCOUNT_PERCENT = 0
DISCOUNT_PRICE = 1
DISCOUNT_TYPE_CHOICES = [
    (DISCOUNT_PERCENT, '百分比'),
    (DISCOUNT_PRICE, '优惠价'),
]

# 基础信息
SETTINGS_BASIC = 'BASIC'
# 前台网站
SETTINGS_FRONT_SITE = 'FRONT_SITE'
# 后台Logo
SETTINGS_ADMIN_LOGO = 'ADMIN_LOGO'
# 客服设置
SETTINGS_CONSULT_SETTING = 'CONSULT_SETTING'
# 登录验证
SETTINGS_AUTH_SETTING = 'AUTH_SETTING'
# 信息提醒
SETTINGS_REMIND_SETTING = 'REMIND_SETTING'
# 单项字典
SETTINGS_SINGLE = 'SINGLE'

# 支付状态
HAS_REFUND = -1
NOT_PAID = 0
HAS_PAID = 1
PAY_STATUS_CHOICES = [
    (HAS_REFUND, '已退款'),
    (NOT_PAID, '未付款'),
    (HAS_PAID, '已付款'),
]

# 改价状态
# CHANGE_PRICE_STATE_CHOICES = [
#     (0, '无'),
#     (1, '待审批'),
#     (2, '通过'),
#     (3, '不通过'),
# ]

# # 开票状态
# INVOICE_STATE_CHOICES = [
#     (0, '未开票'),
#     (1, '已开票'),
# ]

# # 审核状态
# VERIFY_STATE_CHOICES = [
#     (0, '待审核'),
#     (1, '通过'),
#     (2, '不通过'),
# ]

# 交易状态
ORDER_NOT_PAID = 0
ORDER_HAS_PAID = 1
ORDER_IS_PICKING = 2
ORDER_IS_SHIPPING = 3
ORDER_FINISHED = 4
ORDER_IS_REFUNDING = 5
ORDER_CLOSED = 6
TRADE_STATE_CHOICES = [
    (ORDER_NOT_PAID, '待付款'),
    (ORDER_HAS_PAID, '已付款'),
    (ORDER_IS_PICKING, '拣配中'),
    (ORDER_IS_SHIPPING, '已发货'),
    (ORDER_FINISHED, '交易完成'),
    (ORDER_IS_REFUNDING, '退款中'),
    (ORDER_CLOSED, '交易关闭'),
]

# 退款类型
REFUND = 0
RETURN = 1
REFUND_TYPE_CHOICES = [
    (REFUND, '退款'),
    (RETURN, '退货'),
]

# 退款状态
REFUND_HANDLING = 0
REFUND_REVIEWING = 1
REFUND_RETURNING = 2
REFUND_RECEIVING = 3
REFUND_FINISHED = 4
REFUND_CLOSED = 5
REFUND_STATUS_CHOICES = [
    (REFUND_HANDLING, '处理中'),
    (REFUND_REVIEWING, '审核中'),
    (REFUND_RETURNING, '等待退货'),
    (REFUND_RECEIVING, '等待收货'),
    (REFUND_FINISHED, '退款完成'),
    (REFUND_CLOSED, '退款关闭'),
]

# 性别
# todo by liuhuan 2017-4-11 企业列表 注册
MALE = 1
FAMALE = 2
GENDER_CHOICE = [
    (MALE, '男'),
    (FAMALE, '女'),
]

# 分页数
PAGE_LIMIT = 25

# 页面
PAGE_FOOT = 'PAGE_FOOT'
PAGE_ESHOP_HOME = 'ESHOP_HOME'
PAGE_GOOD_LIST = 'GOOD_LIST'
PAGE_GOOD_DETAIL = 'GOOD_DETAIL'
PAGE_CHOICES = [
    (PAGE_FOOT, '商城页脚'),
    (PAGE_ESHOP_HOME, '商城首页'),
    (PAGE_GOOD_LIST, '商品列表页'),
    (PAGE_GOOD_DETAIL, '商品详情页'),
]

# URL 导航字典
NAV_URL_DICT = {
    'dts_home': ['dts_home'],
    'basic_settings': [
        'basic_info',
        'data_dictionary',
        'member_settings',
        'payment_method',
        'shipping_method',
        'area_settings',
    ],
    'info_manage': [
        'enterprise_list',
        'user_manage',
        'role_manage',
        'permission_manage',
        'log_manage',
        'publish_manage',
        'data_backup',
        'consult_feedback',
    ],
    'good_manage': [
        'good_category',
        'good_list',
    ],
    'order_manage': [
        'order_list',
        'approval_list',
        'returns_and_refunds',
        'trading_record',
        'lack_good',
        'order_statistic',
    ],
}

# 信息发布 相关标识
INFO_STATUS_PENDING = 0
INFO_STATUS_ACTIVE = 1
INFO_STATUS_SHIELD = 2
INFO_STATUS_CHOICES = [
    (INFO_STATUS_PENDING, '待投放'),
    (INFO_STATUS_ACTIVE, '投放中'),
    (INFO_STATUS_SHIELD, '已屏蔽'),
]
INFO_TYPE_INFO = 'I'
INFO_TYPE_NOTICE = 'N'
INFO_TYPE_CHOICES = [
    (INFO_TYPE_INFO, '资讯'),
    (INFO_TYPE_NOTICE, '公告'),
]

# BOOL相对应的值
BOOL_YES = 1
BOOL_NO = 0

AUDIENCE_ALL = 'A'
AUDIENCE_PURCHASER = 'P'
AUDIENCE_ENTERPRISE = 'E'
AUDIENCE_MEMBER = 'M'
AUDIENCE_OPERATOR = 'O'
INFO_AUDIENCE_CHOICES = [
    (AUDIENCE_ALL, '全部'),
    (AUDIENCE_PURCHASER, '采购方'),     # 企业会员 + 个人会员
    (AUDIENCE_ENTERPRISE, '企业会员'),
    (AUDIENCE_MEMBER, '个人会员'),
    (AUDIENCE_OPERATOR, '运营商'),
]

#咨询反馈
CF_STATUS_PENDING = 0
CF_STATUS_ACTIVE = 1
CF_STATUS_CHOICES = [
    (CF_STATUS_PENDING, '未处理'),
    (CF_STATUS_ACTIVE, '已处理'),
]

CONSULT = 0
FEEDBACK = 1
REPLY = 2
FEEDBACK_TYPE_CHOICES = [
    (CONSULT, '咨询留言'),
    (FEEDBACK, '投诉建议'),
    (REPLY, '客服答复'),
]

SITE_MESSAGE_TYPE_ORDER = 0
SITE_MESSAGE_TYPE_SYSTEM = 1
SITE_MESSAGE_TYPE = [
    (SITE_MESSAGE_TYPE_ORDER, '订单信息'),
    (SITE_MESSAGE_TYPE_SYSTEM, '系统消息'),
]

GOOD_MODAL = 'Good'
ORDER_MODAL = 'Order'
USER_MODAL = 'User'
ENTERPRISE_MODAL = 'Enterprise'
ROLE_MODAL = 'Role'
SETTINGS_MODAL = 'Settings'
REFUND_MODAL = 'RefundRecord'
RECORD_DATA_TYPE_CHOICES = [
    (GOOD_MODAL, '商品'),
    (ORDER_MODAL, '订单'),
    (USER_MODAL, '账户'),
    (ENTERPRISE_MODAL, '企业'),
    (ROLE_MODAL, '角色'),
    (SETTINGS_MODAL, '信息设置'),
    (REFUND_MODAL, '退款退货'),
]

#  交易类型 账户记录
TRADE_TYPE_ALL = 0
TRADE_TYPE_COST = 1
TRADE_TYPE_PAY = 2
TRADE_TYPE_REFUND = 3
TRADE_TYPE_CHOICES = [
    (TRADE_TYPE_ALL, ' 全部'),
    (TRADE_TYPE_COST, '消费'),
    (TRADE_TYPE_PAY, '充值'),
    (TRADE_TYPE_REFUND, '退款'),
]

