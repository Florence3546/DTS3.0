# coding:UTF-8

from django.shortcuts import render
from django.utils.decorators import wraps
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from common.utils.utils_log import log


def perm_check(request, codename):
    """验证权限"""
    try:
        if codename is not None:
            if request.user.has_perm(codename):
                log.info('perm_check info: ====》权限已匹配')
                return True
            else:
                log.info('perm_check info: ====》权限没有匹配')
                return False
        else:
            return False
    except Exception, e:
        log.error("perm_check raise exception,error:%s" % e)
        return False


def check_permission(codename=[]):
    """定义一个装饰器，在views中应用"""
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated():  # 判断用户是否登录
                if perm_check(request, codename):
                    return func(request, *args, **kwargs)
                # return render(request, 'auth/../common/templates/403.html', locals())
                return render(request,'403.html',locals())
            else:
                return HttpResponseRedirect('/eshop/user_login/')
        return returned_wrapper
    return decorator
