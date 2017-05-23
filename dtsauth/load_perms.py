# coding:UTF-8
import simplejson as json

permission_json =[{
        'codename': 'dtsadmin',
        'name': '后台管理',
        'children': [
            {
                'codename': 'dtsadmin.dts_home',
                'name': '首页',
                'children': []
            },
            {
                'codename': 'dtsadmin.basic_settings',
                'name': '基本设置',
                'children': [
                    {
                        'codename': 'dtsadmin.basic_settings.basic_info',
                        'name': '基本信息',
                        'children': [
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.mag_front_site',
                                'name': '前台网站信息管理',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.view_front_site',
                                'name': '前台网站信息查看',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.mag_admin_logo',
                                'name': '后台Logo信息管理',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.view_admin_logo',
                                'name': '后台Logo信息查看',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.mag_consult_settings',
                                'name': '客服设置信息管理',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.view_consult_settings',
                                'name': '客服设置信息查看',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.mag_auth_settings',
                                'name': '权限设置信息管理',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.view_auth_settings',
                                'name': '权限设置信息查看',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.mag_remind_settings',
                                'name': '信息提醒管理',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.basic_info.view_remind_settings',
                                'name': '信息提醒查看',
                                'children': []
                            },
                        ]
                    },
                    {
                        'codename': 'dtsadmin.basic_settings.data_dictionary',
                        'name': '数据字典',
                        'children': [
                            {
                                'codename': 'dtsadmin.basic_settings.data_dictionary.add_dict',
                                'name': '添加数据字典',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.data_dictionary.del_dict',
                                'name': '删除数据字典',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.data_dictionary.upd_dict',
                                'name': '更新数据字典',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.data_dictionary.add_child_dict',
                                'name': '添加子字典项',
                                'children': []
                            },
                        ]
                    },
                    {
                        'codename': 'dtsadmin.basic_settings.member_settings',
                        'name': '会员设置',
                        'children': [
                            {
                                'codename': 'dtsadmin.basic_settings.member_settings.add_mem_rat',
                                'name': '添加会员等级',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.member_settings.del_mem_rat',
                                'name': '删除会员等级',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.member_settings.upd_mem_rat',
                                'name': '更新会员等级',
                                'children': []
                            }
                        ]
                    },
                    {
                        'codename': 'dtsadmin.basic_settings.payment_method',
                        'name': '支付方式',
                        'children': [
                            {
                                'codename': 'dtsadmin.basic_settings.payment_method.add_pay_mth',
                                'name': '添加支付方式',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.payment_method.del_pay_mth',
                                'name': '删除支付方式',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.payment_method.upd_pay_mth',
                                'name': '更新支付方式',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.payment_method.sav_pay_ord',
                                'name': '保存排序',
                                'children': []
                            },
                        ]
                    },
                    {
                        'codename': 'dtsadmin.basic_settings.shipping_method',
                        'name': '配送方式',
                        'children': [
                            {
                                'codename': 'dtsadmin.basic_settings.shipping_method.add_ship',
                                'name': '添加配送方式',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.shipping_method.del_ship',
                                'name': '删除配送方式',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.shipping_method.upd_ship',
                                'name': '更新配送方式',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.basic_settings.shipping_method.sav_ship_ord',
                                'name': '保存配送方式排序',
                                'children': []
                            },
                        ]
                    },
                    {
                        'codename': 'dtsadmin.basic_settings.area_settings',
                        'name': '地区设置',
                        'children': [
                            {
                                'codename': 'dtsadmin.basic_settings.area_settings.enb_dis_area',
                                'name': '启用/禁用',
                                'children': []
                            }
                        ]
                    }
                ]
            },
            {
                'codename': 'dtsadmin.info_manage',
                'name': '信息管理',
                'children': [
                    {
                        'codename': 'dtsadmin.info_manage.enterprise_list',
                        'name': '企业列表',
                        'children': [
                            {
                                'codename': 'dtsadmin.info_manage.enterprise_list.add_erp',
                                'name': '添加企业',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.enterprise_list.del_erp',
                                'name': '删除企业',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.enterprise_list.upd_erp',
                                'name': '更新企业',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.enterprise_list.ver_erp',
                                'name': '审核企业',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.enterprise_list.lock_erp',
                                'name': '锁定/解锁企业',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.enterprise_list.log_erp',
                                'name': '企业操作日志',
                                'children': []
                            }
                        ]
                    },
                    {
                        'codename': 'dtsadmin.info_manage.user_manage',
                        'name': '用户管理',
                        'children': [
                            {
                                'codename': 'dtsadmin.info_manage.user_manage.add_user',
                                'name': '添加用户',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.user_manage.del_user',
                                'name': '删除用户',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.user_manage.upd_user',
                                'name': '更新用户',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.user_manage.lock_user',
                                'name': '锁定/解锁用户',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.user_manage.log_user',
                                'name': '日志查看',
                                'children': []
                            }
                        ]
                    },
                     {
                        'codename': 'dtsadmin.info_manage.role_manage',
                        'name': '角色管理',
                        'children': [
                            {
                                'codename': 'dtsadmin.info_manage.role_manage.add_role',
                                'name': '添加角色',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.role_manage.del_role',
                                'name': '删除角色',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.role_manage.upd_role',
                                'name': '更新角色',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.role_manage.grant_role',
                                'name': '设置权限',
                                'children': []
                            }
                        ]
                    },
                    {
                        'codename': 'dtsadmin.info_manage.permission_manage',
                        'name': '权限管理',
                        'children': []
                    },
                    {
                        'codename': 'dtsadmin.info_manage.log_manage',
                        'name': '日志管理',
                        'children': []
                    },
                    {
                        'codename': 'dtsadmin.info_manage.publish_manage',
                        'name': '信息管理',
                        'children': [
                            {
                                'codename': 'dtsadmin.info_manage.publish_manage.add_inf_ntc',
                                'name': '添加资讯公告',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.publish_manage.del_inf_ntc',
                                'name': '删除资讯公告',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.publish_manage.upd_inf_ntc',
                                'name': '更新资讯公告',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.publish_manage.pub_inf_ntc',
                                'name': '投放/屏蔽资讯公告',
                                'children': []
                            },
                        ]
                    },
                    {
                        'codename': 'dtsadmin.info_manage.data_backup',
                        'name': '数据备份',
                        'children': [
                            {
                                'codename': 'dtsadmin.info_manage.data_backup.add_data_bak',
                                'name': '新增备份',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.data_backup.auto_data_bak',
                                'name': '自动备份',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.data_backup.ret_data_bak',
                                'name': '还原备份',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.data_backup.del_data_bak',
                                'name': '删除备份',
                                'children': []
                            },
                        ]
                    },
                    {
                        'codename': 'dtsadmin.info_manage.consult_feedback',
                        'name': '咨询反馈',
                        'children': [
                            {
                                'codename': 'dtsadmin.info_manage.consult_feedback.add_con_feed',
                                'name': '添加咨询反馈',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.consult_feedback.del_con_feed',
                                'name': '删除咨询反馈',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.info_manage.consult_feedback.show_con_feed',
                                'name': '设为显示/取消显示咨询反馈',
                                'children': []
                            }
                        ]
                    }
                ]
            },
            {
                'codename': 'dtsadmin.good_manage',
                'name': '商品管理',
                'children': [
                    {
                        'codename': 'dtsadmin.good_manage.good_category',
                        'name': '商品分类',
                        'children': [
                            {
                                'codename': 'dtsadmin.good_manage.good_category.add_ctr',
                                'name': '添加商品分类',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_category.del_ctr',
                                'name': '删除商品分类',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_category.upd_ctr',
                                'name': '更新商品分类',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_category.add_cld_ctr',
                                'name': '添加商品子分类',
                                'children': []
                            }
                        ]
                    },
                    {
                        'codename': 'dtsadmin.good_manage.good_list',
                        'name': '商品列表',
                        'children': [
                            {
                                'codename': 'dtsadmin.good_manage.good_list.add_good',
                                'name': '添加商品',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_list.del_good',
                                'name': '删除商品',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_list.upd_good',
                                'name': '更新商品',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_list.ver_good',
                                'name': '审核商品',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_list.shf_good',
                                'name': '上架/下架商品',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_list.exp_good',
                                'name': '导出商品',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.good_manage.good_list.load_good',
                                'name': '导入商品',
                                'children': []
                            },
                        ]
                    },
                ]
            },
            {
                'codename': 'dtsadmin.order_manage',
                'name': '订单管理',
                'children': [
                    {
                        'codename': 'dtsadmin.order_manage.order_list',
                        'name': '订单列表',
                        'children': [
                            {
                                'codename': 'dtsadmin.order_manage.order_list.exp_ord',
                                'name': '导出订单',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.order_list.view_ord',
                                'name': '审核订单',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.order_list.chg_ord',
                                'name': '改价订单',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.order_list.view_ord_bill',
                                'name': '查看发票号',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.order_list.add_ord_bill',
                                'name': '开票',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.order_list.dev_ord_god',
                                'name': '发货',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.order_list.log_ord_god',
                                'name': '日志',
                                'children': []
                            },
                        ]
                    },
                    {
                        'codename': 'dtsadmin.order_manage.approval_list',
                        'name': '改价审批',
                        'children': []
                    },
                    {
                        'codename': 'dtsadmin.order_manage.returns_and_refunds',
                        'name': '退货退款',
                        'children': [
                            {
                                'codename': 'dtsadmin.order_manage.returns_and_refunds.mark_reviewing',
                                'name': '提交审核',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.returns_and_refunds.mark_reviewing',
                                'name': '退款审核通过',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.returns_and_refunds.mark_refund_finished',
                                'name': '确认收货',
                                'children': []
                            },
                            {
                                'codename': 'dtsadmin.order_manage.returns_and_refunds.mark_refund_closed',
                                'name': '退款关闭',
                                'children': []
                            }
                        ]
                    },
                    {
                        'codename': 'dtsadmin.order_manage.trading_record',
                        'name': '交易记录',
                        'children': []
                    },
                    {
                        'codename': 'dtsadmin.order_manage.lack_good',
                        'name': '缺货登记',
                        'children': [
                            {
                                'codename': 'dtsadmin.order_manage.del_lack_good',
                                'name': '删除缺货登记',
                                'children': []
                            }
                        ]
                    },
                ]
            },
            {
                'codename': 'dtsadmin.tabulate_statistic',
                'name': '汇总统计',
                'children': [
                    {
                        'codename': 'dtsadmin.tabulate_statistic.order_statistic',
                        'name': '订单统计',
                        'children': []
                    }
                ]
            },
            {
                'codename': 'dtsadmin.template_manage',
                'name': '商城装修',
                'children': [
                    {
                        'codename': 'dtsadmin.template_manage.template_list',
                        'name': '模板列表',
                        'children': []
                    }
                ]
            },
            {
                'codename': 'dtsadmin.supplier_manage',
                'name': '供货商管理',
                'children': [
                    {
                        'codename': 'dtsadmin.supplier_manage.supplier_list',
                        'name': '供货商列表',
                        'children': []
                    },
                    {
                        'codename': 'dtsadmin.supplier_manage.clft_auth',
                        'name': '分类权限',
                        'children': []
                    },
                    {
                        'codename': 'dtsadmin.supplier_manage.settle_tran',
                        'name': '交易结算',
                        'children': []
                    }
                ]
            },
        ]
    }
]
perm = json.dumps(permission_json)
lst = json.loads(perm)
for first in lst:  # 循环第一级
    print "------------------------------"
    print first['codename']
    for item in first['children']:
         print item['children']

#
# def print_dict(k, v):
#     if isinstance(v, dict):
#         print k, v
#         for key in v.keys():
#             print_dict(key, v[key])
#     else:
#         print k, v
#
# for k in lst:  # 循环第一级
#     print_dict(k, dict)

