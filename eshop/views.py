# -*- coding: utf-8 -*-
from compiler.ast import obj
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import Http404, HttpResponseNotFound
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, Http404, HttpResponse
from eshop.forms import (LoginForm,
                         LoginPhoneForm,
                         RegisterForm,
                         MerchantRegisterForm,
                         AccountInfoForm,
                         ConsultFeedbackForm,
                         ForgetPasswordForm,
                         AccountSafetyForm,
                         )
from dtsauth.models import User, Enterprise, EnterpriseQualification, OperateRecord
from order.models import ReceivingAddress, QuicklyOrder
from django.core.exceptions import ObjectDoesNotExist
from common.models import SettingsType, SettingsItem, Region
from common.utils.utils_log import log
from common.utils.utils_paginator import get_paginator_bar
from django.db import transaction
from django.db.models import Q, F
from good.models import Good, GoodPhoto, DrugAttr, LackRegister
from dtsadmin.models import ConsultFeedback

from slugify import slugify
from .forms import CaptchaTestForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from order.models import (Order,
                          OrderItem,
                          QuicklyOrder,
                          OrderItem,
                          PaymentMethod,
                          ShippingMethod,
                          MyFavorites,
                          ShoppingCartItem,
                          RefundRecord,
                          Invoice)
from order.forms import ReceivingAddressForm
from eshop.models import PageSection
from eshop.models import SiteMessage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.constant import PAGE_LIMIT
from common.constant import (
    PAGE_LIMIT,
    PAGE_ESHOP_HOME,
    PAGE_FOOT,
    INFO_STATUS_ACTIVE,
    INFO_TYPE_INFO,
    INFO_TYPE_NOTICE,
    CONSULT,
    FEEDBACK,
    ORDER_MODAL,
    REFUND_HANDLING,
    ORDER_IS_REFUNDING,
    REFUND_MODAL,
    USERTYPE_CHOICES,
    ORDER_NOT_PAID,
    ORDER_HAS_PAID,
    ORDER_IS_PICKING,
    ORDER_IS_SHIPPING,
    ORDER_CLOSED,
    # 支付类型
    PAY_TYPE_CHOICES,
    # 配送类型
    SHIPPING_TYPE_CHOICES,
    # 退款关闭
    REFUND_CLOSED
)
from bpmn.configs import REFUND as BPMN_REFUND, DELIVERY as BPMN_DELIVERY
from common.utils.utils_log import log
from good.models import Good, GoodPhoto
from common.utils import utils_datetime
from dtsadmin.models import Informations

from bpmn.models import Process
import time
import datetime
import json
import re
import random

from django.utils.decorators import method_decorator, available_attrs
from django.contrib.auth.decorators import login_required

# 短信验证
from common.sms import make_sms
from common.utils.utils_sms import send_sms
from functools import wraps


def eshop_context(func):
    @wraps(func, assigned=available_attrs(func))
    def inner(request, *args, **kwargs):
        site_settings = SettingsType.get_front_site_settings()
        consult_settings = SettingsType.get_consult_settings()
        servive_qq_list = [data['QQ_number'] for data in json.loads(consult_settings.get('service_account_list', '[]'))]
        extras = {
            'foot_ads': {'title': u'平台推广图', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                         'sectiongood_list': []},
            'foot_help_nav': {'title': u'帮助导航', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                              'sectiongood_list': []},
            'foot_about_us': {'title': u'关于我们', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                              'sectiongood_list': []},
            'copyright': site_settings.get('admin_copyright', u'Copyright © 2015-2016 武汉葫芦娃科技有限公司版权所有'),
            'site_record_no': site_settings.get('admin_site_no', u'鄂ICP备16019117号-1'),
            'input_service_number': consult_settings.get('input_service_number', '027-84886797'),
            'enable_cust_service': True if consult_settings.get('enable_cust_service', 'Y') == 'Y' else False,
            'servive_qq': random.choice(servive_qq_list) if servive_qq_list else '735018963',
            'admin_complain': site_settings.get('admin_complain', '12331'),
            'admin_email': site_settings.get('admin_email', 'hb1004@dingtalk.com'),
        }
        # 页脚动态区域
        foot_section_data = PageSection.build_tree_by_page(PAGE_FOOT)
        extras.update(foot_section_data)
        request.extras = extras
        return func(request, *args, **kwargs)

    return inner


def home(request):
    # from dtsauth.models import User
    # user_list = User.objects.all()
    # from django.core.mail import mail_admins, send_mail
    # from django.conf import settigs
    # mail_admins(u'测试DTS mail_admins', '123', fail_silently=False)
    # send_mail(u'测试DTS send_mail', '123', settings.DEFAULT_FROM_EMAIL, ['zhongchao@paithink.com'], fail_silently=False)
    from common.utils.utils_sms import send_sms
    # send_sms([15377697510], 'DTS测试')
    # send_sms([18707123609], '派生科技刘焕')
    # send_sms([18986977682], 'DTS测试')
    # send_sms([18672688994], 'DTS测试 谢')
    # send_sms([13037142208], 'DTS测试 熊')

    # send_sms([15071242278], '你好段润')
    # send_sms([15810559569], '派生科技邹安超')

    user_list = [
        {'username': 'zhongchao', 'email': '123'},
        {'username': 'duanrun', 'email': '123'},
    ]
    return render(request, 'eshop/home.html', {'user_list': user_list})


@eshop_context
def eshop_home(request):
    info_mations = []
    info_notics = []
    home_section = {
        'category_nav': {'title': u'全部商品分类', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                         'sectiongood_list': []},
        'main_nav': {'title': u'主导航', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                     'sectiongood_list': []},
        'main_carousel': {'title': u'主轮播图', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                          'sectiongood_list': []},
        'good_tabs': {'title': u'商品标签页', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                      'sectiongood_list': []},
        'good_list': {'title': u'商品分类列表', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                      'sectiongood_list': []},
    }
    try:
        # 加载资讯
        td = datetime.date.today()  # 当前系统时间
        info_kwargs = {'info_type': INFO_TYPE_INFO, 'info_status': INFO_STATUS_ACTIVE, 'start_date__lte': td,
                       'end_date__gte': td}
        info_mations = Informations.objects.filter(**info_kwargs).order_by('order_no')[0:9]
        # 加载公告
        notic_kwargs = {'info_type': INFO_TYPE_NOTICE, 'info_status': INFO_STATUS_ACTIVE, 'start_date__lte': td,
                        'end_date__gte': td}
        info_notics = Informations.objects.filter(**notic_kwargs).order_by('order_no')[0:9]

        # 首页动态区域
        home_section_data = PageSection.build_tree_by_page(PAGE_ESHOP_HOME)
        home_section.update(home_section_data)
        # 系统自动挑选商品 TODO by zhongchao 2017-04-20
        HOME_GOOD_LIST_AUTO = False
        if HOME_GOOD_LIST_AUTO:
            if isinstance(home_section['good_list'], PageSection):
                section_list = getattr(home_section['good_list'], 'child_list', [])
                for section in section_list:
                    good_set = Good.objects.select_related('category').filter(
                        Q(category__name__contains=section.title) | Q(external_category__contains=section.title) | Q(
                            extra_category__contains=section.title)) \
                                   .order_by('-online_time')[:10]
                    section.sectiongood_list = [{'good': good} for good in good_set]
    except Exception, e:
        log.error("dts_home raise exception,error:%s" % e)

    result = {
        'info_mations': info_mations,
        'info_notics': info_notics,
        'home_section': home_section,
    }
    return render(request, 'eshop/eshop_home.html', result)


@eshop_context
def eshop_notice(request, info_id):
    """前台首页:公告资讯详情"""
    publish_obj = Informations.objects.filter(pk=info_id).first()
    home_section = {
        'category_nav': {'title': u'全部商品分类', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                         'sectiongood_list': []},
        'main_nav': {'title': u'主导航', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                     'sectiongood_list': []},
        'main_carousel': {'title': u'主轮播图', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                          'sectiongood_list': []},
        'good_tabs': {'title': u'商品标签页', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                      'sectiongood_list': []},
        'good_list': {'title': u'商品分类列表', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                      'sectiongood_list': []},
    }
    try:
        # 首页动态区域
        home_section_data = PageSection.build_tree_by_page(PAGE_ESHOP_HOME)
        home_section.update(home_section_data)
        # 系统自动挑选商品 TODO by zhongchao 2017-04-20
        HOME_GOOD_LIST_AUTO = False
        if HOME_GOOD_LIST_AUTO:
            if isinstance(home_section['good_list'], PageSection):
                section_list = getattr(home_section['good_list'], 'child_list', [])
                for section in section_list:
                    good_set = Good.objects.select_related('category').filter(
                        Q(category__name__contains=section.title) | Q(external_category__contains=section.title) | Q(
                            extra_category__contains=section.title)) \
                                   .order_by('-online_time')[:10]
                    section.sectiongood_list = [{'good': good} for good in good_set]
    except Exception, e:
        log.exception("eshop_notice raise,Error:%s" % e)
    result = {
        'obj': publish_obj,
        'home_section': home_section,
    }
    return render(request, 'eshop/eshop_notice.html', result)


@eshop_context
def notice_list(request, info_type):
    """前台首页:公告资讯列表"""
    pub_lst = []
    home_section = {
        'category_nav': {'title': u'全部商品分类', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                         'sectiongood_list': []},
        'main_nav': {'title': u'主导航', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                     'sectiongood_list': []},
        'main_carousel': {'title': u'主轮播图', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                          'sectiongood_list': []},
        'good_tabs': {'title': u'商品标签页', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                      'sectiongood_list': []},
        'good_list': {'title': u'商品分类列表', 'child_list': [], 'sectionimage_list': [], 'sectionhref_list': [],
                      'sectiongood_list': []},
    }
    try:
        # 公告资讯
        cur_date = datetime.date.today()  # 当前系统时间
        info_kwargs = {'info_type': info_type, 'info_status': '1', 'start_date__lte': cur_date,
                       'end_date__gte': cur_date}
        pub_lst = Informations.objects.filter(**info_kwargs).order_by('order_no')

        # 首页动态区域
        home_section_data = PageSection.build_tree_by_page(PAGE_ESHOP_HOME)
        home_section.update(home_section_data)
        # 系统自动挑选商品 TODO by zhongchao 2017-04-20
        HOME_GOOD_LIST_AUTO = False
        if HOME_GOOD_LIST_AUTO:
            if isinstance(home_section['good_list'], PageSection):
                section_list = getattr(home_section['good_list'], 'child_list', [])
                for section in section_list:
                    good_set = Good.objects.select_related('category').filter(
                        Q(category__name__contains=section.title) | Q(external_category__contains=section.title) | Q(
                            extra_category__contains=section.title)) \
                                   .order_by('-online_time')[:10]
                    section.sectiongood_list = [{'good': good} for good in good_set]
    except Exception, e:
        log.error("show_publish_more raise exception,error:%s" % e)
    result = {
        'pub_lst': pub_lst,
        'info_type': info_type,
        'home_section': home_section,
    }
    return render(request, 'eshop/notice_list.html', result)


def user_register(request):
    operate_mode_choices = SettingsType.get_item_list('OPERATE_MODE')

    return render(request, 'eshop/user_register.html', {})


