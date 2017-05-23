# coding=UTF-8
from django.http import JsonResponse
from common.utils.utils_log import log
from good.models import LackRegister
from order.models import MyFavorites, ShoppingCartItem, ReceivingAddress
import simplejson as json
from django.conf import settings
# 短信验证
from common.sms import make_sms
from common.utils.utils_sms import send_sms
from functools import wraps
import re
from dtsauth.models import User
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

MODEL_DICT = {
    'LackRegister': LackRegister,
    'ReceivingAddress': ReceivingAddress,
}


def test_upload_file(request):
    """测试上传图片"""
    from .forms import TestUploadFileForm
    try:
        if request.method == 'POST' and request.is_ajax():
            for photo in request.FILES.getlist('photo'):
                form = TestUploadFileForm(request.POST, {'photo': photo})
                if form.is_valid():
                    form.save()
            result = {
                'status': 1,
                'msg': '上传成功',
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


def add_user(request):
    """添加缺货"""
    try:
        if request.method == 'POST' and request.is_ajax():
            print request.POST['username']
            print request.POST['password']
            LackRegister.objects.create_user(
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
    except LackRegister, e:
        result = {
            'status': 0,
            'msg': str(e),
        }
    return JsonResponse(result)


def delete_favorites(request):
    #####################################删除收藏############################################################
    try:
        user_pk = request.user.id
        list_pk = json.loads(request.POST.get('pk', '[]'))
        if request.method == 'POST' and request.is_ajax():
            MyFavorites.objects.filter(pk__in=list_pk, coll_user__pk=user_pk).delete()
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


def add_shopping_cart(request):
    try:
        list_pk = json.loads(request.POST.get('pk', '[]'))
        if request.method == 'POST' and request.is_ajax():
            kwargs = {}
            kwargs['buyer'] = request.user
            for good in list_pk:
                obj = ShoppingCartItem.objects.filter(buyer=request.user).filter(good_id=good["pk"]).first()
                if obj:
                    obj.quantity = obj.quantity + int(good["num"])
                    obj.save()
                else:
                    kwargs['good_id'] = good["pk"]
                    kwargs['quantity'] = good["num"]
                    ShoppingCartItem.objects.update_or_create(**kwargs)
                result = {
                    'status': 1,
                    'msg': '添加成功',
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


def set_default(request, obj_id):
    """设置默认地址"""
    try:
        if request.method == 'POST' and request.is_ajax():
            is_default = ReceivingAddress.objects.filter(is_default=True)
            if is_default:
                ReceivingAddress.objects.update(is_default=False)
            kwargs = {'is_default': bool(int(request.POST['is_lock']))}
            p = ReceivingAddress.objects.filter(pk=obj_id).update(**kwargs)
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


def send_validate_code(request):
    """发送验证码"""
    result = {
        'status': 0,
        'msg': '网络异常，请稍后刷新重试'
    }
    try:
        if request.method == 'POST' and request.is_ajax():
            # 验证电话号码
            phone = request.POST.get('phone', '')
            phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$')
            is_phone = phone_re.match(phone)
            if is_phone:
                #  判断这个用户存在与否
                is_phone_exist = User.objects.filter(phone=str(phone)).first()
                if is_phone_exist:
                    # # 避免多次发送短信
                    # request.session.set_expiry(180)
                    # phone_session = request.session.get('account_safety', '')
                    # if phone_session:
                    #     result = {
                    #         'status': 0,
                    #         'msg': u'验证码已经发送，请注意查收'
                    #     }
                    #     return JsonResponse(result)
                    # 发送验证码
                    sms_msg = make_sms()
                    c = CaptchaStore()
                    # 把验证码存入session
                    request.session['account_safety'] = sms_msg[1]
                    # 存库
                    c.response = sms_msg[1]
                    c.challenge = phone
                    c.save()
                    result = {
                        'status': 1,
                        'msg': '验证码已经发送，请注意查收'
                    }
                    # 测试 可不发短信 去CaptchaStore中查看验证码
                    if not settings.DEBUG:
                        send_sms([phone], sms_msg[0])
                        result = {
                            'status': 1,
                            'key': c.hashkey,

                        }
                        return JsonResponse(result)
                else:
                    # result = {
                    #     'status': 0,
                    #     'msg': u'这个电话没有注册，请先注册'
                    # }
                    # return JsonResponse(result)
                    raise Exception('这个电话没有注册，请先注册')
            else:
                result = {
                    'status': 0,
                    'msg': '请输入正确的电话号码'
                }
                return JsonResponse(result)
        else:
            raise Exception("请求异常")
    except Exception, e:
        log.exception("send_validate_code raise, Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)


def send_validate_code_new(request):
    """发送验证码"""
    result = {
        'status': 0,
        'msg': '网络异常，请稍后刷新重试'
    }
    try:
        if request.method == 'POST' and request.is_ajax():
            # 验证电话号码
            phone = request.POST.get('phone', '')
            phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$')
            is_phone = phone_re.match(phone)
            if is_phone:
                    # 发送验证码
                    sms_msg = make_sms()
                    c = CaptchaStore()
                    # 把验证码存入session
                    request.session['account_safety'] = sms_msg[1]
                    # 存库
                    c.response = sms_msg[1]
                    c.challenge = phone
                    c.save()
                    result = {
                        'status': 1,
                        'msg': '验证码已经发送，请注意查收'
                    }
                    # 测试 可不发短信 去CaptchaStore中查看验证码
                    if not settings.DEBUG:
                        send_sms([phone], sms_msg[0])
                        result = {
                            'status': 1,
                            'key': c.hashkey,
                        }
                        return JsonResponse(result)
            else:
                result = {
                    'status': 0,
                    'msg': '请输入正确的电话号码'
                }
                return JsonResponse(result)
        else:
            raise Exception("请求异常")
    except Exception, e:
        log.exception("send_validate_code_new raise, Error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)

