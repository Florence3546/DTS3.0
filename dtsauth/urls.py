# coding=UTF-8
from django.conf.urls import url
import views

app_name = 'dtsauth'
urlpatterns = [
    url(r'^test/$', views.test, name='test'),
]
