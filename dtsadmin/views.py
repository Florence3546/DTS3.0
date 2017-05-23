# coding=UTF-8
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http.response import HttpResponse
from common.models import SettingsType, SettingsItem
from common.models import Region
from common.utils.utils_log import log
from common.utils.utils_paginator import get_paginator_bar
from common.templatetags.extras import media_url
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dtsauth.models import Enterprise, Role, Permission, User, EnterpriseQualification, OperateRecord
from order.models import ShippingMethod, Order, OrderItem, PaymentMethod, ChangePriceRecord, RefundRecord, ReceivingAddress, Invoice
from good.models import Good, DrugAttr, GoodCategory, LackRegister
from eshop.forms import TestUploadFileForm, ConsultFeedbackForm
from django.views.generic import View
from django.http import JsonResponse
from models import Informations
import datetime
import simplejson as json
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from dtsauth.permission import check_permission
from dtsadmin.models import ConsultFeedback
from dtsadmin.forms import LogoSittingsForm
from dtsauth.forms import EnterpriseForm, UserForm
from .forms import AddEnterpriseForm, AddUserForm, EnterpriseQualificationForm
from slugify import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime
from django.db.models import Sum, F, Q
from bpmn.models import Process
from bpmn.configs import REFUND as BPMN_REFUND
from eshop.models import SiteMessage
from common.utils import (
    utils_export_excel as export_excel,
    utils_datetime,
    utils_mysql,
)

from common.constant import (
    STOCK_STATUS_CHOICES,
    SETTINGS_BASIC,  # 基本信息
    REVIEW_STATUS_CHOICES,  # 审核状态
    STOCK_STATUS_CHOICES,  # 缺货状态
    USERTYPE_CHOICES,  # 用户类型
    PAGE_LIMIT,  # 分页限制
    PAY_TYPE_CHOICES,  # 支付类型
    SHIPPING_TYPE_CHOICES,  # 发货方式
    SETTINGS_SINGLE,
    TRADE_STATE_CHOICES,  # 交易状态
    INFO_TYPE_INFO,  # 资讯
    INFO_TYPE_NOTICE,  # 公告
    BOOL_YES,  # BOOL 是
    BOOL_NO,  # BOOL 否
    REVIEWING,  # 审核中
    ORDER_IS_PICKING,  # 拣配中
    ORDER_NOT_PAID,  # 待付款
    PAY_COD,  # 付款方式
    REFUND,  # 退款
    RETURN,  # 退货
    REFUND_HANDLING,  # 处理中
    REFUND_REVIEWING,  # 审核中
    REFUND_RECEIVING,  # 等待收货
    CONSULT,  # 咨询留言
    FEEDBACK,  # 投诉建议
    RECORD_DATA_TYPE_CHOICES,  #
    CF_STATUS_PENDING,
    CF_STATUS_ACTIVE,
    ORDER_MODAL,
    USERTYPE_PURCHASER,
    ORDER_HAS_PAID,
    ORDER_IS_SHIPPING,
    ORDER_FINISHED,
    ORDER_IS_REFUNDING,
    VALID,
    REFUND_MODAL,
    HAS_PAID,
    SETTINGS_ADMIN_LOGO,
    SETTINGS_CONSULT_SETTING,
    SETTINGS_REMIND_SETTING,
    ORDER_CLOSED,
    SITE_MESSAGE_TYPE_SYSTEM,  # 系统消息
    SITE_MESSAGE_TYPE_ORDER,  # 订单信息
    NO_APPLY,  # 改价审批未申请
)


def dts_home(request):
    """后台首页"""
    info_mations = []  # 资讯
    info_notics = []  # 公告
    new_order_count = 0  # 今日新增订单
    new_user_count = 0  # 今日新增用户
    new_order_money = 0  # 今日订单金额
    verify_order_count = 0  # 待审核的订单
    pick_order_count = 0  # 待发货的订单
    change_count = 0  # 待处理的改价申请
    payment_count = 0  # 待确认的收款
    refund_count = 0  # 待处理的退款
    return_count = 0  # 待处理的退货
    ref_ret_count = 0  # 待审核退款退货
    ref_rec_count = 0  # 待确认收货
    erp_rev_count = 0  # 待审核的企业
    gd_rev_count = 0  # 待审核商品
    confd_count = 0  # 待回复留言
    lack_count = 0  # 缺货登记
    admin_logo_obj = {'logo_path': '', 'logo_href': ''}  # 后台Logo
    cur_date = datetime.date.today()  # 当前系统时间
    try:
        # 加载资讯
        info_kwargs = {'info_type': INFO_TYPE_INFO, 'info_status': BOOL_YES, 'start_date__lte': cur_date,
                       'end_date__gte': cur_date}
        info_mations = Informations.objects.filter(**info_kwargs).order_by('order_no')[0:5]
        # 加载公告
        notic_kwargs = {'info_type': INFO_TYPE_NOTICE, 'info_status': BOOL_YES, 'start_date__lte': cur_date,
                        'end_date__gte': cur_date}
        info_notics = Informations.objects.filter(**notic_kwargs).order_by('order_no')[0:12]
        date_dict = get_search_date()
        # 统计今日新增用户
        user_kwargs = {'is_deleted': BOOL_NO,
                       'usertype': USERTYPE_PURCHASER,
                       'date_joined__gte': date_dict['today'],
                       'date_joined__lt': date_dict['tomorrow']
                       }
        new_user_count = User.objects.filter(**user_kwargs).count()
        # 统计今日新增订单
        order_kwargs = {
            'ord_time__gte': date_dict['today'],
            'ord_time__lt': date_dict['tomorrow']
        }
        new_order_count = Order.objects.filter(**order_kwargs).count()
        # 统计今日订单金额
        # 除去待付款和交易关闭状态的订单
        trade_state_status = [ORDER_HAS_PAID, ORDER_IS_PICKING, ORDER_IS_SHIPPING, ORDER_FINISHED, ORDER_IS_REFUNDING]
        order_money_kwargs = {
            'trade_state__in': trade_state_status,
            'ord_time__gte': date_dict['today'],
            'ord_time__lt': date_dict['tomorrow']
        }
        new_order_money = Order.objects.filter(**order_money_kwargs).aggregate(total_real_price=Sum('real_price'))[
            'total_real_price']
        # 后台Logo
        settings_item_list = SettingsItem.objects.filter(s_type__code=SETTINGS_BASIC).filter(name=SETTINGS_ADMIN_LOGO)
        if settings_item_list:
            admin_logo_obj = json.loads(settings_item_list[0].note)
        request.session['admin_logo_obj'] = admin_logo_obj
        # 统计待审核，待发货的订单, 待处理的改价申请,
        sql_str = '''SELECT verify.ver_count, pick.pick_count, chang.change_count, payment.payment_count ,
                refund.refund_count, ret.return_count, ref_ret.ref_ret_count, ref_rec.ref_rec_count,
                erp.erp_rev_count, gd.gd_rev_count, confd.confd_count, lack_gd.lack_count FROM
                (SELECT COUNT(1) ver_count,1 t_id FROM order_order od WHERE od.verify_state=%s ) verify
                LEFT JOIN (SELECT COUNT(1) pick_count,1 t_id FROM order_order od WHERE od.trade_state=%s) pick
                ON verify.t_id = pick.t_id
                LEFT JOIN (SELECT COUNT(1) change_count,1 t_id FROM order_order od WHERE od.change_price_state=%s ) chang
                ON verify.t_id = chang.t_id
                LEFT JOIN (SELECT COUNT(1) payment_count,1 t_id FROM order_order od INNER JOIN order_paymentmethod op 
                ON od.payment_method_id=op.id WHERE op.pay_type=%s AND od.trade_state=%s) payment
                ON verify.t_id = payment.t_id
                LEFT JOIN (SELECT COUNT(1) refund_count, 1 t_id FROM order_refundrecord orf WHERE orf.refund_type=%s
                AND orf.refund_status=%s) refund
                ON verify.t_id = refund.t_id 
                LEFT JOIN (SELECT COUNT(1) return_count, 1 t_id FROM order_refundrecord orf WHERE orf.refund_type=%s
                AND orf.refund_status=%s) ret
                ON verify.t_id = ret.t_id
                LEFT JOIN (SELECT COUNT(1) ref_ret_count, 1 t_id FROM order_refundrecord orf WHERE orf.refund_status=%s) ref_ret
                ON verify.t_id = ref_ret.t_id 
                LEFT JOIN (SELECT COUNT(1) ref_rec_count, 1 t_id FROM order_refundrecord orf WHERE orf.refund_status=%s) ref_rec
                ON verify.t_id = ref_rec.t_id 
                LEFT JOIN (SELECT COUNT(1) erp_rev_count, 1 t_id FROM dtsauth_enterprise erp WHERE erp.review_status=%s) erp
                ON verify.t_id = erp.t_id 
                LEFT JOIN (SELECT COUNT(1) gd_rev_count, 1 t_id FROM good_good gd WHERE gd.is_qualified=%s) gd
                ON verify.t_id = gd.t_id 
                LEFT JOIN (SELECT COUNT(1) confd_count, 1 t_id FROM dtsadmin_consultfeedback conf 
                WHERE conf.feedback_type IN (%s,%s) AND conf.is_replied=%s) confd
                ON verify.t_id = confd.t_id  
                LEFT JOIN (SELECT COUNT(1) lack_count,1 t_id FROM good_lackregister lack 
                INNER JOIN good_good gd ON lack.good_id = gd.id
                WHERE gd.stock_amount = 0) lack_gd
                ON verify.t_id = lack_gd.t_id'''
        sql_val_lst = [REVIEWING,  # 审核状态审核中 1
                       ORDER_IS_PICKING,  # 交易状态：拣配中 2
                       REVIEWING,  # 改价申请审核中 1
                       PAY_COD,  # 支付方式，货到付款 3
                       ORDER_NOT_PAID,  # 待付款 0
                       REFUND,  # 退款 0
                       REFUND_HANDLING,  # 处理中 0
                       RETURN,  # 退货  1
                       REFUND_HANDLING,  # 处理中 0
                       REFUND_REVIEWING,  # 审核中 1
                       REFUND_RECEIVING,  # 等待收货 3
                       REVIEWING,  # 审核中 1
                       REVIEWING,  # 审核中 1
                       CONSULT,  # 咨询留言 0
                       FEEDBACK,  # 投诉建议 1
                       BOOL_NO,  # 未回复 0
                       ]
        order_lst = utils_mysql.execute_query_sql(sql_str, sql_val_lst)
        if order_lst is not None:
            verify_order_count = order_lst[0]['ver_count']
            pick_order_count = order_lst[0]['pick_count']
            change_count = order_lst[0]['change_count']
            payment_count = order_lst[0]['payment_count']
            refund_count = order_lst[0]['refund_count']
            return_count = order_lst[0]['return_count']
            ref_ret_count = order_lst[0]['ref_ret_count']
            ref_rec_count = order_lst[0]['ref_rec_count']
            erp_rev_count = order_lst[0]['erp_rev_count']
            gd_rev_count = order_lst[0]['gd_rev_count']
            confd_count = order_lst[0]['confd_count']
            lack_count = order_lst[0]['lack_count']
    except Exception, e:
        log.error("dts_home raise exception,error:%s" % e)
    result = {
        'info_mations': info_mations,
        'info_notics': info_notics,
        'new_user_count': new_user_count,
        'new_order_count': new_order_count,
        'new_order_money': new_order_money,
        'verify_order_count': verify_order_count,
        'pick_order_count': pick_order_count,
        'change_count': change_count,
        'payment_count': payment_count,
        'refund_count': refund_count,
        'return_count': return_count,
        'ref_ret_count': ref_ret_count,
        'ref_rec_count': ref_rec_count,
        'erp_rev_count': erp_rev_count,
        'gd_rev_count': gd_rev_count,
        'confd_count': confd_count,
        'lack_count': lack_count,
        'cur_date': cur_date,
    }
    return render(request, 'dtsadmin/dts_home.html', result)


def show_publish_detail(request, info_id):
    """显示公告资讯详情"""
    publish_obj = Informations.objects.filter(pk=info_id).first()
    result = {
        'obj': publish_obj
    }
    return render(request, 'dtsadmin/publish_info_show.html', result)


def show_publish_more(request, info_type):
    """显示更多公告资讯"""
    pub_lst = []
    try:
        cur_date = datetime.date.today()  # 当前系统时间
        info_kwargs = {'info_type': info_type, 'info_status': '1', 'start_date__lte': cur_date,
                       'end_date__gte': cur_date}
        pub_lst = Informations.objects.filter(**info_kwargs).order_by('order_no')
    except Exception, e:
        log.error("show_publish_more raise exception,error:%s" % e)
    result = {
        'pub_lst': pub_lst,
        'info_type': info_type,
    }
    return render(request, 'dtsadmin/publish_info_list.html', result)


# 基本信息
def basic_info(request):
    # 定义变量
    sittings_item_dict = {}
    # 前端网站数据
    front_site_item = SettingsItem.objects.filter(name='FRONT_SITE').first()
    if front_site_item:
        front_site = json.loads(front_site_item.note)
        sittings_item_dict['FRONT_SITE'] = front_site
    # 后台LOGO
    return render(request, 'dtsadmin/basic_info.html', {'sittings_item_dict': sittings_item_dict})


def data_dictionary(request):
    # 定义变量
    result = []
    type_item_dict = {}
    try:
        # 归纳数据
        item_set = SettingsItem.objects.select_related('s_type').exclude(s_type__code=SETTINGS_BASIC).order_by('name')
        for item in item_set:
            type_item_dict.setdefault(item.s_type.code, []).append(item)
        type_set = SettingsType.objects.order_by('name')
        for s_type in type_set:
            item_list = type_item_dict.get(s_type.code, [])
            if s_type.code == SETTINGS_SINGLE:
                result.insert(0, (s_type, item_list))
            else:
                result.append((s_type, item_list))
    except Exception, e:
        log.exception("data_dictionary raise,Error:%s" % e)
    return render(request, 'dtsadmin/data_dictionary.html', {'result': result})


def payment_method(request):
    # payment_list = PaymentMethod.objects.all().exclude(id__in=[1,2,3]).order_by('order_no')
    payment_list = PaymentMethod.objects.all().order_by('order_no')
    obj = {}
    obj['pay_type_choices'] = PAY_TYPE_CHOICES
    return render(request, 'dtsadmin/payment_method.html', {
        'payment_list': payment_list,
        'obj': obj
    })


def member_settings(request):
    return render(request, 'dtsadmin/member_settings.html', {})


# 配送方式
def shipping_method(request):
    delivery_list = ShippingMethod.objects.all().exclude(pk__in=[1, 2, 3]).order_by('order_no')
    obj = {}
    obj['shipping_type_choices'] = SHIPPING_TYPE_CHOICES
    return render(request, 'dtsadmin/shipping_method.html', {
        'delivery_list': delivery_list,
        'obj': obj
    })


# 地区设置
def area_settings(request):
    def get_flat_tree(key, data_dict, result, level=0):
        node_list = data_dict.get(key, [])
        for node in node_list:
            node.level = level
            node.level1 = node.level + 1
            node.has_child = node.id in data_dict
            result.append(node)
            get_flat_tree(node.id, data_dict, result, level + 1)
        return result

    region_set = Region.objects.all().order_by('region_code')
    region_id_list = [obj.id for obj in region_set]
    region_dict = {}
    for obj in region_set:
        parent_id = obj.parent_id if obj.parent_id in region_id_list else 0
        region_dict.setdefault(parent_id, []).append(obj)
    data_list = get_flat_tree(1, region_dict, [])
    return render(request, 'dtsadmin/area_settings.html', {'data_list': data_list})


