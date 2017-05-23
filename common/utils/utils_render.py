# coding=UTF-8
from django.shortcuts import render_to_response
from django.template import RequestContext


def render_to_error(request = None, msg = '', back = '', context = {}, template = 'error.html'):
    '''经过认证的用户，发生操作错误的跳转页(有菜单栏和返回链接)'''
    if not msg:
        if context.has_key('msg'):
            msg = context['msg']
        else:
            msg = "访问错误,请确认"
    if not back:
        if context.has_key('back'):
            back = context['back']
        elif request:
            back = request.path
        else:
            back = "/"
    context['msg'] = msg
    context['back'] = back
    context['error'] = True

    if request.session.get('platform', '') in ['qnpc', 'qnyd']:
        template = request.session['platform'] + '_error.html'

    if request:
        return render_to_response(template, context, context_instance = RequestContext(request))
    else:
        return render_to_response(template, context)

def render_to_limited(request = None, msg = '', context = {}, template = 'limited.html'):
    '''限制登录权限的用户，认证受限，需要重新登录或退出的跳转页(无菜单栏和返回链接)'''
    if not msg:
        if context.has_key('msg'):
            msg = context['msg']
        else:
            msg = "访问错误,请确认"
    context['msg'] = msg
    context['error'] = True

    if request.session.get('platform', '') in ['qnpc', 'qnyd']:
        template = request.session['platform'] + '_limited.html'

    if request:
        return render_to_response(template, context, context_instance = RequestContext(request))
    else:
        return render_to_response(template, context)
