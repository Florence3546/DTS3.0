# coding=UTF-8
from django.http import JsonResponse
from common.utils.utils_log import log
from .models import LackRegister


def create_lack_register(request):
    """添加缺货登记"""
    try:
        if request.method == 'POST' and request.is_ajax():
            kwargs = {}
            kwargs['people'] = request.user
            good_id = int(request.POST['good_id'])
            flag = LackRegister.objects.filter(good__id=good_id)
            if flag:
                result = {
                    'status': 0,
                    'msg': '您已登记该物品，无法重复登记！'
                }
            else:
                kwargs['good_id'] = good_id
                kwargs['note'] = request.POST.get('note', '')
                LackRegister.objects.create(**kwargs)
                result = {
                    'status': 1,
                    'msg': '缺货登记成功'
                }
    except Exception, e:
        log.error("lack_register,error:%s" % e)
        result = {
            'status': 0,
            'msg': str(e)
        }
    return JsonResponse(result)
