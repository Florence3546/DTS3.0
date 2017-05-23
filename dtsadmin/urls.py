# coding=UTF-8
import ajax
import views
from django.conf.urls import include, url
from dtsadmin.views import (
    BasicSettingsView,
    InfomationsView,
    EnterpriseListView,
    UserManageView,
    RefundsAndReturnView,
    OrderListView,
	ConsultFeedbackView,
    ApprovalListView,
)

app_name = 'dtsadmin'

ajax_patterns = ([
    # 删除商品分类
    url(r'^delete/good_category/(?P<obj_id>\d+)/$', ajax.delete_good_category_byid, name='delete_good_category_byid'),

    url(r'^model/(?P<model_class>\w+)/verify_enterprise/(?P<obj_id>\d+)/$', ajax.verify_enterprise, name='verify_enterprise'),
    # 快递 修改模态框
    url(r'^switch_delivery_lock/(?P<method>\w+)/(?P<obj_id>\d+)/$', ajax.switch_delivery_lock, name='switch_delivery_lock'),
    # 地区设置 返回地区
    # url(r'^get_area/(?P<method>\w+)/(?P<obj_id>\d+)/$', ajax.get_area, name='get_area'),

    # 启用禁用地址
    url(r'^switch_area_bypk/(?P<model_name>\w+)/(?P<obj_pk>.+)/$', ajax.switch_area_bypk, name='switch_area_bypk'),

    # 企业锁定解锁切换
    url(r'^switch_enterprise_lock/$', ajax.switch_enterprise_lock, name='switch_enterprise_lock'),

    # 添加商品
    url(r'^add_good/$', ajax.add_good, name='add_good'),
    # 返回商品模态框
    url(r'^get_good_form/(?P<modal_name>\w+)/(?P<obj_id>\d+)/$', ajax.get_good_form, name='get_good_form'),
    # 删除商品
    url(r'^delete_good/(?P<obj_id>\d+)/$', ajax.delete_good, name='delete_good'),
    # 更新商品
    url(r'^update_good/$', ajax.update_good, name='update_good'),
    # 上架下架
    url(r'^switch_drug_online/(?P<method>\w+)/(?P<obj_id>\d+)/$', ajax.switch_drug_online, name='switch_drug_online'),

    # 添加用户
    url(r'^add_user/$', ajax.add_user, name='add_user'),

    # 公用锁定解锁切换
    url(r'^switch_lock/(?P<model_class>\w+)/(?P<action>\w+)/$', ajax.switch_lock, name='switch_lock'),
    url(r'^switch_bool/(?P<model_class>\w+)/(?P<obj_id>\d+)/(?P<field>\w+)/$', ajax.switch_bool, name='switch_bool'),
    # 公用保存排序
    url(r'^save_order/(?P<model_name>\w+)/$', ajax.save_order, name='save_order'),
    # 权限管理 权限状态切换
    url(r'^switch_permission_lock/(?P<model_class>\w+)/(?P<action>\w+)/$', ajax.switch_permission_lock, name='switch_permission_lock'),
    # 审核订单 通过 不通过
    url(r'^order_verify/$', ajax.order_verify, name='order_verify'),
    # 商品分类
    url(r'^add/by/category_form/(?P<form_class>\w+)/$', ajax.add_good_category_byform, name='add_good_category_byform'),
    # 通用增删改查
    url(r'^add/by/form/(?P<form_class>\w+)/$', ajax.add_object_byform, name='add_object_byform'),

    url(r'^update/by/form/(?P<form_class>\w+)/$', ajax.update_object_byform, name='update_object_byform'),
    url(r'^update/(?P<model_name>\w+)/(?P<obj_id>\d+)/$', ajax.update_object_byid, name='update_object_byid'),
    url(r'^update/(?P<model_name>\w+)/(?P<obj_pk>.+)/$', ajax.update_object_bypk, name='update_object_bypk'),
    url(r'^get/modal/(?P<modal_name>\w+)/(?P<obj_id>\d+)/$', ajax.get_modal_byid, name='get_modal_byid'),
    url(r'^delete/(?P<model_class>\w+)/(?P<obj_id>\d+)/$', ajax.delete_object_byid, name='delete_object_byid'),
    url(r'^bulk_delete/(?P<model_class>\w+)/$', ajax.bluk_delete_byids, name='bluk_delete_byids'),

    # 信息发布
    url(r'^get_info_publish/(?P<modal_name>\w+)/(?P<obj_id>\d+)/$', ajax.get_info_publish, name='get_info_publish'),
    url(r'^delete_info_publish/(?P<modal_name>\w+)/(?P<obj_id>\d+)/$', ajax.delete_info_publish, name='delete_info_publish'),

     # 跳转商品添加
     url(r'^get_good_byid/(?P<modal_name>\w+)/(?P<obj_id>\d+)/$', ajax.get_good_byid, name='get_good_byid'),
     url(r'^check_good_status/$', ajax.check_good_status, name='check_good_status'),

     # 角色管理
    url(r'^add_role_byform/$', ajax.add_role_byform, name='add_role_byform'),
    url(r'^update_role_byform/$', ajax.update_role_byform, name='update_role_byform'),
    url(r'^del_role_byid/(?P<obj_id>\d+)$', ajax.del_role_byid, name='del_role_byid'),
    url(r'^grant_role_permission/$', ajax.grant_role_permission, name='grant_role_permission'),
    url(r'^get_this_perm_role/$', ajax.get_this_perm_role, name='get_this_perm_role'),

    # 退款退货处理
    url(r'^get_refund_form/(?P<modal_name>\w+)/(?P<obj_id>\d+)/$', ajax.get_refund_form, name='get_refund_form'),
    # 订单操作流程
    url(r'^get_order_log/(?P<modal_name>\w+)/(?P<obj_id>\d+)/$', ajax.get_order_log, name='get_order_log'),
    # 订单编号查看模态框
    url(r'^order_no_check/(?P<obj_id>\d+)/$', ajax.order_no_check, name='order_no_check'),

    #  咨询反馈
     url(r'^delete_consult_feedback/(?P<obj_id>\d+)/$', ajax.delete_consult_feedback, name='delete_consult_feedback'),
     url(r'^get_consult_feedback/(?P<modal_name>\w+)/(?P<obj_id>\d+)/$', ajax.get_consult_feedback, name='get_consult_feedback'),
     url(r'^replied_consult_feedback/$', ajax.replied_consult_feedback, name='replied_consult_feedback'),
], 'ajax')

