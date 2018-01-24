#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: 陈二狗

from __future__ import unicode_literals
from gameidl.models import GameIdlReply

import urllib2, urllib
import json
import time
from config import *

# 获取google token 加上时间戳
def get_atoken():
    f = urllib2.urlopen(
        url = url,
        data = urllib.urlencode(data)
        )
    a = f.read()
    text = json.loads(a)
    atoken = text['access_token']
    global firsttime
    firsttime = int(time.time())
    return atoken , firsttime


# 比较时间如果少于3000秒则不需要重新获取token
def diff(first):
    secondtime = int(time.time())
    if secondtime - first <= 3000:
        pass
    else:
        global atoken
        atoken = (get_atoken()[0])
        return atoken


# 获取20条评论列表
def get_list():
    atoken = get_atoken()[0]
    url = Scope
    textmod = {'access_token': atoken}
    textmod = urllib.urlencode(textmod)
    req = urllib2.Request(url='%s%s%s&maxResults=20' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    res = res.read()
    dataall = json.dumps(json.loads(res), ensure_ascii=False)
    dataalljson = json.loads(dataall)
    return dataalljson


# 根据reviewId判断数据库中是否有重复，如果重复返回False
def repeat(rid):
    a = 0
    for i in GameIdlReply.objects.order_by('-id')[0:40]:
        if i.reviewId == rid.encode('utf-8'):
            a = 1
        else:
            a = a
    if a > 0:
        return True
    else:
        return False


# 把时间戳转换为时间格式
def timeconversion(seconds):
    #转换int
    timestamp = int(seconds)
    #转换成localtime
    time_local = time.localtime(timestamp)
    #转换成新的时间格式
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return dt


# 把评论存到数据库中
def savadb(data):

    comments = data['comments'][0]
    userComment = comments['userComment']
    lastModified = userComment['lastModified']
    deviceMetadata = userComment['deviceMetadata']

    onereply = GameIdlReply()

    if repeat(data.get('reviewId')):
        print "haha"
    else:
        onereply.reviewId = data.get('reviewId')
        onereply.authorName = data.get('authorName')
        onereply.text = userComment.get('text')
        onereply.seconds = lastModified.get('seconds')
        onereply.time = timeconversion(onereply.seconds)
        onereply.nanos = lastModified.get('nanos')
        onereply.starRating = userComment.get('starRating')
        onereply.device = userComment.get('device')
        onereply.reviewerLanguage = userComment.get('reviewerLanguage')
        onereply.androidOsVersion = userComment.get('androidOsVersion')
        onereply.appVersionCode = userComment.get('appVersionCode')
        onereply.appVersionName = userComment.get('appVersionName')
        onereply.thumbsDownCount = userComment.get('thumbsDownCount')
        onereply.thumbsUpCount = userComment.get('thumbsUpCount')
        onereply.screenDensityDpi = deviceMetadata.get('screenDensityDpi')
        onereply.screenHeightPx = deviceMetadata.get('screenHeightPx')
        onereply.screenWidthPx = deviceMetadata.get('screenWidthPx')
        onereply.cpuModel = deviceMetadata.get('cpuModel')
        onereply.productName = deviceMetadata.get('productName')
        onereply.deviceClass = deviceMetadata.get('deviceClass')
        onereply.cpuMake = deviceMetadata.get('cpuMake')
        onereply.ramMb = deviceMetadata.get('ramMb')
        onereply.manufacturer = deviceMetadata.get('manufacturer')
        onereply.nativePlatform = deviceMetadata.get('nativePlatform')
        onereply.glEsVersion = deviceMetadata.get('glEsVersion')

        onereply.save()


def replymessage(reviewsid, atoken, text):
    rurl = "https://www.googleapis.com/androidpublisher/v2/applications/com.feelingtouch.idl/reviews/%s:reply?access_token=%s" % (reviewsid, atoken)
    data = {
        "replyText": text
    }
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=rurl, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)


def main():
    dataalljson = get_list()
    for i in range(19,-1,-1):
        data = dataalljson['reviews'][i]
        savadb(data)


if __name__ == '__main__':
    main()
    print("Done!")
