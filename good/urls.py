# coding=UTF-8
from django.conf.urls import include, url
import ajax
import views

app_name = 'good'

ajax_patterns = ([
    url(r'^create_lack_register/$', ajax.create_lack_register, name='create_lack_register'),
], 'ajax')

urlpatterns = [
    url(r'^ajax/', include(ajax_patterns)),
]