class UserRegisterView(View):
    @method_decorator(eshop_context)
    def get(self, request):
        method = request.GET.get('method', '')
        # 审核的企业
        # if 'merchant' == method:
        #     return render(request, 'eshop/user_register.html', {})


        try:
            operate_mode_choices = SettingsType.get_item_list('OPERATE_MODE')
            operate_set = SettingsType.get_item_list('OPERATE_SCOPE')

        except Exception, e:
            log.error(e)

        return render(request, 'eshop/user_register.html', {
            'operate_mode_choices': operate_mode_choices,
            'operate_scope': operate_set,
        })

    def post(self, request):
        if 'type' in request.POST:
            type = request.POST.get('type', '')
            # 个人用户注册
            if 'member' == type:
                return self._handle_member_form(request)
            # 企业用户注册
            elif 'merchant' == type:
                return self._handle_merchant_form(request)

            # 发送短信验证码
            elif 'message_code' == type:

                # 验证电话号码
                phone = request.POST.get('phone', '')
                phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^147\d{8}')
                is_phone = phone_re.match(phone)
                if not is_phone:
                    result = {
                        'status': 0,
                        'msg': u'请输入正确的电话号码'
                    }
                    return JsonResponse(result)

                is_phone_exist = User.objects.filter(phone=phone)
                if is_phone_exist:
                    result = {
                        'status': 0,
                        'msg': u'这个电话已经注册过了，请直接登录!'
                    }
                    return JsonResponse(result)

                # 防止重复递交电话号码
                request.session.set_expiry(60)
                phone_session = request.session.get('phone', '')
                if phone_session == phone:
                    result = {
                        'status': 0,
                        'msg': u'验证码已发送，请注意查收!'
                    }
                    return JsonResponse(result)
                request.session['phone'] = phone

                sms_msg = make_sms()
                c = CaptchaStore()
                c.response = sms_msg[1]
                c.challenge = phone
                c.save()

                # 测试 可不发短信 去CaptchaStore中查看验证码
                if not settings.DEBUG:
                    send_sms([phone], sms_msg[0])

                json_response = {
                    'key': c.hashkey,
                    'status': 1
                }
                return JsonResponse(json_response)
        else:
            result = {
                'status': 0,
                'msg': '请求错误'
            }
        return JsonResponse(result)

    def _handle_member_form(self, request):
        """处理个人用户注册"""
        member_from = RegisterForm(request.POST)

        phone_session = request.session.get('phone', '')
        if not phone_session:
            result = {
                'status': 0,
                'msg': '验证码失效，请重新发送验证码并填写'
            }
            return JsonResponse(result)

        # 验证短信验证码
        captcha = request.POST.get('captcha', '')
        captcha_0 = request.POST.get('captcha_0', '')
        is_cap = CaptchaStore.objects.filter(response=str(captcha), challenge=phone_session, hashkey=captcha_0)

        if not is_cap:
            result = {
                'status': 0,
                'msg': '短信验证失败 请重试'
            }
            return JsonResponse(result)

        if member_from.is_valid():
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            first_name = request.POST.get('first_name', '')
            phone = request.POST.get('phone', '')
            gender = request.POST.get('gender', '')
            try:
                User.objects.get(username=username)
                result = {
                    'status': 0,
                    'msg': '用户已经存在'
                }
                return JsonResponse(result)
            except ObjectDoesNotExist:
                passwd = request.POST.get('passwd', '')
                passwd2 = request.POST.get('passwd2', '')
                if passwd == passwd2:
                    User.objects.create(username=username,
                                        email=email,
                                        first_name=first_name,
                                        phone=phone,
                                        gender=gender,
                                        is_active=True,
                                        is_master=False,
                                        password=make_password(passwd))
                    result = {
                        'status': 1,
                        'msg': '注册成功'
                    }

                    # 注册成功删掉session
                    del request.session['phone']

                    return JsonResponse(result)

                else:
                    result = {
                        'status': 0,
                        'msg': '两次密码不一致'
                    }
                    return JsonResponse(result)
        else:
            result = {
                'status': 0,
                'msg': str(member_from.errors)  # '表单验证失败'
            }
            return JsonResponse(result)

    def _handle_merchant_form(self, request):
        """处理企业用户注册"""
        merchant_from = MerchantRegisterForm(request.POST, request.FILES)

        phone_session = request.session.get('phone', '')
        if not phone_session:
            result = {
                'status': 0,
                'msg': '验证码失效，请重新发送验证码并填写'
            }
            return JsonResponse(result)

        # 验证短信验证码
        captcha = request.POST.get('captcha', '')
        captcha_0 = request.POST.get('captcha_0', '')
        is_cap = CaptchaStore.objects.filter(response=str(captcha), challenge=phone_session, hashkey=captcha_0)

        if not is_cap:
            result = {
                'status': 0,
                'msg': '短信验证失败 请重试'
            }
            return JsonResponse(result)

        if merchant_from.is_valid():
            # 验证表单字段
            try:
                enter_name = request.POST.get('enterprise_name', '')
                Enterprise.objects.get(name=enter_name)
                result = {
                    'status': 0,
                    'msg': '该企业已经存在'
                }
                return JsonResponse(result)
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
                    enter.save()

                    try:
                        username = request.POST.get('username', '')
                        email = request.POST.get('email', '')
                        first_name = request.POST.get('first_name', '')
                        phone = request.POST.get('phone', '')
                        gender = request.POST.get('gender', '')

                        User.objects.get(username=username)
                        result = {
                            'status': 0,
                            'msg': '用户已经存在'
                        }
                        return JsonResponse(result)
                    except ObjectDoesNotExist:
                        passwd = request.POST.get('passwd', '')
                        passwd2 = request.POST.get('passwd2', '')

                        if passwd == passwd2:
                            user = User()
                            user.username = username
                            user.email = email
                            user.first_name = first_name
                            user.gender = gender
                            user.phone = phone
                            user.password = make_password(passwd)
                            user.enterprise = enter
                            user.is_active = False
                            user.is_master = True
                            user.usertype = u'Purchaser'
                            user.save()

                            user_address = ReceivingAddress()
                            user_address.user = user
                            user_address.region = region
                            user_address.address = address
                            user_address.is_default = True
                            user_address.save()

                            #  资质文件处理
                            # 企业许可证
                            if merchant_from.cleaned_data['qyxk']:
                                enter_file = EnterpriseQualification()
                                enter_file.enterprise = enter
                                enter_file.photo = merchant_from.cleaned_data['qyxk']
                                enter_file.save()

                            # 营业执照
                            if merchant_from.cleaned_data['yyzz']:
                                enter_file = EnterpriseQualification()
                                enter_file.enterprise = enter
                                enter_file.photo = merchant_from.cleaned_data['yyzz']
                                enter_file.save()

                            # 法人委托书
                            if merchant_from.cleaned_data['wts']:
                                enter_file = EnterpriseQualification()
                                enter_file.enterprise = enter
                                enter_file.photo = merchant_from.cleaned_data['wts']
                                enter_file.save()
                            result = {
                                'status': 1,
                                'msg': '注册成功',
                                # 'html': html
                            }

                            # 注册成功删掉session
                            del request.session['phone']

                            return JsonResponse(result)
                        else:
                            result = {
                                'status': 0,
                                'msg': '两次密码不一致'
                            }
                            return JsonResponse(result)
        else:
            if merchant_from.has_error('qyxk'):
                result = {
                    'status': 0,
                    'msg': '请上传企业资质文件以便快速审核通过'
                }
                return JsonResponse(result)
            result = {
                'status': 0,
                'msg': str(merchant_from.errors)
                # 'msg': str(merchant_from.non_field_errors())
            }
            return JsonResponse(result)


class UserLoginView(View):
    """前台登录"""

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/member_center/')
        form = LoginForm
        return render(request, 'eshop/user_login.html', {'form': form})

    def post(self, request):
        method = request.POST.get('method', '')
        # 自动登录
        auto_logo = request.POST.get('auto_logo', '')
        if auto_logo:
            request.session.set_expiry(None)
        if method == 'user':
            form = LoginForm(request.POST)
            if form.is_valid():
                name = request.POST.get('name', '')
                passwd = request.POST.get('passwd', '')
                # user = authenticate(username=name, password=passwd)
                user = User.objects.filter(username=name).first()
                if not user:
                    result = {
                        'status': 0,
                        'msg': '该用户没有注册',
                    }
                    return JsonResponse(result)
                # if user is not None:  # 如果用户名和密码匹配
                is_user = user.check_password(passwd)
                # 验证密码
                if is_user:
                    # 导航条我的订单 付款 发货 收货
                    dfk = Order.objects.filter(buyer=user, trade_state=ORDER_NOT_PAID).count()
                    dfh = Order.objects.filter(buyer=user, trade_state__in=[ORDER_HAS_PAID, ORDER_IS_PICKING]).count()
                    dsh = Order.objects.filter(buyer=user, trade_state=ORDER_IS_SHIPPING).count()
                    request.session['order'] = {'dfk': dfk, 'dfh': dfh, 'dsh': dsh}

                    # usertype = SettingsItem.objects.filter(value=user.usertype).first()
                    user_type_tuple = {}
                    for u_tuple in USERTYPE_CHOICES:
                        value, name = u_tuple
                        if value == user.usertype:
                            user_type_tuple['value'] = value
                            user_type_tuple['name'] = name
                    # 跳转url
                    if user.usertype in ['Purchaser', 'Members']:
                        user_type_tuple['url'] = '/eshop/eshop_home/'
                    elif user.usertype in ['System', 'Regulator', 'Supplier']:
                        user_type_tuple['url'] = '/dtsadmin/dts_home/'

                    # 如果是超级管理员
                    if user.is_superuser:
                        login(request, user)
                        result = {
                            'status': 2,
                            'msg': '超级用户',
                            'url': '/dtsadmin/dts_home/',
                        }
                        return JsonResponse(result)
                    # 如果是企业账号
                    if user.enterprise:
                        if user.enterprise.is_lock:
                            result = {
                                'status': 0,
                                'msg': u'企业锁定无法登录',
                                # 'url': user_type_tuple['url'],
                            }
                            return JsonResponse(result)

                        if user.enterprise.review_status != 2:
                            result = {
                                'status': 0,
                                'msg': user.enterprise.get_review_status_display() + u'无法登录',
                                # 'url': user_type_tuple['url'],
                            }
                            return JsonResponse(result)
                        if user.is_master:
                            # 企业审核通过
                            if user.is_active:
                                # 用户未锁定
                                login(request, user)
                                result = {
                                    'status': 2,
                                    'msg': user_type_tuple['name'],
                                    'url': user_type_tuple['url'],
                                }
                                return JsonResponse(result)
                            # 企业没有审核
                            else:
                                # 用户已锁定
                                result = {
                                    'status': 0,
                                    'msg': u'您的账户已被锁定，请联系客服解锁!',
                                }
                                return JsonResponse(result)
                        else:
                            if user.is_active:
                                login(request, user)
                                result = {
                                    'status': 2,
                                    'msg': user_type_tuple['name'],
                                    'url': user_type_tuple['url'],
                                }
                                return JsonResponse(result)
                            else:
                                result = {
                                    'status': 0,
                                    'msg': u'您的账户已被锁定，请联系客服解锁!',
                                    'url': '/eshop/user_register/?method=merchant'
                                }
                                return JsonResponse(result)
                    # 如果是个人账号
                    else:
                        # 如果用户是激活状态
                        if user.is_active:
                            login(request, user)
                            result = {
                                'status': 2,
                                'msg': user_type_tuple['name'],
                                'url': user_type_tuple['url'],
                            }
                            return JsonResponse(result)
                        # 用户未激活
                        else:
                            result = {
                                'status': 0,
                                'msg': '用户未激活'
                            }
                            return JsonResponse(result)
                # 用户名和密码错误
                else:
                    result = {
                        'status': 0,
                        'msg': '用户名和密码错误'
                    }
                    return JsonResponse(result)
            else:
                if form.has_error('captcha'):
                    result = {
                        'status': 0,
                        'msg': '验证码错误'
                    }
                    return JsonResponse(result)
                result = {
                    'status': 0,
                    # 'form': str(form.non_field_errors()),
                    'msg': '表单验证失败'
                }
                return JsonResponse(result)

        elif method == 'phone':
            form = LoginPhoneForm(request.POST)
            if form.is_valid():
                phone = request.POST.get('phone', '')
                captcha = request.POST.get('captcha', '')

                user = User.objects.filter(phone=phone).first()
                if not user:
                    result = {
                        'status': 0,
                        'msg': '这个电话没有注册'
                    }
                    return JsonResponse(result)

                if CaptchaStore.objects.filter(response=str(captcha), challenge=phone):

                    # usertype = SettingsItem.objects.filter(value=user.usertype).first()

                    user_type_tuple = {}
                    for u_tuple in USERTYPE_CHOICES:
                        value, name = u_tuple
                        if value == user.usertype:
                            user_type_tuple['value'] = value
                            user_type_tuple['name'] = name
                    # 跳转url
                    if user.usertype in ['Purchaser', 'Members']:
                        user_type_tuple['url'] = '/eshop/eshop_home/'
                    elif user.usertype in ['System', 'Regulator', 'Supplier']:
                        user_type_tuple['url'] = '/dtsadmin/dts_home/'

                    # 如果数据字典中没有值
                    # if usertype:
                    #     usertype_name = usertype.name
                    # else:
                    #     usertype_name = u'用户'

                    # 如果是企业
                    if user.enterprise:
                        if user.enterprise.is_lock:
                            result = {
                                'status': 0,
                                'msg': u'企业锁定无法登录',
                                # 'url': user_type_tuple['url'],
                            }
                            return JsonResponse(result)
                        if user.enterprise.review_status != 2:
                            result = {
                                'status': 0,
                                'msg': user.enterprise.get_review_status_display() + u'无法登录',
                                # 'url': user_type_tuple['url'],
                            }
                            return JsonResponse(result)
                        if user.is_master:
                            # 企业审核通过
                            if user.is_active:
                                login(request, user)
                                result = {
                                    'status': 2,
                                    'msg': user_type_tuple['name'],
                                    'url': user_type_tuple['url']
                                }
                                return JsonResponse(result)
                            # 企业没有审核
                            else:
                                result = {
                                    'status': 3,
                                    'msg': u'您的企业还在审核中，请耐心等待!',
                                    'url': '/eshop/user_register/?method=merchant'
                                }
                                return JsonResponse(result)

                        else:
                            login(request, user)
                            result = {
                                'status': 2,
                                'msg': user_type_tuple['name'],
                                'url': user_type_tuple['url'],
                            }
                            return JsonResponse(result)


                    # 如果不是企业账号
                    else:
                        # 如果用户是激活状态
                        if user.is_active:
                            login(request, user)
                            result = {
                                'status': 2,
                                'msg': user_type_tuple['name'],
                                'url': user_type_tuple['url']
                            }
                            return JsonResponse(result)
                        # 用户未激活
                        else:
                            result = {
                                'status': 0,
                                'msg': '用户未激活'
                            }
                            return JsonResponse(result)
                else:
                    result = {
                        'status': 0,
                        'msg': '短信验证码错误'
                    }
                    return JsonResponse(result)
            else:
                result = {
                    'status': 0,
                    'msg': '表单验证失败'
                }
                return JsonResponse(result)

        # 发送短信验证码
        elif 'sms_code' == method:
            # 验证电话号码
            phone = request.POST.get('phone', '')
            phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
            is_phone = phone_re.match(phone)
            if not is_phone:
                result = {
                    'status': 0,
                    'msg': u'请输入正确的电话号码'
                }
                return JsonResponse(result)

            is_phone_exist = User.objects.filter(phone=phone)
            if not is_phone_exist:
                result = {
                    'status': 0,
                    'msg': u'这个电话没有注册，请先注册!'
                }
                return JsonResponse(result)

            # 避免多次发送短信
            request.session.set_expiry(60)
            phone_session = request.session.get('phone', '')
            if phone_session == phone:
                result = {
                    'status': 0,
                    'msg': u'验证码已发送，请注意查收!'
                }
                return JsonResponse(result)

            request.session['phone'] = phone

            sms_msg = make_sms()
            c = CaptchaStore()
            c.response = sms_msg[1]
            c.challenge = phone
            c.save()

            # 测试 可不发短信 去CaptchaStore中查看验证码
            if not settings.DEBUG:
                send_sms([phone], sms_msg[0])

            json_response = {
                'key': c.hashkey,
                'status': 1
            }
            return JsonResponse(json_response)







        else:  # FORM验证出错，并吧出错信息传递到前端
            result = {
                'status': 0,
                'msg': '表单验证失败'
            }
            return JsonResponse(result)

    def _is_phone(self, phone):
        try:
            int(phone)
            return True
        except Exception, e:
            log.error(e)
            return False


class UserLogoutView(View):
    """退出登录"""

    def get(self, request):
        logout(request)
        # return HttpResponseRedirect(reverse('login'))
        return redirect('eshop:eshop_home')


# TODO by liuhuan 2017-3-20 删掉
def user_login(request):
    """用户登录"""
    if request.method == 'POST':
        # 用户密码登录
        if 'passwd' in request.POST and request.POST['passwd']:
            passwd = request.POST.get('passwd')
            username = request.POST.get('name')

            user = authenticate(username=username, password=passwd)
            print user


            # 短信登录

    return render(request, 'eshop/user_login.html', {})


