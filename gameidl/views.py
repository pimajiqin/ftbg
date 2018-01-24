#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author: 陈二狗

from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render_to_response
from gameidl.models import GameIdlReply
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from gameidl.getdata import *
from django.http import HttpResponseRedirect


def replylist(request):
    try:
        request.COOKIES["username"] and request.session['username']
        username = request.COOKIES['username']

        contact_list = GameIdlReply.objects.order_by('-id')
        paginator = Paginator(contact_list, 15)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'gameidl/replylist.html', {'contacts': contacts})
    except:
        return HttpResponseRedirect("/accounts/login")




def reviews(request, src):
    try:
        request.COOKIES["username"] and request.session['username']
        username = request.COOKIES['username']

        if request.method == "POST" and request.POST:
            developertext = request.POST['developertext']
            replyseconds = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            dt = GameIdlReply.objects.get(id=src)
            dt.developertext = developertext
            dt.replyseconds = replyseconds
            dt.save()
            reviewsid = dt.reviewId
            text = developertext
            atoken = get_atoken()[0]
            replymessage(reviewsid, atoken, text)
            return render_to_response("gameidl/replylist.html", locals())
        else:
            one_reply = GameIdlReply.objects.get(id=src)
            return render_to_response("gameidl/reviews.html", locals())

    except:
        return HttpResponseRedirect("/accounts/login")



# def replylist(request):
#     contact_list = GameIdlReply.objects.order_by('-id')
#     paginator = Paginator(contact_list, 15)  # Show 15 contacts per page
#
#     page = request.GET.get('page')
#     try:
#         contacts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         contacts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         contacts = paginator.page(paginator.num_pages)
#
#     return render(request, 'gameidl/replylist.html', {'contacts': contacts})

# def reviews(request, src):
#     if request.method == "POST" and request.POST:
#         developertext = request.POST['developertext']
#         replyseconds = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         dt = GameIdlReply.objects.get(id=src)
#         dt.developertext = developertext
#         dt.replyseconds = replyseconds
#         dt.save()
#         reviewsid = dt.reviewId
#         text = developertext
#         atoken = get_atoken()[0]
#         replymessage(reviewsid, atoken, text)
#         return render_to_response("gameidl/replylist.html", locals())
#     else:
#         one_reply = GameIdlReply.objects.get(id=src)
#         return render_to_response("gameidl/reviews.html", locals())