class EnterpriseListView(View):
    """基本信息"""

    def get(self, request):
        # 查询 get方式
        # if request.method == 'POST':
        kwargs = {}
        # 企业名称
        if 'search_enterprise_name' in request.GET:
            kwargs['name__contains'] = request.GET.get('search_enterprise_name')
        # 法人代表
        if 'search_enterprise_legal_repr' in request.GET:
            kwargs['legal_repr__contains'] = request.GET['search_enterprise_legal_repr']
        # 经营方式
        if 'search_enterprise_operate_mode' in request.GET:
            kwargs['operate_mode__contains'] = request.GET['search_enterprise_operate_mode']
        # 会员等级
        # if 'search_enterprise_member_grade' in request.GET:
        #     kwargs['legal_repr__contains'] = request.GET['search_enterprise_member_grade']
        # 营业期限自
        if 'search_enterprise_created_from' in request.GET and request.GET['search_enterprise_created_from']:
            kwargs['created__gte'] = request.GET['search_enterprise_created_from']
        # 营业期限到
        if 'search_enterprise_created_to' in request.GET and request.GET['search_enterprise_created_to']:
            created_to = datetime.datetime.strptime(request.GET['search_enterprise_created_to'],
                                                    "%Y-%m-%d") + datetime.timedelta(days=1)
            kwargs['created__lt'] = created_to
        # 审核状态
        if 'search_enterprise_review_status' in request.GET and request.GET['search_enterprise_review_status']:
            kwargs['review_status'] = int(request.GET['search_enterprise_review_status'])

        # 企业状态
        if 'search_enterprise_is_lock' in request.GET and request.GET['search_enterprise_is_lock']:
            kwargs['is_lock'] = bool(int(request.GET['search_enterprise_is_lock']))

        data_set = Enterprise.objects.filter(**kwargs).order_by('review_status', ).order_by('-created')
        # else:
        #     data_set = Enterprise.objects.all().order_by('id')

        paginator = Paginator(data_set, PAGE_LIMIT)
        page = request.GET.get('page', 1)

        try:
            data_list = paginator.page(page)
        except PageNotAnInteger:
            data_list = paginator.page(1)
        except EmptyPage:
            data_list = paginator.page(paginator.num_pages)

        # TODO cache
        operate_mode_choices = SettingsType.get_item_list('OPERATE_MODE')
        member_level_choices = SettingsType.get_item_list('MEMBER_LEVEL')
        # operate_mode_choices = []
        # member_level_choices = []
        choices = {}
        # 经营方式
        choices['operate_mode'] = operate_mode_choices
        # 审核状态
        choices['review_status'] = [(str(k), v) for k, v in REVIEW_STATUS_CHOICES]
        # 经营范围
        # operate_set = SettingsItem.objects.filter(s_type_id=4)
        operate_set = SettingsType.get_item_list('OPERATE_SCOPE')

        # 企业选择补全
        choices['auto_enter'] = Enterprise.objects.all().values('name', 'pinyin').distinct()
        return render(request, 'dtsadmin/enterprise_list.html', {
            'data_list': data_list,
            'pagi_bar': get_paginator_bar(data_list),
            'operate_mode_choices': operate_mode_choices,
            'choices': choices,
            'member_level_choices': member_level_choices,
            'operate_scope': operate_set,
        })

    def post(self, request):
        if 'action' in request.POST:
            action = request.POST.get('action')

            if request.POST.get('action') == 'add_enterprise':
                result = self._handle_add_enterprise(request)

            elif request.POST.get('action') == 'get_enterprise':
                return self._handle_get_enterprise(request)

            elif request.POST.get('action') == 'update_enterprise':
                result = self._handle_update_enterprise(request)

            # 审核企业
            elif request.POST.get('action') == 'verify_enterprise':
                return self._handle_verify_enterprise(request)
            # 审核 通过 不通过
            elif request.POST.get('action') == 'verify_enter':
                result = self._handle_verify_enter(request)

            elif action == 'look_enterprise':
                return self._handle_look_enterprise(request)

            # 日志
            # elif action == 'look_enterprises':
            #     return self._handle_look_enterprises(request)

            # 批量删除
            elif action == 'delete_enterprises':
                result = self._handle_delete_enterprises(request)

            else:
                result = {
                    'status': 0,
                    'msg': '请求action错误'
                }
        else:
            result = {
                'status': 0,
                'msg': '请求错误'
            }

        return JsonResponse(result)

    def _handle_add_enterprise(self, request):
        """处理企业用户注册"""
        enterprise_form = AddEnterpriseForm(request.POST, request.FILES)
        if enterprise_form.is_valid():
            # 验证表单字段
            try:
                enter_name = request.POST.get('enterprise_name', '')
                Enterprise.objects.get(name=enter_name)
                result = {
                    'status': 0,
                    'msg': '该企业已经存在'
                }
                return result
            except ObjectDoesNotExist:
                short_name = request.POST.get('short_name', '')
                pinyin = slugify(enter_name)
                pinyin = ''.join([word[0].upper() for word in pinyin.split('-') if word])  # 拼音码
                operate_mode = request.POST.get('operate_mode', '')  # 经营方式
                region = request.POST.get('region', '')  # 地区
                address = request.POST.get('address', '')  # 详细地址
                enter_phone = request.POST.get('enter_phone', '')  # 企业电话
                legal_repr = request.POST.get('legal_repr', '')  # 法人代表
                biz_scope = request.POST.get('biz_scope', '')  # 经营范围

                with transaction.atomic():

                    enter = Enterprise()
                    enter.name = enter_name
                    enter.short_name = short_name
                    enter.pinyin = pinyin
                    enter.operate_mode = operate_mode
                    enter.region = region
                    enter.address = address
                    enter.phone = enter_phone
                    enter.legal_repr = legal_repr
                    enter.biz_scope = biz_scope
                    enter.is_lock = False
                    enter.review_status = 2
                    enter.save()

                    try:
                        username = request.POST.get('username', '')
                        email = request.POST.get('email', '')
                        first_name = request.POST.get('first_name', '')
                        user_phone = request.POST.get('user_phone', '')
                        gender = request.POST.get('gender', '')

                        User.objects.get(username=username)
                        result = {
                            'status': 0,
                            'msg': '用户已经存在'
                        }
                        return result
                    except ObjectDoesNotExist:
                        passwd = request.POST.get('passwd', '')
                        passwd2 = request.POST.get('passwd2', '')
                        if passwd == passwd2:
                            user = User()
                            user.username = username
                            user.email = email
                            user.first_name = first_name
                            user.gender = gender
                            user.phone = user_phone
                            user.password = make_password(passwd)
                            user.enterprise = enter
                            user.is_master = True
                            user.is_active = False
                            user.save()
                        else:
                            result = {
                                'status': 0,
                                'msg': '两次密码不一致'
                            }
                            return result

                        # 资质文件处理
                        # 企业许可证
                        if enterprise_form.cleaned_data['qyxk']:
                            enter_file = EnterpriseQualification()
                            enter_file.enterprise = enter
                            enter_file.photo = enterprise_form.cleaned_data['qyxk']
                            enter_file.save()

                        # 营业执照
                        if enterprise_form.cleaned_data['yyzz']:
                            enter_file = EnterpriseQualification()
                            enter_file.enterprise = enter
                            enter_file.photo = enterprise_form.cleaned_data['yyzz']
                            enter_file.save()

                        # 法人委托书
                        if enterprise_form.cleaned_data['wts']:
                            enter_file = EnterpriseQualification()
                            enter_file.enterprise = enter
                            enter_file.photo = enterprise_form.cleaned_data['wts']
                            enter_file.save()

                        result = {
                            'status': 1,
                            'msg': '添加成功'
                        }
                        return result
        else:
            result = {
                'status': 0,
                'msg': str(enterprise_form.errors)
            }
            return result

    def _handle_get_enterprise(self, request):
        try:
            pk = int(request.POST.get('pk'))
            obj = Enterprise.objects.get(pk=pk)
            try:
                user = User.objects.get(enterprise=pk, is_master=True)
            except ObjectDoesNotExist, e:
                log.error("EnterpriseListView _handle_get_enterprise %s" % e)
                result = {
                    'status': 0,
                    'msg': '该企业没有主账号，请在用户管理中关联'
                }
                return JsonResponse(result)

            try:
                qualification = EnterpriseQualification.objects.filter(enterprise=pk).order_by('-upload_time')
            except ObjectDoesNotExist, e:
                log.error("EnterpriseListView _handle_get_enterprise %s" % e)
                result = {
                    'status': 0,
                    'msg': 'dfasdf'
                }
                return JsonResponse(result)

                # return render(request, 'dtsadmin/modals/modal_error.html', {
                #     'error': "没有发现企业图片 %s" % e
                # })

            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']

            # operate_mode_choices = SettingsType.get_item_list('OPERATE_MODE')
            operate_mode_choices = SettingsItem.objects.filter(s_type_id=2)
            choices = {}
            choices['operate_mode'] = operate_mode_choices
            operate_set = SettingsItem.objects.filter(s_type_id=4)

            return render(request, 'dtsadmin/modals/modal_enterprise.html', {
                'obj': obj,
                'user': user,
                'qualification': qualification,
                'choices': choices,
                'operate_scope': operate_set,
            })
        except Exception, e:
            log.error("EnterpriseListView _handle_get_enterprise %s" % e)
            result = {
                'status': 0,
                'msg': '内部错误'
            }
            return JsonResponse(result)

    def _handle_update_enterprise(self, request):

        # todo liu 结构优化

        user_phone = request.POST.get('user_phone')
        enter_phone = request.POST.get('enter_phone')

        enter = Enterprise.objects.get(pk=int(request.POST.get('pk', '')))
        user = User.objects.get(pk=int(request.POST.get('user_pk')))
        temp_dict = request.POST.dict()

        # 处理修改密码
        passwd = request.POST.get('passwd')
        passwd2 = request.POST.get('passwd2')
        if passwd and passwd2:
            if passwd == passwd2:
                temp_dict['password'] = make_password(passwd)
            else:
                result = {
                    'status': 0,
                    'msg': '两次密码不一致',
                }
                return result
        else:
            temp_dict['password'] = user.password

        temp_dict['phone'] = user_phone
        # temp_dict['enterprise_id'] = enter.id
        user_form = UserForm(temp_dict, instance=user)

        if user_form.is_valid():
            # user_form.save()
            try:
                with transaction.atomic():
                    user.enterprise_id = enter.id
                    user.save()

                    temp_dict['phone'] = enter_phone
                    temp_dict['name'] = request.POST.get('enterprise_name', '')
                    temp_dict['external_id'] = enter.external_id
                    enterprise_form = EnterpriseForm(temp_dict, instance=enter)

                    # 处理企业资质图片
                    qualification = EnterpriseQualificationForm(request.POST, request.FILES)
                    if qualification.is_valid():
                        # 企业许可证
                        if qualification.cleaned_data['qyxk']:
                            enter_file = EnterpriseQualification()
                            enter_file.enterprise = enter
                            enter_file.photo = qualification.cleaned_data['qyxk']
                            enter_file.save()
                        # 营业执照
                        if qualification.cleaned_data['yyzz']:
                            enter_file = EnterpriseQualification()
                            enter_file.enterprise = enter
                            enter_file.photo = qualification.cleaned_data['yyzz']
                            enter_file.save()

                        # 法人委托书
                        if qualification.cleaned_data['wts']:
                            enter_file = EnterpriseQualification()
                            enter_file.enterprise = enter
                            enter_file.photo = qualification.cleaned_data['wts']
                            enter_file.save()

                    if enterprise_form.is_valid():
                        enterprise_form.save()

                        result = {
                            'status': 1,
                            'msg': '修改成功',
                        }
                        return result
                    else:
                        result = {
                            'status': 0,
                            # 'msg': str(enterprise_form.errors)
                            'log': str(enterprise_form.errors),
                            'msg': '企业修改失败'

                        }
                        return result
            except Exception, e:
                result = {
                    'status': 0,
                    # 'msg': str(enterprise_form.errors)
                    'log': str(e),
                    'msg': '表单修改失败'
                }
                return result
        else:
            result = {
                'status': 0,
                # 'msg': str(enterprise_form.errors)
                'msg': '企业主用户修改失败'
            }
            return result

    def _handle_verify_enterprise(self, request):
        try:
            pk = int(request.POST.get('pk'))
            obj = Enterprise.objects.get(pk=pk)
            print pk
            try:
                user = User.objects.get(enterprise=pk, is_master=True)
            except ObjectDoesNotExist, e:
                log.error("EnterpriseListView _handle_get_enterprise %s" % e)
                # return render(request, 'dtsadmin/modals/modal_error.html', {
                #     'error': "没有发现企业图片 %s" % e
                # })
                result = {
                    'status': 0,
                    'msg': '该企业没有主账号，请在用户管理中关联'
                }
                return JsonResponse(result)

            try:
                qualification = EnterpriseQualification.objects.filter(enterprise=pk).order_by('-upload_time')
            except ObjectDoesNotExist, e:
                log.error("EnterpriseListView _handle_get_enterprise %s" % e)
                #
                # result = {
                #     'status': 0,
                #     'msg': 'dfasdf'
                # }
                # return result

                # return render(request, 'dtsadmin/modals/modal_error.html', {
                #     'error': "没有发现企业图片 %s" % e
                # })

            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']

            # operate_mode_choices = SettingsType.get_item_list('OPERATE_MODE')
            operate_mode_choices = SettingsItem.objects.filter(s_type_id=2)
            choices = {}
            choices['operate_mode'] = operate_mode_choices
            operate_set = SettingsItem.objects.filter(s_type_id=4)

            return render(request, 'dtsadmin/modals/modal_enterprise_check.html', {
                'obj': obj,
                'user': user,
                'qualification': qualification,
                'choices': choices,
                'operate_scope': operate_set,
            })


        except Exception, e:
            log.error("EnterpriseListView _handle_get_enterprise %s" % e)
            result = {
                'status': 0,
                'msg': '内部错误'
            }

    def _handle_verify_enter(self, request):
        try:
            with transaction.atomic():
                pk = int(request.POST.get('pk'))
                method = request.POST.get('method')
                if method == 'verify_enter_nopass':
                    with transaction.atomic():
                        User.objects.filter(is_master=True, enterprise_id=pk).update(is_active=False)
                        Enterprise.objects.filter(pk=pk).update(review_status=3)
                        # 添加站内消息
                        remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                        if remind_settings:
                            remind_item = json.loads(remind_settings.note)
                            remind_item_seting = remind_item['remind_settings']
                            item_list = json.loads(remind_item_seting)
                            flag = item_list[0]['mail']
                            if flag == 'Y':
                                id = User.objects.get(enterprise=pk, is_master=True).id
                                SiteMessage.objects.create(
                                    user_id=id,
                                    msg_type=SITE_MESSAGE_TYPE_SYSTEM,
                                    contant='企业注册审核不通过',
                                    is_read=False,
                                )
                        result = {
                            'status': 0,
                            'msg': '该企业审核不通过'
                        }
                        return result
                elif method == 'verify_enter_pass':
                    User.objects.filter(is_master=True, enterprise_id=pk).update(is_active=True)
                    Enterprise.objects.filter(pk=pk).update(review_status=2)
                    # 添加站内消息
                    remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                    if remind_settings:
                        remind_item = json.loads(remind_settings.note)
                        remind_item_seting = remind_item['remind_settings']
                        item_list = json.loads(remind_item_seting)
                        flag = item_list[0]['mail']
                        if flag == 'Y':
                            id = User.objects.get(enterprise=pk, is_master=True).id
                            SiteMessage.objects.create(
                                user_id=id,
                                msg_type=SITE_MESSAGE_TYPE_SYSTEM,
                                contant='企业注册审核通过',
                                is_read=False,
                            )
                    result = {
                        'status': 1,
                        'msg': '该企业审核通过',
                    }
                    return result
                else:
                    result = {
                        'status': 1,
                        'msg': 'method错误',
                    }
                    return result
        except Exception, e:
            log.error("EnterpriseListView _handle_verify_enter %s" % e)
            result = {
                'status': 0,
                'msg': '内部错误'
            }
            return result

    def _handle_look_enterprise(self, request):
        try:
            pk = int(request.POST.get('pk'))
            obj = Enterprise.objects.get(pk=pk)
            try:
                user = User.objects.get(enterprise=pk, is_master=True)
            except ObjectDoesNotExist, e:
                log.error("EnterpriseListView _handle_get_enterprise %s" % e)
                result = {
                    'status': 0,
                    'msg': '该企业没有主账号，请在用户管理中关联'
                }
                return JsonResponse(result)

            try:
                qualification = EnterpriseQualification.objects.filter(enterprise=pk).order_by('upload_time')
            except ObjectDoesNotExist, e:
                log.error("EnterpriseListView _handle_get_enterprise %s" % e)
                result = {
                    'status': 0,
                    'msg': 'dfasdf'
                }
                return JsonResponse(result)

                # return render(request, 'dtsadmin/modals/modal_error.html', {
                #     'error': "没有发现企业图片 %s" % e
                # })

            # todo 删掉
            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']

            # operate_mode_choices = SettingsType.get_item_list('OPERATE_MODE')
            operate_mode_choices = SettingsItem.objects.filter(s_type_id=2)
            choices = {}
            choices['operate_mode'] = operate_mode_choices
            operate_set = SettingsItem.objects.filter(s_type_id=4)

            return render(request, 'dtsadmin/modals/modal_enterprise_check.html', {
                'obj': obj,
                'user': user,
                'qualification': qualification,
                'choices': choices,
                'operate_scope': operate_set,
            })


        except Exception, e:
            log.error("EnterpriseListView _handle_get_enterprise %s" % e)
            result = {
                'status': 0,
                'msg': '内部错误'
            }
            return JsonResponse(result)

    def _handle_delete_enterprises(self, request):
        from django.db.models.deletion import ProtectedError
        try:
            enter_id_list = request.POST.get('enter_id_list')
            if enter_id_list:
                enter_id_list = json.loads(enter_id_list)
                is_delete = Enterprise.objects.filter(id__in=enter_id_list).delete()
                result = {
                    'status': 1,
                    'msg': "批量删除成功"
                }
                return result


        except ProtectedError:
            result = {
                'status': 0,
                'msg': '请先删掉关联用户'
            }
            return result

        except Exception, e:
            log.error("EnterpriseListView _handle_verify_enter %s" % e)
            result = {
                'status': 0,
                'msg': '内部错误'
            }
            return result


# def enterprise_list(request):
#     # 查询 更多查询条件
#     if request.method == 'POST':
#         kwargs = {}
#         # 企业名称
#         if 'search_enterprise_name' in request.POST:
#             kwargs['name__contains'] = request.POST['search_enterprise_name']
#         # 法人代表
#         if 'search_enterprise_legal_repr' in request.POST:
#             kwargs['legal_repr__contains'] = request.POST['search_enterprise_legal_repr']
#         # 经营方式
#         if 'search_enterprise_operate_mode' in request.POST:
#             kwargs['operate_mode__contains'] = request.POST['search_enterprise_operate_mode']
#         # 会员等级
#         # if 'search_enterprise_member_grade' in request.POST:
#         #     kwargs['legal_repr__contains'] = request.POST['search_enterprise_member_grade']
#
#         # 营业期限自
#         if 'search_enterprise_created_from' in request.POST and request.POST['search_enterprise_created_from']:
#             kwargs['created__gte'] = request.POST['search_enterprise_created_from']
#         # 营业期限到
#         if 'search_enterprise_created_to' in request.POST and request.POST['search_enterprise_created_to']:
#             created_to = datetime.datetime.strptime(request.POST['search_enterprise_created_to'],
#                                                     "%Y-%m-%d") + datetime.timedelta(days=1)
#             kwargs['created__lt'] = created_to
#         # 企业状态
#         if 'search_enterprise_is_lock' in request.POST and request.POST['search_enterprise_is_lock']:
#             kwargs['is_lock'] = bool(int(request.POST['search_enterprise_is_lock']))
#         data_set = Enterprise.objects.filter(**kwargs)
#     else:
#         data_set = Enterprise.objects.all().order_by('id')
#
#     paginator = Paginator(data_set, PAGE_LIMIT)
#     page = request.GET.get('page', 1)
#
#     try:
#         data_list = paginator.page(page)
#     except PageNotAnInteger:
#         data_list = paginator.page(1)
#     except EmptyPage:
#         data_list = paginator.page(paginator.num_pages)
#
#     # TODO cache
#     operate_mode_choices = SettingsType.get_item_list('OPERATE_MODE')
#     member_level_choices = SettingsType.get_item_list('MEMBER_LEVEL')
#     # operate_mode_choices = []
#     # member_level_choices = []
#
#
#     choices = {}
#     choices['operate_mode'] = operate_mode_choices
#     # 经营范围
#     operate_set = SettingsItem.objects.filter(s_type_id=4)
#
#     return render(request, 'dtsadmin/enterprise_list.html', {
#         'data_list': data_list,
#         'paginator': paginator,
#         'page': page,
#         'page_limit': PAGE_LIMIT,
#         'operate_mode_choices': operate_mode_choices,
#         'choices': choices,
#         'member_level_choices': member_level_choices,
#         'operate_scope': operate_set,
#     })


