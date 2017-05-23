# coding=UTF-8
from django.conf.urls import url
import views
from .views import MyFavoritesView, CartView

app_name = 'order'
urlpatterns = [
    url(r'^my_favorites/$', MyFavoritesView.as_view(), name='my_favorites'),
    url(r'^cart/$', CartView.as_view(), name='cart')
]
