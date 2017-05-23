# coding:UTF-8
import views
from django.conf.urls import url
from common.views import page_error, page_not_found, page_forbidden

app_name = 'common'


urlpatterns = [
    url(r'^GenerateCheckCode/$', views.GenerateCheckCode, name='GenerateCheckCode'),
    url(r'^validate_checkCode/$', views.validate_checkCode, name='validate_checkCode'),
    url(r'^403/$', views.page_forbidden, name='page_forbidden'),
    url(r'^404/$', views.page_not_found, name='page_not_found'),
    url(r'^500/$', views.page_error, name='page_error'),
]
handler403 = page_forbidden
handler404 = page_not_found
handler500 = page_error