class UserManageView(View):
    """用户管理"""

    def get(self, request):
        kwargs = {}
        # 用户名
        if 'username' in request.GET and request.GET['username']:
            kwargs['username__contains'] = request.GET['username']
        # 用户类型
        if 'usertype' in request.GET and request.GET['usertype']:
            kwargs['usertype__contains'] = request.GET['usertype']
        # 姓名 只取first_name
        if 'first_name' in request.GET:
            kwargs['first_name__contains'] = request.GET['first_name']
        # 企业名称
        if 'enter_name' in request.GET and request.GET['enter_name']:
            # todo liuhuan 2017年3月14日 企业全称简称
            kwargs['enterprise__name__contains'] = request.GET['enter_name']
        # 用户状态 锁定 解锁
        if 'is_active' in request.GET and request.GET['is_active']:
            kwargs['is_active'] = request.GET['is_active']
            # kwargs['is_active__contains'] = request.POST['is_active']
        # 注册时间开始
        if 'date_joined_from' in request.GET and request.GET['date_joined_from']:
            kwargs['date_joined__gte'] = request.GET['date_joined_from']
        # 注册时间结束
        if 'date_joined_to' in request.GET and request.GET['date_joined_to']:
            date_joined_to = datetime.datetime.strptime(request.GET['date_joined_to'], "%Y-%m-%d") + datetime.timedelta(
                days=1)
            print date_joined_to
            kwargs['date_joined__lt'] = date_joined_to
        # 只删除未删除的用户
        kwargs['is_deleted'] = False
        data_set = User.objects.select_related('enterprise').filter(**kwargs).order_by('pk').order_by('-date_joined')

        # 后台分页
        paginator = Paginator(data_set, PAGE_LIMIT)
        page = request.GET.get('page', 1)

        try:
            data_list = paginator.page(page)
        except PageNotAnInteger:
            data_list = paginator.page(1)
        except EmptyPage:
            data_list = paginator.page(paginator.num_pages)

        # 用户类型 从数据字典里取
        # usertype_choices = SettingsType.get_item_list('USERTYPE')

        choices = {}
        # 用户类型
        choices['usertype'] = USERTYPE_CHOICES
        # 系统用户角色
        choices['system_role'] = Role.objects.filter(usertype='System')
        # 企业名称列表
        # todo 2017-5-2 liu 浏览器缓存
        enterprise_set = Enterprise.objects.all()
        choices['enterprise'] = enterprise_set
        choices['auto_user'] = User.objects.all().values('username', 'first_name').distinct()
        return render(request, 'dtsadmin/user_manage.html', {
            'data_list': data_list,
            'choices': choices,
            'pagi_bar': get_paginator_bar(data_list),
        })

    def post(self, request):
        if 'action' in request.POST:
            action = request.POST.get('action')
            if request.POST.get('action') == 'add_user':
                return self._handle_add_user(request)
            elif request.POST.get('action') == 'get_user':
                return self._handle_get_user(request)
            elif request.POST.get('action') == 'update_user':
                result = self._handle_update_user(request)
            elif request.POST.get('action') == 'personage_info':
                return self._handle_update_personage_info(request)
            elif request.POST.get('action') == 'personage_password':
                return self._handle_update_personage_password(request)

            # 查看用户
            elif action == 'look_user':
                return self._handle_look_user(request)

            # 日志
            # elif action == 'look_enterprises':
            #     return self._handle_look_enterprises(request)

            # 批量删除
            elif action == 'delete_users':
                result = self._handle_delete_users(request)

            else:
                result = {
                    'status': 0,
                    'msg': '请求action错误'
                }

        else:
            result = {
                'status': 0,
                'msg': '请求错误'
            }

        return JsonResponse(result)

    def _handle_add_user(self, request):
        """用户管理 添加用户"""
        user_type = request.POST.get('user_type', '')  # 用户类型 系统用户 个人会员 ..
        user_form = AddUserForm(request.POST)
        if user_form.is_valid():
            # 验证表单字段
            try:
                username = request.POST.get('username', '')
                # todo 其他页面不用get处理
                if User.objects.filter(username=username):
                    result = {
                        'status': 0,
                        'msg': '该用户已经存在'
                    }
                    return JsonResponse(result)
                else:
                    passwd = request.POST.get('passwd', '')
                    passwd2 = request.POST.get('passwd2', '')
                    if passwd == passwd2:
                        user = User()
                        email = request.POST.get('email', '')
                        first_name = request.POST.get('first_name', '')
                        phone = request.POST.get('phone', '')
                        gender = request.POST.get('gender', '')
                        enter_pk = request.POST.get('enter_pk', '') or request.POST.get('system_enter_pk', '')
                        is_master = request.POST.get('is_master', '')
                        user.username = username
                        user.email = email
                        user.first_name = first_name
                        user.usertype = user_type
                        user.gender = gender
                        user.phone = phone
                        user.enterprise_id = int(enter_pk)
                        user.password = make_password(passwd)
                        user.is_master = True if is_master == '1' else False
                        user.is_active = True
                        enterprise = Enterprise.objects.filter(id=enter_pk).first()
                        u_region = enterprise.region
                        u_address = enterprise.address

                        # 个人会员
                        if user_type == 'Members':
                            user.save()
                            result = {
                                'status': 1,
                                'msg': '添加成功'
                            }
                            return JsonResponse(result)
                        # 企业会员
                        # 用户收货地址设置
                        if user_type == 'Purchaser':
                            enter_pk = request.POST.get('enter_pk', '')
                            user.enterprise_id = int(enter_pk) if enter_pk else None
                            is_master = User.objects.filter(is_master=True, enterprise_id=enter_pk)
                            if is_master:
                                if is_master.first().enterprise:
                                    is_master.update(is_master=False)
                            user.save()
                            user_address = ReceivingAddress()
                            user_address.user = user
                            user_address.region = u_region
                            user_address.address = u_address
                            user_address.is_default = True
                            user_address.save()
                            result = {
                                'status': 1,
                                'msg': '添加成功'
                            }
                            return JsonResponse(result)
                        # 系统用户
                        elif user_type == 'System':
                            department = request.POST.get('department', '')
                            role_list = request.POST.getlist('role_list', '')
                            # 检查角色
                            is_role_exist = Role.objects.filter(id__in=role_list)
                            if not is_role_exist:
                                result = {
                                    'status': 0,
                                    'msg': '权限表不存在'
                                }
                                return JsonResponse(result)
                            user.department = department
                            user.enterprise_id = int(enter_pk)
                            user.save()
                            # 添加角色
                            for role in role_list:
                                user.role.add(role)

                            result = {
                                'status': 1,
                                'msg': '添加成功'
                            }
                            return JsonResponse(result)
                        # 监管部门 供应商
                        else:
                            enter_pk = request.POST.get('enter_pk', '')
                            user.enterprise_id = int(enter_pk) if enter_pk else None
                            user.save()
                            result = {
                                'status': 1,
                                'msg': '添加成功'
                            }
                            return JsonResponse(result)
                    else:
                        result = {
                            'status': 0,
                            'msg': '两次密码不一致'
                        }
                        return JsonResponse(result)
                return JsonResponse(result)

            except Exception, e:
                log.error("UserManage _handle_add_user,error:%s" % e)
                result = {
                    'status': 0,
                    'log': str(e),
                    'msg': '网络异常，请刷新重试'
                }
                return JsonResponse(result)

        else:
            result = {
                'status': 0,
                # 'msg': json.dumps(user_form.errors),
                'msg': str(user_form.errors)
            }
            return JsonResponse(result)

    def _handle_get_user(self, request):
        try:
            user_pk = int(request.POST.get('pk'))
            try:
                obj = User.objects.get(pk=user_pk)
            except ObjectDoesNotExist, e:
                log.error("EnterpriseListView _handle_get_enterprise %s" % e)
                result = {
                    'status': 0,
                    'msg': '没有这个用户'
                }
                return JsonResponse(result)

            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']

            # operate_mode_choices = SettingsType.get_item_list('OPERATE_MODE')

            # 用户类型 固定值
            # usertype_choices = SettingsType.get_item_list('USERTYPE')


            choices = {}
            choices['usertype'] = USERTYPE_CHOICES
            choices['system_role'] = Role.objects.filter(usertype='System')
            enterprise_set = Enterprise.objects.all()
            choices['enterprise'] = enterprise_set
            checked = [role.id for role in obj.role.all()]

            return render(request, 'dtsadmin/modals/modal_user.html', {
                'obj': obj,
                'choices': choices,
                'checked': checked,
            })

        except Exception, e:
            log.error("EnterpriseListView _handle_get_enterprise %s" % e)
            result = {
                'status': 0,
                'msg': '内部错误'
            }
            return JsonResponse(result)

    def _handle_update_user(self, request):
        user_pk = request.POST.get('user_pk')
        phone = request.POST.get('phone')
        role_list = request.POST.getlist('role_list', '')
        user = User.objects.get(pk=user_pk)
        temp_dict = request.POST.dict()
        # 处理修改密码
        passwd = request.POST.get('passwd')
        passwd2 = request.POST.get('passwd2')
        if passwd and passwd2:
            if passwd == passwd2:
                temp_dict['password'] = make_password(passwd)
            else:
                result = {
                    'status': 0,
                    'msg': '两次密码不一致',
                }
                return result
        else:
            temp_dict['password'] = user.password
        enter_pk = request.POST.get('enter_pk')
        temp_dict['enterprise'] = enter_pk
        temp_dict['role'] = request.POST.getlist('role_list', '')
        user_form = UserForm(temp_dict, instance=user)
        if user_form.is_valid():
            form = user_form.save(commit=False)
            form.save()
            user_form.save_m2m()
            result = {
                'status': 1,
                'msg': '修改成功',
            }
            return result
        else:
            result = {
                'status': 0,
                # 'msg': str(enterprise_form.errors)
                'msg': '用户修改失败'
            }
            return result

    def _handle_update_personage_info(self, request):
        # 头部个人资料修改
        try:
            user_pk = request.POST.get('user_pk')
            first_name = request.POST.get('first_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            gender = int(request.POST.get('gender'))
            user = User.objects.get(pk=user_pk)
            user.first_name = first_name
            user.phone = phone
            user.email = email
            user.gender = gender
            user.save()
            result = {
                'status': 1,
                'msg': '修改成功',
            }
        except Exception, e:
            log.error("UserManageView _handle_update_personage_info %s" % e)
            result = {
                'status': 0,
                'msg': '网络异常，请稍后重试！'
            }
        return JsonResponse(result)

    def _handle_update_personage_password(self, request):
        # 头部个人密码修改
        try:
            user_pk = request.POST.get('user_pk')
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            user = User.objects.get(pk=user_pk)
            if user.check_password(old_password):
                user.password = make_password(new_password)
                user.save()
                result = {
                    'status': 1,
                    'msg': '修改成功',
                }
            else:
                result = {
                    'status': 0,
                    'msg': '密码输入错误',
                }
        except Exception, e:
            log.error("UserManageView _handle_update_personage_password %s" % e)
            result = {
                'status': 0,
                'msg': '网络异常，请稍后重试！'
            }
        return JsonResponse(result)

    def _handle_look_user(self, request):
        try:
            pk = int(request.POST.get('pk'))
            try:
                user = User.objects.get(pk=pk)
            except ObjectDoesNotExist, e:
                log.error("EnterpriseListView _handle_get_enterprise %s" % e)
                result = {
                    'status': 0,
                    'msg': '没有这个用户'
                }
                return JsonResponse(result)
            # obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']

            return render(request, 'dtsadmin/modals/modal_user_check.html', {
                # 'obj': obj,
                'user': user,
            })


        except Exception, e:
            log.error("EnterpriseListView _handle_get_enterprise %s" % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e
            }
            return JsonResponse(result)


# def user_manage(request):
#     if request.method == 'POST':
#         kwargs = {}
#         # 用户名
#         if 'username' in request.POST and request.POST['username']:
#             kwargs['username__contains'] = request.POST['username']
#         # 用户类型
#         if 'usertype' in request.POST and request.POST['usertype']:
#             kwargs['usertype__contains'] = request.POST['usertype']
#         # 姓名 只取first_name
#         if 'first_name' in request.POST:
#             kwargs['first_name__contains'] = request.POST['first_name']
#         # 企业名称
#         if 'enter_name' in request.POST and request.POST['enter_name']:
#             # todo liuhuan 2017年3月14日 企业全称简称
#             kwargs['enterprise__name__contains'] = request.POST['enter_name']
#         # 用户状态 锁定 解锁
#         if 'is_active' in request.POST and request.POST['is_active']:
#             kwargs['is_active'] = request.POST['is_active']
#             # kwargs['is_active__contains'] = request.POST['is_active']
#         # 注册时间开始
#         if 'date_joined_from' in request.POST and request.POST['date_joined_from']:
#             kwargs['date_joined__gte'] = request.POST['date_joined_from']
#         # 注册时间结束
#         if 'date_joined_to' in request.POST and request.POST['date_joined_to']:
#             date_joined_to = datetime.datetime.strptime(request.POST['date_joined_to'],
#                                                         "%Y-%m-%d") + datetime.timedelta(days=1)
#             kwargs['date_joined__lt'] = date_joined_to
#
#         print kwargs
#         data_set = User.objects.select_related('enterprise').filter(**kwargs).order_by('pk')
#
#     else:
#         data_set = User.objects.select_related('enterprise').all().order_by('pk')
#
#     paginator = Paginator(data_set, PAGE_LIMIT)
#     page = request.GET.get('page', 1)
#
#     try:
#         data_list = paginator.page(page)
#     except PageNotAnInteger:
#         data_list = paginator.page(1)
#     except EmptyPage:
#         data_list = paginator.page(page.num_page)
#
#     obj = {}
#     obj['usertype_choices'] = USERTYPE_CHOICES
#     return render(request, 'dtsadmin/user_manage.html', {
#         'data_list': data_list,
#         'paginator': paginator,
#         'page': page,
#         'page_limit': PAGE_LIMIT,
#         'obj': obj,
#     })


def inform_manage_menu(request):
    # return render(request, 'dtsadmin/company_list.html', {})
    return redirect('/dtsadmin/company_list/')


def permission_manage(request):
    def get_flat_tree(key, data_dict, result, level=0):
        node_list = data_dict.get(key, [])
        for node in node_list:
            node.level = level
            node.has_child = node.codename in data_dict
            result.append(node)
            get_flat_tree(node.codename, data_dict, result, level + 1)
        return result

    permission_set = Permission.objects.all().order_by('codename')
    codename_list = [obj.codename for obj in permission_set]
    permission_dict = {}
    for obj in permission_set:
        path_list = obj.codename.split('.')
        parent_codename = '.'.join(path_list[:-1])
        parent_codename = parent_codename if parent_codename in codename_list else ''
        permission_dict.setdefault(parent_codename, []).append(obj)
    data_list = get_flat_tree('', permission_dict, [])
    return render(request, 'dtsadmin/permission_manage.html', {'data_list': data_list})


def log_manage(request):
    kwargs = {}
    operator_name = request.GET.get('operator_name', '').strip()
    data_type = request.GET.get('data_type')
    created_from = request.GET.get('created_from')
    created_to = request.GET.get('created_to')
    note = request.GET.get('note', '').strip()
    operate_cn = request.GET.get('operate_cn', '').strip()

    if operator_name:
        kwargs['operator__first_name__icontains'] = operator_name
    if data_type:
        kwargs['data_type'] = data_type
    if created_from:
        kwargs['created__gte'] = parse_datetime(created_from + ' 00:00:00')
    if created_to:
        kwargs['created__lt'] = parse_datetime(created_to + ' 00:00:00') + datetime.timedelta(days=1)
    if note:
        kwargs['note__icontains'] = note
    if operate_cn:
        kwargs['operate_cn__icontains'] = operate_cn

    record_list = OperateRecord.objects.select_related('operator').filter(**kwargs)
    paginator = Paginator(record_list, PAGE_LIMIT)
    page = request.GET.get('page')
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    return render(request, 'dtsadmin/log_manage.html', {
        'data_list': data_list,
        'RECORD_DATA_TYPE_CHOICES': RECORD_DATA_TYPE_CHOICES,
        'pagi_bar': get_paginator_bar(data_list),
    })


def good_category(request):
    def get_flat_tree(key, data_dict, result, level=0):
        node_list = data_dict.get(key, [])
        for node in node_list:
            node.level = level
            node.level1 = node.level + 1
            node.has_child = node.id in data_dict
            result.append(node)
            get_flat_tree(node.id, data_dict, result, level + 1)
        return result

    good_category_set = GoodCategory.objects.all().order_by('path')
    category_id_list = [obj.id for obj in good_category_set]
    good_category_dict = {}
    for obj in good_category_set:
        parent_id_list = [_id for _id in obj.path.split('/') if _id]
        parent_id = int(parent_id_list[-1]) if parent_id_list else ''
        parent_id = parent_id if parent_id in category_id_list else ''
        good_category_dict.setdefault(parent_id, []).append(obj)
    data_list = get_flat_tree('', good_category_dict, [])
    return render(request, 'dtsadmin/good_category.html', {'data_list': data_list})


def good_list(request):
    """商品列表"""
    try:
        enter_select = []
        dosage_form_select = []
        category_select = []
        good_list = []
        kwargs = {}
        s_is_qua = ''
        good_set = []
        good_list = []
        # 查询 更多查询条件
        # 商品编码
        if 'search_good_external_id' in request.GET:
            kwargs['external_id__contains'] = request.GET['search_good_external_id']
        # 商品名称
        if 'search_good_trade_name' in request.GET:
            kwargs['trade_name__contains'] = request.GET['search_good_trade_name']
        # 剂型
        if 'search_good_dosage_form' in request.GET:
            dosage_form = request.GET.get('search_good_dosage_form')
            if dosage_form != '':
                kwargs['drugattr__dosage_form__contains'] = dosage_form
        # 分类
        if 'search_good_category' in request.GET:
            sea_category = request.GET.get('search_good_category')
            if sea_category != '':
                kwargs['category_id'] = sea_category
        # 批准文号
        if 'search_good_license' in request.GET:
            license = request.GET.get('search_good_license')
            if license != '':
                kwargs['drugattr__license__contains'] = license
        # 出售状态
        if 'search_good_is_online' in request.GET:
            sea_is_online = request.GET['search_good_is_online']
            if sea_is_online != '':
                kwargs['is_online'] = sea_is_online
        if 's_is_qua' in request.GET:
            s_is_qua = request.GET.get('s_is_qua')
            if s_is_qua != '':
                kwargs['is_qualified'] = s_is_qua
        good_set = Good.objects.filter(**kwargs).order_by('-external_id')
        # 后台分页实现
        paginator = Paginator(good_set, PAGE_LIMIT)
        page = request.GET.get('page', 1)
        try:
            good_list = paginator.page(page)
        except PageNotAnInteger, e:
            good_list = paginator.page(1)
            log.error('good_list error:%s' % e)
        except EmptyPage, e:
            good_list = paginator.page(paginator.num_pages)
            log.error('good_list error:%s' % e)
        # 查询条件值
        setting_type = SettingsType.objects.filter(code='DOSAGE_FORM').first()
        if setting_type is not None:
            dosage_form_select = SettingsItem.objects.filter(s_type=setting_type)
        enter_select = Enterprise.objects.filter(review_status=VALID)
        category_select_list = GoodCategory.objects.exclude(path='/').order_by('path')
        category_select = [{'id': str(k.id), 'name': k.name} for k in category_select_list]
    except Exception, e:
        log.error("good_list raise,Error:%s" % e)
    # 商品选择补全
    choices = {}
    choices['auto_good'] = Good.objects.all().values('name', 'pinyin').distinct()
    return render(request, 'dtsadmin/good_list.html', {
        'data_list': good_list,
        'enter_select': enter_select,
        'dosage_form_select': dosage_form_select,
        'category_select': category_select,
        's_is_qua': s_is_qua,
        'page': page,
        'pagi_bar': get_paginator_bar(good_list),
        'choices': choices,
    })


class OrderListView(View):
    """订单列表"""

    def get(self, request):
        page_no = int(request.GET.get('page_no', 1))
        kwargs = {}
        # 订单编号
        if 'order_no' in request.GET and request.GET['order_no']:
            kwargs['order_no__contains'] = request.GET['order_no']
        # 订单状态 交易状态
        if 'trade_state' in request.GET and request.GET['trade_state']:
            kwargs['trade_state__contains'] = request.GET['trade_state']
        # 下单人
        if 'buyer_name' in request.GET and request.GET['buyer_name']:
            kwargs['buyer__username__contains'] = request.GET['buyer_name']
        # 企业名称
        if 'purchaser_name' in request.GET and request.GET['purchaser_name']:
            kwargs['purchaser__name__contains'] = request.GET['purchaser_name']

        # 支付方式
        if 'payment_method_type' in request.GET and request.GET['payment_method_type']:
            kwargs['payment_method__pay_type'] = int(request.GET['payment_method_type'])

        # 下单时间开始
        if 'ord_time_from' in request.GET and request.GET['ord_time_from']:
            kwargs['ord_time__gte'] = request.GET['ord_time_from']
        # 下单时间结束
        if 'ord_time_to' in request.GET and request.GET['ord_time_to']:
            ord_time_to = datetime.datetime.strptime(request.GET['ord_time_to'], "%Y-%m-%d") + datetime.timedelta(
                days=1)
            kwargs['ord_time__lt'] = ord_time_to

        # 订单金额开始
        if 'total_price_from' in request.GET and request.GET['total_price_from']:
            kwargs['total_price__gte'] = int(request.GET['total_price_from']) * 100
        # 订单金额结束
        if 'total_price_to' in request.GET and request.GET['total_price_to']:
            kwargs['total_price__lt'] = int(request.GET['total_price_to']) * 100

        # 开票状态
        if 'order_invoice_state' in request.GET and request.GET['order_invoice_state']:
            invoice_state = int(request.GET['order_invoice_state'])
            if invoice_state:
                kwargs['invoice_no__regex'] = r'\d'
            else:
                kwargs['invoice_no'] = ''
        # 审核状态
        if 'verify_state' in request.GET and request.GET['verify_state']:
            kwargs['verify_state__contains'] = request.GET['verify_state']
        # 商品信息 商品名称
        filter_order_good_name = 'order_good_name' in request.GET and request.GET['order_good_name']
        if kwargs or filter_order_good_name:
            filter_order_id_list = []
            if filter_order_good_name:
                filter_order_id_list = list(set(
                    OrderItem.objects.filter(good__name__icontains=request.GET['order_good_name']).values_list(
                        'order_id',
                        flat=True)))

            if kwargs:
                order_list = list(Order.objects.filter(**kwargs).order_by('-ord_time'))
                if filter_order_good_name:
                    order_list = [order for order in order_list if order.id in filter_order_id_list]
            else:
                order_list = list(Order.objects.filter(id__in=filter_order_id_list))
                # page_total = len(order_list)
                # order_list = order_list[PAGE_LIMIT * (page_no - 1):PAGE_LIMIT * page_no]
                # order_list = Order.objects.filter(**kwargs)
        else:
            # page_no = int(request.GET.get('page_no', 1))
            # page_total = Order.objects.count()
            # order_list = Order.objects.all()[PAGE_LIMIT * (page_no - 1):PAGE_LIMIT * page_no]
            order_list = Order.objects.all().order_by('-ord_time')
        paginator = Paginator(order_list, PAGE_LIMIT)
        page = int(request.GET.get('page', 1))
        try:
            order_data = paginator.page(page)
        except PageNotAnInteger:
            order_data = paginator.page(1)
        except EmptyPage:
            order_data = paginator.page(paginator.num_pages)
        except Exception, e:
            log.error('OrderListView get %s' % e)
            result = {
                'status': 0,
                'msg': 'OrderListView 内部错误'

            }
            return JsonResponse(result)

        obj = {}
        # 交易状态 转换成字符串 前台比对
        obj['trade_state_choices'] = [(str(k), v) for k, v in TRADE_STATE_CHOICES]

        # 支付方式 转换成字符串 前台比对
        pay_set = PaymentMethod.objects.all()
        pay_list = []
        for a in pay_set:
            pay_list.append({"id": str(a.pk), "name": a.name_cn})
        obj['paymentmethod'] = pay_list
        # 开票状态
        # obj['invoice_state_choices'] = [(str(k), v) for k, v in INVOICE_STATE_CHOICES]
        choices = {}
        # 交易状态
        # choices['trade_state'] = TRADE_STATE_CHOICES
        choices['trade_state'] = [(str(k), v) for k, v in TRADE_STATE_CHOICES]
        # 审核状态
        choices['review_status'] = [(str(k), v) for k, v in REVIEW_STATUS_CHOICES]
        # 支付方式
        choices['payment_method'] = PAY_TYPE_CHOICES
        return render(request, 'dtsadmin/order_list.html', {
            'order_data': order_data,
            'choices': choices,
            'obj': obj,
            'pagi_bar': get_paginator_bar(order_data),
        })

    def post(self, request):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action', '')
                # 查看订单信息
                if action == 'look_order':
                    return self._handle_look_order(request)
                # 审核订单信息
                elif action == 'verify_order':
                    return OrderListView._handle_verify_order(request)
                # 获取改价模态框
                elif action == 'get_change_price':
                    return self._handle_get_change_price(request)
                # 处理改价申请
                elif action == 'change_price':
                    return self._handle_change_price(request)
                # 开票
                elif action == 'order_invoice':
                    return self._handle_order_invoice(request)
                # 查看发票
                elif action == 'look_invoice':
                    return self._handle_look_invoice(request)
                # 发货look
                elif action == 'deliver_order':
                    return OrderListView._handle_deliver_order(request)
                # # 日志
                # elif action == 'remove_failed_goods':
                #     result = self._handle_remove_failed_goods(request)
                # 确认收款
                elif action == 'receipt_order':
                    result = OrderListView._handle_receipt_order(request)
                else:
                    result = {
                        'status': 0,
                        'msg': '请求action错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': '请求错误'
                }
            return JsonResponse(result)
        except Exception, e:
            log.error('OrderListView %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e

            }
        return JsonResponse(result)

    def _handle_look_order(self, request):
        try:
            pk = int(request.POST.get('pk', ''))
            user_pk = request.user.id
            order = Order.objects.filter(pk=pk).first()
            user = User.objects.filter(pk=int(user_pk)).first()

            return render(request, 'dtsadmin/modals/modal_order_approve.html', {
                'order': order,
                'user': user,

            })
        except Exception, e:
            log.error('_handle_look_order %s' % e)
            result = {
                'status': 0,
                'msg': '_handle_look_order错误 %s' % e
            }
            return JsonResponse(result)

    # def _handle_look_invoice(self, request):
    #     try:
    #         pk = int(request.POST.get('pk', ''))
    #         invoice = Invoice.objects.filter(order_id=pk).first()
    #         return render(request, 'dtsadmin/modals/modal_order_invoice.html', {
    #             'invoice': invoice,
    #         })
    #     except Exception, e:
    #         log.error('_handle_look_invoice %s' % e)
    #         result = {
    #             'status': 0,
    #             'msg': '_handle_look_invoice错误 %s' % e
    #         }
    #         return JsonResponse(result)

    @staticmethod
    def _handle_verify_order(request):
        """审核订单"""
        try:
            pk = int(request.POST.get('pk', ''))
            method = request.POST.get('method')
            ord_item = Order.objects.filter(pk=pk).first()
            with transaction.atomic():
                if method == 'verify_pass':
                    if ord_item:
                        # .update(verify_state=2)
                        task = ord_item.proc_delivery.get_task_obj("mark_order_valid")
                        res, msg = task.transit()
                        if res:
                            note_msg = "订单审核通过"
                            # 添加站内消息
                            remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                            if remind_settings:
                                remind_item = json.loads(remind_settings.note)
                                remind_item_seting = remind_item['remind_settings']
                                item_list = json.loads(remind_item_seting)
                                flag = item_list[5]['mail']
                                if flag == 'Y':
                                    content_str = '您的订单%s审核已通过' % ord_item.order_no.encode('utf-8')
                                    id = ord_item.buyer.id
                                    SiteMessage.objects.create(
                                        user_id=id,
                                        order_id=ord_item.id,
                                        msg_type=SITE_MESSAGE_TYPE_ORDER,
                                        contant=content_str,
                                        is_read=False,
                                    )
                            # 写入日志
                            OperateRecord.objects.create(
                                operate=task.name,
                                operate_cn=task.name_cn,
                                process=ord_item.proc_delivery,
                                operator=request.user,
                                note=note_msg,
                                data_type=ORDER_MODAL,
                                data_id=ord_item.id,
                            )
                            result = {
                                'status': 1,
                                'msg': msg.encode('utf-8')
                            }
                            return JsonResponse(result)
                        else:
                            note_msg = "订单审核通过,失败。原因：%s" % msg.encode('utf-8')
                            result = {
                                'status': 0,
                                'msg': msg.encode('utf-8')
                            }
                            return JsonResponse(result)
                elif method == 'verify_nopass':
                    """审核不通过"""
                    # Order.objects.filter(pk=pk).update(verify_state=3)
                    if ord_item:
                        task = ord_item.proc_delivery.get_task_obj("mark_order_invalid")
                        res, msg = task.transit()
                        if res:
                            note_msg = "订单审核不通过"
                            # 添加站内消息
                            remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                            if remind_settings:
                                remind_item = json.loads(remind_settings.note)
                                remind_item_seting = remind_item['remind_settings']
                                item_list = json.loads(remind_item_seting)
                                flag = item_list[5]['mail']
                                if flag == 'Y':
                                    content_str = '您的订单%s审核未通过' % ord_item.order_no.encode('utf-8')
                                    id = ord_item.buyer.id
                                    SiteMessage.objects.create(
                                        user_id=id,
                                        order_id=ord_item.id,
                                        msg_type=SITE_MESSAGE_TYPE_ORDER,
                                        contant=content_str,
                                        is_read=False,
                                    )
                            if ord_item.verify_state == 3:
                                if ord_item.trade_state != 0:
                                    with transaction.atomic():
                                        ref_proc = Process.objects.create_process(BPMN_REFUND)
                                        user = request.user
                                        RefundRecord.objects.create(
                                            order_id=pk,  # 订单，Id
                                            refund=ord_item.real_price,
                                            applicant=user,  # 当前登录人
                                            refund_type=REFUND,  #
                                            proc_refund=ref_proc,
                                            refund_desc='',  # 买家填写的退款说明
                                        )
                                        res, msg = ref_proc.start()
                                        # TODO 退款至账户余额
                                        task = ref_proc.get_task_obj("mark_refund_finished")
                                        task.transit()
                                task = ord_item.proc_delivery.get_task_obj("close_order")
                                task.transit()
                                # 写入日志
                                OperateRecord.objects.create(
                                    operate=task.name,
                                    operate_cn=task.name_cn,
                                    process=ord_item.proc_delivery,
                                    operator=request.user,
                                    note=note_msg,
                                    data_type=ORDER_MODAL,
                                    data_id=ord_item.id,
                                )

                            result = {
                                'status': 1,
                                'msg': msg.encode('utf-8')
                            }
                            return JsonResponse(result)
                        else:
                            note_msg = "订单审核不通过，失败。原因：%s" % msg.encode('utf-8')
                            result = {
                                'status': 0,
                                'msg': msg.encode('utf-8')
                            }
                            return JsonResponse(result)
                else:
                    raise Exception("请求异常")


        except Exception, e:
            log.exception('_handle_verify_order raise,Error:%s' % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)

    def _handle_get_change_price(self, request):
        try:
            pk = int(request.POST.get('pk', ''))
            order = Order.objects.filter(pk=pk).first()
            return render(request, 'dtsadmin/modals/modal_change_price.html', {
                'order': order,
            })
        except Exception, e:
            log.error('_handle_look_order %s' % e)
            print str(e)
            result = {
                'status': 0,
                'msg': '_handle_get_change_price 错误'
            }
            return JsonResponse(result)

    # 改价 走流程
    def _handle_change_price(self, request):
        try:
            if 'method' in request.POST:
                if request.POST.get('method', '') == 'submit_change_price':
                    change_price_list = request.POST.get('change_price_list', '')
                    change_price_list_json = json.loads(change_price_list)
                    for list in change_price_list_json:
                        kwargs = {
                            'apply_discount': int(float(list['change_price']) * 100),
                            'order_item_id': int(list['pk']),
                            'change_price_state': 1,
                            'starff_id': request.user.id,
                            # 'leader_id': request.user.id,
                        }
                        ChangePriceRecord.objects.update_or_create(order_item_id=int(list['pk']), defaults=kwargs)
                    order_pk = int(request.POST.get('pk', ''))
                    # Order.objects.filter(pk=order_pk).update(change_price_state=1)
                    order = Order.objects.filter(pk=order_pk).first()
                    task = order.proc_delivery.get_task_obj('apply_change_price')
                    res, msg = task.transit()
                    if not res:
                        result = {
                            'status': 0,
                            # 'msg': '系统忙,请稍后再试'
                            'msg': msg
                        }
                        return JsonResponse(result)
                    # 写入日志
                    OperateRecord.objects.create(
                        operate=task.name,
                        operate_cn=task.name_cn,
                        process=order.proc_delivery,
                        operator=request.user,
                        note='订单支付前，申请改价',
                        data_type=ORDER_MODAL,
                        data_id=order.id,
                    )

                    result = {
                        'status': 1,
                        'msg': '改价提交成功'
                    }
                    return JsonResponse(result)
                elif request.POST.get('method', '') == 'submit_change_price_cancel':
                    change_price_list = request.POST.get('change_price_list', '')
                    change_price_list_json = json.loads(change_price_list)
                    changeprice = ChangePriceRecord.objects.filter(order_item_id__in=change_price_list_json, leader_id__isnull=False)
                    if changeprice:
                        result = {
                            'status': 1,
                            'msg': '已审批无法撤销'
                        }
                        return JsonResponse(result)
                    else:
                        ChangePriceRecord.objects.filter(order_item_id__in=change_price_list_json).update(change_price_state=NO_APPLY)
                        order_pk = int(request.POST.get('pk', ''))
                        order = Order.objects.filter(pk=order_pk).first()
                        if 'apply_change_price' in order.proc_delivery.reversible_task_list:
                            task = order.proc_delivery.get_task_obj('apply_change_price')
                            res, msg = task.reverse()
                        if not res:
                            result = {
                                'status': 0,
                                # 'msg': '系统忙,请稍后再试'
                                'msg': msg
                            }
                            return JsonResponse(result)
                        # 写入日志
                        OperateRecord.objects.create(
                            operate=task.name,
                            operate_cn=task.name_cn,
                            process=order.proc_delivery,
                            operator=request.user,
                            note='已撤销改价申请',
                            data_type=ORDER_MODAL,
                            data_id=order.id,
                        )
                        result = {
                            'status': 1,
                            'msg': '改价撤销成功'
                        }
                        return JsonResponse(result)
                else:
                    result = {
                        'status': 0,
                        'msg': 'method错误'
                    }
                    return JsonResponse(result)
            else:
                pk = int(request.POST.get('pk', ''))
                user_pk = request.user.id
                order = Order.objects.filter(pk=pk).first()
                user = User.objects.filter(pk=int(user_pk)).first()
                return render(request, 'dtsadmin/modals/modal_change_price.html', {
                    'order': order,
                    'user': user,

                })

        except Exception, e:
            log.error('_handle_verify_order %s' % e)
            result = {
                'status': 0,
                'msg': '_handle_change_price'
            }
            return result

    def _handle_order_invoice(self, request):
        """开票"""
        try:
            if 'method' in request.POST:
                if request.POST.get('method', '') == 'submit_order_invoice':
                    pk = int(request.POST.get('pk', ''))
                    invoice_no_12 = request.POST.get('invoice_no_12', '')
                    invoice_no_8 = request.POST.get('invoice_no_8', '')
                    invoice_no = invoice_no_12 + invoice_no_8
                    order = Order.objects.filter(pk=pk).update(invoice_no=invoice_no)
                    if order:
                        result = {
                            'status': 1,
                            'msg': '开票成功'
                        }
                    else:
                        result = {
                            'status': 0,
                            'msg': 'order修改失败'
                        }
                    return JsonResponse(result)
                else:
                    result = {
                        'status': 0,
                        'msg': 'method错误'
                    }
                    return JsonResponse(result)
            else:
                pk = int(request.POST.get('pk', ''))
                user_pk = request.user.id
                order = Order.objects.filter(pk=pk).first()
                user = User.objects.filter(pk=int(user_pk)).first()
                invoice = Invoice.objects.filter(order_id=pk).first()
                return render(request, 'dtsadmin/modals/modal_order_invoice.html', {
                    'order': order,
                    'user': user,
                    'invoice': invoice,

                })
        except Exception, e:
            log.error('_handle_order_invoice %s' % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
            return JsonResponse(result)

    @staticmethod
    def _handle_deliver_order(request):
        """订单发货"""
        try:
            if 'method' in request.POST:
                if request.POST.get('method', '') == 'submit_deliver_order':
                    with transaction.atomic():
                        waybill_no = request.POST.get('waybill_no', '')
                        shipping_method_id = request.POST.get('shipping_method_id', '')
                        pk = int(request.POST.get('pk', ''))
                        order = Order.objects.filter(pk=pk).first()
                        if order.trade_state == 2:
                            # 订单 拣配完药品，并装车发货后，点击【已发货】
                            task = order.proc_delivery.get_task_obj('mark_order_shipping')
                            res, msg = task.transit()
                            if not res:
                                result = {
                                    'status': 0,
                                    'msg': '系统忙,请稍后再试'
                                }
                                return JsonResponse(result)
                            order.waybill_no = waybill_no
                            order.shipping_method_id = shipping_method_id
                            order.save()
                            # 添加站内消息
                            remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                            if remind_settings:
                                remind_item = json.loads(remind_settings.note)
                                remind_item_seting = remind_item['remind_settings']
                                item_list = json.loads(remind_item_seting)
                                flag = item_list[2]['mail']
                                if flag == 'Y':
                                    content_str = '您的订单%s已发货' % order.order_no.encode('utf-8')
                                    id = order.buyer.id
                                    SiteMessage.objects.create(
                                        user_id=id,
                                        order_id=order.id,
                                        msg_type=SITE_MESSAGE_TYPE_ORDER,
                                        contant=content_str,
                                        is_read=False,
                                    )
                            # 添加操作日志
                            OperateRecord.objects.create(
                                operate=task.name,
                                operate_cn=task.name_cn,
                                process=order.proc_delivery,
                                operator=request.user,
                                note=u'标记发货',
                                data_type=ORDER_MODAL,
                                data_id=order.id,
                            )
                            result = {
                                'status': 1,
                                'msg': '发货成功'
                            }
                            return JsonResponse(result)
                        else:
                            result = {
                                'status': 0,
                                'msg': '网络异常，请刷新后重试！'
                            }
                            return JsonResponse(result)
                else:
                    result = {
                        'status': 0,
                        'msg': 'method错误'
                    }
                    return JsonResponse(result)
            else:
                pk = int(request.POST.get('pk', ''))
                user_pk = request.user.id
                order = Order.objects.filter(pk=pk).first()
                if order.trade_state == 2:
                    user = User.objects.filter(pk=int(user_pk)).first()
                    # 配送类型 根据物流类型显示对应的物流公司
                    shipping_type = order.shipping_method.shipping_type
                    choices = {
                        # 'shipping_method': ShippingMethod.objects.exclude(pk__in=[1,2,3])
                        'shipping_method': ShippingMethod.objects.filter(shipping_type=shipping_type, is_active=True)
                    }
                    return render(request, 'dtsadmin/modals/modal_deliver_order.html', {
                        'order': order,
                        'user': user,
                        'choices': choices
                    })
                else:
                    result = {
                        'status': 0,
                        'msg': '网络异常，请刷新后重试！'
                    }
                    return JsonResponse(result)
        except Exception, e:
            log.exception('_handle_deliver_order %s' % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
            return JsonResponse(result)

    @staticmethod
    def _handle_receipt_order(request):
        """确认收款"""
        try:
            obj_id = request.POST.get('obj_id')
            ord_item = Order.objects.filter(id=obj_id).first()
            if ord_item is not None:
                with transaction.atomic():
                    # 获取订单流程中标记付款流程任务
                    task = ord_item.proc_delivery.get_task_obj("mark_order_paid")
                    # 如果订单关闭
                    if ord_item.trade_state == ORDER_CLOSED:
                        note_msg = "收款失败，原因：该订单已关闭，无法确认收款"
                        result = {
                            'status': 'err',
                            'msg': note_msg
                        }
                    else:
                        res, msg = task.transit()
                        # 如果任务正常执行，更新订单
                        if res:
                            # ord_item.trade_state = ORDER_HAS_PAID
                            # ord_item.pay_status = HAS_PAID
                            # 更新实付价格总计
                            ord_item.real_price = float(request.POST.get('real_price'))
                            ord_item.save()
                            # 更新订单商品实付单价
                            OrderItem.objects.filter(order_id=ord_item.id).update(real_price=F('price') * F('quantity'))
                            result = {
                                'status': 1,
                                'msg': '收款成功'
                            }
                            recipt_price = float(ord_item.real_price) * 0.01
                            note_msg = "成功收款%s元" % recipt_price
                        else:
                            note_msg = "收款失败，原因：%s" % msg.encode('utf-8')
                            result = {
                                'status': 0,
                                'msg': msg
                            }
                    # 写入日志
                    OperateRecord.objects.create(
                        operate=task.name,
                        operate_cn=task.name_cn,
                        process=ord_item.proc_delivery,
                        operator=request.user,
                        note=note_msg,
                        data_type=ORDER_MODAL,
                        data_id=ord_item.id,
                    )
        except Exception, e:
            log.exception("_handle_receipt_order raise ,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result


def lack_good(request):
    # 查询条件
    kwargs = {}
    # 商品名称
    if request.GET.get('good_name'):
        kwargs['good__trade_name__contains'] = request.GET['good_name']
    # 缺货状态
    if request.GET.get('stock_amount', ''):
        if int(request.GET.get('stock_amount', '')) == 0:
            kwargs['good__stock_amount__lte'] = 0
        else:
            kwargs['good__stock_amount__gt'] = 0
    # 登记时间自
    if request.GET.get('register_created_from'):
        kwargs['created__gte'] = request.GET['register_created_from']
    # 登记时间到
    if request.GET.get('register_created_to'):
        created_to = datetime.datetime.strptime(request.GET['register_created_to'], "%Y-%m-%d") + datetime.timedelta(
            days=1)
        kwargs['created__lt'] = created_to
    # 分页
    data_set = LackRegister.objects.select_related('good').filter(**kwargs)
    paginator = Paginator(data_set, PAGE_LIMIT)
    page = request.GET.get('page', 1)
    try:
        data_list = paginator.page(int(page))
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    return render(request, 'dtsadmin/lack_good.html', {
        'data_list': data_list,
        'pagi_bar': get_paginator_bar(data_list),
    })


def order_list1(request):
    return render(request, 'dtsadmin/order_list1.html', {})


def returns_and_refunds(request):
    return render(request, 'dtsadmin/returns_and_refunds.html', {})


class ApprovalListView(View):
    """改价审批列表"""

    def get(self, request):
        change_price_kwargs = {}
        order_kwargs = {}
        change_price_state = [1, 2, 3]
        # slug 我发起的 待我审批 我已审批
        if request.GET.get('slug', ''):
            slug = request.GET.get('slug', '')
            if 'is_my_start' == slug:
                change_price_kwargs['starff'] = request.user
            elif 'is_my_approval' == slug:
                # kwargs['change_price_state__in'] = [0, 1]
                change_price_state = [1]
            elif 'is_my_approved' == slug:
                change_price_kwargs['leader'] = request.user
                change_price_state = [2, 3]
                # kwargs['change_price_state__in'] = [2, 3]
            else:
                change_price_kwargs = {}
        # 发起时间
        if 'start_time_from' in request.GET and request.GET.get('start_time_from', ''):
            change_price_kwargs['apply_time__gte'] = request.GET.get('start_time_from', '')
        if 'start_time_to' in request.GET and request.GET.get('start_time_to', ''):
            start_time_to = datetime.datetime.strptime(request.GET.get('start_time_to', ''),
                                                       "%Y-%m-%d") + datetime.timedelta(days=1)
            change_price_kwargs['apply_time__lt'] = start_time_to
        # 完成时间
        if 'finish_time_from' in request.GET and request.GET.get('finish_time_from', ''):
            change_price_kwargs['apply_time__gte'] = request.GET['finish_time_from']
        if 'finish_time_to' in request.GET and request.GET.get('finish_time_to', ''):
            finish_time_to = datetime.datetime.strptime(request.GET.get('finish_time_to', ''),
                                                        "%Y-%m-%d") + datetime.timedelta(days=1)
            change_price_kwargs['apply_time__lt'] = finish_time_to
        # 通过改价审批列表拿到订单id
        change_price_set = ChangePriceRecord.objects.filter(**change_price_kwargs).order_by('-apply_time')
        order_pk_list = []
        for record in change_price_set:
            order_pk = record.order_item.order.pk
            if order_pk not in order_pk_list:
                order_pk_list.append(order_pk)
        # 订单编号
        if request.GET.get('order_no', ''):
            order_kwargs['order_no__contains'] = request.GET.get('order_no', '')
        # 状态
        if request.GET.get('change_price_state', ''):
            order_kwargs['change_price_state'] = int(request.GET.get('change_price_state', ''))
        order_list = list(Order.objects.filter(pk__in=order_pk_list, change_price_state__in=change_price_state, **order_kwargs))
        order_list.sort(lambda x, y: cmp(order_pk_list.index(x.pk), order_pk_list.index(y.pk)))
        # 分页
        paginator = Paginator(order_list, PAGE_LIMIT)
        page = int(request.GET.get('page', 1))
        try:
            change_price_list = paginator.page(page)
        except PageNotAnInteger:
            change_price_list = paginator.page(1)
        except EmptyPage:
            change_price_list = paginator.page(paginator.num_pages)
        except Exception, e:
            log.error('ApprovalListView get %s' % e)
            result = {
                'status': 0,
                'msg': 'ApprovalListView 内部错误'

            }
            return JsonResponse(result)
        # 状态
        choices = {
            'change_price_state': REVIEW_STATUS_CHOICES
        }
        return render(request, 'dtsadmin/approval_list.html', {
            'order_list': change_price_list,
            'pagi_bar': get_paginator_bar(change_price_list),
            'choices': choices
        })

    def post(self, request):
        try:
            if 'method' in request.POST:
                method = request.POST.get('method', '')

                # 查看改价申请
                if 'get_approval' == method:
                    return self._handle_get_approval(request)
                else:
                    result = {
                        'status': 0,
                        'msg': '请求method错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': '请求错误'
                }
            return JsonResponse(result)

        except Exception, e:
            log.error('ApprovalListView %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e
            }
            return JsonResponse(result)

    def _handle_get_approval(self, request):
        action = request.POST.get('action', '')
        # 获取改价申请模态框 点击查看
        if 'get_look_change_price' == action:
            user_pk = request.user.id
            pk = int(request.POST.get('pk', ''))
            change_price = ChangePriceRecord.objects.filter(pk=pk).first()
            order = Order.objects.filter(pk=pk).first()
            user = User.objects.filter(pk=int(user_pk)).first()
            return render(request, 'dtsadmin/modals/modal_approval_verify.html', {
                'change_price': change_price,
                'order': order,
                'user': user,
                'slug': 'check',
            })
        # 获取改价申请模态框 点击审核
        elif 'get_verify_change_price' == action:
            user_pk = request.user.id
            pk = int(request.POST.get('pk', ''))
            change_price = ChangePriceRecord.objects.filter(pk=pk).first()
            order = Order.objects.filter(pk=pk).first()
            user = User.objects.filter(pk=int(user_pk)).first()
            order_record = OperateRecord.objects.filter(data_id=order.id, data_type=ORDER_MODAL).order_by('-created')
            return render(request, 'dtsadmin/modals/modal_approval_verify.html', {
                'change_price': change_price,
                'order': order,
                'order_record': order_record,
                'slug': 'approval',
            })
        # 审核通过
        elif 'submit_change_price_pass' == action:
            order_pk = int(request.POST.get('pk', ''))
            is_order = Order.objects.filter(pk=order_pk).first()
            real_total_price = request.POST.get('real_total_price', '')
            is_order.real_price = real_total_price
            is_order.save()
            change_price_list = request.POST.get('change_price_list', '')
            change_price_list_json = json.loads(change_price_list)
            for list in change_price_list_json:
                obj = ChangePriceRecord.objects.filter(order_item_id=int(list['pk'])).first()
                obj.real_discount = int(float(list['change_price']) * 100)
                obj.change_price_state = 2
                obj.leader_id = request.user.id
                obj.save()
            if not is_order:
                result = {
                    'status': 0,
                    'msg': '订单错误'
                }
                return JsonResponse(result)
            # 改价通过
            task = is_order.proc_delivery.get_task_obj('change_price_valid')
            res, msg = task.transit()
            if not res:
                result = {
                    'status': 0,
                    'msg': '系统忙,请稍后再试'
                }
                return JsonResponse(result)
            is_change_price_update = ChangePriceRecord.objects.filter(order_item__order__pk=order_pk).update(
                change_price_state=2,
                leader=request.user,
                reply_time=datetime.datetime.now()
            )
            # 添加操作日志
            OperateRecord.objects.create(
                operate=task.name,
                operate_cn=task.name_cn,
                process=is_order.proc_delivery,
                operator=request.user,
                note='改价通过',
                data_type=ORDER_MODAL,
                data_id=is_order.id,
            )
            if is_change_price_update:
                result = {
                    'status': 1,
                    'msg': '修改成功'
                }
            else:
                result = {
                    'status': 0,
                    'msg': '修改失败'
                }
            return JsonResponse(result)

        # 审核不通过
        elif 'submit_change_price_nopass' == action:
            order_pk = int(request.POST.get('pk', ''))
            is_order = Order.objects.filter(pk=order_pk).first()
            if not is_order:
                result = {
                    'status': 0,
                    'msg': '订单错误'
                }
                return JsonResponse(result)
            # 改价不通过
            task = is_order.proc_delivery.get_task_obj('change_price_invalid')
            res, msg = task.transit()
            if not res:
                result = {
                    'status': 0,
                    'msg': '系统忙,请稍后再试'
                }
                return JsonResponse(result)
            is_change_price_update = ChangePriceRecord.objects.filter(order_item__order__pk=order_pk).update(
                change_price_state=3,
                leader=request.user,
                reply_time=datetime.datetime.now()
            )
            # 添加操作日志
            OperateRecord.objects.create(
                operate=task.name,
                operate_cn=task.name_cn,
                process=is_order.proc_delivery,
                operator=request.user,
                note='改价不通过',
                data_type=ORDER_MODAL,
                data_id=is_order.id,
            )
            if is_change_price_update:
                result = {
                    'status': 1,
                    'msg': '修改成功'
                }
            else:
                result = {
                    'status': 0,
                    'msg': '修改失败'
                }
            return JsonResponse(result)
        # 点击订单编号查看
        elif 'look_order' == action:
            user_pk = request.user.id
            pk = int(request.POST.get('pk', ''))
            order = Order.objects.filter(pk=pk).first()
            user = User.objects.filter(pk=int(user_pk)).first()
            return render(request, 'dtsadmin/modals/modal_approve_look_order.html', {
                'order': order,
                'user': user,
            })
        else:
            result = {
                'status': 0,
                'msg': 'action错误'
            }
            return JsonResponse(result)


def approval_list(request):
    return render(request, 'dtsadmin/approval_list.html', {})


def order_statistic(request):
    return render(request, 'dtsadmin/order_statistic.html', {})


def trading_record(request):
    return render(request, 'dtsadmin/trading_record.html', {})


def refund(request):
    return render(request, 'dtsadmin/refund.html', {})


def return_good(request):
    return render(request, 'dtsadmin/return_good.html', {})


def data_backup(request):
    return render(request, 'dtsadmin/data_backup.html', {})


class ConsultFeedbackView(View):
    """咨询反馈"""

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)
        kwargs = {}
        try:
            feedback_type = ''
            is_active = ''
            if 'feedback_type' in request.GET:
                feedback_type = request.GET.get('feedback_type')
                if feedback_type != '':
                    kwargs['feedback_type'] = feedback_type
            if 'feedback_status' in request.GET:
                is_active = request.GET.get('feedback_status')
                if is_active != '':
                    kwargs['is_replied'] = is_active
            pending_list = ConsultFeedback.objects.filter(user=request.user, is_replied=CF_STATUS_PENDING).order_by(
                '-created')
            active_list = ConsultFeedback.objects.filter(user=request.user, is_replied=CF_STATUS_ACTIVE).order_by(
                '-created')

            data_set = ConsultFeedback.objects.filter(**kwargs).order_by('-updated')
            # PAGE_LIMIT = 1
            paginator = Paginator(data_set, PAGE_LIMIT)  # 分页
            cur_page = int(request.GET.get('page', 1))  # 获取第一页
            try:
                consult_feedback_list = paginator.page(cur_page)
            except PageNotAnInteger, e:
                log.error("ConsultFeedbackView.get error:%s" % e)
                consult_feedback_list = paginator.page(1)
            except EmptyPage, e:
                log.error("ConsultFeedbackView.get error:%s" % e)
                consult_feedback_list = paginator.page(paginator.num_pages)
            result = {
                'feedback_type': feedback_type,
                'is_active': is_active,
                'pending_list': pending_list,
                'active_list': active_list,
                'consult_feedback_list': consult_feedback_list,
                # 'page_limit': PAGE_LIMIT,
                'pagi_bar': get_paginator_bar(consult_feedback_list),
            }

        except Exception, e:
            log.error("ConsultFeedbackView.get error: %s" % e)
            result = {}
        return render(request, 'dtsadmin/consult_feedback.html', result)

    def post(self, request):
        try:
            if request.method == 'POST':
                if request.is_ajax():
                    method = request.POST['method']  # 具体操作:判断具体做什么
                    if method == 'del_batch':
                        cf_ids = request.POST.get('cf_ids')  # 拿到所有待删除的咨询id
                        del_ids = json.loads(cf_ids)
                        result = self._delete_feedback_batch(del_ids)
                    elif method == 'show':
                        cf_ids = request.POST.get('cf_ids')
                        feed_ids = json.loads(cf_ids)
                        result = self._update_show_feedback_batch(feed_ids, True)
                    elif method == 'cancel':
                        cf_ids = request.POST.get('cf_ids')
                        feed_ids = json.loads(cf_ids)
                        result = self._update_show_feedback_batch(feed_ids, False)

                else:
                    result = self._handle_cf_search(request)
                    return render(request, 'dtsadmin/consult_feedback.html', result)
            else:
                raise Exception('请求异常')
        except Exception, e:
            log.error("ConsultFeedbackView post raise, Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)

    def _handle_info_active(self, request, cf_ids, is_active):
        """显示 咨询反馈"""
        try:
            user = request.user  # 当前登录用户
            with transaction.atomic():
                for cf_id in cf_ids:
                    cf = ConsultFeedback.objects.get(id=cf_id)
                    if cf is not None:
                        cf.update_user = user
                        cf.reviewer = user
                        cf.is_active = is_active
                        cf.save()
                if is_active == 1:
                    msg = '显示成功'
                else:
                    msg = '未显示'
                result = {
                    'status': 1,
                    'msg': msg
                }
        except Exception, e:
            log.error("ConsultFeedbackView._handle_cf_active error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    def _handle_cf_search(self, request):
        """多条件查询"""
        kwargs = {}
        feedback_type = ''
        is_active = ''
        consult_feedback_list = []
        if 's_feedback_type' in request.POST:
            feedback_type = request.POST['s_feedback_type']
            if feedback_type != '':
                kwargs['feedback_type__contains'] = feedback_type
        if 's_feedback_status' in request.POST:
            is_active = request.POST['s_feedback_status']
            if is_active != '':
                kwargs['is_replied'] = is_active
        data_set = ConsultFeedback.objects.filter(**kwargs).order_by('-updated')
        paginator = Paginator(data_set, PAGE_LIMIT)  # 分页
        cur_page = int(request.POST.get('page', 1))  # 获取当前页 1
        try:
            consult_feedback_list = paginator.page(cur_page)
        except PageNotAnInteger, e:
            log.error("ConsultFeedbackView._handle_feedback_search error:%s" % e)
            consult_feedback_list = paginator.page(1)
        except EmptyPage, e:
            log.error("ConsultFeedbackView._handle_feedback_search error:%s" % e)
            consult_feedback_list = paginator.page(paginator.num_pages)
        result = {
            'feedback_type': feedback_type,
            'is_active': is_active,
            'consult_feedback_list': consult_feedback_list,
            # 'paginator': paginator,
            # 'page': cur_page,
            # 'page_limit': PAGE_LIMIT,
            'pagi_bar': get_paginator_bar(consult_feedback_list),
        }
        return result

    def _delete_feedback_batch(self, del_ids):
        """批量删除咨询反馈"""
        with transaction.atomic():
            ConsultFeedback.objects.filter(id__in=del_ids).delete()
        result = {
            'status': 1,
            'msg': "删除成功"
        }
        return result

    def _update_show_feedback_batch(self, upd_ids, is_display):
        """批量显示获取取消显示咨询反馈"""
        try:

            with transaction.atomic():
                ConsultFeedback.objects.filter(id__in=upd_ids).update(is_display=bool(is_display))
            result = {
                'status': 1,
                'msg': "操作成功"
            }
            return result
        except Exception, e:
            result = {
                'status': 0,
                'msg': e
            }
            return result


def consult_feedback(request):
    return render(request, 'dtsadmin/consult_feedback.html', {})


def template_list(request):
    return render(request, 'dtsadmin/template_list.html', {})


def supplier_list(request):
    return render(request, 'dtsadmin/supplier_list.html', {})


def classify_access(request):
    return render(request, 'dtsadmin/classify_access.html', {})


def trading_balance(request):
    return render(request, 'dtsadmin/trading_balance.html', {})


def role_manage(request):
    """加载所有的角色"""
    obj = {}
    try:
        role_list = Role.objects.all().order_by('-id')
        obj['usertype_choices'] = SettingsType.get_item_list('USERTYPE')
        perms = Permission.objects.filter(id=1).first()
    except Exception, e:
        log.error("role_manage raise, Error:%s" % e)
    return render(request, 'dtsadmin/role_manage.html', {
        'data_list': role_list,
        'page_limit': PAGE_LIMIT,
        'obj': obj,
        'perms': perms
    })


class BasicSettingsView(View):
    """基本信息"""

    def get(self, request):
        """处理GET请求"""
        settings_item_dict = {}
        try:
            settings_type = SettingsType.objects.filter(note=SETTINGS_BASIC).first()
            if settings_type is not None:
                settings_item_dict = self._load_basic_settings(request, settings_type)  # 加载基本信息
        except Exception, e:
            log.exception("BasicSettingsView get raise exception,error:%s" % e)
        return render(request, 'dtsadmin/basic_info.html', {'settings_item_dict': settings_item_dict})

    def post(self, request):
        """处理POST请求"""
        try:
            if request.method == 'POST' and request.is_ajax():
                settings_type = self._handle_basic_settings_type(request)
                if request.POST.get('op_type') == 'front_site':  # 前台网站
                    result = self._handle_site_settings(request, settings_type)
                elif request.POST.get('op_type') == 'admin_logo':  # 后台Logo
                    result = self._handle_admin_logo(request, settings_type)
                elif request.POST.get('op_type') == 'consult_settings':  # 客服设置
                    result = self._handle_consult_settings(request, settings_type)
                elif request.POST.get('op_type') == 'auth_settings':  # 权限设置
                    result = self._handle_auth_settings(request, settings_type)
                elif request.POST.get('op_type') == 'remind_settings':  # 信息提醒
                    result = self._handle_remind_settings(request, settings_type)
            else:
                result = {
                    'status': 0,
                    'msg': '请求错误'
                }
        except Exception, e:
            log.exception("BasicSettingsView post raise exception,error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)

    @staticmethod
    def _load_basic_settings(request, settings_type):
        """加载基本信息"""
        settings_item_dict = {}
        settings_item_list = SettingsItem.objects.filter(s_type=settings_type)
        if settings_item_list:
            for item in settings_item_list:
                if item.name == SETTINGS_CONSULT_SETTING:  # 客服设置
                    settings_item_dict[item.name] = json.loads(item.note)
                    settings_item_dict[item.name]['service_account_list'] = json.loads(
                        json.loads(item.note)['service_account_list'])
                    settings_item_dict[item.name]['service_account_list_str'] = json.loads(item.note)[
                        'service_account_list']
                    work_date_list = [{'key': '1', 'value': '周一'},
                                      {'key': '2', 'value': '周二'},
                                      {'key': '3', 'value': '周三'},
                                      {'key': '4', 'value': '周四'},
                                      {'key': '5', 'value': '周五'},
                                      {'key': '6', 'value': '周六'},
                                      {'key': '7', 'value': '周日'}
                                      ]
                    settings_item_dict[item.name]['work_date_list'] = work_date_list
                elif item.name == SETTINGS_REMIND_SETTING:  # 信息提醒
                    settings_item_dict[item.name] = json.loads(item.note)
                    settings_item_dict[item.name]['remind_settings'] = json.loads(
                        json.loads(item.note)['remind_settings'])
                else:
                    settings_item_dict[item.name] = json.loads(item.note)
        return settings_item_dict

    @staticmethod
    def _handle_basic_settings_type(request):
        """ 处理基本信息SettingsType """
        settings_type = SettingsType.objects.filter(code=SETTINGS_BASIC).first()
        if settings_type is None:
            settings_type = SettingsType.objects.create(
                code=SETTINGS_BASIC,
                name='基本信息',
                note=SETTINGS_BASIC
            )
        return settings_type

    @staticmethod
    def _handle_site_settings(request, settings_type):
        """处理前台网站信息"""
        try:
            # 获取FORM表单数据
            form_data = {'site_name': request.POST['site_name'],
                         'admin_phone': request.POST['admin_phone'],
                         'admin_telephone': request.POST['admin_telephone'],
                         'admin_complain': request.POST['admin_complain'],
                         'admin_email': request.POST['admin_email'],
                         'admin_address': request.POST['admin_address'],
                         'admin_code': request.POST['admin_code'],
                         'admin_company': request.POST['admin_company'],
                         'admin_copyright': request.POST['admin_copyright'],
                         'admin_icp': request.POST['admin_icp'],
                         'admin_site_no': request.POST['admin_site_no'],
                         'admin_note': request.POST['admin_note'],
                         }
            item_data = json.dumps(form_data)
            settings_item = SettingsItem.objects.filter(name='FRONT_SITE').first()
            if settings_item is None:
                SettingsItem.objects.create(
                    name='FRONT_SITE',
                    value='前台网站',
                    note=item_data,
                    s_type=settings_type
                )
            else:
                settings_item.note = item_data
                settings_item.save()
            result = {
                'status': 1,
                'msg': '保存成功'
            }
        except Exception, e:
            log.exception("BasicSettingsView._handle_site_settings error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    @staticmethod
    def _handle_admin_logo(request, settings_type):
        """上传更新后台Logo图片"""
        try:

            for photo in request.FILES.getlist('logo_img'):
                if photo.size > 1048576:  # 图片大小限制1M
                    result = {
                        'status': 10,
                        'msg': '图片过大，不能超过1M'
                    }
                else:
                    form = LogoSittingsForm(request.POST, {'photo': photo})
                    if form.is_valid():
                        img = form.save()
                        # 存入SettingsItem
                        form_data = {
                            'logo_path': img.photo.name,
                            'logo_href': request.POST.get('logo_href')
                        }
                        item_data = json.dumps(form_data)
                        settings_item = SettingsItem.objects.filter(name='ADMIN_LOGO').first()
                        if settings_item is None:
                            SettingsItem.objects.create(
                                name='ADMIN_LOGO',
                                value='后台Logo',
                                note=item_data,
                                s_type=settings_type
                            )
                        else:
                            settings_item.note = item_data
                            settings_item.save()
                        admin_logo_obj = {'logo_path': form_data['logo_path'], 'logo_href': form_data['logo_href']}
                        request.session['admin_logo_obj'] = admin_logo_obj
                        result = {
                            'status': 1,
                            'msg': '上传成功',
                            'logo_path': media_url(form_data['logo_path']),
                            'logo_href': form_data['logo_href']
                        }
        except Exception, e:
            log.exception("BasicSettingsView._handle_admin_logo error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    @staticmethod
    def _handle_consult_settings(request, settings_type):
        """客户设置信息处理"""
        try:
            form_data = {
                'enable_cust_service': request.POST['enable_cust_service'],
                'work_date_start': request.POST['work_date_start'],
                'work_date_end': request.POST['work_date_end'],
                'time_online_start': request.POST['time_online_start'],
                'time_online_end': request.POST['time_online_end'],
                'input_service_number': request.POST['input_service_number'],
                'service_account_list': request.POST['service_account_list']
            }
            item_data = json.dumps(form_data)
            consult_settings = SettingsItem.objects.filter(name='CONSULT_SETTING').first()
            if consult_settings is None:
                SettingsItem.objects.create(
                    name='CONSULT_SETTING',
                    value='客服设置',
                    note=item_data,
                    s_type=settings_type
                )
            else:
                consult_settings.note = item_data
                consult_settings.save()
            result = {
                'status': 1,
                'msg': '保存成功'
            }
        except Exception, e:
            log.exception("BasicSettingsView._handle_consult_settings error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    @staticmethod
    def _handle_auth_settings(request, settings_type):
        """登录验证信息处理"""
        try:
            form_data = {
                'picture_limit_verify': request.POST['picture_limit_verify'],
                'picture_limit_count': request.POST['picture_limit_count'],
                'message_limit_verify': request.POST['message_limit_verify'],
                'message_limit_count': request.POST['message_limit_count']
            }
            item_data = json.dumps(form_data)
            auth_settings = SettingsItem.objects.filter(name='AUTH_SETTING').first()
            if auth_settings is None:
                SettingsItem.objects.create(
                    name='AUTH_SETTING',
                    value='登录验证',
                    note=item_data,
                    s_type=settings_type
                )
            else:
                auth_settings.note = item_data
                auth_settings.save()
            result = {
                'status': 1,
                'msg': '保存成功'
            }
        except Exception, e:
            log.exception("BasicSettingsView._handle_auth_settings error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    @staticmethod
    def _handle_remind_settings(request, settings_type):
        """提醒设置处理"""
        try:
            form_data = {
                'remind_settings': request.POST['remind_settings_val']
            }
            item_data = json.dumps(form_data)
            remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
            if remind_settings is None:
                SettingsItem.objects.create(
                    name='REMIND_SETTING',
                    value='信息提醒',
                    note=item_data,
                    s_type=settings_type
                )
            else:
                remind_settings.note = item_data
                remind_settings.save()
            result = {
                'status': 0,
                'msg': '保存成功'
            }
        except Exception, e:
            log.exception("BasicSettingsView._handle_remind_settings error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result


def ckeditor(request):
    from .forms import BasicckForm, FullckForm
    form_full = FullckForm()
    form_basic = BasicckForm()
    return render(request, 'dtsadmin/ckeditor.html', {'form_full': form_full, 'form_basic': form_basic})


class InfomationsView(View):
    """信息发布视图"""

    @method_decorator(check_permission(codename='dtsadmin.publish_manage'))
    def get(self, request):
        """处理GET请求 加载所有发布信息数据"""
        try:
            kwargs = {}
            info_type = ''
            info_status = ''
            name = ''
            if 's_info_type' in request.GET:
                info_type = request.GET['s_info_type']
                kwargs['info_type__contains'] = info_type
            if 's_info_status' in request.GET:
                info_status = request.GET['s_info_status']
                kwargs['info_status__contains'] = info_status
            if 's_info_name' in request.GET:
                name = request.GET['s_info_name']
                kwargs['name__contains'] = name
            data_set = Informations.objects.filter(**kwargs).order_by('-update_date')
            paginator = Paginator(data_set, PAGE_LIMIT)
            page = int(request.GET.get('page', 1))
            try:
                info_list = paginator.page(page)
            except PageNotAnInteger, e:
                log.error("InfomationsView._handle_info_search error:%s" % e)
                info_list = paginator.page(1)
            except EmptyPage, e:
                log.error("InfomationsView._handle_info_search error:%s" % e)
                info_list = paginator.page(paginator.num_pages)
            result = {
                'status': 1,
                'msg': 'suc',
                'info_list': info_list,
                'page': page,
                'pagi_bar': get_paginator_bar(info_list),
                'kwargs': {
                    'info_type': info_type,
                    'info_status': info_status,
                    'name': name
                }
            }
        except Exception, e:
            log.exception("InfomationsView.get error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return render(request, 'dtsadmin/publish_manage.html', result)

    def post(self, request):
        """处理POST请求"""
        try:
            if request.method == 'POST':
                op_type = request.POST.get('op_type')
                if request.is_ajax():
                    if op_type == 'add':  # 添加发布信息
                        result = InfomationsView._handle_info_add(request)
                    elif op_type == 'edit':  # 编辑修改发布信息
                        result = InfomationsView._handle_info_edit(request)
                    elif op_type == 'del_batch':  # 批量删除发布信息
                        info_ids = request.POST.get('info_ids')
                        delete_ids = json.loads(info_ids)
                        result = InfomationsView._handle_info_delete(request, delete_ids)
                    elif op_type == 'act_batch':  # 投放发布信息
                        info_ids = request.POST.get('info_ids')
                        act_ids = json.loads(info_ids)
                        result = InfomationsView._handle_info_active(request, act_ids, 1)
                    elif op_type == 'shd_batch':  # 批量屏蔽发布信息
                        info_ids = request.POST.get('info_ids')
                        shd_ids = json.loads(info_ids)
                        result = InfomationsView._handle_info_active(request, shd_ids, 2)
                else:
                    result = InfomationsView._handle_info_search(request)
                    return render(request, 'dtsadmin/publish_manage.html', result)
            else:
                result = {
                    'status': 0,
                    'msg': '请求错误'
                }
        except Exception, e:
            log.exception("InfomationsView.post error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)

    @staticmethod
    def _handle_info_add(request):
        """添加发布信息"""
        try:
            cur_user = request.user  # 当前登录对象
            Informations.objects.create(
                info_type=request.POST.get('info_type'),
                name=request.POST.get('name'),
                content=request.POST.get('content'),
                order_no=request.POST.get('order_no'),
                info_status=bool(request.POST.get('info_status')),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                update_user=cur_user,
                is_top=request.POST.get('is_top'),
                audience=request.POST.get('audience')
            )
            result = {
                'status': 1,
                'msg': '保存成功'
            }
        except Exception, e:
            log.exception("InfomationsView._handle_info_add error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    @staticmethod
    def _handle_info_edit(request):
        """修改发布信息"""
        try:
            cur_user = request.user  # 当前登录对象
            info_id = request.POST.get("info_id")
            info = Informations.objects.filter(id=info_id).first()
            if 'info_type' in request.POST:
                info.info_type = request.POST.get('info_type')
            if 'name' in request.POST:
                info.name = request.POST.get('name')
            if 'content' in request.POST:
                info.content = request.POST.get('content')
            if 'order_no' in request.POST:
                info.order_no = request.POST.get('order_no')
            if 'info_status' in request.POST:
                info.info_status = bool(request.POST.get('info_status'))
            if 'start_date' in request.POST:
                info.start_date = request.POST.get('start_date')
            if 'end_date' in request.POST:
                info.end_date = request.POST.get('end_date')
            if 'is_top' in request.POST:
                info.is_top = request.POST.get('is_top')
            if 'visible_obj' in request.POST:
                info.audience = request.POST.get('audience')
            info.update_user = cur_user
            info.save()
            result = {
                'status': 1,
                'msg': '保存成功'
            }
        except Exception, e:
            log.exception("InfomationsView._handle_info_edit error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    @staticmethod
    def _handle_info_delete(request, info_ids):
        """批量删除发布信息"""
        try:
            with transaction.atomic():
                Informations.objects.filter(id__in=info_ids).delete()
                result = {
                    'status': 1,
                    'msg': '删除成功'
                }
        except Exception, e:
            log.exception("InfomationsView._handle_info_delete error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    @staticmethod
    def _handle_info_active(request, info_ids, info_status):
        """批量投放,屏蔽发布信息"""
        try:
            user = request.user  # 当前登录用户
            with transaction.atomic():
                info_list = Informations.objects.filter(id__in=info_ids)
                for info in info_list:
                    if info is not None:
                        info.update_user = user
                        info.reviewer = user
                        info.info_status = info_status
                        info.save()
                if info_status == 1:
                    msg = '投放成功'
                else:
                    msg = '屏蔽成功'
                result = {
                    'status': 1,
                    'msg': msg
                }
        except Exception, e:
            log.exception("InfomationsView._handle_info_active error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return result

    @staticmethod
    def _handle_info_search(request):
        """多条件查询"""
        kwargs = {}
        info_type = ''
        info_status = ''
        name = ''
        if 's_info_type' in request.POST:
            info_type = request.POST['s_info_type']
            kwargs['info_type__contains'] = info_type
        if 's_info_status' in request.POST:
            info_status = request.POST['s_info_status']
            kwargs['info_status__contains'] = info_status
        if 's_info_name' in request.POST:
            name = request.POST['s_info_name']
            kwargs['name__contains'] = name
        data_set = Informations.objects.filter(**kwargs).order_by('-update_date')
        paginator = Paginator(data_set, PAGE_LIMIT)  # 分页
        cur_page = int(request.POST.get('load_page', 1))  # 获取当前页 1
        try:
            info_list = paginator.page(cur_page)
        except PageNotAnInteger, e:
            log.exception("InfomationsView._handle_info_search error:%s" % e)
            info_list = paginator.page(1)
        except EmptyPage, e:
            log.exception("InfomationsView._handle_info_search error:%s" % e)
            info_list = paginator.page(paginator.num_pages)
        result = {
            'status': 1,
            'msg': 'suc',
            'info_list': info_list,
            'pagi_bar': get_paginator_bar(info_list),
            'kwargs': {
                'info_type': info_type,
                'info_status': info_status,
                'name': name
            }
        }
        return result


def export_good_list(request):
    """导出商品列表"""
    try:
        choose = request.GET.get('choose')
        cur_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        title = '商品详情%s' % cur_time
        search_list = []
        columns = [
            {'key': 'external_id', 'name': '商品编码'},
            {'key': 'name', 'name': '商品通用名称'},
            {'key': 'trade_name', 'name': '商品名称'},
            {'key': 'category', 'name': '商品分类'},
            {'key': 'prep_spec', 'name': '制剂规格'},
            {'key': 'license', 'name': '批准文号'},
            {'key': 'manufacturer', 'name': '厂家'},
            {'key': 'locality', 'name': '产地'},
            {'key': 'unit', 'name': '包装单位'},
            {'key': 'pack_spec', 'name': '包装规格'},
            {'key': 'stock_amount', 'name': '库存数量'},
            {'key': 'supplier', 'name': '供应商'},
            {'key': 'is_zybh', 'name': '是否中药保护'},
            {'key': 'is_oem', 'name': '是否委托加工'},
            {'key': 'is_otc', 'name': '是否OTC'},
            {'key': 'otc_type', 'name': 'OTC类型'},
            {'key': 'recipe_type', 'name': '处方类型'},
            {'key': 'retail_price', 'name': '零售价（元）'},
            {'key': 'member_price', 'name': '会员价（元）'}
        ]
        data_list = []
        if choose == 'ck':
            good_ids = request.GET.get('good_ids')
            export_ids = json.loads(good_ids)
            search_list = Good.objects.filter(id__in=export_ids)
        else:
            kwargs = {}
            # 查询 更多查询条件
            # 商品编码
            if 'search_good_external_id' in request.GET:
                kwargs['external_id__contains'] = request.GET['search_good_external_id']
            # 商品名称
            if 'search_good_trade_name' in request.GET:
                kwargs['trade_name__contains'] = request.GET['search_good_trade_name']
            # 剂型
            if 'search_good_dosage_form' in request.GET:
                dosage_form = request.GET.get('search_good_dosage_form')
                if dosage_form != '':
                    kwargs['drugattr__dosage_form__contains'] = dosage_form
            # 分类
            if 'search_good_category' in request.GET:
                sea_category = request.GET.get('search_good_category')
                if sea_category != '':
                    kwargs['category_id'] = sea_category
            # 批准文号
            if 'search_good_license' in request.GET:
                license = request.GET.get('search_good_license')
                if license != '':
                    kwargs['drugattr__license__contains'] = license
            # 出售状态
            if 'search_good_is_online' in request.GET:
                sea_is_online = request.GET['search_good_is_online']
                if sea_is_online != '':
                    kwargs['is_online'] = sea_is_online
            if 's_is_qua' in request.GET:
                s_is_qua = request.GET.get('s_is_qua')
                if s_is_qua != '':
                    kwargs['is_qualified'] = s_is_qua
            search_list = Good.objects.filter(**kwargs).order_by('-external_id')
        for item in search_list:
            good = {'external_id': item.external_id,
                    'name': item.name,
                    'trade_name': item.trade_name,
                    'category': item.category.name if item.category is not None else '',
                    'prep_spec': item.prep_spec,
                    'license': item.drugattr.license if hasattr(item, 'drugattr') else '',
                    'manufacturer': item.manufacturer,
                    'locality': item.locality,
                    'unit': item.unit,
                    'pack_spec': item.pack_spec,
                    'stock_amount': item.stock_amount,
                    'supplier': item.supplier.name if item.supplier is not None else '',
                    'is_zybh': translate_is_true(item.drugattr.is_zybh) if hasattr(item, 'drugattr') else '',
                    'is_oem': translate_is_true(item.drugattr.is_oem) if hasattr(item, 'drugattr') else '',
                    'is_otc': translate_is_true(item.drugattr.is_otc) if hasattr(item, 'drugattr') else '',
                    'otc_type': item.drugattr.get_otc_type_display() if hasattr(item, 'drugattr') else '',
                    'recipe_type': item.drugattr.recipe_type if hasattr(item, 'drugattr') else '',
                    'retail_price': item.retail_price * 0.01 if item.retail_price is not None else '',
                    'member_price': item.member_price * 0.01 if item.member_price is not None else ''
                    }
            data_list.append(good)
        response = export_excel.export_excel(title, columns, data_list)
    except Exception, e:
        log.exception("exportGoodList raise, Error:%s" % e)
        response = HttpResponse("Sorry ,网络出现异常，请稍后重试!", content_type="text/plain;charset=utf-8")
    return response


def exportOrderList(request):
    """导出订单列表"""
    try:
        choose = request.POST.get('choose')
        cur_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        title = '订单详情%s' % cur_time
        search_list = []
        columns = [
            {'key': 'order_no', 'name': '订单编号'},
            {'key': 'buyer', 'name': '下单人'},
            {'key': 'purchaser', 'name': '企业名称'},
            {'key': 'purchasea_greement', 'name': '协议客户'},
            {'key': 'total_price', 'name': '订单金额（元）'},
            {'key': 'real_price', 'name': '实付金额（元）'},
            {'key': 'payment_method', 'name': '支付方式'},
            {'key': 'order_source', 'name': '订单来源'},
            {'key': 'change_price_state', 'name': '改价状态'},
            {'key': 'invoice_state', 'name': '开票状态'},
            {'key': 'verify_state', 'name': '审核状态'},
            {'key': 'trade_state', 'name': '交易状态'},
            {'key': 'name', 'name': '姓名'},
            {'key': 'order_placer_phone', 'name': '下单人手机号'},
            {'key': 'order_time', 'name': '下单时间'},
            {'key': 'shipping_method', 'name': '配送方式'},
            {'key': 'note', 'name': '买家留言'},
            {'key': 'consignee', 'name': '收货人'},
            {'key': 'consignee_phone', 'name': '收货人手机号'},
            {'key': 'address', 'name': '地址'},
            {'key': 'postcode', 'name': '邮编'}
        ]
        data_list = []
        if choose == 'ck':
            order_ids = request.POST.get('order_ids')
            export_ids = json.loads(order_ids)
            order_list = Order.objects.filter(id__in=export_ids)
        else:
            # 查询 更多查询条件
            kwargs = {}
            # 订单编号
            if 'order_no' in request.POST and request.POST['order_no']:
                kwargs['order_no__contains'] = request.POST['order_no']
            # 订单状态 交易状态
            if 'trade_state' in request.POST and request.POST['trade_state']:
                kwargs['trade_state__contains'] = request.POST['trade_state']
            # 下单人
            if 'buyer_name' in request.POST and request.POST['buyer_name']:
                kwargs['buyer__username__contains'] = request.POST['buyer_name']
            # 企业名称
            if 'purchaser_name' in request.POST and request.POST['purchaser_name']:
                kwargs['purchaser__name__contains'] = request.POST['purchaser_name']

            # 支付方式
            if 'payment_method_name' in request.POST and request.POST['payment_method_name']:
                kwargs['payment_method__pay_type'] = request.POST['payment_method_name']

            # 下单时间开始
            if 'ord_time_from' in request.POST and request.POST['ord_time_from']:
                kwargs['ord_time__gte'] = request.POST['ord_time_from']
            # 下单时间结束
            if 'ord_time_to' in request.POST and request.POST['ord_time_to']:
                ord_time_to = datetime.datetime.strptime(request.POST['ord_time_to'], "%Y-%m-%d") + datetime.timedelta(
                    days=1)
                kwargs['ord_time__lt'] = ord_time_to

            # 订单金额开始
            if 'total_price_from' in request.POST and request.POST['total_price_from']:
                kwargs['total_price__gte'] = int(request.POST['total_price_from']) * 100
            # 订单金额结束
            if 'total_price_to' in request.POST and request.POST['total_price_to']:
                kwargs['total_price__lt'] = int(request.POST['total_price_to']) * 100

            # 开票状态
            if 'order_invoice_state' in request.POST and request.POST['order_invoice_state']:
                invoice_state = int(request.POST['order_invoice_state'])
                if invoice_state:
                    kwargs['invoice_no__regex'] = r'\d'
                else:
                    kwargs['invoice_no'] = ''
            # 审核状态
            if 'verify_state' in request.POST and request.POST['verify_state']:
                kwargs['verify_state__contains'] = request.POST['verify_state']
            # 商品信息 商品名称
            filter_order_good_name = 'order_good_name' in request.POST and request.POST['order_good_name']
            if kwargs or filter_order_good_name:
                filter_order_id_list = []
                if filter_order_good_name:
                    filter_order_id_list = list(set(
                        OrderItem.objects.filter(good__name__icontains=request.POST['order_good_name']).values_list(
                            'order_id',
                            flat=True)))

                if kwargs:
                    order_list = list(Order.objects.filter(**kwargs))
                    if filter_order_good_name:
                        order_list = [order for order in order_list if order.id in filter_order_id_list]
                else:
                    order_list = list(Order.objects.filter(id__in=filter_order_id_list))
            else:
                order_list = Order.objects.all()
        for item in order_list:
            order = {'order_no': item.order_no,
                     'buyer': item.buyer.username,
                     'purchaser': item.purchaser.name,
                     'purchasea_greement': '是' if item.is_purchasea_greement else '否',
                     'total_price': item.total_price * 0.01,
                     'real_price': item.real_price * 0.01,
                     'payment_method': item.payment_method.get_pay_type_display(),
                     'order_source': item.order_source,
                     'change_price_state': item.get_change_price_state_display(),
                     'invoice_state': '已开票' if item.invoice_no else '未开票',
                     'verify_state': item.get_verify_state_display(),
                     'trade_state': item.get_trade_state_display(),
                     'name': item.buyer.first_name,
                     'order_placer_phone': item.buyer.phone,
                     'order_time': item.ord_time,
                     'shipping_method': item.shipping_method.get_shipping_type_display(),
                     'note': item.note,
                     'consignee': item.receiving_address.people,
                     'consignee_phone': item.receiving_address.telephone,
                     'address': item.receiving_address.address,
                     'postcode': '是' if item.receiving_address.email else '否'
                     }
            data_list.append(order)
        response = export_excel.export_excel(title, columns, data_list)
    except Exception, e:
        log.error("exportOrderList raise, Error:%s" % e)
        response = HttpResponse("Sorry ,网络出现异常，请稍后重试!", content_type="text/plain;charset=utf-8")
    return response


def exportOrderDetailList(request):
    """导出订单列表"""
    try:
        choose = request.POST.get('choose')
        cur_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        title = '订单详情%s' % cur_time
        search_list = []
        columns = [
            {'key': 'order_no', 'name': '订单编号'},
            {'key': 'buyer', 'name': '下单人'},
            {'key': 'purchaser', 'name': '企业名称'},
            {'key': 'purchasea_greement', 'name': '协议客户'},
            {'key': 'total_price', 'name': '订单金额（元）'},
            {'key': 'real_price', 'name': '实付金额（元）'},
            {'key': 'payment_method', 'name': '支付方式'},
            {'key': 'order_source', 'name': '订单来源'},
            {'key': 'change_price_state', 'name': '改价状态'},
            {'key': 'invoice_state', 'name': '开票状态'},
            {'key': 'verify_state', 'name': '审核状态'},
            {'key': 'trade_state', 'name': '交易状态'},
            {'key': 'name', 'name': '姓名'},
            {'key': 'order_placer_phone', 'name': '下单人手机号'},
            {'key': 'order_time', 'name': '下单时间'},
            {'key': 'shipping_method', 'name': '配送方式'},
            {'key': 'note', 'name': '买家留言'},
            {'key': 'consignee', 'name': '收货人'},
            {'key': 'consignee_phone', 'name': '收货人手机号'},
            {'key': 'address', 'name': '地址'},
            {'key': 'postcode', 'name': '邮编'},
            {'key': 'trade_name', 'name': '商品名'},
            {'key': 'retail_price', 'name': '单价（元）'},
            {'key': 'price_discount', 'name': '单价优惠（元）'},
            {'key': 'quantity', 'name': '数量'},
            {'key': 'good_total_price', 'name': '小计（元）'},
            {'key': 'good_real_price', 'name': '实付金额（元）'}
        ]
        data_list = []
        if choose == 'ck':
            order_ids = request.POST.get('order_ids')
            export_ids = json.loads(order_ids)
            order_list = Order.objects.filter(id__in=export_ids)
        else:
            # 查询 更多查询条件
            kwargs = {}
            # 订单编号
            if 'order_no' in request.POST and request.POST['order_no']:
                kwargs['order_no__contains'] = request.POST['order_no']
            # 订单状态 交易状态
            if 'trade_state' in request.POST and request.POST['trade_state']:
                kwargs['trade_state__contains'] = request.POST['trade_state']
            # 下单人
            if 'buyer_name' in request.POST and request.POST['buyer_name']:
                kwargs['buyer__username__contains'] = request.POST['buyer_name']
            # 企业名称
            if 'purchaser_name' in request.POST and request.POST['purchaser_name']:
                kwargs['purchaser__name__contains'] = request.POST['purchaser_name']

            # 支付方式
            if 'payment_method_name' in request.POST and request.POST['payment_method_name']:
                kwargs['payment_method__pay_type'] = request.POST['payment_method_name']

            # 下单时间开始
            if 'ord_time_from' in request.POST and request.POST['ord_time_from']:
                kwargs['ord_time__gte'] = request.POST['ord_time_from']
            # 下单时间结束
            if 'ord_time_to' in request.POST and request.POST['ord_time_to']:
                ord_time_to = datetime.datetime.strptime(request.POST['ord_time_to'], "%Y-%m-%d") + datetime.timedelta(
                    days=1)
                kwargs['ord_time__lt'] = ord_time_to

            # 订单金额开始
            if 'total_price_from' in request.POST and request.POST['total_price_from']:
                kwargs['total_price__gte'] = int(request.POST['total_price_from']) * 100
            # 订单金额结束
            if 'total_price_to' in request.POST and request.POST['total_price_to']:
                kwargs['total_price__lt'] = int(request.POST['total_price_to']) * 100

            # 开票状态
            if 'order_invoice_state' in request.POST and request.POST['order_invoice_state']:
                invoice_state = int(request.POST['order_invoice_state'])
                if invoice_state:
                    kwargs['invoice_no__regex'] = r'\d'
                else:
                    kwargs['invoice_no'] = ''
            # 审核状态
            if 'verify_state' in request.POST and request.POST['verify_state']:
                kwargs['verify_state__contains'] = request.POST['verify_state']
            # 商品信息 商品名称
            filter_order_good_name = 'order_good_name' in request.POST and request.POST['order_good_name']
            if kwargs or filter_order_good_name:
                filter_order_id_list = []
                if filter_order_good_name:
                    filter_order_id_list = list(set(
                        OrderItem.objects.filter(good__name__icontains=request.POST['order_good_name']).values_list(
                            'order_id',
                            flat=True)))

                if kwargs:
                    order_list = list(Order.objects.filter(**kwargs))
                    if filter_order_good_name:
                        order_list = [order for order in order_list if order.id in filter_order_id_list]
                else:
                    order_list = list(Order.objects.filter(id__in=filter_order_id_list))
            else:
                order_list = Order.objects.all()
        for item in order_list:
            for orderitem in item.orderitem_set.all():
                order = {'order_no': item.order_no,
                         'buyer': item.buyer.username,
                         'purchaser': item.purchaser.name,
                         'purchasea_greement': '是' if item.is_purchasea_greement else '否',
                         'total_price': item.total_price * 0.01,
                         'real_price': item.real_price * 0.01,
                         'payment_method': item.payment_method.get_pay_type_display(),
                         'order_source': item.order_source,
                         'change_price_state': item.get_change_price_state_display(),
                         'invoice_state': '已开票' if item.invoice_no else '未开票',
                         'verify_state': item.get_verify_state_display(),
                         'trade_state': item.get_trade_state_display(),
                         'name': item.buyer.first_name,
                         'order_placer_phone': item.buyer.phone,
                         'order_time': item.ord_time,
                         'shipping_method': item.shipping_method.get_shipping_type_display(),
                         'note': item.note,
                         'consignee': item.receiving_address.people,
                         'consignee_phone': item.receiving_address.telephone,
                         'address': item.receiving_address.address,
                         'postcode': '是' if item.receiving_address.email else '否',
                         'trade_name': orderitem.good.trade_name,
                         'retail_price': orderitem.price * 0.01,
                         'price_discount': orderitem.price * 0.01 - orderitem.real_price * 0.01,
                         'quantity': orderitem.quantity,
                         'good_total_price': orderitem.price * 0.01 * orderitem.quantity,
                         'good_real_price': orderitem.real_price * 0.01 * orderitem.quantity
                         }
                data_list.append(order)
        response = export_excel.export_excel(title, columns, data_list)
    except Exception, e:
        log.error("exportOrderList raise, Error:%s" % e)
        response = HttpResponse("Sorry ,网络出现异常，请稍后重试!", content_type="text/plain;charset=utf-8")
    return response


def translate_is_true(param):
    """布尔值做个转换"""
    if param:
        return '是'
    else:
        return '否'


def get_search_date():
    """获取当前天零点和明天零点"""
    today = datetime.date.today()
    today_str = utils_datetime.date_2datetime(today)
    tomorrow = today_str + datetime.timedelta(days=1)
    date_dict = {'today': today_str, 'tomorrow': tomorrow}
    return date_dict


class RefundsAndReturnView(View):
    """退款退货处理视图"""

    def get(self, request):
        """处理GET请求 加载所有发布信息数据"""
        data_list = []  # 数据结果集
        kwargs = {}  # 查询参数
        refund_type = ''
        refund_status = ''
        try:
            if 'ref_id' in request.GET:
                ref_id = request.GET.get('ref_id')
                if ref_id != '':
                    kwargs['id'] = ref_id
            if 'order_no' in request.GET:
                order_no = request.GET.get('order_no')
                if order_no != '':
                    kwargs['order__order_no__contains'] = order_no
            if 'refund_type' in request.GET:
                refund_type = request.GET.get('refund_type')
                if refund_type != '':
                    kwargs['refund_type'] = refund_type
            if 'refund_status' in request.GET:
                refund_status = request.GET.get('refund_status')
                if refund_status != '':
                    kwargs['refund_status'] = refund_status
            if 'start_date' in request.GET:
                start_date = request.GET.get('start_date')
                if start_date != '':
                    kwargs['created__gte'] = parse_datetime(start_date + ' 00:00:00')
            if 'end_date' in request.GET:
                end_date = request.GET.get('end_date')
                if end_date != '':
                    kwargs['created__lt'] = parse_datetime(end_date + ' 00:00:00') + datetime.timedelta(days=1)
            data_set = RefundRecord.objects.filter(**kwargs).order_by('-created')
            paginator = Paginator(data_set, PAGE_LIMIT)  # 分页
            cur_page = int(request.GET.get('page', 1))  # 获取第一页
            try:
                data_list = paginator.page(cur_page)
            except PageNotAnInteger, e:
                log.error("RefundsAndReturnView.get error:%s" % e)
                data_list = paginator.page(1)
            except EmptyPage, e:
                log.error("RefundsAndReturnView.get error:%s" % e)
                data_list = paginator.page(paginator.num_pages)
        except Exception, e:
            log.error('RefundsAndReturnView raise, Error:%s' % e)
        result = {
            'data_list': data_list,
            'refund_type': refund_type,
            'refund_status': refund_status,
            'pagi_bar': get_paginator_bar(data_list),
        }
        return render(request, 'dtsadmin/returns_and_refunds.html', result)

    def post(self, request):
        """post请求处理"""
        op_type = request.POST.get('op_type')
        try:
            if request.method == 'POST':
                if request.is_ajax():
                    op_type = request.POST.get('op_type')
                    if op_type == 'pas':  # 售后通过审核
                        obj_id = request.POST.get('obj_id')
                        obj = RefundRecord.objects.get(id=obj_id)
                        if obj.refund_status == 0:  # 售后处理
                            result = RefundsAndReturnView._pass_return_refund(request)
                        else:  #
                            result = RefundsAndReturnView._pass_return_lead_refund(request)
                    elif op_type == 'ref':  # 售后审核不通过
                        result = RefundsAndReturnView._refuse_return_refund(request)
                    elif op_type == 'rec':  # 售后确认收货并退款
                        result = RefundsAndReturnView._receipt_return_refund(request)
                    elif op_type == 'fsh':  # 平台确认退款
                        result = RefundsAndReturnView._return_refund(request)
                else:
                    # result = RefundsAndReturnView._handle_refund_search(request)
                    # return render(request, 'dtsadmin/returns_and_refunds.html', result)
                    raise Exception('请求异常')
            else:
                raise Exception('请求异常')
        except Exception, e:
            log.error("RefundsAndReturnView post raise, Error:%s" % e)
            if op_type == 'search':
                return render(request, 'dtsadmin/returns_and_refunds.html', {})
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)

    @staticmethod
    def _pass_return_refund(request):
        """后台:售后审核通过退款退货申请"""
        try:
            with transaction.atomic():
                obj_id = request.POST.get('obj_id')
                obj = RefundRecord.objects.get(id=obj_id)
                # 获取审核对象
                if obj.proc_refund is not None:
                    mark_ref = 'mark_refund_reviewing'
                    note_msg = '平台同意售后处理'
                    # 获取工作流中的task,并执行该task
                    task = obj.proc_refund.get_task_obj(mark_ref)
                    res, msg = task.transit()
                    if res:  # 通过审核操作成功
                        result = {
                            'status': 1,
                            'msg': "操作成功",
                        }
                    else:  # 通过审核操作失败
                        note_msg = "售后处理流程失败: %s" % msg.encode('utf-8')
                        result = {
                            'status': 0,
                            'msg': msg,
                        }
                    # 添加操作日志
                    OperateRecord.objects.create(
                        operate=task.name,
                        operate_cn=task.name_cn,
                        process=obj.proc_refund,
                        operator=request.user,
                        note=note_msg,
                        data_type=REFUND_MODAL,
                        data_id=obj.id,
                    )
                else:
                    raise Exception("请求异常")
        except Exception, e:
            log.error("_pass_return_refund raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e),
            }
        return result

    @staticmethod
    def _pass_return_lead_refund(request):
        """后台:售后领导审核通过退款退货申请"""
        try:
            with transaction.atomic():
                obj_id = request.POST.get('obj_id')
                obj = RefundRecord.objects.get(id=obj_id)
                # 获取审核对象
                if obj.proc_refund is not None:
                    mark_ref = 'mark_refund_returning'
                    if obj.refund_type == 1:
                        note_msg = '平台同意售后处理,等待买家退货'
                        # 添加站内消息
                        remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                        if remind_settings:
                            remind_item = json.loads(remind_settings.note)
                            remind_item_seting = remind_item['remind_settings']
                            item_list = json.loads(remind_item_seting)
                            flag = item_list[4]['mail']
                            if flag == 'Y':
                                content_str = '您的订单%s退货申请已通过' % obj.order.order_no.encode('utf-8')
                                id = obj.order.buyer.id
                                SiteMessage.objects.create(
                                    user_id=id,
                                    order_id=obj.order.id,
                                    msg_type=SITE_MESSAGE_TYPE_ORDER,
                                    contant=content_str,
                                    is_read=False,
                                )
                    else:
                        note_msg = '平台同意售后处理,等待平台退款'
                        # 添加站内消息
                        remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                        if remind_settings:
                            remind_item = json.loads(remind_settings.note)
                            remind_item_seting = remind_item['remind_settings']
                            item_list = json.loads(remind_item_seting)
                            flag = item_list[3]['mail']
                            if flag == 'Y':
                                content_str = '您的订单%s退款申请已通过' % obj.order.order_no.encode('utf-8')
                                id = obj.order.buyer.id
                                SiteMessage.objects.create(
                                    user_id=id,
                                    order_id=obj.order.id,
                                    msg_type=SITE_MESSAGE_TYPE_ORDER,
                                    contant=content_str,
                                    is_read=False,
                                )
                    # 获取工作流中的task,并执行该task
                    task = obj.proc_refund.get_task_obj(mark_ref)
                    res, msg = task.transit()
                    if res:  # 通过审核操作成功
                        result = {
                            'status': 1,
                            'msg': "操作成功",
                        }
                    else:  # 通过审核操作失败
                        note_msg = "售后处理流程失败: %s" % msg.encode('utf-8')
                        result = {
                            'status': 0,
                            'msg': msg,
                        }
                    # 添加操作日志
                    OperateRecord.objects.create(
                        operate=task.name,
                        operate_cn=task.name_cn,
                        process=obj.proc_refund,
                        operator=request.user,
                        note=note_msg,
                        data_type=REFUND_MODAL,
                        data_id=obj.id,
                    )
                else:
                    raise Exception("请求异常")
        except Exception, e:
            log.error("_pass_return_refund raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e),
            }
        return result

    @staticmethod
    def _refuse_return_refund(request):
        """后台:审核不通过退款退货申请"""
        try:
            with transaction.atomic():
                obj_id = request.POST.get('obj_id')
                obj = RefundRecord.objects.get(id=obj_id)
                # 获取审核对象
                if obj.proc_refund is not None:
                    mark_ref = 'mark_refund_closed'
                    # 获取工作流中的task,并执行该task
                    task = obj.proc_refund.get_task_obj(mark_ref)
                    result, msg = task.transit()
                    if result:
                        note_msg = "平台不同意售后处理，等待买家修改"
                        # 添加站内消息
                        remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                        if remind_settings:
                            remind_item = json.loads(remind_settings.note)
                            remind_item_seting = remind_item['remind_settings']
                            item_list = json.loads(remind_item_seting)
                            if obj.refund_type == 0:
                                flag = item_list[3]['mail']
                                if flag == 'Y':
                                    content_str = '您的订单%s退款申请未通过' % obj.order_no.encode('utf-8')
                                    id = obj.buyer.id
                                    SiteMessage.objects.create(
                                        user_id=id,
                                        order_id=obj.id,
                                        msg_type=SITE_MESSAGE_TYPE_ORDER,
                                        contant=content_str,
                                        is_read=False,
                                    )
                            else:
                                flag = item_list[4]['mail']
                                if flag == 'Y':
                                    content_str = '您的订单%s退货申请未通过' % obj.order_no.encode('utf-8')
                                    id = obj.buyer.id
                                    SiteMessage.objects.create(
                                        user_id=id,
                                        order_order_no=obj.order_no,
                                        msg_type=SITE_MESSAGE_TYPE_ORDER,
                                        contant=content_str,
                                        is_read=False,
                                    )
                        result = {
                            'status': 1,
                            'msg': "操作成功",
                        }
                    else:
                        note_msg = "售后处理失败,原因：%s" % msg.encode('utf-8')
                        result = {
                            'status': 0,
                            'msg': msg,
                        }
                    # 添加操作日志
                    OperateRecord.objects.create(
                        operate=task.name,
                        operate_cn=task.name_cn,
                        process=obj.proc_refund,
                        operator=request.user,
                        note=note_msg,
                        data_type=REFUND_MODAL,
                        data_id=obj.id,
                    )
                else:
                    raise Exception("请求异常")
        except Exception, e:
            log.error("_refuse_return_refund raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e),
            }
        return result

    @staticmethod
    def _receipt_return_refund(request):
        """确认收货:并退款"""
        try:
            with transaction.atomic():
                obj_id = request.POST.get('obj_id')
                obj = RefundRecord.objects.get(id=obj_id)
                # 获取审核对象
                if obj.proc_refund is not None:
                    mark_ref = 'mark_refund_finished'
                    # 获取工作流中的task,并执行该task
                    task = obj.proc_refund.get_task_obj(mark_ref)
                    result, msg = task.transit()
                    if result:
                        print type(obj.refund)
                        note_msg = "平台确认收货，退款完成，退款金额：%s元" % str(obj.refund * 0.01)
                        result = {
                            'status': 1,
                            'msg': "操作成功",
                        }
                    else:
                        note_msg = "确认收货失败,原因：%s" % msg.encode('utf-8')
                        result = {
                            'status': 0,
                            'msg': msg,
                        }
                    # 添加操作日志
                    OperateRecord.objects.create(
                        operate=task.name,
                        operate_cn=task.name_cn,
                        process=obj.proc_refund,
                        operator=request.user,
                        note=note_msg,
                        data_type=REFUND_MODAL,
                        data_id=obj.id,
                    )
                else:
                    raise Exception("请求异常")
        except Exception, e:
            log.error("_receipt_return_refund raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e),
            }
        return result

    @staticmethod
    def _return_refund(request):
        """确认退款"""
        try:
            with transaction.atomic():
                obj_id = request.POST.get('obj_id')
                obj = RefundRecord.objects.get(id=obj_id)
                # 获取审核对象
                if obj.proc_refund is not None:
                    mark_ref = 'mark_refund_finished'
                    # 获取工作流中的task,并执行该task
                    task = obj.proc_refund.get_task_obj(mark_ref)
                    result, msg = task.transit()
                    if result:
                        print type(obj.refund)
                        note_msg = "平台同意并确认退款，退款金额：%s元" % str(obj.refund * 0.01)
                        # 添加站内消息
                        remind_settings = SettingsItem.objects.filter(name='REMIND_SETTING').first()
                        if remind_settings:
                            remind_item = json.loads(remind_settings.note)
                            remind_item_seting = remind_item['remind_settings']
                            item_list = json.loads(remind_item_seting)
                            flag = item_list[3]['mail']
                            if flag == 'Y':
                                content_str = '您的订单%s退款审核已通过' % obj.order.order_no.encode('utf-8')
                                id = obj.order.buyer.id
                                SiteMessage.objects.create(
                                    user_id=id,
                                    order_id=obj.order.id,
                                    msg_type=SITE_MESSAGE_TYPE_ORDER,
                                    contant=content_str,
                                    is_read=False,
                                )
                        result = {
                            'status': 1,
                            'msg': "操作成功",
                        }
                    else:
                        note_msg = "平台同意并确认退款失败,原因：%s" % msg.encode('utf-8')
                        result = {
                            'status': 0,
                            'msg': msg,
                        }
                    # 添加操作日志
                    OperateRecord.objects.create(
                        operate=task.name,
                        operate_cn=task.name_cn,
                        process=obj.proc_refund,
                        operator=request.user,
                        note=note_msg,
                        data_type=REFUND_MODAL,
                        data_id=obj.id,
                    )
                else:
                    raise Exception("请求异常")
        except Exception, e:
            log.error("_receipt_return_refund raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e),
            }
        return result

    @staticmethod
    def _handle_refund_search(request):
        """多条件查询退款退货"""
        kwargs = {}
        refund_type = ''
        refund_status = ''
        if 'ref_id' in request.POST:
            ref_id = request.POST.get('ref_id')
            if ref_id != '':
                kwargs['id'] = ref_id
        if 'order_no' in request.POST:
            order_no = request.POST.get('order_no')
            if order_no != '':
                kwargs['order__order_no__contains'] = order_no
        if 'refund_type' in request.POST:
            refund_type = request.POST.get('refund_type')
            if refund_type != '':
                kwargs['refund_type'] = refund_type
        if 'refund_status' in request.POST:
            refund_status = request.POST.get('refund_status')
            if refund_status != '':
                kwargs['refund_status'] = refund_status
        if 'start_date' in request.POST:
            start_date = request.POST.get('start_date')
            if start_date != '':
                kwargs['created__gte'] = parse_datetime(start_date + ' 00:00:00')
        if 'end_date' in request.POST:
            end_date = request.POST.get('end_date')
            if end_date != '':
                kwargs['created__lt'] = parse_datetime(end_date + ' 00:00:00') + datetime.timedelta(days=1)
        data_set = RefundRecord.objects.filter(**kwargs).order_by('-created')
        total_count = data_set.count()  # 总记录数
        paginator = Paginator(data_set, PAGE_LIMIT)  # 分页
        cur_page = int(request.POST.get('load_page', 1))  # 获取第一页
        data_list = []
        try:
            data_list = paginator.page(cur_page)
        except PageNotAnInteger, e:
            log.error("RefundsAndReturnView.get error:%s" % e)
            data_list = paginator.page(1)
        except EmptyPage, e:
            log.error("RefundsAndReturnView.get error:%s" % e)
            data_list = paginator.page(paginator.num_pages)
        result = {
            'data_list': data_list,
            'total_count': total_count,
            'per_page': PAGE_LIMIT,
            'cur_page': cur_page,
            'page': paginator,
            'refund_type': refund_type,
            'refund_status': refund_status
        }
        return result
