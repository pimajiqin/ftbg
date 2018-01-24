#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: 陈二狗

from django.conf.urls import include, url
from django.contrib import admin
from gameidl.views import replylist

urlpatterns = [
    url(r'replylist/$', 'gameidl.views.replylist'),
    url(r'replylist/(\w+)', 'gameidl.views.reviews')
]