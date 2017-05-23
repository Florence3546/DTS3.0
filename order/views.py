# coding=UTF-8
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, get_object_or_404
from django.http import JsonResponse, Http404, HttpResponse
from .models import MyFavorites, Order, OrderItem, ShoppingCartItem
from good.models import Good

from django.db import transaction
from django.db.models import F
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from common.utils.utils_log import log
import simplejson as json





class CartView(View):
    """购物车api"""
    def get(self, request):
        pass
    def post(self, request):
        if not request.user.is_authenticated():
            # return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)
            result = {
                'status': 0,
                'msg': "请登录后 再添加到购物车",
                'url': '/eshop/user_login/?next=%s' % request.path
            }
            return JsonResponse(result)

        if 'method' in request.POST:
            method = request.POST.get('method', '')

            if method == 'add_cart':
                count = int(request.POST.get('count', 1))
                gid = int(request.POST.get('gid', ''))
                good = Good.objects.filter(id=gid).first()
                # 查询该用户购物车中是否存在改商品，并计算最终商品数量
                sci = ShoppingCartItem.objects.filter(buyer=request.user, good=good).first()
                if sci:
                    count += sci.quantity
                good = Good.objects.filter(id=gid, stock_amount__gte=count).first()
                if good:
                    return self._handle_add_cart(request)
                else:
                    result = {
                        'status': 0,
                        'msg': "超过库存，请重新输入"
                    }

            else:
                result = {
                    'status': 0,
                    'msg': "请求method错误"
                }


        else:
            result = {
                'status': 0,
                'msg': "post请求错误"
            }
        return JsonResponse(result)

    def _handle_add_cart(self, request):

        if 'action' in request.POST:
            user_id = request.user.id
            id_list = json.loads(request.POST.get('id_list', '[]'))
            action = request.POST.get('action', '')

            # 单个加入购物车
            if 'add' == action:
                try:
                    good = int(request.POST.get('gid', ''))
                    quantity = int(request.POST.get('count', ''))
                    # 失效商品不能添加购物车中
                    is_good = Good.objects.filter(id=good, is_online=1, is_qualified=2, stock_amount__gt=0)
                    if not is_good:
                        result = {
                            'status': 1,
                            'msg': '加入购物车失败,商品失效',
                        }
                        return JsonResponse(result)
                    is_good_in_cart = ShoppingCartItem.objects.filter(
                        buyer=request.user,
                        good_id=good
                    )
                    if is_good_in_cart:
                        ShoppingCartItem.objects.filter(
                            buyer=request.user,
                            good_id=good
                        ).update(
                            quantity=F('quantity') + quantity
                        )
                        cart_count = ShoppingCartItem.objects.filter(buyer=request.user)
                        result = {
                            'status': 1,
                            'msg': '再加入购物车成功',
                            'count': cart_count.count()
                        }
                    else:
                        ShoppingCartItem.objects.create(
                            buyer=request.user,
                            good_id=good,
                            quantity=quantity
                        )
                        cart_count = ShoppingCartItem.objects.filter(buyer=request.user)
                        result = {
                            'status': 1,
                            'msg': '加入购物车成功',
                            'count': cart_count.count()
                        }
                    return JsonResponse(result)
                except Exception, e:
                    log.error('MyFavoritesView _handle_my_favorites add %s' % e)
                    result = {
                        'status': 0,
                        'msg': '加入购物车失败 %s' % e,
                        'log': e
                    }
                    return JsonResponse(result)


            # 移除购物车
            elif 'remove' == action:
                try:
                    with transaction.atomic():
                        favorites = MyFavorites.objects.filter(coll_user=request.user, pk__in=id_list).delete()
                        result = {
                            'status': 1,
                            'msg': '移除成功'
                        }
                        return JsonResponse(result)
                except Exception, e:
                    log.error('MyFavoritesView _handle_my_favorites add %s' % e)
                    result = {
                        'status': 0,
                        'msg': '移除失败'
                    }
                    return JsonResponse(result)

        else:
            result = {
                'status': 1,
                'msg': '请求action错误',
            }
        return JsonResponse(result)




class MyFavoritesView(View):
    """我的收藏api"""

    def get(self, request):
        gid = int(request.GET.get('gid', ''))
        # get_object_or_404(MyFavorites, coll_good_id=gid)
        favorites = MyFavorites.objects.filter(coll_good=gid)
        if favorites:
            result = {
                'status': 1,
                'msg': u'已经收藏了'
            }
        else:
            result = {
                'status': 0,
                'msg': u'没有收藏'
            }
        return JsonResponse(result)


    # @method_decorator(login_required('/eshop/user_login/'))
    def post(self, request):
        if not request.user.is_authenticated():
            # return HttpResponseRedirect('/eshop/user_login/?next=%s' % request.path)
            result = {
                'status': 0,
                'msg': "请登录后 再收藏",
                'url': '/eshop/user_login/?next=%s' % request.path
            }
            return JsonResponse(result)

        if 'method' in request.POST:
            method = request.POST.get('method', '')

            if method == 'my_favorites':
                return self._handle_my_favorites(request)

            else:
                result = {
                    'status': 0,
                    'msg': "请求method错误"
                }


        else:
            result = {
                'status': 0,
                'msg': "post请求错误"
            }
        return JsonResponse(result)


    def _handle_my_favorites(self, request):
        if 'action' in request.POST:
            user_id = request.user.id
            id_list = json.loads(request.POST.get('id_list', '[]'))
            action = request.POST.get('action', '')

            # 加入收藏
            if 'add' == action:
                # 如果之前加入过
                is_favorites = MyFavorites.objects.filter(coll_good__pk__in=id_list)
                if is_favorites:
                    result = {
                        'status': 1,
                        'msg': '您已经收藏过了'
                    }
                    return JsonResponse(result)
                try:
                    with transaction.atomic():
                        for good_id in id_list:
                            favorites = MyFavorites.objects.update_or_create(
                                coll_user_id=user_id,
                                coll_good_id=int(good_id)
                            )
                        result = {
                            'status': 1,
                            'msg': '收藏成功'
                        }
                        return JsonResponse(result)
                except Exception, e:
                    log.error('MyFavoritesView _handle_my_favorites add %s' % e)
                    result = {
                        'status': 0,
                        'msg': '收藏失败',
                        'log': e
                    }
                    return JsonResponse(result)


            # 移除收藏
            elif 'remove' == action:
                try:
                    with transaction.atomic():
                        favorites = MyFavorites.objects.filter(coll_user=request.user, pk__in=id_list).delete()
                        result = {
                            'status': 1,
                            'msg': '移除成功'
                        }
                        return JsonResponse(result)
                except Exception, e:
                    log.error('MyFavoritesView _handle_my_favorites add %s' % e)
                    result = {
                        'status': 0,
                        'msg': '移除失败'
                    }
                    return JsonResponse(result)

        else:
            result = {
                'status': 1,
                'msg': '请求action错误',
            }
        return JsonResponse(result)





