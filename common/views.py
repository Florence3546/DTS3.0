# coding:UTF-8
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
import StringIO
import utils.util_check_code as Checkcode
from utils.utils_log import log
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def GenerateCheckCode(request):
    """生成验证码"""
    mstream = StringIO.StringIO()
    validate_code = Checkcode.create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
    # 将验证码保存到session
    request.session["CheckCode"] = validate_code[1]
    return HttpResponse(mstream.getvalue(), 'image/gif')


def validate_checkCode(request):
    """ajax校验验证码"""
    try:
        if request.method == 'POST' and request.is_ajax():
            if 'captcha' in request.POST:
                captcha = request.POST.get('captcha')
                if captcha.upper() == request.session['CheckCode'].upper():
                    result = {
                        'status': 1,
                        'msg': "验证码验证通过"
                    }
                else:
                    result = {
                        'status': 0,
                        'msg': "验证码输入有误"
                    }
            else:
                raise Exception('请求异常')
        else:
            raise Exception('请求异常')
    except Exception, e:
        log.exception("validate_checkCode error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)


@csrf_exempt
def page_forbidden(request):
    return render(request, '403.html')


@csrf_exempt
def page_not_found(request):
    return render(request, '404.html')


@csrf_exempt
def page_error(request):
    return render(request, '500.html')

