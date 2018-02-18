#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: mum
@license: Apache Licence
@contact: shuo502@163.com
@author: ‘yo‘
@site: http://github.com/shuo502
@software: PyCharm
@file: fy.py
@time: 2018/2/7 0:36
"""

# !/usr/bin/python
# coding=utf8



import urllib
import http.client
import random
import json, re
import subprocess
import sys
import hashlib


class fanyi():
    def __init__(self):
        self.appid = '20151113000005349'
        self.secretKey = 'osubCEzlGjzvw8qdQc41'
        self.httpClient = None
        self.myurl = '/api/trans/vip/translate'
        self.q = 'apple'
        self.fromLang = 'en'
        self.toLang = 'zh'
        self.spd = 5
        self.salt = random.randint(32768, 65536)

    def createstr(self):
        if re.match('[a-z]', self.q, re.I) is not None:
            self.fromLang, self.toLang = 'en', 'zh'
        else:
            self.fromLang, self.toLang = 'zh', 'en'

        sign = self.appid + self.q + str(self.salt) + self.secretKey
        # self.m1 = hashlib.md5()
        # self.m1.update(sign)
        # sign = self.m1.hexdigest()
        sign = hashlib.md5(bytes(sign, encoding='utf-8')).hexdigest()

        self.myurl = self.myurl + '?appid=' + self.appid + '&q=' +urllib.parse.quote(self.q) + '&from=' + self.fromLang + '&to=' + self.toLang + '&salt=' + str(self.salt) + '&sign=' + sign

    def reques(self):
        try:


            httpClient =http.client.HTTPSConnection('api.fanyi.baidu.com')

            httpClient.request('GET', self.myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            return response.read()

        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()

    def setq(self, q):
        self.q = q
        return self.q

    def fanyi(self, q=""):
        if q: self.setq(q)
        self.createstr()
        return self.reques()

    def getSpeech(self, text):
        url = 'http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=' + str(self.spd) + '&text='
        return url + str(text)

    def audioplay(self, text):
        subprocess.call(["mplayer", self.getSpeech(text)], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def dicts(self, keys):
        key1 = keys[0]
        var = (keys[1:]).strip()

        def abc(var):
            var = int(var)
            if var: self.spd = var

        def bcd(var):
            pass

        def cde(var):
            pass

        setdict = {"s": abc(var), "f": bcd(var), "c": cde(var)}
        dicr = setdict[key1]
        return dicr


if __name__=="__main__":
    import os
    word = sys.argv
    delk=word.pop(0)
    word=" ".join(word)
    selects=word.split(" --")
    word=selects.pop(0)
    # word="help"
    x = fanyi()
    # print()
    # for i in selects:
    #     d = x.dicts(i)
    # z=json.loads(x.fanyi(word))["trans_result"][0]["dst"]
    z = json.loads(x.fanyi(word).decode())["trans_result"][0]["dst"]
    s=str(word)+str("  -->翻译为--->  ")+str(z)
    print (s)
    #x.audioplay(s)
    while 1 :
        strkey=input()
        if strkey=="q":
            break;
        else:
            # os.system('clear')#linux
            os.system('cls')#windows
            # z=json.loads(x.fanyi(strkey))["trans_result"][0]["dst"]
            z=json.loads(x.fanyi(strkey).decode())["trans_result"][0]["dst"]
            s=str(strkey)+str("  -->翻译为--->  ")+str(z)
            print (s)

