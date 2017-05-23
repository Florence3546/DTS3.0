# coding=UTF-8
from common.forms import SettingsTypeForm, SettingsItemForm
from common.forms import RegionForm
from common.models import SettingsType, SettingsItem
from common.models import Region
from common.utils.utils_log import log
import datetime

from common.constant import (
    USERTYPE_CHOICES,
    SETTINGS_BASIC,
    PAY_TYPE_CHOICES,
    SHIPPING_TYPE_CHOICES,
    # CHANGE_PRICE_STATE,             # 改价状态
    # INVOICE_STATE_CHOICES,          # 开票状态
    # VERIFY_STATE_CHOICES,           # 审核状态
    # TRADE_STATE_CHOICES,      # 交易状态
    REFUND_MODAL,
    ORDER_MODAL,
)

from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render
from django.conf import settings
from dtsauth.models import Enterprise, User, Permission, Role, OperateRecord, RolePermission
from dtsauth.forms import EnterpriseForm, UserForm, PermissionForm, RoleForm, RoleAttrForm
from order.models import PaymentMethod, ShippingMethod, Order, RefundRecord, ChangePriceRecord, ReceivingAddress
from order.forms import PaymentMethodForm, ShippingMethodForm, OrderForm, ReceivingAddressForm
from good.models import Good, DrugAttr, GoodCategory, GoodPhoto, GoodQualification, LackRegister
from good.forms import GoodForm, DrugAttrForm, GoodCategoryForm, GoodDrugAttrForm, LackRegisterForm
from dtsadmin.models import Informations, ConsultFeedback
from eshop.forms import ConsultFeedbackForm

import simplejson as json
import time
import os

from django.db.models.deletion import ProtectedError


FORM_DICT = {
    'SettingsTypeForm': SettingsTypeForm,
    'SettingsItemForm': SettingsItemForm,
    'EnterpriseForm': EnterpriseForm,
    'PaymentMethodForm': PaymentMethodForm,
    'ShippingMethodForm': ShippingMethodForm,
    'Region': RegionForm,
    'GoodCategoryForm': GoodCategoryForm,
    'UserForm': UserForm,
    'RoleForm': RoleForm,
    'PermissionForm': PermissionForm,
    'ReceivingAddressForm': ReceivingAddressForm,
    'LackRegisterForm': LackRegisterForm,
    'OrderForm': OrderForm,
    'RoleAttrForm': RoleAttrForm,
    'ConsultFeedbackForm': ConsultFeedbackForm,

}

MODEL_DICT = {
    'SettingsType': SettingsType,
    'SettingsItem': SettingsItem,
    'Enterprise': Enterprise,
    'PaymentMethod': PaymentMethod,
    'ShippingMethod': ShippingMethod,
    'Region': Region,
    'GoodCategory': GoodCategory,
    'User': User,
    'Role': Role,
    'Permission': Permission,
    'LackRegister': LackRegister,
    'Order': Order,
    'ReceivingAddress': ReceivingAddress,
    'GoodCheck': Good,
    'ConsultFeedbackAttr': ConsultFeedback,
    'OperateRecord': OperateRecord,
}

MODAL_DICT = {
    'Enterprise': (Enterprise, 'dtsadmin/modals/modal_enterprise.html'),
    'PaymentMethod': (PaymentMethod, 'dtsadmin/modals/modal_payment_method.html'),
    'ShippingMethod': (ShippingMethod, 'dtsadmin/modals/modal_shipping_method.html'),
    'Region': (Region, 'dtsadmin/modals/modal_area.html'),
    'GoodDrugAttr': (Good, 'dtsadmin/modals/modal_good.html'),
    'GoodCategory': (GoodCategory, 'dtsadmin/modals/modal_good_category.html'),
    'User': (User, 'dtsadmin/modals/modal_user.html'),
    'Permission': (Permission, 'dtsadmin/modals/modal_permission.html'),
    'Order': (Order, 'dtsadmin/modals/modal_order.html'),
    'Role': (Role, 'dtsadmin/modals/modal_role.html'),
    'InformationAttr': (Informations, 'dtsadmin/modals/modal_informations.html'),
    'InformationShow': (Informations, 'dtsadmin/modals/modal_informations_preview.html'),
    'ConsultFeedbackAttr': (ConsultFeedback, 'dtsadmin/modals/modal_consult_feedback.html'),
    'ConsultFeedbackShow': (ConsultFeedback, 'dtsadmin/modals/modal_consult_feedback_preview.html'),
    'GoodCheck': (Good, 'dtsadmin/modals/modal_good_check.html'),
    'LackRegister': (LackRegister, 'eshop/modals/modal_lack_register.html'),
    'ReceivingAddress': (ReceivingAddress, 'eshop/modals/modal_receiving_address.html'),
    'RefundRecord': (RefundRecord, 'dtsadmin/modals/modal_returns_refunds.html'),
    'OperateRecord': (OperateRecord, 'dtsadmin/modals/modal_common_log.html'),
}