urlpatterns = [
    url(r'^ajax/', include(ajax_patterns)),
    # 首页
    url(r'^dts_home/$', views.dts_home, name='dts_home'),
    url(r'^show_publish_detail/(\d+)/$', views.show_publish_detail, name='show_publish_detail'),
    url(r'^show_publish_more/(\w+)/$', views.show_publish_more, name='show_publish_more'),
    # 基本设置
    url(r'^basic_info/$', BasicSettingsView.as_view(), name='basic_info'),
    url(r'^data_dictionary/$', views.data_dictionary, name='data_dictionary'),
    url(r'^member_settings/$', views.member_settings, name='member_settings'),
    url(r'^payment_method/$', views.payment_method, name='payment_method'),
    url(r'^shipping_method/$', views.shipping_method, name='shipping_method'),
    url(r'^area_settings/$', views.area_settings, name='area_settings'),
    # 信息管理
    # url(r'^enterprise_list/$', views.enterprise_list, name='enterprise_list'),
    url(r'^enterprise_list/$', EnterpriseListView.as_view(), name='enterprise_list'),
    # url(r'^user_manage/$', views.user_manage, name='user_manage'),
    url(r'^user_manage/$', UserManageView.as_view(), name='user_manage'),
    url(r'^role_manage/$', views.role_manage, name='role_manage'),
    url(r'^permission_manage/$', views.permission_manage, name='permission_manage'),
    url(r'^log_manage/$', views.log_manage, name='log_manage'),
    url(r'^publish_manage/$', InfomationsView.as_view(), name='publish_manage'),
    # 商品管理
    url(r'^good_category/$', views.good_category, name='good_category'),
    url(r'^good_list/$', views.good_list, name='good_list'),
    url(r'^exportGoodList/$', views.export_good_list, name='exportGoodList'),
    # 订单管理
    # url(r'^order_list/$', views.order_list, name='order_list'),
    url(r'^order_list/$', OrderListView.as_view(), name='order_list'),
    url(r'^order_list1/$', views.order_list1, name='order_list1'),
    url(r'^returns_and_refunds/$', RefundsAndReturnView.as_view(), name='returns_and_refunds'),
    # url(r'^approval_list/$', views.approval_list, name='approval_list'),
    url(r'^approval_list/$', ApprovalListView.as_view(), name='approval_list'),
    url(r'^lack_good/$', views.lack_good, name='lack_good'),
	url(r'^trading_record/$', views.trading_record, name='trading_record'),
    url(r'^exportOrderList/$', views.exportOrderList, name='exportOrderList'),
    url(r'^exportOrderDetailList/$', views.exportOrderDetailList, name='exportOrderDetailList'),
    # 售后处理
    url(r'^refund/$', views.refund, name='refund'),
    url(r'^return_good/$', views.return_good, name='return_good'),
    url(r'^data_backup/$', views.data_backup, name='data_backup'),
    url(r'^consult_feedback/$', ConsultFeedbackView.as_view(), name='consult_feedback'),

    url(r'^order_statistic/$', views.order_statistic, name='order_statistic'),

    url(r'^template_list/$', views.template_list, name='template_list'),
    url(r'^supplier_list/$', views.supplier_list, name='supplier_list'),
    url(r'^classify_access/$', views.classify_access, name='classify_access'),
    url(r'^trading_balance/$', views.trading_balance, name='trading_balance'),
    url(r'^ckeditor/$', views.ckeditor, name='ckeditor'),

]
