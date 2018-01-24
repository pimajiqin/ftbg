#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: 陈二狗
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def index(request):
    try:
        request.COOKIES["username"] and request.session['username']
        username = request.COOKIES['username']
        return render_to_response("index.html", locals())
    except:
        return HttpResponseRedirect("/accounts/login")
