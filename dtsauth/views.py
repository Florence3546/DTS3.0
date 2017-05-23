from django.http import HttpResponse
from django.shortcuts import render

from common.utils.utils_log import log


def test(request):
    log.info('test')
    return HttpResponse('test')