def add_object_byform(request, form_class):
    """利用form新增数据对象"""
    try:
        if request.method == 'POST' and request.is_ajax():
            form = FORM_DICT[form_class](request.POST)
            if form.is_valid():
                form.save()
                result = {
                    'status': 1,
                    'msg': '添加成功',
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
            'msg': str(e),
        }
    return JsonResponse(result)


def add_good_category_byform(request, form_class):
    """利用form新增数据对象"""
    try:
        if request.method == 'POST' and request.is_ajax():
            form = FORM_DICT[form_class](request.POST)
            if form.is_valid():
                form.save()
                result = {
                    'status': 1,
                    'msg': '添加成功',
                }
            else:
                result = {
                    'status': 0,
                    'msg': '类目名称不能为空',
                }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def update_object_byform(request, form_class):
    """利用form修改数据对象"""
    try:
        if request.method == 'POST' and request.is_ajax():
            form_class = FORM_DICT[form_class]
            model_class = form_class.Meta.model
            obj = model_class.objects.get(pk=int(request.POST['id']))
            form = form_class(request.POST, instance=obj)
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
            'msg': str(e),
        }
    return JsonResponse(result)


def update_object_byid(request, model_name, obj_id):
    """修改数据对象"""
    try:
        if request.method == 'POST' and request.is_ajax():
            update_dict = request.POST.dict()
            update_dict.pop('csrfmiddlewaretoken')
            MODEL_DICT[model_name].objects.filter(id=obj_id).update(**update_dict)
            result = {
                'status': 1,
                'msg': '修改成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def update_object_bypk(request, model_name, obj_pk):
    """修改数据对象"""
    try:
        if request.method == 'POST' and request.is_ajax():
            update_dict = request.POST.dict()
            update_dict.pop('csrfmiddlewaretoken')
            MODEL_DICT[model_name].objects.filter(pk=obj_pk).update(**update_dict)
            result = {
                'status': 1,
                'msg': '修改成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def switch_area_bypk(request, model_name, obj_pk):
    """开启/禁用地址"""
    try:
        if request.method == 'POST' and request.is_ajax():
            update_dict = request.POST.dict()
            update_dict.pop('csrfmiddlewaretoken')
            MODEL_DICT[model_name].objects.filter(pk=obj_pk).update(**update_dict)
            region_all = Region.objects.filter(is_active=True).exclude(parent_id=0)
            temp_dict = {}
            for region in region_all:
                temp_dict.setdefault(region.parent_id, {})[region.region_code] = region.region_name
                # if region.parent_id not in temp_dict:
                #     temp_dict[region.parent_id] = {}
                # temp_dict[region.parent_id][int(region.region_code)] = region.region_name
            parent_region_dict = dict(Region.objects.filter(id__in=temp_dict.keys()).values_list('id', 'region_code'))
            temp_dict = {parent_region_dict[k]: v for k, v in temp_dict.items() if k in parent_region_dict}
            # for k, v in temp_dict.items():
            #     if k in parent_region_dict:
            #         temp_code = int(parent_region_dict[k])
            #         temp_dict[temp_code] = v
            #         del temp_dict[k]
            data_js = "var DTS = window.DTS || {};\nDTS.DISTRICTS = %s;" % json.dumps(temp_dict)
            datajs_path = os.path.join(settings.BASE_DIR, 'eshop', 'static', 'eshop', 'js', 'data.js')
            with open(datajs_path, 'w') as f:
                f.write(data_js)
            if not settings.DEBUG:
                datajs_path = os.path.join(settings.BASE_DIR, 'static', 'eshop', 'js', 'data.js')
                with open(datajs_path, 'w') as f:
                    f.write(data_js)
            result = {
                'status': 1,
                'msg': '修改成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def delete_object_byid(request, model_class, obj_id):
    """根据id删除某个对象"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            MODEL_DICT[model_class].objects.filter(id=obj_id).delete()
            result = {
                'status': 1,
                'msg': '删除成功',
            }
        else:
            raise Exception('异常请求')
    except ProtectedError, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': '请先删掉关联字段',
        }
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def bluk_delete_byids(request, model_class):
    """根据id删除某个对象"""
    try:
        obj_id_list = json.loads(request.POST.get('id_list'), '[]')
        if obj_id_list and request.method == 'POST' and request.is_ajax():
            MODEL_DICT[model_class].objects.filter(id__in=obj_id_list).delete()
            result = {
                'status': 1,
                'msg': '删除成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def delete_good_category_byid(request, obj_id):
    """根据id删除商品分类"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            obj = GoodCategory.objects.filter(id=obj_id).first()
            if obj:
                children = GoodCategory.objects.filter(path__contains=obj.full_path)
                if children:
                    result = {
                        'status': 0,
                        'msg': '先删除子项',
                    }
                else:
                    obj.delete()
                    result = {
                        'status': 1,
                        'msg': '删除成功',
                    }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def verify_enterprise(request, model_class, obj_id):
    """审核企业"""
    from django.db.models import F
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            MODEL_DICT[model_class].objects.filter(id=obj_id).update(is_active=False if F('is_active') else True)
            result = {
                'status': 1,
                'msg': '修改成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def get_modal_byid(request, modal_name, obj_id):
    """根据id渲染模态对话框"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            model_class, modal_templ = MODAL_DICT[modal_name]
            obj = model_class.objects.get(pk=obj_id)
            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']

            if model_class == User:
                obj.usertype_choices = USERTYPE_CHOICES  # TODO 需要转换为实例方法 by zhongchao 2017/3/20

            if model_class == Role:
                obj.usertype_choices = SettingsType.get_item_list('USERTYPE')

            if model_class == PaymentMethod:
                obj.pay_type_choices = PAY_TYPE_CHOICES
                obj.api_args = json.loads(obj.api_args)

            if model_class == ShippingMethod:
                obj.shipping_type_choices = SHIPPING_TYPE_CHOICES

            return render(request, modal_templ, {'obj': obj})
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


# todo liuhuan 2017-3-14 删掉
def switch_enterprise_lock(request):
    """企业 锁定 解锁"""

    try:
        if request.method == 'POST' and request.is_ajax():

            enter_id_list = request.POST['enter_id_list']
            is_lock = int(request.POST['is_lock'])
            if enter_id_list:
                enter_id_list = json.loads(enter_id_list)
            Enterprise.objects.filter(id__in=enter_id_list).update(is_lock=bool(is_lock))
            result = {
                'status': 1,
                'msg': '%s操作成功' % ('锁定' if is_lock else '解锁'),
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    # return JsonResponse(result)

    return JsonResponse(result)


def switch_lock(request, model_class, action):
    """公用 锁定 解锁"""

    try:
        if request.method == 'POST' and request.is_ajax():

            id_list = request.POST['id_list']
            is_lock = int(request.POST['is_lock'])
            if id_list:
                id_list = json.loads(id_list)
                kwargs = {}
                kwargs[action] = bool(is_lock)
                MODEL_DICT[model_class].objects.filter(pk__in=id_list).update(**kwargs)
            result = {
                'status': 1,
                # 'msg': '%s操作成功' % ('锁定' if is_lock else '解锁'),
                'msg': '操作成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    # return JsonResponse(result)

    return JsonResponse(result)


def switch_bool(request, model_class, obj_id, field):
    """公用 bool 启用 禁用"""

    try:
        if request.method == 'POST' and request.is_ajax():
            kwargs = {field: bool(int(request.POST['is_lock']))}
            p = MODEL_DICT[model_class].objects.filter(pk=obj_id).update(**kwargs)
            result = {
                'status': 1,
                'msg': '操作成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def switch_permission_lock(request, model_class, action):
    """权限管理 权限状态切换"""

    try:
        if request.method == 'POST' and request.is_ajax():

            if action == 'lock':
                action = 0
            elif action == 'un_lock':
                action = 1
            print action
            print bool(action)
            pk = int(request.POST['id'])

            MODEL_DICT[model_class].objects.filter(pk=pk).update(is_active=bool(action))
            result = {
                'status': 1,
                'msg': '%s操作成功' % ('启用' if bool(action) else '禁用'),
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    # return JsonResponse(result)

    return JsonResponse(result)


def switch_delivery_lock(request, method, obj_id):
    """修改快递状态"""

    try:
        if request.method == 'POST' and request.is_ajax():
            is_active = ''
            if method == 'on':
                is_active = True
            elif method == 'off':
                is_active = False
            ShippingMethod.objects.filter(id=obj_id).update(is_active=bool(is_active))
            result = {
                'status': 1,
                'msg': '%s操作成功' % ('启用' if is_active else '禁用'),
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    # return JsonResponse(result)

    return JsonResponse(result)


# 添加用户
def add_user(request):
    try:
        if request.method == 'POST' and request.is_ajax():
            print request.POST['username']
            print request.POST['password']
            User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                usertype=request.POST['usertype'],
            )

            result = {
                'status': 1,
                'msg': '添加成功',
            }

        else:
            result = {
                'status': 0,
                'msg': '账户添加错误',

            }
    except Enterprise, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def order_verify(request):
    """审核订单状态 通过不通过"""

    try:
        if request.method == 'POST' and request.is_ajax():

            id_list = request.POST['id_list']
            is_pass = int(request.POST['is_pass'])
            if id_list:
                id_list = json.loads(id_list)
            # 判断is_pass
            Order.objects.filter(id__in=id_list).update(verify_state=is_pass)
            result = {
                'status': 1,
                'msg': '%s操作成功' % ('不通过' if is_pass else '通过'),
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    # return JsonResponse(result)

    return JsonResponse(result)


def get_info_publish(request, modal_name, obj_id):
    """根据id渲染info_publish模态对话框"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            obj = Informations.objects.get(pk=obj_id)
            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']
            _, modal_templ = MODAL_DICT[modal_name]
            return render(request, modal_templ, {
                'obj': obj
            })
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def delete_info_publish(request, modal_name, obj_id):
    """根据id删除某个对象"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            with transaction.atomic():
                Informations.objects.filter(id=obj_id).delete()
                result = {
                    'status': 1,
                    'msg': '删除成功',
                }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def get_consult_feedback(request, modal_name, obj_id):
    """根据id渲染consult_feedback模态对话框"""
    try:
        obj_id = int(obj_id)
        replied = None
        if request.method == 'POST' and request.is_ajax():
            obj =ConsultFeedback.objects.filter(pk=obj_id).first()
            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']
            _, modal_templ = MODAL_DICT[modal_name]
            return render(request, modal_templ, {
                'obj': obj
            })
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def delete_consult_feedback(request, obj_id):
    """根据id删除某个对象"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            with transaction.atomic():
                ConsultFeedback.objects.filter(id=obj_id).delete()
                result = {
                    'status': 1,
                    'msg': '删除成功',
                }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error(e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def replied_consult_feedback(request):
    """"回复操作"""
    try:
        obj_id = request.POST.get('obj_id')
        con_obj = ConsultFeedback.objects.filter(id=obj_id).first()
        if con_obj is not None:
            content = request.POST.get('content')
            con_obj.replied_content = content
            con_obj.is_replied = True
            con_obj.save()
            result = {
                'status': 1,
                'msg': "回复成功"
            }
        else:
            raise Exception("web端网络异常，请稍后重试")
    except Exception, e:
        log.error("replied_consult_feedback raise,Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)


def save_order(request, model_name):
    """公用保存排序
    post => [{"pk":"1","order":"1"},{"pk":"2","order":"2"}]
    
    """
    result = {
        'status': 0,
        'msg': 'sb',
    }
    try:
        if request.method == 'POST' and request.is_ajax():
            order_name = request.POST.get('order_name', '')
            order_data = request.POST.get('data', '')
            json_order_data = json.loads(order_data)
            print json_order_data
            for data in json_order_data:
                order = {}
                order[order_name] = data['value']
                MODEL_DICT[model_name].objects.filter(id=data['pk']).update(**order)
            result = {
                'status': 1,
                'msg': '修改成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.exception("save_order %s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)



def add_good(request):
    """添加商品"""
    try:
        if request.method == 'POST' and request.is_ajax():
            if request.POST.get('member_price') != '':
                request.POST.__setitem__('member_price', float(request.POST.get('member_price')) * 100)
            if request.POST.get('retail_price') != '':
                request.POST.__setitem__('retail_price', float(request.POST.get('retail_price')) * 100)
            good_form = GoodDrugAttrForm(request.POST)
            if good_form.is_valid():
                good_dict = good_form.cleaned_data
                with transaction.atomic():
                    good = Good.objects.create(
                        external_id=good_dict['external_id'],
                        name=good_dict['name'],
                        trade_name=good_dict['trade_name'],
                        brand=good_dict['brand'],
                        category_id=good_dict['category'],
                        supplier_id=good_dict['supplier'],
                        manufacturer=good_dict['manufacturer'],
                        locality=good_dict['locality'],
                        unit=good_dict['unit'],
                        prep_spec=good_dict['prep_spec'],
                        pack_spec=good_dict['pack_spec'],
                        retail_price=good_dict['retail_price'],
                        member_price=good_dict['member_price'],
                        stock_amount=good_dict['stock_amount'],
                    )
                    if good is not None:
                        for main_photo in request.FILES.getlist('main_photo'):
                            main_photo.name = str(int(time.time())) + "_%s" % main_photo.name
                            good.main_photo = main_photo
                            good.save()
                        # 商品属性
                        DrugAttr.objects.create(
                            good=good,
                            license=good_dict['license'],
                            dosage_form=good_dict['dosage_form'],
                            is_otc=bool(good_dict['is_otc']),
                            is_zybh=bool(good_dict['is_zybh']),
                            is_new=bool(good_dict['is_new']),
                            is_oem=bool(good_dict['is_oem']),
                            otc_type=good_dict['otc_type'],
                            recipe_type=good_dict['recipe_type'],
                            desc_drug=good_dict['desc_drug'],
                            desc_good=good_dict['desc_good'],
                        )
                        # 上传商品图片和商品资质
                        photo_index = 1
                        for good_photo in request.FILES.getlist('good_photo'):
                            good_photo.name = str(int(time.time())) + "_%s" % good_photo.name
                            GoodPhoto.objects.create(
                                good=good,
                                order_no=photo_index,
                                photo=good_photo,
                                upload_man=request.user
                            )
                            photo_index += 1
                        for good_qua in request.FILES.getlist('good_qua'):
                            good_qua.name = str(int(time.time())) + "_%s" % good_qua.name
                            GoodQualification.objects.create(
                                good=good,
                                photo=good_qua,
                                upload_man=request.user
                            )
                result = {
                    'status': 1,
                    'msg': '添加成功',
                }
            else:
                result = {
                    'status': 0,
                    'msg': '商品信息输入不完整',
                }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.exception("add_good raise , Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def get_good_form(request, modal_name, obj_id):
    """根据id渲染good模态对话框"""
    try:
        enter_select = []
        dosage_form_select = []
        category_select = []
        good_photo = []
        qualification = []
        if request.method == 'POST' and request.is_ajax():
            obj = Good.objects.get(id=obj_id)
            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']
            _, modal_templ = MODAL_DICT[modal_name]
            if obj is not None:
                setting_type = SettingsType.objects.filter(code='DOSAGE_FORM').first()
                if setting_type is not None:
                    dosage_form_select = SettingsItem.objects.filter(s_type=setting_type)
                enter_select = Enterprise.objects.all()
                category_select = GoodCategory.objects.exclude(path='/').order_by('path')
                good_photo = obj.goodphoto_set.all()
                qualification = obj.goodqualification_set.all()
            return render(request, modal_templ, {
                'obj': obj,
                'enter_select': enter_select,  # 企业列表下拉框数据
                'dosage_form_select': dosage_form_select,  # 剂型下拉框数据
                'category_select': category_select,  # 分类下拉框数据
                'good_photo': good_photo,
                'qualification': qualification,
            })
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.error("get_good_form raise,Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def delete_good(request, obj_id):
    """根据id删除某个对象"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            with transaction.atomic():
                # 删除商品图片 ，资质图， 相关属性， 商品本身
                GoodPhoto.objects.filter(good_id=obj_id).delete()
                GoodQualification.objects.filter(good_id=obj_id).delete()
                DrugAttr.objects.filter(good_id=obj_id).delete()
                Good.objects.filter(pk=obj_id).delete()
                result = {
                    'status': 1,
                    'msg': '删除成功',
                }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.exception("delete_good raise ,Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def update_good(request):
    """更新商品"""
    try:
        if request.method == 'POST' and request.is_ajax():
            if request.POST.get('member_price') != '':
                request.POST.__setitem__('member_price', float(request.POST.get('member_price')) * 100)
            if request.POST.get('retail_price') != '':
                request.POST.__setitem__('retail_price', float(request.POST.get('retail_price')) * 100)
            good_form = GoodDrugAttrForm(request.POST)
            if good_form.is_valid():
                good_dict = good_form.cleaned_data
                with transaction.atomic():
                    up_good = Good.objects.filter(id=good_dict['fk_good_id']).first()
                    if up_good is not None:
                        # 更新商品属性
                        up_good.external_id = good_dict['external_id']
                        up_good.name = good_dict['name']
                        up_good.trade_name = good_dict['trade_name']
                        up_good.brand = good_dict['brand']
                        up_good.category_id = good_dict['category']
                        if good_dict['supplier'] != '':
                            up_good.supplier_id = good_dict['supplier']
                        up_good.manufacturer = good_dict['manufacturer']
                        up_good.locality = good_dict['locality']
                        up_good.unit = good_dict['unit']
                        up_good.prep_spec = good_dict['prep_spec']
                        up_good.pack_spec = good_dict['pack_spec']
                        if good_dict['retail_price'] != '':
                            up_good.retail_price = good_dict['retail_price']
                        if good_dict['member_price'] != '':
                            up_good.member_price = good_dict['member_price']
                        up_good.stock_amount = good_dict['stock_amount']
                        up_good.save()
                        # 更新商品主图
                        for main_photo in request.FILES.getlist('main_photo'):
                            main_photo.name = str(int(time.time())) + "_%s" % main_photo.name
                            up_good.main_photo = main_photo
                            up_good.save()

                        # 更新商品具体属性
                        drug_attr = DrugAttr.objects.filter(good_id=up_good.id).first()
                        if drug_attr is not None:
                            drug_attr.license = good_dict['license']
                            drug_attr.dosage_form = good_dict['dosage_form']
                            drug_attr.is_otc = bool(good_dict['is_otc'])
                            drug_attr.is_zybh = bool(good_dict['is_zybh'])
                            drug_attr.is_new = bool(good_dict['is_new'])
                            drug_attr.is_oem = bool(good_dict['is_oem'])
                            drug_attr.otc_type = good_dict['otc_type']
                            drug_attr.recipe_type = good_dict['recipe_type']
                            drug_attr.desc_drug = good_dict['desc_drug']
                            drug_attr.desc_good = good_dict['desc_good']
                            drug_attr.save()
                        else:
                            DrugAttr.objects.create(
                                good=up_good,
                                license=good_dict['license'],
                                dosage_form=good_dict['dosage_form'],
                                is_otc=bool(good_dict['is_otc']),
                                is_zybh=bool(good_dict['is_zybh']),
                                is_new=bool(good_dict['is_new']),
                                is_oem=bool(good_dict['is_oem']),
                                otc_type=good_dict['otc_type'],
                                recipe_type=good_dict['recipe_type'],
                                desc_drug=good_dict['desc_drug'],
                                desc_good=good_dict['desc_good'],
                            )
                        pho_ids = request.POST.get('pho_id')
                        qua_ids = request.POST.get('qua_id')

                        # 删除不需要保留商品主图
                        if pho_ids:
                            pho_ids_list = json.loads(pho_ids)
                            for key in pho_ids_list:
                                del_photo = GoodPhoto.objects.filter(id=key).first()
                                if del_photo is not None:
                                    del_photo.photo.delete()
                                    del_photo.delete()
                        else:  # 删除所有原有商品主图
                            GoodPhoto.objects.filter(good_id=up_good.id).delete()

                        # 删除不需要的资质图
                        if qua_ids:
                            qua_ids_list = json.loads(qua_ids)
                            for key in qua_ids_list:
                                del_qua = GoodQualification.objects.filter(id=key).first()
                                if del_qua is not None:
                                    del_qua.photo.delete()
                                    del_qua.delete()
                        else:  # 删除所有原有商品主图
                            GoodQualification.objects.filter(good_id=up_good.id).delete()

                        # 上传新的商品主图和商品资质
                        good_photo_files = request.FILES.getlist('good_photo')
                        order_no = 1
                        for good_photo in good_photo_files:
                            good_photo.name = str(int(time.time())) + "_%s" % good_photo.name
                            GoodPhoto.objects.create(
                                good=up_good,
                                order_no=order_no,
                                photo=good_photo,
                                upload_man=request.user
                            )
                            order_no += 1
                        for good_qua in request.FILES.getlist('good_qua'):
                            good_qua.name = str(int(time.time())) + "_%s" % good_qua.name
                            GoodQualification.objects.create(
                                good=up_good,
                                photo=good_qua,
                                upload_man=request.user
                            )
                result = {
                    'status': 1,
                    'msg': '保存成功',
                }
            else:
                result = {
                    'status': 0,
                    'msg': '商品信息输入异常',
                }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.exception("update_good raise,Error:" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def switch_drug_online(request, method, obj_id):
    """商品上架下架"""
    try:
        if request.method == 'POST' and request.is_ajax():
            is_online = ''
            if method == 'on':
                is_online = 1
            elif method == 'off':
                is_online = 2
            good = Good.objects.filter(pk=obj_id).first()
            if good is not None:
                good.is_online = is_online
                good.online_time = datetime.datetime.now()
                good.save()
            result = {
                'status': 1,
                'msg': '修改成功',
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.exception("switch_drug_online raise,Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def get_good_byid(request, modal_name, obj_id):
    """根据商品ID获取商品详情"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            model_class, modal_templ = MODAL_DICT[modal_name]
            obj = model_class.objects.get(pk=obj_id)
            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']
            good_photo = []
            qualification = []
            if obj is not None:
                good_photo = obj.goodphoto_set.all()
                qualification = obj.goodqualification_set.all()
            result = {
                'obj': obj,
                'good_photo': good_photo,
                'qualification': qualification
            }
            return render(request, modal_templ, result)
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.exception("get_good_byid raise ,Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def check_good_status(request):
    """ 审核商品 """
    try:
        if request.method == 'POST' and request.is_ajax():
            op_type = request.POST.get('op_type')
            obj_id = request.POST.get('obj_id')
            with transaction.atomic():
                if op_type == 'ref':  # 拒绝
                    good = Good.objects.filter(id=obj_id).first()
                    if good is not None:
                        good.is_qualified = 3
                        good.save()
                else:  # 通过并上架
                    good = Good.objects.filter(id=obj_id).first()
                    if good is not None:
                        good.is_qualified = 2
                        good.online_time = datetime.datetime.now()
                        good.is_online = 1
                        good.save()
            result = {
                'status': 1,
                'msg': '修改成功'
            }
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.exception("ajax.check_good_status,error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)


def add_role_byform(request):
    """添加角色"""
    try:
        if request.method == 'POST' and request.is_ajax():
            role_form = RoleAttrForm(request.POST)
            if role_form.is_valid():
                with transaction.atomic():
                    role_dict = role_form.cleaned_data
                    Role.objects.create(
                        name=role_dict['name'],
                        usertype=role_dict['usertype'],
                        desc=role_dict['desc']
                    )
                    result = {
                        'status': 1,
                        'msg': "保存成功"
                    }
            else:
                raise Exception("输入参数异常")
    except Exception, e:
        log.exception("request raise Exception,%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)


def update_role_byform(request):
    """添加角色"""
    try:
        if request.method == 'POST' and request.is_ajax():
            role_form = RoleAttrForm(request.POST)
            if role_form.is_valid():
                with transaction.atomic():
                    role_id = request.POST.get('role_id')
                    role_dict = role_form.cleaned_data
                    role = Role.objects.filter(id=role_id).first()
                    if role is not None:
                        role.name = role_dict['name']
                        role.desc = role_dict['desc']
                        role.usertype = role_dict['usertype']
                        role.save()
                        result = {
                            'status': 1,
                            'msg': "保存成功"
                        }
                    else:
                        raise Exception("web端异常，请稍后刷新重试")
            else:
                raise Exception("输入参数异常")
    except Exception, e:
        log.exception("request raise Exception,%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)


def del_role_byid(request, obj_id):
    """删除角色:用户表已经配置级联保护，权限表已配置权限级联删除"""
    try:
        if request.method == 'POST' and request.is_ajax():
            with transaction.atomic():
                del_role = Role.objects.filter(id=obj_id).first()
                del_role.user_set.clear()  # 清除用户角色关系
                del_role.rolepermission_set.all().delete()  # 清除角色权限关系
                del_role.delete()  # 删除角色
                result = {
                    'status': 1,
                    'msg': '删除成功'
                }
        else:
            raise Exception('请求异常')
    except Exception, e:
        log.exception("del_role_byid raise, Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)


def get_this_perm_role(request):
    """获取当前角色所有权限"""
    try:
        if request.method == 'POST' and request.is_ajax():
            role_id = request.POST.get("role_id")
            role_perms = RolePermission.objects.filter(role_id=role_id)
            perm_lst = []
            for item in role_perms:
                perm_lst.append({'codename': item.codename})
            result = {
                'status': 1,
                'perm_lst': json.dumps(perm_lst)
            }
    except Exception, e:
        log.exception("get_this_perm_role raise, Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)

def grant_role_permission(request):
    """授权：将角色和权限关联"""
    try:
        if request.method == 'POST' and request.is_ajax():
            with transaction.atomic():
                role_id = request.POST.get("role_id")
                role = Role.objects.filter(id=role_id).first()
                if role is not None:
                    RolePermission.objects.filter(role_id=role_id).delete()
                    perm_code = request.POST.get("perm_code")
                    perm_codes = json.loads(perm_code)
                    for perm in perm_codes:
                        RolePermission.objects.create(
                            role=role,
                            codename=perm
                        )
                    result = {
                        'status': 1,
                        'msg': '授权成功'
                    }
                else:
                    raise Exception("数据异常，请刷新后重试")
        else:
            raise Exception("请求异常")
    except Exception, e:
        log.exception("grant_role_permission raise, Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)


def get_refund_form(request, modal_name, obj_id):
    """后台:获取退款退货信息"""
    try:
        if request.method == 'POST' and request.is_ajax():
            obj = RefundRecord.objects.get(id=obj_id)
            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']
            _, modal_templ = MODAL_DICT[modal_name]
            # 订单列表详情
            order_items = obj.order.orderitem_set.all()
            # 退款操作日志
            kwargs = {}
            kwargs['data_type'] = REFUND_MODAL
            kwargs['data_id'] = obj.id
            op_logs = OperateRecord.objects.filter(**kwargs).order_by("-created")
            result = {
                'obj': obj,
                'order_items': order_items,
                'op_logs': op_logs
            }
            return render(request, modal_templ, result)
        else:
            raise Exception('异常请求')
    except Exception, e:
        log.exception("get_refund_form raise,Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def get_order_log(request, modal_name, obj_id):
    """获取订单日志"""
    try:
        if request.method == 'POST' and request.is_ajax():
            obj = Order.objects.filter(pk=obj_id).first()
            obj.csrfmiddlewaretoken = request.POST['csrfmiddlewaretoken']
            _, modal_templ = MODAL_DICT[modal_name]

            # 退款操作日志
            kwargs = {}
            kwargs['data_type'] = ORDER_MODAL
            kwargs['data_id'] = obj.id
            op_logs = OperateRecord.objects.filter(**kwargs).order_by("-created")
            result = {
                'obj': obj,
                'op_logs': op_logs
            }
            return render(request, modal_templ, result)
        else:
            raise Exception("请求异常")
    except Exception, e:
        log.exception("get_order_log raise,Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
    return result


def order_no_check(request, obj_id):
    """订单编号查看"""
    try:
        obj_id = int(obj_id)
        if request.method == 'POST' and request.is_ajax():
            user_pk = request.user.id
            pk = int(obj_id)
            order = Order.objects.filter(pk=pk).first()
            user = User.objects.filter(pk=int(user_pk)).first()
            return render(request, 'dtsadmin/modals/modal_approve_look_order.html', {
                'order': order,
                'user': user,
            })
        else:
            raise Exception('系统忙,请稍后再试')
    except Exception, e:
        log.exception("dtsadmin.ajax.order_no_check Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e),
        }
        return JsonResponse(result)