class ForgetPasswordView(View):
    """找回密码操作"""

    @method_decorator(eshop_context)
    def get(self, request):
        """get请求"""
        step = request.GET.get('step', 'account')

        # step_session = request.session.get('forget_password', '')
        if 'account' == step:
            forget_password_session = request.session.get('forget_password', {})
            if forget_password_session and forget_password_session['step']:
                url = '/eshop/forget_password/?step=' + forget_password_session['step']
                return redirect(url)


        elif 'verify' == step:
            # phone = request.session.get('forget_password_verify_phone_username', '')
            forget_password_session = request.session.get('forget_password', '')
            if not forget_password_session:
                return redirect('/eshop/forget_password/')
            return render(request, 'eshop/forget_password.html', {
                'step': step,
                'phone': forget_password_session['phone']
            })

        elif 'new_password' == step:
            # step = request.session.get('forget_password_step', '')
            forget_password_session = request.session.get('forget_password', '')
            if not forget_password_session:
                return redirect('/eshop/forget_password/')
            return render(request, 'eshop/forget_password.html', {
                'step': step
            })


        elif 'complate' == step:
            pass

        return render(request, 'eshop/forget_password.html', {
            'step': step
        })

    def post(self, request):
        """POST处理"""
        step = request.POST.get('step')
        try:
            if request.method == 'POST' and request.is_ajax():
                if 'account' == step:  # 验证用户基本信息
                    if 'captcha' in request.POST:
                        captcha = request.POST.get('captcha')
                        # 校验验证码
                        if captcha.upper() == request.session['CheckCode'].upper():
                            if "phone_username" in request.POST:
                                search_key = request.POST.get('phone_username')
                                user_tmp = User.objects.filter(Q(username=search_key) | Q(phone=search_key)).first()
                                if user_tmp:

                                    request.session['forget_password'] = {'step': 'verify', 'phone': user_tmp.phone}

                                    result = {
                                        'status': 1,
                                        'msg': '验证通过'
                                    }
                                else:
                                    result = {
                                        'status': 0,
                                        'msg': '用户不存在，请核对用户名或者手机'
                                    }
                        else:
                            result = {
                                'status': 2,
                                'msg': '验证码输入有误'
                            }
                    else:
                        raise Exception('用户名或者手机号输入有误')
                elif 'verify' == step:
                    phone = request.POST.get('phone', '')
                    captcha = request.POST.get('phone_yzm', '')
                    forget_password_session = request.session.get('forget_password', '')
                    if not forget_password_session:
                        result = {
                            'status': 0,
                            'msg': u'验证码失败',

                        }
                        return JsonResponse(result)
                    if CaptchaStore.objects.filter(response=str(captcha), challenge=phone):
                        request.session['forget_password'] = {'step': 'new_password', 'phone': phone}
                        result = {
                            'status': 1,
                            'msg': u'验证成功',
                            'url': '/eshop/forget_password/?step=new_password'
                        }
                        return JsonResponse(result)


                elif 'new_password' == step:
                    forget_password_session = request.session.get('forget_password', {})
                    if not forget_password_session:
                        result = {
                            'status': 0,
                            'msg': u'step 错误 请从新填写',
                            'url': '/eshop/forget_password/'
                        }
                        return JsonResponse(result)
                    passwd = request.POST.get('passwd', '')
                    passwd2 = request.POST.get('passwd2', '')
                    if not (passwd or passwd2):
                        result = {
                            'status': 0,
                            'msg': u'请填写密码',
                        }
                        return JsonResponse(result)
                    if passwd != passwd2:
                        result = {
                            'status': 0,
                            'msg': u'两次密码不一致',
                        }
                        return JsonResponse(result)

                    user = User.objects.filter(phone=forget_password_session['phone']).update(password=make_password(passwd))
                    if user:
                        if request.user.get('forget_password_session', ''):
                            del request.session['forget_password']
                        result = {
                            'status': 1,
                            'msg': u'修改成功',
                        }
                        return JsonResponse(result)

                elif 'complate' == step:
                    pass
                elif 'sms_code' == step:
                    # 验证电话号码
                    phone = request.POST.get('phone', '')
                    phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
                    is_phone = phone_re.match(phone)
                    if not is_phone:
                        result = {
                            'status': 0,
                            'msg': u'请输入正确的电话号码'
                        }
                        return JsonResponse(result)

                    is_phone_exist = User.objects.filter(phone=phone)
                    if not is_phone_exist:
                        result = {
                            'status': 0,
                            'msg': u'这个电话没有注册，请先注册!'
                        }
                        return JsonResponse(result)

                    # 避免多次发送短信
                    request.session.set_expiry(60)
                    phone_session = request.session.get('forget_password_verify_phone', '')
                    if phone_session == phone:
                        result = {
                            'status': 0,
                            'msg': u'验证码已发送，请注意查收!'
                        }
                        return JsonResponse(result)

                    request.session['forget_password_verify_phone'] = phone

                    sms_msg = make_sms()
                    c = CaptchaStore()
                    c.response = sms_msg[1]
                    c.challenge = phone
                    c.save()

                    # 测试 可不发短信 去CaptchaStore中查看验证码
                    if not settings.DEBUG:
                        send_sms([phone], sms_msg[0])

                    json_response = {
                        'key': c.hashkey,
                        'status': 1
                    }
                    return JsonResponse(json_response)

                else:
                    raise Exception('请求异常')
            else:
                raise Exception('请求异常')
        except Exception, e:
            log.exception("ForgetPasswordView post raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)


@eshop_context
def forget_password(request):
    return render(request, 'eshop/forget_password.html', {})


class GoodSearchListView(View):
    """商品搜索页面"""

    @method_decorator(eshop_context)
    def get(self, request):
        kwargs = {}
        data = {}

        # TODO by liuhuan 2017-4-1 定期生成 缓存读取
        data['brand'] = Good.objects.values('brand').distinct()
        data['locality'] = Good.objects.values('locality').distinct()
        data['dosage_form'] = DrugAttr.objects.values('dosage_form').distinct()
        # data['category'] = Good.objects.values('category').distinct()
        data['external_category'] = Good.objects.values('external_category').distinct()

        if 'brand' in request.GET:  # 品牌名
            # brand = request.GET.get('brand', '')
            brand = request.GET.getlist('brand', '')
            kwargs['brand__in'] = brand
        if 'locality' in request.GET:  # 产地
            kwargs['locality__contains'] = request.GET.get('locality', '')
        if 'dosage_form' in request.GET:  # 剂型
            kwargs['drugattr__dosage_form__contains'] = request.GET.get('dosage_form', '')
        if 'external_category' in request.GET:  # 类别
            kwargs['external_category__contains'] = request.GET.get('external_category', '')

        # 排序 综合 新品 销量


        # 关键字
        keyword = request.GET.get('keyword', '')

        kwargs['name__contains'] = keyword
        kwargs['trade_name__contains'] = keyword

        # 上架切审核通过的商品才能在搜索结果中
        kwargs['is_online'] = 1
        kwargs['is_qualified'] = 2
        good_set = Good.objects.filter(**kwargs)
        if request.GET.get('external_category'):  # 类别
            category = request.GET['external_category'].strip()
            good_set = good_set.select_related('category').filter(
                Q(external_category__contains=category) | Q(extra_category__contains=category) | Q(
                    category__name__contains=category))
        data['count'] = good_set.count()

        # 分页
        PAGE_LIMIT = 28  # 补全空位
        paginator = Paginator(good_set, PAGE_LIMIT)
        page = request.GET.get('page', 1)
        try:
            good_list = paginator.page(page)
        except PageNotAnInteger:
            good_list = paginator.page(1)
        except EmptyPage:
            good_list = paginator.page(paginator.num_pages)
        except Exception, e:
            log.error('GoodSearchListView %s' % e)

        return render(request, 'eshop/good_search_list.html', {
            'good_list': good_list,
            'paginator': paginator,
            'page': page,
            'data': data,
            'pagi_bar': get_paginator_bar(good_list),
        })

    def post(self, request):
        pass


def good_search_list(request):
    return render(request, 'eshop/good_search_list.html', {})


@eshop_context
def good_detail(request, good_id):
    good = Good.objects.filter(pk=int(good_id)).first()
    photo_list = GoodPhoto.objects.filter(good_id=int(good_id))
    return render(request, 'eshop/good_detail.html', {'good': good, 'photo_list': photo_list})


def good_detail1(request):
    return render(request, 'eshop/good_detail1.html', {})


class ShoppingCartListView(View):
    # todo 用户控制 错误处理
    @method_decorator(eshop_context)
    def get(self, request):

        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

        user = request.user
        # 购物车数量
        shopping_cart_count = request.GET.get('shopping_cart_count', '')
        if shopping_cart_count == 'shopping_cart_count':
            try:
                cart_count = ShoppingCartItem.objects.filter(buyer=user, good__is_online=1).count()
                result = {
                    'status': 1,
                    'cart_count': cart_count
                }
            except Exception, e:
                log.exception('eshop.views.ShoppingCartListView.get error: %s, user: %s' % (e, request.user))
                result = {
                    'status': 0,
                    'data': '',
                }
            return JsonResponse(result)

        shopping_cart_list = ShoppingCartItem.objects.filter(buyer=user)
        return render(request, 'eshop/shopping_cart_list.html', {
            'shopping_data': shopping_cart_list
        })

    def post(self, request):
        try:

            if 'action' in request.POST:
                action = request.POST.get('action', '')

                # 删除商品
                if request.POST.get('action') == 'delete_good':
                    result = self._handle_delete_good(request)

                # 登记缺货
                elif request.POST.get('action') == 'want_book':
                    return self._handle_want_book(request)

                # 移到收藏夹
                elif request.POST.get('action') == 'move_to_favorites':
                    result = self._handle_move_to_favorites(request)

                # 移除失效商品
                elif request.POST.get('action') == 'remove_failed_goods':
                    result = self._handle_remove_failed_goods(request)

                # 更新商品数量
                elif 'good_count' == action:
                    return self._handle_good_count(request)

                else:
                    result = {
                        'status': 0,
                        'msg': '请求错误'
                    }
                    return JsonResponse(result)

            else:
                result = {
                    'status': 0,
                    'msg': '请求错误'
                }

            return JsonResponse(result)
        except Exception, e:
            log.error('ShoppingCartLlist post %s' % e)
            print str(e)
            result = {
                'status': 0,
                'msg': '内部错误'
            }

            return JsonResponse(result)

    def _handle_delete_good(self, request):
        """购物车 删除商品 可以批量删除"""
        list_pk = json.loads(request.POST.get('pk', '[]'))
        ShoppingCartItem.objects.filter(pk__in=list_pk, buyer=request.user).delete()

        result = {
            'status': 1,
            'msg': '删除成功!'
        }
        return result

    def _handle_want_book(self, request):
        # todo 缺货登记
        """购物车 缺货登记 可以批量删除"""
        list_pk = request.POST.get('pk', '')

        ShoppingCartItem.objects.filter(pk__in=list_pk).delete()

        result = {
            'status': 1,
            'msg': '缺货登记成功'
        }
        return result

    def _handle_move_to_favorites(self, request):
        """购物车 移到收藏夹 可以批量移到"""
        list_pk = json.loads(request.POST.get('pk', '[]'))
        user_id = request.user.id
        ShoppingCartItem.objects.filter(good_id__in=list_pk, buyer=request.user).delete()
        kwargs = {}
        kwargs['coll_user_id'] = user_id
        for good in list_pk:
            kwargs['coll_good_id'] = good
            MyFavorites.objects.update_or_create(**kwargs)
        result = {
            'status': 1,
            'msg': '收藏成功'
        }
        return result

    def _handle_remove_failed_goods(self, request):
        """购物车 移除失效商品"""
        list_pk = json.loads(request.POST.get('pk', '[]'))
        ShoppingCartItem.objects.filter(pk__in=list_pk).delete()

        result = {
            'status': 1,
            'msg': '移除成功'
        }
        return result

    def _handle_good_count(self, request):
        """购物车 更新商品数量"""
        cart_item_id = int(request.POST.get('id', ''))
        good_count = int(request.POST.get('good_count', 1))

        is_cart_item = ShoppingCartItem.objects.filter(pk=cart_item_id).first()
        if is_cart_item:
            good = Good.objects.filter(pk=is_cart_item.good.id, stock_amount__gte=good_count).first()
            if not good:
                is_cart_item.quantity
                result = {
                    'status': 0,
                    'msg': '超过库存',
                    'good_count': is_cart_item.quantity
                }
                return JsonResponse(result)
        is_cart_item_update = ShoppingCartItem.objects.filter(pk=cart_item_id).update(
            quantity=good_count,
            id=cart_item_id,
            buyer=request.user
        )
        if is_cart_item_update:
            result = {
                'status': 1,
                'msg': '更新数量成功'
            }
            return JsonResponse(result)
        else:
            result = {
                'status': 0,
                'msg': '更新数量失败'
            }
            return JsonResponse(result)


class ShoppingBalanceView(View):
    """结算页面"""

    @method_decorator(eshop_context)
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

        # 订单类型
        order_type = request.GET.get('order_type', '')

        # 购物车提交
        if 'cart' == order_type:
            cart_id_list = request.session.get('cart_id_list', '')
            if cart_id_list:
                # 拿到当前用户的购物车商品
                is_shopping_cart_list = ShoppingCartItem.objects.filter(id__in=cart_id_list, buyer=request.user)
                if not is_shopping_cart_list:
                    return redirect('eshop:shopping_cart_list')

                # 收货地址
                address_list = ReceivingAddress.objects.filter(user=request.user)
                # 支付方式
                pay_type = [i[0] for i in PAY_TYPE_CHOICES]
                payment_method = PaymentMethod.objects.filter(pay_type__in=pay_type, is_active=True).order_by(
                    'order_no')
                # 配送方式 todo liu 2017-5-8 待优化
                shipping_type = [i[0] for i in SHIPPING_TYPE_CHOICES]
                shipping_method = ShippingMethod.objects.filter(shipping_type__in=shipping_type,
                                                                is_active=True).order_by('order_no')
                return render(request, 'eshop/shopping_balance.html', {
                    'shopping_data': is_shopping_cart_list,
                    'address_list': address_list,
                    'order_type': order_type,
                    'payment_method': payment_method,
                    'shipping_method': shipping_method
                })


        # 快速下单
        elif 'quickly' == order_type:
            quickly_order_id_list = request.session.get('quickly_order_id_list', '')
            if quickly_order_id_list:
                is_quickly_list = QuicklyOrder.objects.filter(pk__in=quickly_order_id_list, user=request.user)
                if not is_quickly_list:
                    return redirect('eshop:shopping_cart_list')

                # 收货地址
                address_list = ReceivingAddress.objects.filter(user=request.user)
                # 支付方式
                pay_type = [i[0] for i in PAY_TYPE_CHOICES]
                payment_method = PaymentMethod.objects.filter(pay_type__in=pay_type, is_active=True).order_by(
                    'order_no')
                # 配送方式 todo liu 2017-5-8 待优化
                shipping_method = [i[0] for i in SHIPPING_TYPE_CHOICES]
                shipping_method = ShippingMethod.objects.filter(shipping_type__in=shipping_method,
                                                                is_active=True).order_by('order_no')
                return render(request, 'eshop/shopping_balance.html', {
                    'shopping_data': is_quickly_list,
                    'address_list': address_list,
                    'order_type': order_type,
                    'payment_method': payment_method,
                    'shipping_method': shipping_method
                })
        else:
            # return redirect('eshop:shopping_cart_list')
            return redirect('/eshop/shopping_cart_list/?order_type=cart')

    def post(self, request):
        try:
            if 'method' in request.POST:
                method = request.POST.get('method', '')
                # 根据商品id和数量
                if 'add_order' == method:
                    return self._handle_add_order(request)
                # 快速下单
                # elif 'quickly_order' == method:
                #    return self._handle_quickly_order(request)
                # 配送信息处理
                elif 'receiving_address' == method:
                    return self._handle_receiving_address(request)
                else:
                    result = {
                        'status': 0,
                        'msg': '请求错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': '请求错误'
                }
            return JsonResponse(result)
        except Exception, e:
            log.error('ShoppingCartLlist post %s' % e)

            result = {
                'status': 0,
                'msg': '内部错误'
            }
            return JsonResponse(result)

    def _handle_add_order(self, request):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action', '')
                # 购物车提交
                if 'cart_add' == action:
                    cart_id_list = json.loads(request.POST.get('pk', '[]'))
                    request.session['cart_id_list'] = cart_id_list
                    result = {
                        'status': 2,
                        'msg': '添加成功跳转结算页面',
                        'url': '/eshop/shopping_balance/?order_type=cart'
                    }
                # 快速下单
                elif 'quickly_add' == action:
                    quickly_order_ids = json.loads(request.POST.get('quickly_order_ids', '[]'))
                    request.session['quickly_order_id_list'] = quickly_order_ids
                    is_quickly_order = QuicklyOrder.objects.filter(pk__in=quickly_order_ids, user=request.user)
                    result = {
                        'status': 2,
                        'msg': '成功跳转结算页面',
                        'url': '/eshop/shopping_balance/?order_type=quickly'
                    }
                else:
                    result = {
                        'status': 0,
                        'msg': 'action错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': 'action错误'
                }
            return JsonResponse(result)
        except Exception, e:
            log.error('ShoppingBalanceView _handle_add_order %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e

            }
            return JsonResponse(result)

    def _handle_receiving_address(self, request):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action', '')

                # 保存添加新的收货地址
                if 'address_add' == action:
                    # form = ReceivingAddressForm(request.POST)

                    # 如果是第一条地址就是设为默认地址
                    is_address_exist = ReceivingAddress.objects.filter(user=request.user, is_default=True)
                    # todo 2017-4-28 liu 待优化
                    if is_address_exist:
                        is_address_create = ReceivingAddress.objects.create(
                            user=request.user,
                            people=request.POST.get('people', ''),
                            region=request.POST.get('region', ''),
                            address=request.POST.get('address', ''),
                            telephone=request.POST.get('telephone', ''),
                            email=request.POST.get('email', ''),
                            is_default=False
                        )
                    else:
                        is_address_create = ReceivingAddress.objects.create(
                            user=request.user,
                            people=request.POST.get('people', ''),
                            region=request.POST.get('region', ''),
                            address=request.POST.get('address', ''),
                            telephone=request.POST.get('telephone', ''),
                            email=request.POST.get('email', ''),
                            is_default=True
                        )

                    if is_address_create:
                        result = {
                            'status': 1,
                            'msg': '添加成功',
                        }
                    else:
                        result = {
                            'status': 0,
                            'msg': '添加失败',
                        }

                # 修改地址 用于获取地址渲染数据
                elif 'get_address' == action:
                    pk = int(request.POST.get('pk', ''))
                    address = ReceivingAddress.objects.filter(pk=pk, user=request.user).first()
                    return render(request, 'eshop/modals/modal_shopping_balance_receiving_address.html', {
                        "obj": address
                    })

                # 修改保存
                elif 'save_address' == action:
                    pk = int(request.POST.get('id', ''))
                    is_address_save = ReceivingAddress.objects.filter(pk=pk, user=request.user).update(
                        people=request.POST.get('people', ''),
                        region=request.POST.get('region', ''),
                        address=request.POST.get('address', ''),
                        telephone=request.POST.get('telephone', ''),
                        email=request.POST.get('email', ''),
                    )
                    if is_address_save:
                        result = {
                            'status': 1,
                            'msg': '修改成功',
                        }
                    else:
                        result = {
                            'status': 0,
                            'msg': '修改失败',
                        }

                # 删除地址
                elif 'address_delete' == action:
                    pk = int(request.POST.get('pk', ''))
                    flag = False
                    addr = ReceivingAddress.objects.filter(pk=pk, user=request.user).first()
                    if addr and addr.is_default:
                        flag = True
                    is_delete = ReceivingAddress.objects.filter(pk=pk, user=request.user).delete()
                    if is_delete:
                        if flag:
                            new_default = ReceivingAddress.objects.filter(user=request.user).first()
                            ReceivingAddress.objects.filter(pk=new_default.id).update(is_default=True)
                        result = {
                            'status': 1,
                            'msg': '删除成功',
                        }
                    else:
                        result = {
                            'status': 0,
                            'msg': '删除失败',
                        }

                # 设为默认地址
                elif 'address_default' == action:
                    pk = int(request.POST.get('pk', ''))
                    try:
                        with transaction.atomic():
                            ReceivingAddress.objects.filter(user=request.user).update(is_default=False)
                            ReceivingAddress.objects.filter(pk=pk, user=request.user).update(is_default=True)

                            result = {
                                'status': 1,
                                'msg': '修改成功'
                            }


                    except Exception, e:
                        result = {
                            'status': 0,
                            'msg': '修改失败'
                        }

                else:
                    result = {
                        'status': 0,
                        'msg': 'action错误'
                    }

            else:
                result = {
                    'status': 0,
                    'msg': 'action错误'
                }
            return JsonResponse(result)

        except Exception, e:
            log.error('ShoppingBalanceView _handle_add_order %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e

            }
            return JsonResponse(result)


@eshop_context
def shopping_balance(request):
    """根据订单编号来生成订单"""

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

    print request.GET.get('rid')

    return render(request, 'eshop/shopping_balance.html', {})


class SubmitOrderView(View):
    @method_decorator(eshop_context)
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

        # 必须传入订单编号 根据订单编号渲染页面
        if 'oid' in request.GET:
            oid = request.GET.get('oid', '')
            pay_method = PaymentMethod.objects.filter(is_active=True, pay_type=0)
            is_order = Order.objects.filter(order_no=oid, buyer=request.user, pay_status=0).first()
            if not is_order:
                # raise Http404("order does not exist")
                # return HttpResponseNotFound('<h1>不要搞事情</h1>')
                return redirect('eshop:shopping_cart_list')

            return render(request, 'eshop/submit_order.html', {
                'order': is_order,
                'pay_method': pay_method,

            })

        else:
            return redirect('eshop:shopping_balance')

    def post(self, request):
        try:
            if 'method' in request.POST:
                method = request.POST.get('method', '')
                # 生成订单
                if 'create_order' == method:
                    return self._handle_create_order(request)
                # 预存款支付
                if 'pre_pay' == method:
                    return self._handle_pre_pay(request)
                else:
                    result = {
                        'status': 0,
                        'msg': '请求错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': '请求错误'
                }
            return JsonResponse(result)
        except Exception, e:
            log.error('ShoppingCartLlist post %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误'
            }
            return JsonResponse(result)

    def _handle_create_order(self, request):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action', '')
                # 购物车订单
                if 'cart' == action:
                    id_cart_id_list = request.session.get('cart_id_list', '')
                    # 生成订单
                    if id_cart_id_list:
                        is_shopping_cart_list = ShoppingCartItem.objects.filter(pk__in=id_cart_id_list,
                                                                                buyer=request.user)
                        if not is_shopping_cart_list:
                            # raise Http404("order does not exist")
                            # return HttpResponseNotFound('<h1>不要搞事情</h1>')
                            result = {
                                'status': 0,
                                'msg': '请求错误 没有商品',
                            }
                            return JsonResponse(result)

                    # 收货地址
                    receiving_address = request.POST.get('receiving_address', '')
                    # 配送方式
                    shipping_method = request.POST.get('shipping_method', '')
                    # 支付方式
                    payment_method = request.POST.get('payment_method', '')
                    # 买家留言
                    note = request.POST.get('note', '')
                    # 生成订单 删掉购物车中的商品
                    try:
                        with transaction.atomic():
                            # 总价
                            total_price = 0
                            for cart in is_shopping_cart_list:
                                total_price += cart.quantity * cart.good.member_price

                            order_no = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(request.user.id).zfill(6)
                            # 创建流程
                            proc = Process.objects.create_process(BPMN_DELIVERY)
                            order_kwargs = {}
                            order_kwargs['order_no'] = order_no
                            order_kwargs['buyer'] = request.user
                            order_kwargs['receiving_address_id'] = receiving_address
                            order_kwargs['shipping_method_id'] = shipping_method
                            order_kwargs['payment_method_id'] = payment_method
                            order_kwargs['total_price'] = total_price
                            order_kwargs['real_price'] = total_price
                            order_kwargs['proc_delivery'] = proc
                            order_kwargs['reviewer'] = request.user
                            order_kwargs['note'] = note
                            # 创建订单
                            is_order_save = Order.objects.create(**order_kwargs)
                            # 发票
                            # invoice_kwargs = {}
                            company_name = request.POST.get('company_name', '')
                            taxpayer_no = request.POST.get('taxpayer_no', '')
                            address_phone = request.POST.get('address_phone', '')
                            bank_account = request.POST.get('bank_account', '')
                            # invoice_kwargs['order_id'] = is_order_save.id
                            # invoice_kwargs['company_name'] = company_name
                            # invoice_kwargs['taxpayer_no'] = taxpayer_no
                            # invoice_kwargs['address_phone'] = address_phone
                            # invoice_kwargs['bank_account'] = bank_account
                            # Invoice.objects.create(**invoice_kwargs)
                            invoice = Invoice()
                            invoice.order_id = is_order_save.id
                            invoice.taxpayer_no = taxpayer_no
                            invoice.address_phone = address_phone
                            invoice.bank_account = bank_account
                            invoice.company_name = company_name
                            invoice.save()
                            # 启动流程
                            # res, msg = proc.start()
                            proc.start()
                            # if not 1:
                            #     raise Exception("订单生成失败")
                            # 记录日志
                            task = is_order_save.proc_delivery.get_task_obj('init_order')
                            note_msg = u'订单生成成功'
                            OperateRecord.objects.create(
                                operate=task.name,
                                operate_cn=task.name_cn,
                                process=is_order_save.proc_delivery,
                                operator=request.user,
                                note=note_msg,
                                data_type=ORDER_MODAL,
                                data_id=is_order_save.id,
                            )
                            # 生成订单项
                            for shopping_cart in is_shopping_cart_list:
                                is_order_item = OrderItem.objects.create(
                                    order=is_order_save,
                                    good_id=shopping_cart.good.id,
                                    price=shopping_cart.good.member_price,
                                    real_price=0,
                                    quantity=shopping_cart.quantity,
                                )
                            # 删除购物车清单中的数据
                            ShoppingCartItem.objects.filter(pk__in=id_cart_id_list).delete()
                            result = {
                                'status': 2,
                                'msg': '添加成功跳转结算页面',
                                'url': '/eshop/submit_order/?oid=' + is_order_save.order_no
                            }
                            return JsonResponse(result)


                    except Exception, e:
                        log.error('订单生成失败 %s' % e)
                        result = {
                            'status': 0,
                            'msg': '订单生成失败'
                        }
                        return JsonResponse(result)


                # 快速下单
                elif 'quickly' == action:
                    quickly_order_id_list = request.session.get('quickly_order_id_list', '')
                    # 生成订单
                    if quickly_order_id_list:
                        is_quickly_list = QuicklyOrder.objects.filter(pk__in=quickly_order_id_list, user=request.user)
                        if not is_quickly_list:
                            result = {
                                'status': 0,
                                'msg': '请求错误 快速下单中 没有商品',
                            }
                            return JsonResponse(result)
                    # 收货地址
                    receiving_address = request.POST.get('receiving_address', '')
                    # 配送方式
                    shipping_method = request.POST.get('shipping_method', '')
                    # 支付方式
                    payment_method = request.POST.get('payment_method', '')
                    # 买家留言
                    note = request.POST.get('note', '')
                    # 生成订单 删掉购物车中的商品
                    try:
                        with transaction.atomic():
                            # 总价
                            total_price = 0
                            for cart in is_quickly_list:
                                total_price += cart.quantity * cart.good.member_price

                            # 预存款支付 查看余额
                            if int(payment_method) == 2:
                                is_user = request.user
                                if is_user.balance > total_price:
                                    is_user.balance -= total_price
                                    is_user.save()
                                # todo 跳页面 输密码
                                else:
                                    result = {
                                        'status': 0,
                                        'msg': '余额不足! 请充值 或者使用其他支付方式'
                                    }
                                    return JsonResponse(result)

                            order_no = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(request.user.id)

                            # 流程
                            process = Process.objects.create(
                                proc_type='asdf',
                                proc_conf='fasdf',
                                state_json='asdfa'
                            )
                            order_kwargs = {}
                            order_kwargs['order_no'] = order_no
                            order_kwargs['buyer'] = request.user
                            order_kwargs['receiving_address_id'] = receiving_address
                            order_kwargs['shipping_method_id'] = shipping_method
                            order_kwargs['payment_method_id'] = payment_method
                            order_kwargs['total_price'] = total_price
                            order_kwargs['proc_delivery'] = process
                            order_kwargs['reviewer'] = request.user
                            order_kwargs['note'] = note
                            # 实付价格总计
                            order_kwargs['real_price'] = 0
                            is_order_save = Order.objects.create(**order_kwargs)

                            for shopping_cart in is_quickly_list:
                                is_order_item = OrderItem.objects.create(
                                    order=is_order_save,
                                    good_id=shopping_cart.good.id,
                                    price=shopping_cart.good.member_price,
                                    real_price=0,
                                    quantity=shopping_cart.quantity,
                                )

                            # 删除快速下单中的数据
                            QuicklyOrder.objects.filter(pk__in=is_quickly_list).delete()

                            result = {
                                'status': 2,
                                'msg': '添加成功跳转结算页面',
                                'url': '/eshop/submit_order/?oid=' + is_order_save.order_no
                            }

                            return JsonResponse(result)


                    except Exception, e:
                        log.error('订单生成失败 %s' % e)
                        result = {
                            'status': 0,
                            'msg': '订单生成失败'
                        }
                        return JsonResponse(result)
                else:
                    result = {
                        'status': 0,
                        'msg': 'action错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': 'action错误'
                }
            return JsonResponse(result)
        except Exception, e:
            log.error('SubmitOrderView _handle_create_order %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e

            }
            return JsonResponse(result)

    def _handle_pre_pay(self, request):
        if not request.user.pay_password:
            result = {
                'status': 1,
                'msg': '您还没有设置支付密码，请先设置支付密码！',
                'url': reverse('eshop:account_safety')
            }
            return JsonResponse(result)
        # 预存款支付 查看余额
        # order = int(request.POST.get('oid', ''))
        order_pk = int(request.POST.get('opk', ''))
        is_order = Order.objects.filter(pk=order_pk)
        if not is_order.first():
            result = {
                'status': 0,
                'msg': '没有这个订单'
            }
            return JsonResponse(result)
        is_user = request.user
        # 验证密码
        pay_passwd = request.POST.get('pay_passwd', '')
        if check_password(pay_passwd, is_user.pay_password):
            # 密码正确 检查余额
            if is_user.balance > is_order.first().total_price:
                # 订单修改为已付款
                task = is_order.first().proc_delivery.get_task_obj('mark_order_paid')
                res, msg = task.transit()
                if not res:
                    result = {
                        'status': 0,
                        'msg': '系统忙,请稍后再试'
                    }
                    return JsonResponse(result)
                # 修改价格
                is_user.balance -= is_order.first().total_price
                is_user.save()
                # 修改订单实付金额
                is_order.real_price = is_order.first().total_price
                # 修改订单项实付金额
                OrderItem.objects.filter(order_id=is_order.id).update(real_price=F('price') * F('quantity'))

                # 添加操作日志
                OperateRecord.objects.create(
                    operate=task.name,
                    operate_cn=task.name_cn,
                    process=is_order.first().proc_delivery,
                    operator=request.user,
                    note='付款成功',
                    data_type=ORDER_MODAL,
                    data_id=is_order.first().id,
                )
                result = {
                    'status': 1,
                    'msg': '支付成功！',
                    'url': '/eshop/my_order/'
                }
                return JsonResponse(result)
            else:
                result = {
                    'status': 0,
                    'msg': '余额不足! 请充值 或者使用其他支付方式'
                }
                return JsonResponse(result)
        else:
            result = {
                'status': 0,
                'msg': '支付密码错误！'
            }
            return JsonResponse(result)


def submit_order(request):
    return render(request, 'eshop/submit_order.html', {})


class MemberCenterView(View):
    """用户后台首页"""

    @method_decorator(eshop_context)
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

        data = {}
        # 待支付
        dzf = Order.objects.filter(buyer__username=request.user).filter(trade_state__contains=0).count()
        data['dzf'] = dzf
        # 待发货
        dfh = Order.objects.filter(buyer__username=request.user).filter(trade_state__in=[1, 2]).count()
        data['dfh'] = dfh
        # 待收货
        dsh = Order.objects.filter(buyer__username=request.user).filter(trade_state__in=[3]).count()
        data['dsh'] = dsh
        # 待退款
        dtk = Order.objects.filter(buyer__username=request.user).filter(trade_state__in=[5]).count()
        data['dtk'] = dtk

        # 我的订单
        order_list = Order.objects.filter(buyer__username=request.user).order_by('-ord_time')[:5]

        # 我的收藏
        user_coll_set = MyFavorites.objects.filter(coll_user__username=request.user.username).order_by('-created')
        data['collection'] = user_coll_set[:10]

        return render(request, 'eshop/member_center.html', {
            'order_list': order_list,
            'data': data,
        })

    def post(self, request):
        pass


def member_center(request):
    return render(request, 'eshop/member_center.html', {})


class MyOrderView(View):
    """全部订单"""

    @method_decorator(eshop_context)
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)
        # 头部我的订单 get
        order_state = request.GET.get('order_state', '')
        if order_state == 'order_state':
            try:
                temp_list = Order.objects.filter(buyer__username=request.user).filter(
                    trade_state__in=[ORDER_NOT_PAID, ORDER_IS_PICKING, ORDER_IS_SHIPPING]).values_list('trade_state',
                                                                                                       flat=True)
                data = {
                    'not_paid': 0,
                    'is_picking': 0,
                    'is_shipping': 0,
                }
                for order_state in temp_list:
                    if order_state == ORDER_NOT_PAID:
                        data['not_paid'] += 1
                    elif order_state == ORDER_IS_PICKING:
                        data['is_picking'] += 1
                    elif order_state == ORDER_IS_SHIPPING:
                        data['is_shipping'] += 1
                result = {
                    'status': 1,
                    'data': data,
                }
            except Exception, e:
                log.exception('eshop.views.MyOrderView.get error: %s, user: %s' % (e, request.user))
                result = {
                    'status': 0,
                    'data': '',
                }
            return JsonResponse(result)

        kwargs = {}
        countargs = {}
        # 订单分类
        if 'state' in request.GET:  # 待付款 待付款 待发货 待退款 已关闭
            kwargs['trade_state__contains'] = int(request.GET.get('state', ''))
        # 近期订单
        if 'date' in request.GET:  # 近期 一个月 两个月 三个月
            day = request.GET.get('date', '30')
            now = datetime.date.today() + datetime.timedelta(1)
            past = now - datetime.timedelta(days=int(day))
            kwargs['ord_time__range'] = (past, now)
            countargs['ord_time__range'] = (past, now)
        # 查询订单编号
        if 'order_no' in request.GET:
            kwargs['order_no__contains'] = request.GET.get('order_no', '')
            countargs['order_no__contains'] = request.GET.get('order_no', '')
        if request.GET.get('trade_state'):
            kwargs['trade_state'] = request.GET['trade_state']
        data = {}
        # 待支付
        not_paid = Order.objects.filter(buyer__username=request.user).filter(**countargs).filter(
            trade_state__contains=ORDER_NOT_PAID).count()
        data['not_paid'] = not_paid
        # 待发货
        is_picking = Order.objects.filter(buyer__username=request.user).filter(**countargs).filter(
            trade_state__contains=ORDER_IS_PICKING).count()
        data['is_picking'] = is_picking
        # 待收货(已发货)
        is_ship = Order.objects.filter(buyer__username=request.user).filter(**countargs).filter(
            trade_state__contains=ORDER_IS_SHIPPING).count()
        data['is_ship'] = is_ship
        # 退款中
        is_refund = Order.objects.filter(buyer__username=request.user).filter(**countargs).filter(
            trade_state__contains=ORDER_IS_REFUNDING).count()
        data['is_refund'] = is_refund
        # 已关闭
        ord_closed = Order.objects.filter(buyer__username=request.user).filter(**countargs).filter(
            trade_state__contains=ORDER_CLOSED).count()
        data['ord_closed'] = ord_closed
        # 查询数据
        data_set = Order.objects.filter(buyer__username=request.user).filter(**kwargs).order_by('-ord_time')
        # 分页
        paginator = Paginator(data_set, PAGE_LIMIT)
        page = request.GET.get('page', 1)
        try:
            order_list = paginator.page(page)
        except PageNotAnInteger:
            order_list = paginator.page(1)
        except EmptyPage:
            order_list = paginator.page(paginator.num_pages)
        for order in order_list:
            order.order_item_set = order.orderitem_set.all()
            order.good_total_price = 0
            order.total_preferential_price = 0
            order.good_real_total_price = 0
            for item in order.order_item_set:
                item.preferential_price = item.price - item.real_price
                item.subtotal = item.quantity * item.price
                item.real_subtotal = item.quantity * item.real_price
                order.good_total_price += item.subtotal
                order.good_real_total_price += item.real_subtotal
                order.total_preferential_price += item.preferential_price * item.quantity
        choices = Order._meta._forward_fields_map['trade_state'].choices
        return render(request, 'eshop/my_order.html', {
            'order_list': order_list,
            'paginator': paginator,
            'page': page,
            'data': data,
            'pagi_bar': get_paginator_bar(order_list),
            'choices': choices
        })

    def post(self, request):
        """我的订单列表POST处理"""
        try:
            if request.method == 'POST' and request.is_ajax():
                op_type = request.POST.get("op_type")
                # 取消订单
                if op_type == "cal_ord":
                    result = MyOrderView._handle_cancel_order(request)
                # 确认收货
                elif op_type == "conf_rec":
                    result = MyOrderView._handle_confirm_receipt(request)
                # 导航条 我的订单数量
                elif op_type == '':
                    pass

            else:
                raise Exception("请求异常")
        except Exception, e:
            log.exception("MyOrderView  raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)

    @staticmethod
    def _handle_cancel_order(request):
        """取消订单"""
        obj_id = request.POST.get("obj_id")
        ord_item = Order.objects.filter(pk=obj_id).first()
        with transaction.atomic():
            if ord_item.trade_state == 0:
                # 获取取消订单任务[即关闭订单]
                task = ord_item.proc_delivery.get_task_obj("close_order")
                res, msg = task.transit()
                if res:
                    note_msg = "取消订单，结果:%s" % msg.encode('utf-8')
                    result = {
                        'status': 1,
                        'msg': msg.encode('utf-8')
                    }
                else:
                    note_msg = "取消订单失败，原因:%s" % msg.encode('utf-8')
                    result = {
                        'status': 0,
                        'msg': msg.encode('utf-8')
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
            else:
                result = {
                    'status': 0,
                    'msg': '网络异常请刷新后再试！'
                }
        return result

    @staticmethod
    def _handle_confirm_receipt(request):
        """确认收货"""
        obj_id = request.POST.get("obj_id")
        ord_item = Order.objects.filter(pk=obj_id).first()
        with transaction.atomic():
            if ord_item:
                # 获取确认收货任务
                task = ord_item.proc_delivery.get_task_obj("mark_order_received")
                res, msg = task.transit()
                if res:
                    note_msg = "买家确认收货，结果:%s" % msg.encode('utf-8')
                    result = {
                        'status': 1,
                        'msg': msg.encode('utf-8')
                    }
                else:
                    note_msg = "买家确认收货失败，原因:%s" % msg.encode('utf-8')
                    result = {
                        'status': 0,
                        'msg': msg.encode('utf-8')
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
        return result


def my_order(request):
    # todo remove
    return render(request, 'eshop/my_order.html', {})


class RefundsAndReturnView(View):
    """退款退货处理视图"""

    @method_decorator(eshop_context)
    def get(self, request):
        """处理GET请求 加载所有发布信息数据"""
        id = request.GET.get('id')
        order = Order.objects.filter(pk=id).first()
        refund_type = ''
        refund_status = ''
        refund_return = ''
        op_logs = ''
        refund_record = RefundRecord.objects.filter(order_id=id).first()
        if refund_record:
            refund_type = refund_record.refund_type
            refund_status = refund_record.refund_status
            refund_return = refund_record
            kwargs = {}
            kwargs['data_type'] = REFUND_MODAL
            kwargs['data_id'] = refund_record.id
            op_logs = OperateRecord.objects.filter(**kwargs).order_by("-created")
        order_item_set = order.orderitem_set.all()
        for item in order_item_set:
            item.preferential_price = item.real_price - item.price
            item.subtotal = item.quantity * item.price
            item.real_subtotal = item.quantity * item.real_price
        result = {
            'order': order,
            'order_item_set': order_item_set,
            'refund_type': refund_type,
            'refund_status': refund_status,
            'refund_return': refund_return,
            'op_logs': op_logs
        }
        return render(request, 'eshop/changing_or_refunding.html', result)

    def post(self, request):
        """post请求处理"""
        op_type = request.POST.get('op_type')
        try:
            if request.method == 'POST':
                if request.is_ajax():
                    op_type = request.POST.get('op_type')
                    if op_type == 'apl':  # 买家提起退款退货申请
                        result = RefundsAndReturnView._apply_return_refund(request)
                    elif op_type == 'der':  # 买家确认发货
                        result = RefundsAndReturnView._deliver_return_refund(request)
                    elif op_type == 'cel':  # 取消申请
                        result = RefundsAndReturnView._cancel_return_refund(request)
                else:
                    result = RefundsAndReturnView._handle_refund_search(request)
                    return render(request, 'dtsadmin/returns_and_refunds.html', result)

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
    def _apply_return_refund(request):
        """前台：买家发起申请"""
        try:
            id = request.POST.get('id')
            kwargs = {}
            # 1.订单第一次申请退款退货：就创建一个PROC ,然后创建REFUND ,并且关联PROC
            # 2.修改退款退货，就是更新退款退货数据
            # 3.订单重新申请：{
            #     1.创建新的流程，Proc
            #     2.将已有的退款退货记录status更新为初始状态
            #     3.将新的proc关联到已有的退款退货 refund.proc = Proc/refund.save()
            # }
            refund_record = RefundRecord.objects.filter(order_id=id).first()

            if refund_record:  # 订单已经存在退款退货记录
                refund = (0,)  # 定义元组，统一
                if 'money' in request.POST:
                    refund = round(float(request.POST.get('money')) * 100, 2),  # 买家填写
                kwargs["refund"] = refund[0]
                kwargs["refund_desc"] = request.POST.get('reasons')
                kwargs["refund_type"] = request.POST.get('refund_type')
                # 已经关闭了的退款退货（重新申请）
                if refund_record.refund_status == 5:
                    ref_proc = Process.objects.create_process(BPMN_REFUND)
                    refund_record.proc_refund = ref_proc
                    # refund_record.order.trade_state = ORDER_IS_REFUNDING
                    refund_record.refund = kwargs["refund"]
                    refund_record.refund_desc = kwargs["refund_desc"]
                    refund_record.refund_type = kwargs["refund_type"]
                    refund_record.refund_status = REFUND_HANDLING
                    refund_record.consult = None
                    refund_record.reviewer = None
                    refund_record.save()
                    res, msg = ref_proc.start()
                    if not res:
                        raise Exception(msg.encode('utf-8'))
                else:
                    if refund_record.refund_status == 0:
                        RefundRecord.objects.filter(order_id=id).update(**kwargs)
                    else:
                        result = {
                            'status': 0,
                            'msg': '网络异常，请刷新后重试！',
                        }
                        return JsonResponse(result)
                result = {
                    'status': 1,
                    'msg': '成功',
                }
            else:
                with transaction.atomic():
                    ref_proc = Process.objects.create_process(BPMN_REFUND)
                    user = request.user
                    refund = (0,)  # 定义元组
                    if 'money' in request.POST:
                        refund = round(float(request.POST.get('money')) * 100, 2),  # 买家填写
                    RefundRecord.objects.create(
                        order_id=id,  # 订单，Id
                        refund=refund[0],
                        applicant=user,  # 当前登录人
                        refund_type=request.POST.get('refund_type'),  #
                        proc_refund=ref_proc,
                        refund_desc=request.POST.get('reasons', ''),  # 买家填写的退款说明
                    )
                    res, msg = ref_proc.start()
                    if not res:
                        raise Exception(msg.encode('utf-8'))
                    result = {
                        'status': 1,
                        'msg': '成功',
                    }
            # 添加操作日志
            obj = RefundRecord.objects.filter(order_id=id).first()
            if request.POST.get('refund_type') == '0':
                note = "用户申请退款，退款金额：%s元" % str(request.POST.get('money'))
            else:
                note = "用户申请退货,退款金额：%s元" % str(request.POST.get('money'))
            task = obj.proc_refund.get_task_obj("init_refund")
            OperateRecord.objects.create(
                operate=task.name,
                operate_cn=task.name_cn,
                process=obj.proc_refund,
                operator=request.user,
                note=note,
                data_type=REFUND_MODAL,
                data_id=obj.id,
            )
        except Exception, e:
            log.exception("_pass_return_refund raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e),
            }
        return result

    @staticmethod
    def _deliver_return_refund(request):
        """前台：买家确认发货"""
        try:
            with transaction.atomic():
                id = request.POST.get('id')
                refund_record = RefundRecord.objects.filter(order_id=id).first()
                refund_record.waybill_no = request.POST.get('waybill_no')
                refund_record.shipping_method = request.POST.get('shipping_method')
                refund_record.save()
                task = refund_record.proc_refund.get_task_obj('mark_refund_receiving')
                task.transit()
                result = {
                    'status': 1,
                    'msg': '成功',
                }
            # 添加操作日志
            OperateRecord.objects.create(
                operate=task.name,
                operate_cn=task.name_cn,
                process=refund_record.proc_refund,
                operator=request.user,
                note="买家已发货",
                data_type=REFUND_MODAL,
                data_id=refund_record.id,
            )
        except Exception, e:
            log.error("_pass_return_refund raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e),
            }
        return result

    @staticmethod
    def _cancel_return_refund(request):
        """前台：买家取消申请"""
        try:
            id = request.POST.get('id')
            obj = RefundRecord.objects.filter(order_id=id).first()
            if obj.refund_status == 0:
                if 'init_refund' in obj.proc_refund.reversible_task_list:
                    task = obj.proc_refund.get_task_obj('init_refund')
                    res, msg = task.reverse()
                    obj.refund_status = REFUND_CLOSED
                    obj.save()
                if not res:
                    result = {
                        'status': 0,
                        # 'msg': '系统忙,请稍后再试'
                        'msg': msg
                    }
                    return JsonResponse(result)
                # 添加操作日志
                OperateRecord.objects.create(
                    operate=task.name,
                    operate_cn=task.name_cn,
                    process=obj.proc_refund,
                    operator=request.user,
                    note="买家取消申请",
                    data_type=REFUND_MODAL,
                    data_id=obj.id,
                )
                result = {
                    'status': 1,
                    'msg': '成功',
                }
            else:
                result = {
                    'status': 0,
                    'msg': '网络异常，请刷新后重试！',
                }
        except Exception, e:
            log.error("_pass_return_refund raise,Error:%s" % e)
            result = {
                'status': 0,
                'msg': str(e),
            }
        return result


def changing_or_refunding(request):
    return render(request, 'eshop/changing_or_refunding.html', {})


@eshop_context
def my_collect(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

    kwargs = {}
    data = {}
    data['all_count'] = MyFavorites.objects.filter(coll_user=request.user).count()
    state = request.GET.get('state', '0')
    # 搜索商品
    good_name = request.GET.get('good_name', '')
    if good_name:
        kwargs['coll_good__trade_name__icontains'] = good_name
    kwargs['coll_user'] = request.user
    if state == '2':
        kwargs['coll_good__is_online'] = 2

    data['no_valid'] = MyFavorites.objects.filter(coll_user=request.user).filter(coll_good__is_online=2).count()
    data['sales_promotion'] = data['all_count'] - data['no_valid']
    coll_set = MyFavorites.objects.filter(**kwargs).order_by('-created')
    # 分页
    paginator = Paginator(coll_set, 20)
    page = request.GET.get('page', '1')
    if not page:
        page = 1
    try:
        page = int(page)
        coll_list = paginator.page(page)
    except PageNotAnInteger:
        coll_list = paginator.page(1)
    except EmptyPage:
        coll_list = paginator.page(paginator.num_pages)

    data['coll_list'] = coll_list
    return render(request, 'eshop/my_collect.html', {
        'data': data,
        'paginator': paginator,
        'page': page,
        'state': state,
        'pagi_bar': get_paginator_bar(coll_list)
    })


@eshop_context
def lack_good(request):
    lack_list = LackRegister.objects.filter(people=request.user)
    return render(request, 'eshop/lack_good.html', {'lack_list': lack_list})


def after_sale_manage(request):
    return render(request, 'eshop/after_sale_manage.html', {})


def get_day_date():
    """获取当前天零点和明天零点"""
    today = datetime.date.today()
    today_str = utils_datetime.date_2datetime(today)
    tomorrow = today_str + datetime.timedelta(days=1)
    date_dict = {'today': today_str, 'tomorrow': tomorrow}
    return date_dict


@eshop_context
def account_record(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)
    date_dict = get_day_date()
    order_kwargs = {}
    refund_kwargs = {}
    order_list = {}
    refund_list = {}
    time_state = request.GET.get('time_state', '')
    type_state = request.GET.get('type_state', '0')
    method_state = request.GET.get('method_state', '0')
    # 记录时间自
    if request.GET.get('record_created_from'):
        order_kwargs['ord_time__gte'] = request.GET['record_created_from']
        refund_kwargs['created__gte'] = request.GET['record_created_from']
    # 记录时间到
    if request.GET.get('record_created_to'):
        created_to = datetime.datetime.strptime(request.GET['record_created_to'], "%Y-%m-%d") + datetime.timedelta(
            days=1)
        order_kwargs['ord_time__lt'] = created_to
        refund_kwargs['created__lt'] = created_to
    # 钱的数目自
    if request.GET.get('money_from'):
        order_kwargs['real_price__gte'] = int(request.GET['money_from'])
        refund_kwargs['refund__gte'] = int(request.GET['money_from'])
    # 钱的数目到
    if request.GET.get('money_to'):
        order_kwargs['real_price__lte'] = int(request.GET['money_to'])
        refund_kwargs['refund__lte'] = int(request.GET['money_to'])
    # 交易单号
    if request.GET.get('order_no'):
        order_kwargs['order_no'] = int(request.GET['order_no'])
        refund_kwargs['order__order_no'] = int(request.GET['order_no'])
    # 选择时间
    if time_state:
        if time_state == '0':
            order_kwargs = {
                'ord_time__gte': date_dict['today'],
                'ord_time__lt': date_dict['tomorrow']
            }
            refund_kwargs = {
                'created__gte': date_dict['today'],
                'created__lt': date_dict['tomorrow']
            }
    # 支付方式
    if method_state:
        if method_state == '1':
            order_kwargs['payment_method__pay_type'] = '0'
            refund_kwargs['order__payment_method__pay_type'] = '0'
        if method_state == '2':
            order_kwargs['payment_method__pay_type'] = '1'
            refund_kwargs['order__payment_method__pay_type'] = '1'
        if method_state == '3':
            order_kwargs['payment_method__pay_type'] = '2'
            refund_kwargs['order__payment_method__pay_type'] = '2'
        if method_state == '4':
            order_kwargs['payment_method__pay_type'] = '3'
            refund_kwargs['order__payment_method__pay_type'] = '3'

    # 交易类型
    if type_state:
        if type_state == '0':
            order_list = Order.objects.filter(buyer=request.user).filter(**order_kwargs)
            refund_list = RefundRecord.objects.filter(applicant=request.user).filter(**refund_kwargs)
        if type_state == '1':
            order_list = Order.objects.filter(buyer=request.user).filter(**order_kwargs)
        if type_state == '2':
            print 2
        if type_state == '3':
            refund_list = RefundRecord.objects.filter(applicant=request.user).filter(**refund_kwargs)

    return render(request, 'eshop/account_record.html', {
        'time_state': time_state,
        'type_state': type_state,
        'method_state': method_state,
        'order_list': order_list,
        'refund_list': refund_list,
    })


class ConsultFeedbackView(View):
    """咨询反馈"""

    @method_decorator(eshop_context)
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)
        try:
            feedback_type = request.GET.get('feedback_type')
            consult_list_count = ConsultFeedback.objects.filter(feedback_type=0).count()
            feedback_type_count = ConsultFeedback.objects.filter(feedback_type=1).count()
            consult_list = ConsultFeedback.objects.filter(is_display=True, user=request.user,
                                                          feedback_type=CONSULT).order_by('-created')
            feedback_list = ConsultFeedback.objects.filter(is_display=True, user=request.user,
                                                           feedback_type=FEEDBACK).order_by('-created')
            data_set = ConsultFeedback.objects.all().order_by('-updated')
            total_count = data_set.count()  # 总记录数
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
                'consult_list': consult_list,
                'feedback_list': feedback_list,
                'consult_feedback_list': consult_feedback_list,
                'consult_list_count': consult_list_count,
                'feedback_type_count': feedback_type_count,
                'total_count': total_count,
                'per_page': PAGE_LIMIT,
                'cur_page': cur_page,
                'page': paginator
            }

        except Exception, e:
            log.error("ConsultFeedbackView.get error: %s" % e)

        return render(request, 'eshop/consult_feedback.html', result)

    def post(self, request):
        try:
            if request.is_ajax():
                temp_dict = request.POST.dict()
                temp_dict['user'] = request.user.id
                form = ConsultFeedbackForm(temp_dict)
                feedback_type = request.POST['feedback_type']
                if form.is_valid():
                    form.save()
                    result = {
                        'status': 1,
                        'feedback_type': feedback_type,
                        'msg': '提交成功',
                    }
                else:
                    result = {
                        'status': 0,
                        'feedback_type': '',
                        'msg': '参数异常',
                    }
            else:
                raise Exception('异常请求')
        except Exception, e:
            log.error(e)
            result = {
                'status': 0,
                'feedback_type': '',
                'msg': str(e),
            }
        return JsonResponse(result)


def consult_feedback(request):
    return render(request, 'eshop/consult_feedback.html', {})


class SiteMessageView(View):
    @method_decorator(eshop_context)
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

        # 未读消息条数
        is_read = request.GET.get('is_read', '')
        if is_read == 'unread':
            try:
                unread_num = SiteMessage.objects.filter(user=request.user).filter(is_read=False).count()
                result = {
                    'status': 1,
                    'unread_num': unread_num
                }
            except Exception, e:
                log.exception('eshop.views.SiteMessageView.get error: %s, user: %s' % (e, request.user))
                result = {
                    'status': 0,
                    'data': '',
                }
            return JsonResponse(result)

        messages = SiteMessage.objects.filter(user=request.user).order_by('-time')
        read_messages = messages.filter(is_read=False)
        method = request.GET.get('method', '')
        paginator = Paginator(messages, 10)
        page = request.GET.get('page', '1')
        if not page:
            page = 1
        try:
            page = int(page)
            messages_list = paginator.page(page)
        except PageNotAnInteger:
            messages_list = paginator.page(1)
        except EmptyPage:
            messages_list = paginator.page(paginator.num_pages)

        return render(request, 'eshop/site_message.html', {
            'messages_list': messages_list,
            'messages': messages,
            'paginator': paginator,
            'page': page,
            'pagi_bar': get_paginator_bar(messages_list)
        })

    def post(self, request):
        try:
            if request.is_ajax():
                action = request.POST.get('action')
                if action == 'mark_read_all':
                    SiteMessage.objects.filter(user=request.user).update(is_read=True)
                    result = {
                        'status': 1,
                        'msg': '成功标记已读消息',
                    }
                elif action == 'delete_read':
                    SiteMessage.objects.filter(user=request.user, is_read=True).delete()
                    result = {
                        'status': 1,
                        'msg': '成功清空已读消息',
                    }
                elif action == 'mark_read_single':
                    pk = request.POST.get('pk')
                    if pk:
                        SiteMessage.objects.filter(pk=pk).update(is_read=True)
                    result = {
                        'status': 1,
                        'msg': '成功标记已读消息',
                    }
                else:
                    result = {
                        'status': 0,
                        'msg': '请求错误',
                    }
            else:
                raise Exception('异常请求')
        except Exception, e:
            log.error(e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)


def site_message(request):
    return render(request, 'eshop/site_message.html', {})


class AccountInfoView(View):
    @method_decorator(eshop_context)
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

        user = User.objects.get(pk=request.user.id)

        obj = {}

        if user.enterprise:
            obj['operate_mode'] = user.enterprise.operate_mode.split(',')
            obj['region'] = user.enterprise.region.split(',')
            obj['biz_scope'] = user.enterprise.biz_scope.split(',')
            obj['photo'] = EnterpriseQualification.objects.filter(enterprise=user.enterprise.pk)

        return render(request, 'eshop/account_info.html', {'data': user, 'obj': obj})

    def post(self, request):
        try:
            if request.is_ajax():
                pk = request.POST.get('pk')
                user = User.objects.get(pk=pk)
                form = AccountInfoForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    result = {
                        'status': 1,
                        'msg': '修改成功',
                    }
                else:
                    result = {
                        'status': 0,
                        'msg': '输入参数异常',
                    }
            else:
                raise Exception('异常请求')
        except Exception, e:
            log.error(e)
            result = {
                'status': 0,
                'msg': str(e)
            }
        return JsonResponse(result)


def account_info(request):
    return render(request, 'eshop/account_info.html', {})


class AccountSafetyView(View):
    """账户安全"""

    @method_decorator(login_required)
    def get(self, request):
        action = request.GET.get('action', '')
        step = request.GET.get('step', '')
        email = request.user.email
        phone = request.user.phone
        # 登录密码
        if 'action_1' == action:
            if 'verify' == step:  # 修改登录密码
                return render(request, 'eshop/account_safety.html', {
                    'action': action,
                    'step': step,
                    'phone': phone,
                })
            elif 'new_password' == step:
                # account_safety_session = request.session.get('account_safety', {})
                # if not account_safety_session:
                #     return redirect('/eshop/account_safety/')
                return render(request, 'eshop/account_safety.html', {
                    'action': action,
                    'step': step,
                })
            elif 'complate' == step:
                pass
            return render(request, 'eshop/account_safety.html', {
                'action': action,
                'step': step,
            })

        # 手机验证
        elif 'action_2' == action:
            if 'phone' == step:
                return render(request, 'eshop/account_safety.html', {
                    'action': action,
                    'step': step,
                    'phone': phone,
                })
            elif 'phone_new' == step:
                return render(request, 'eshop/account_safety.html', {
                    'action': action,
                    'step': step,
                })
            elif 'complate' == step:
                pass
            return render(request, 'eshop/account_safety.html', {
                'step': step,
                'action': action,
            })

        # 邮箱验证
        elif 'action_3' == action:
            if 'verify' == step:
                return render(request, 'eshop/account_safety.html', {
                    'step': step,
                    'phone': phone,
                    'action': action,

                })
            elif 'email' == step:
                return render(request, 'eshop/account_safety.html', {
                    'step': step,
                    'email': email,
                    'action': action,
                })
            elif 'complete' == step:
                pass
            return render(request, 'eshop/account_safety.html', {
                'step': step,
                'action': action,
            })

        # 支付密码
        elif 'action_4' == action:
            if 'pay_password' == step:
                return render(request, 'eshop/account_safety.html', {
                    'step': step,
                    'action': action,
                })
            elif 'complete' == step:
                pass
            return render(request, 'eshop/account_safety.html', {
                'step': step,
                'action': action,
            })
        else:
            return render(request, 'eshop/account_safety.html', {
                'step': step,
                'action': action,
            })

    def post(self, request):
        if 'action' in request.POST:
            step = request.POST.get('step', {})
            action = request.POST.get('action', {})
            # 登录密码
            if 'action_1' == action:
                try:
                    if request.method == 'POST' and request.is_ajax():
                        if 'verify' == step:
                            # 拿到用户输入的参数
                            phone = request.POST.get('phone', '')
                            captcha = request.POST.get('phone_yzm', '')
                            # 校验验证码
                            account_safety_session = request.session.get('account_safety', '')
                            # CaptchaStore.objects.filter()
                            if not account_safety_session:
                                result = {
                                    'status': 0,
                                    'msg': u'验证码已失效，请重新获取'
                                }
                                return JsonResponse(result)
                            if captcha == account_safety_session:
                                result = {
                                    'status': 1,
                                    'msg': u'验证成功',
                                    'url': 'eshop/account_safety/?action=action_1&step=new_password'
                                }
                                return JsonResponse(result)
                            else:
                                result = {
                                    'status': 0,
                                    'msg': u'验证码输入有误，请核对'
                                }
                                return JsonResponse(result)
                                # if CaptchaStore.objects.filter(response=str(captcha), challenge=phone):
                                #     request.session['account_safety'] = {'step': 'new_password', 'phone': phone}
                                #     result = {
                                #         'status': 1,
                                #         'msg': u'验证成功',
                                #         'url': 'eshop/account_safety/?step:new_password'
                                #     }
                                #     return JsonResponse(result)

                        elif 'new_password' == step:
                            # if not account_safety_session:
                            #     result = {
                            #         'status': 0,
                            #         'msg': u'步骤错误，请重新填写',
                            #         'url': '/eshop/account_safety/'
                            #     }
                            #     return JsonResponse(result)
                            password = request.POST.get('password', '')
                            password2 = request.POST.get('password2', '')
                            captcha = request.POST.get('captcha', '')
                            password_session = request.session.get('password_session', '')
                            if not (password or password2):
                                result = {
                                    'status': 0,
                                    'msg': '请填写密码2',
                                }
                                return JsonResponse(result)
                            if password != password2:
                                result = {
                                    'status': 1,
                                    'msg': '两次密码不一致',
                                }
                                return JsonResponse(result)
                            if not (captcha.upper() == request.session['CheckCode'].upper()):
                                result = {
                                    'status': 0,
                                    'msg': '验证码输入有误'
                                }
                                return JsonResponse(result)

                            user = User.objects.filter(id=request.user.id).update(password=make_password(password))
                            if user:
                                if request.session.get('password_session', ''):
                                    del request.session['password']
                                result = {
                                    'status': 1,
                                    'msg': '修改成功',
                                }
                                return JsonResponse(result)

                        elif 'complete' == step:
                            pass
                            return render(request, 'eshop/account_safety.html', {
                                'step': step
                            })
                        # 验证电话号码
                        elif 'sms_code' == step:  # 验证电话号码
                            phone = request.POST.get('phone', '')
                            phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$')
                            is_phone = phone_re.match(phone)
                            if not is_phone:
                                result = {
                                    'status': 0,
                                    'msg': '请输入正确的电话号码'
                                }
                                return JsonResponse(result)
                            is_phone_exist = User.objects.filter(phone=phone)
                            if not is_phone_exist:
                                result = {
                                    'status': 0,
                                    'msg': '这个电话没有注册，请先注册'
                                }
                                return JsonResponse(result)
                            # 避免多次发送短信
                            request.session.set_expiry(60)
                            phone_session = request.session.get('account_safety_verify_phone', '')
                            if phone_session == phone:
                                result = {
                                    'status': 0,
                                    'msg': '验证码已经发送，请注意查收'
                                }
                                return JsonResponse(result)
                            request.session['account_safety_verify_phone'] = phone

                            sms_msg = make_sms()
                            c = CaptchaStore()
                            c.response = sms_msg[1]
                            c.challenge = phone
                            c.save()

                            # 测试 可不发短信 去CaptchaStore中查看验证码
                            if not settings.DEBUG:
                                send_sms([phone], sms_msg[0])

                            json_response = {
                                'key': c.hashkey,
                                'status': 1
                            }
                            return JsonResponse(json_response)
                        else:
                            raise Exception('请求异常')
                    else:
                        raise Exception('请求异常')
                except Exception, e:
                    log.exception("AccountSafetyView post raise,Error:s%" % e)
                    result = {
                        'status': 0,
                        'msg': str(e)
                    }
                    return JsonResponse(result)

            # 手机验证
            if 'action_2' == action:
                try:
                    if request.method == 'POST' and request.is_ajax():
                        #   旧手机号码的短信验证
                        if 'phone' == step:
                            phone = request.POST.get('phone', '')
                            captcha = request.POST.get('phone_yzm', '')
                            account_safety_session = request.session.get('account_safety', '')
                            if not account_safety_session:
                                result = {
                                    'status': 0,
                                    'msg': '验证码已失效，请重新获取'
                                }
                                return JsonResponse(result)
                            if captcha == account_safety_session:
                                result = {
                                    'status': 1,
                                    'msg': '验证成功',
                                    'url': 'eshop/account_safety/?action=action_2&step=phone_new'
                                }
                                return JsonResponse(result)
                            else:
                                result = {
                                    'status': 0,
                                    'msg': '验证码输入有误，请核对'
                                }
                                return JsonResponse(result)
                        elif 'phone_new' == step:
                            # 验证新手机号 是否存在
                            if 'captcha' in request.POST:
                                captcha = request.POST.get('phone_code', '')
                                phone_new = request.POST.get('phone_new', '')
                                account_safety_session = request.session.get('account_safety', '')
                                # 校验验证码
                                if not account_safety_session:
                                    result = {
                                        'status': 0,
                                        'msg': '验证码已失效，请重新获取'
                                    }
                                    return JsonResponse(result)
                                if not (captcha == account_safety_session):
                                    result = {
                                        'status': 0,
                                        'msg': '验证不成功',
                                        'url': 'eshop/account_safety/?action=action_2&step=complete'
                                    }
                                    return JsonResponse(result)
                                if not (captcha.upper() == request.session['account_safety'].upper()):
                                    result = {
                                        'status': 0,
                                        'msg': '验证码输入有误'
                                    }
                                    return JsonResponse(result)
                                # 验证新手机号是否填写
                                # if not phone_new:
                                #     result = {
                                #         'status': 0,
                                #         'msg': u'请填写手机号'
                                #     }
                                #     return JsonResponse(result)

                                user = User.objects.filter(id=request.user.id).update(phone=phone_new)
                                if user:
                                    del request.session['account_safety']
                                    result = {
                                        'status': 1,
                                        'msg': '修改成功',
                                    }
                                    return JsonResponse(result)
                            else:
                                raise Exception('手机号输入有误')
                        elif 'complete' == step:
                            pass
                            return render(request, 'eshop/account_safety.html', {
                                'step': step
                            })
                        elif 'sms_code' == step:
                            # 验证电话号码
                            phone = request.POST.get('phone', '')
                            phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$')
                            is_phone = phone_re.match(phone)
                            if not is_phone:
                                result = {
                                    'status': 0,
                                    'msg': '请输入正确的电话号码'
                                }
                                return JsonResponse(result)
                            is_phone_exist = User.objects.filter(phone=phone)
                            if not is_phone_exist:
                                result = {
                                    'status': 0,
                                    'msg': '这个电话没有注册，请先注册'
                                }
                                return JsonResponse(result)
                            # 避免多次发送短信
                            request.session.set_expiry(60)
                            phone_session = request.session.get('account_safety_verify_phone', '')
                            if phone_session == phone:
                                result = {
                                    'status': 0,
                                    'msg': '验证码已经发送，请注意查收'
                                }
                                return JsonResponse(result)
                            request.session['account_safety_verify_phone'] = phone

                            sms_msg = make_sms()
                            c = CaptchaStore()
                            c.response = sms_msg[1]
                            c.challenge = phone
                            c.save()

                            # 测试 可不发短信 去CaptchaStore中查看验证码
                            if not settings.DEBUG:
                                send_sms([phone], sms_msg[0])

                            json_response = {
                                'key': c.hashkey,
                                'status': 1
                            }
                            return JsonResponse(json_response)
                        else:
                            raise Exception('请求异常')
                    else:
                        raise Exception('请求异常')
                except Exception, e:
                    log.exception("AccountSafetyView post raise,Error:s%" % e)
                    result = {
                        'status': 0,
                        'msg': str(e)
                    }
                    return JsonResponse(result)

            # 邮箱验证
            if 'action_3' == action:
                try:
                    if request.method == 'POST' and request.is_ajax():
                        if 'verify' == step:
                            phone = request.POST.get('phone', '')
                            captcha = request.POST.get('phone_yzm', '')
                            account_safety_session = request.session.get('account_safety', '')
                            if not account_safety_session:
                                result = {
                                    'status': 0,
                                    'msg': u'验证码失败'
                                }
                                return JsonResponse(result)
                            if CaptchaStore.objects.filter(response=str(captcha), challenge=phone):
                                request.session['account_safety'] = {'step': 'email', 'phone': phone}
                                result = {
                                    'status': 1,
                                    'msg': u'验证成功',
                                    'url': 'eshop/account_safety/?step:email'
                                }
                                return JsonResponse(result)
                        elif 'email' == step:
                            email = request.POST.get('email', '')
                            captcha = request.POST.get('captcha', '')
                            account_safety_session = request.session.get('account_safety_session', '')
                            # if not account_safety_session:
                            #     result = {
                            #         'status': 0,
                            #         'msg': '验证码输入有误'
                            #     }
                            #     return JsonResponse(result)
                            if CaptchaStore.objects.filter(response=str(captcha), challenge=email):
                                request.session['account_safety'] = {'step': 'complete', 'email': email}
                                result = {
                                    'status': 1,
                                    'msg': '验证成功',
                                    'url': 'eshop/account_safety/?step:complete'
                                }
                                return JsonResponse(result)
                            # 验证邮箱是否填写
                            if not email:
                                result = {
                                    'status': 0,
                                    'msg': '请填写邮箱'
                                }
                                return JsonResponse(result)
                            if not (captcha.upper() == request.session['CheckCode'].upper()):
                                result = {
                                    'status': 0,
                                    'msg': '验证码输入有误'
                                }
                                return JsonResponse(result)

                            user = User.objects.filter(id=request.user.id).update(email=email)
                            if user:
                                if request.session.get('account_safety_session', ''):
                                    del request.session['account_safety']
                                result = {
                                    'status': 1,
                                    'msg': '修改成功',
                                }
                                return JsonResponse(result)

                        elif 'complete' == step:
                            return render(request, 'eshop/account_safety.html', {
                                'step': step
                            })
                    else:
                        raise Exception('请求异常')
                except Exception, e:
                    log.exception("AccountSafetyView post raise,Error:s%" % e)
                    result = {
                        'status': 0,
                        'msg': str(e)
                    }
                    return JsonResponse(result)

            # 支付密码
            if 'action_4' == action:
                try:
                    if request.method == 'POST' and request.is_ajax():
                        if 'pay_password' == step:
                            pay_password = request.POST.get('pay_password', '')
                            pay_password2 = request.POST.get('pay_password2', '')
                            pay_password_session = request.session.get('pay_password', '')
                            # if not pay_password_session:
                            #     result = {
                            #         'status': 0,
                            #         'msg': u'步骤错误请重新填写',
                            #         'url': '/eshop/account_safety/'
                            #     }
                            #     return JsonResponse(result)
                            if not (pay_password or pay_password2):
                                result = {
                                    'status': 0,
                                    'msg': '请填写支付密码'
                                }
                                return JsonResponse(result)
                            if pay_password != pay_password2:
                                result = {
                                    'status': 0,
                                    'msg': '两次支付密码不一致',
                                }
                                return JsonResponse(result)

                            user = User.objects.filter(id=request.user.id).update(pay_password=make_password(pay_password))
                            if user:
                                if request.session.get('pay_password_session', ''):
                                    del request.session['pay_password']
                                result = {
                                    'status': 1,
                                    'msg': '修改成功',
                                }
                                return JsonResponse(result)
                        elif 'complete' == step:
                            pass
                            return render(request, 'eshop/account_safety.html', {
                                'step': step
                            })
                    else:
                        raise Exception('请求异常')
                except Exception, e:
                    log.exception("AccountSafetyView post raise,Error:s%" % e)
                    result = {
                        'status': 0,
                        'msg': str(e)
                    }
                    return JsonResponse(result)
            else:
                result = {
                    'status': 1,
                    'msg': '请求错误',
                }
                return JsonResponse(result)
        else:
            result = {
                'status': 1,
                'msg': '请求action错误',
            }
            return JsonResponse(result)


def account_safety(request):
    return render(request, 'eshop/account_safety.html', {})


@eshop_context
def receiving_address(request):
    address_list = ReceivingAddress.objects.filter(user=request.user)
    address_count = address_list.count()
    if address_count == 1:
        first = address_list.first()
        first.is_default = True
        first.save()

    return render(request, 'eshop/receiving_address.html', {
        'address_list': address_list,
    })


class QuicklyOrderView(View):
    @method_decorator(eshop_context)
    def get(self, request):

        if not request.user.is_authenticated():
            return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)

        quickly_order = QuicklyOrder.objects.filter(user=request.user)
        history_order = Order.objects.filter(buyer=request.user)[:20]

        return render(request, 'eshop/quickly_order.html', {
            'quickly_order': quickly_order,
            'history_order': history_order
        })

    def post(self, request):
        try:
            if 'method' in request.POST:
                method = request.POST.get('method', '')

                # 商品搜索结果添加
                if 'search_add_good' == method:
                    return self._handle_search_add_good(request)

                # 商品数量添加
                elif 'good_count' == method:
                    return self._handle_good_count(request)

                # 导入历史订单
                elif 'old_order' == method:
                    return self._handle_old_order(request)

                else:
                    result = {
                        'status': 0,
                        'msg': 'method请求错误'
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

    def _handle_search_add_good(self, request):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action', '')
                # 获取搜索关键字 渲染结果
                if 'search_keywords' == action:
                    search_keywords = request.POST.get('search_keywords', '')

                    # good_search_result = Good.objects.filter(is_online=True, is_qualified=2).filter(
                    good_search_result = Good.objects.filter(
                        Q(name__icontains=search_keywords) |
                        Q(trade_name__icontains=search_keywords) |
                        Q(brand__icontains=search_keywords)
                    )

                    if good_search_result:
                        return render(request, 'eshop/modals/good_search_result.html', {
                            'good_search_result': good_search_result
                        })

                    else:
                        return render(request, 'eshop/modals/good_search_result.html', {
                            'good_search_result': good_search_result
                        })
                # 点击结果取得id返回good插入页面
                elif 'add_good' == action:

                    good_id = int(request.POST.get('good_id', ''))
                    is_quickly_order = QuicklyOrder.objects.filter(
                        user=request.user,
                        good_id=good_id
                    ).first()
                    if is_quickly_order:
                        quickly_order = QuicklyOrder.objects.filter(
                            user=request.user,
                            good_id=good_id
                        )
                        quickly_order.update(
                            quantity=F('quantity') + 1
                        )

                        result = {
                            'status': 2,
                            'count': quickly_order[0].quantity,
                            'quickly_order_id': is_quickly_order.id,
                            'msg': '已经在快速下单列表中，只更新数量'
                        }
                        return JsonResponse(result)

                    else:
                        quickly_order = QuicklyOrder.objects.create(
                            user=request.user,
                            good_id=good_id,
                            quantity=1
                        )
                        good = Good.objects.filter(pk=good_id).first()

                        return render(request, 'eshop/modals/good_search_add_result.html', {
                            'good': good,
                            'quickly_order': quickly_order
                        })

                # 商品数量 增加 减少
                elif 'count' == action:
                    pass
                # 删除快速下单商品
                elif 'remove' == action:
                    quickly_order_id = int(request.POST.get('quickly_order_id', ''))
                    is_quickly_order_delete = QuicklyOrder.objects.filter(
                        user=request.user,
                        pk=quickly_order_id
                    ).delete()
                    result = {
                        'status': 1,
                        'msg': '删除快速下单商品成功'
                    }
                    return JsonResponse(result)
                else:
                    result = {
                        'status': 0,
                        'msg': 'action错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': 'action错误'
                }
            return JsonResponse(result)

        except Exception, e:
            log.error('OrderListView %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e
            }
            return JsonResponse(result)

    def _handle_good_count(self, request):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action', '')
                # 商品id
                gid = int(request.POST.get('gid', ''))
                # 根据数字修改数量
                if 'count_value' == action:
                    good_count_value = int(request.POST.get('good_count_value', ''))
                    quickly_order = QuicklyOrder.objects.filter(pk=gid, user=request.user)
                    quickly_order.update(
                        quantity=good_count_value
                    )
                    result = {
                        'status': 1,
                        'msg': '修改数量',
                        'good_count': quickly_order[0].quantity
                    }
                # 商品加一
                elif 'count_add' == action:
                    QuicklyOrder.objects.filter(pk=gid, user=request.user).update(
                        quantity=F('quantity') + 1
                    )
                    result = {
                        'status': 1,
                        'msg': '加一',
                    }
                # 商品减一
                elif 'count_reduce' == action:
                    QuicklyOrder.objects.filter(pk=gid, user=request.user).update(
                        quantity=F('quantity') - 1
                    )
                    result = {
                        'status': 1,
                        'msg': '减一',
                    }
                else:
                    result = {
                        'status': 0,
                        'msg': 'action错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': 'action错误'
                }
            return JsonResponse(result)
        except Exception, e:
            log.error('OrderListView _handle_good_count %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e
            }
            return JsonResponse(result)

    def _handle_old_order(self, request):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action', '')
                # 获取搜索关键字 渲染结果

                if 'add' == action:
                    old_order_list = json.loads(request.POST.get('old_order_list', '[]'))

                    is_old_order_list = QuicklyOrder.objects.filter(
                        user=request.user,
                        good_id__in=old_order_list
                    )

                    if is_old_order_list:
                        quickly_order = QuicklyOrder.objects.filter(
                            user=request.user,
                            good_id__in=old_order_list
                        )
                        quickly_order.update(
                            quantity=F('quantity') + 1
                        )

                        print quickly_order
                        data = [{"id": i.id, "count": i.quantity} for i in quickly_order]

                        result = {
                            'status': 2,
                            'data': json.dumps(data),
                            'msg': '已经在快速下单列表中，只更新数量'
                        }
                        return JsonResponse(result)

                    else:

                        for order in old_order_list:
                            QuicklyOrder.objects.create(
                                user=request.user,
                                good_id=order,
                                quantity=1
                            )

                        quickly_order = QuicklyOrder.objects.filter(user=request.user, good__pk__in=old_order_list)

                        return render(request, 'eshop/modals/good_old_order_add.html', {
                            'quickly_order': quickly_order
                        })

                # 商品数量 增加 减少
                elif 'xxx' == action:
                    pass



                else:
                    result = {
                        'status': 0,
                        'msg': 'action错误'
                    }

            else:
                result = {
                    'status': 0,
                    'msg': 'action错误'
                }

            return JsonResponse(result)

        except Exception, e:
            log.error('OrderListView %s' % e)
            result = {
                'status': 0,
                'msg': '内部错误 %s' % e

            }
            return JsonResponse(result)


def quickly_place_order(request):
    return render(request, 'eshop/quickly_place_order.html', {})


def user_recharge(request):
    return render(request, 'eshop/user_recharge.html', {})


def eshop_home1(request):
    return render(request, 'eshop/eshop_home1.html', {})


def user_register1(request):
    return render(request, 'eshop/user_register1.html', {})


def user_login1(request):
    return render(request, 'eshop/user_login1.html', {})


def forget_password1(request):
    return render(request, 'eshop/forget_password1.html', {})


def good_search_list1(request):
    return render(request, 'eshop/good_search_list1.html', {})


def shopping_cart_list1(request):
    return render(request, 'eshop/shopping_cart_list1.html', {})


def shopping_balance1(request):
    return render(request, 'eshop/shopping_balance1.html', {})


def submit_order1(request):
    return render(request, 'eshop/submit_order1.html', {})


def member_center1(request):
    return render(request, 'eshop/member_center1.html', {})


def my_order1(request):
    return render(request, 'eshop/my_order1.html', {})


def changing_or_refunding1(request):
    return render(request, 'eshop/changing_or_refunding1.html', {})


def my_collect1(request):
    return render(request, 'eshop/my_collect1.html', {})


def lack_good1(request):
    return render(request, 'eshop/lack_good1.html', {})


def after_sale_manage1(request):
    return render(request, 'eshop/after_sale_manage1.html', {})


def account_record1(request):
    return render(request, 'eshop/account_record1.html', {})


def consult_feedback1(request):
    return render(request, 'eshop/consult_feedback1.html', {})


def site_message1(request):
    return render(request, 'eshop/site_message1.html', {})


def account_info1(request):
    return render(request, 'eshop/account_info1.html', {})


def account_safety1(request):
    return render(request, 'eshop/account_safety1.html', {})


def receiving_address1(request):
    return render(request, 'eshop/receiving_address1.html', {})


def quickly_place_order1(request):
    return render(request, 'eshop/quickly_place_order1.html', {})


def user_recharge1(request):
    return render(request, 'eshop/user_recharge1.html', {})


def test_captcha(request):
    if request.POST:

        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(request.path + '?ok')
    else:
        form = CaptchaTestForm()

    return render(request, 'eshop/test_captcha.html', {'form': form})


def ajax_captcha_val(request):
    """ajax 验证码"""
    if request.is_ajax():
        captchastore = CaptchaStore.objects.filter(response=request.GET['response'],
                                                   hashkey=request.GET['hashkey'])
        if captchastore:
            json_data = {'status': 1}
        else:
            json_data = {'status': 0}
        return JsonResponse(json_data)
    else:
        json_data = {'status': 0}
        return JsonResponse(json_data)


def ajax_captcha_val(request):
    """ajax 验证码"""
    if request.is_ajax():
        captchastore = CaptchaStore.objects.filter(response=request.GET['response'],
                                                   hashkey=request.GET['hashkey'])
        if captchastore:
            json_data = {'status': 1}
        else:
            json_data = {'status': 0}
        return JsonResponse(json_data)
    else:
        json_data = {'status': 0}
        return JsonResponse(json_data)


def ajax_captcha_refresh(request):
    """ajax 刷新"""

    if not request.is_ajax():
        raise Http404

    new_key = CaptchaStore.generate_key()
    to_json_response = {
        'key': new_key,
        'image_url': captcha_image_url(new_key),
    }
    return HttpResponse(json.dumps(to_json_response), content_type='application/json')


def captcha_sms(request, phone_number):
    sms_msg = make_sms()
    print phone_number
    c = CaptchaStore()
    c.response = sms_msg[1]
    c.challenge = phone_number
    c.save()
    # c.hashkey

    # msg = '来自派生科技的验证码' + str(sms_number)
    # print msg.decode('utf-8').encode('gb2312')

    send_sms([phone_number], sms_msg[0])

    json_response = {
        'key': c.hashkey,
        'status': 1
    }
    return JsonResponse(json_response)


@eshop_context
def simple_page_1(request):
    return render(request, 'eshop/simple_page_1.html', {})


@eshop_context
def simple_page_2(request):
    return render(request, 'eshop/simple_page_2.html', {})


@eshop_context
def simple_page_3(request):
    return render(request, 'eshop/simple_page_3.html', {})


@eshop_context
def simple_page_4(request):
    return render(request, 'eshop/simple_page_4.html', {})


@eshop_context
def simple_page_5(request):
    return render(request, 'eshop/simple_page_5.html', {})


@eshop_context
def simple_page_6(request):
    return render(request, 'eshop/simple_page_6.html', {})


@eshop_context
def simple_page_7(request):
    return render(request, 'eshop/simple_page_7.html', {})


@eshop_context
def simple_page_8(request):
    return render(request, 'eshop/simple_page_8.html', {})


@eshop_context
def simple_page_9(request):
    return render(request, 'eshop/simple_page_9.html', {})


@eshop_context
def simple_page_10(request):
    return render(request, 'eshop/simple_page_10.html', {})


@eshop_context
def simple_page_11(request):
    return render(request, 'eshop/simple_page_11.html', {})


@eshop_context
def simple_page_12(request):
    return render(request, 'eshop/simple_page_12.html', {})


@eshop_context
def simple_page_13(request):
    return render(request, 'eshop/simple_page_13.html', {})


@eshop_context
def simple_page_14(request):
    return render(request, 'eshop/simple_page_14.html', {})


@eshop_context
def simple_page_15(request):
    return render(request, 'eshop/simple_page_15.html', {})
