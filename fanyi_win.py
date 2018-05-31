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



import httplib
import random
import json, re
import subprocess
import sys
import hashlib
import os

if sys.version_info < (3, 4):
    pass
    import md5
    import urllib
    import urllib2
    import urlparse
    from urllib2 import urlopen


    reload(sys)
    sys.setdefaultencoding('utf8')
    print ("你好utf8")
    print ("Default Coding is: utf8 \nIf display Err,Please set coding \nSend  '1' Set Commandline coding to GBK \nSend anykey Set Commandline  coding to UTF8\n")
    strkey = str(raw_input("Please Set Commandline Coding :__"))
    strkey = strkey.replace("\n", "").replace("\n", " ")

    if '1'in strkey:
        reload(sys)
        sys.setdefaultencoding('gbk')
        print ("set:gbk")
    else:
        reload(sys)
        sys.setdefaultencoding('utf8')
        print ("Set:utf8")
else:
    pass
    import http.client

    #print("py3")


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
        if sys.version_info < (3, 4):
            pass
            self.m1 = hashlib.md5()
            # self.m1 = md5()
            self.m1.update(sign)
            sign = self.m1.hexdigest()
            self.myurl = self.myurl + '?appid=' + self.appid + '&q=' +urllib.quote(self.q) + '&from=' + self.fromLang + '&to=' + self.toLang + '&salt=' + str(self.salt) + '&sign=' + sign

        else:
            pass
            sign = hashlib.md5(bytes(sign, encoding='utf-8')).hexdigest()
            self.myurl = self.myurl + '?appid=' + self.appid + '&q=' +urllib.parse.quote(self.q) + '&from=' + self.fromLang + '&to=' + self.toLang + '&salt=' + str(self.salt) + '&sign=' + sign



    def reques(self):
        if sys.version_info < (3, 4):
            pass
            try:
                httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
                httpClient.request('GET', self.myurl)

                #response是HTTPResponse对象
                response = httpClient.getresponse()
                return response.read()

            except Exception, e:
                print e
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
    def write(self,s):
        file = open('a.txt', 'a')
        file.write("{}".format(s))
        file.write("\n")
def selectcoding():
    if sys.version_info < (3, 4):
        strkey = str(raw_input("default utf8 \nsend key '1' endcoding gbk \nsend anykey endcoding utf8\n"))
    else:
        strkey = str(input("default utf8 \nsend '1' endcoding gbk \nsend anykey endcoding utf8\n"))
    strkey = strkey.replace("\n", "").replace("\n", " ")
    if strkey==1:
        reload(sys)
        sys.setdefaultencoding('gbk')
    else:
        reload(sys)
        sys.setdefaultencoding('utf8')
if __name__=="__main__":

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
    # z = json.loads(x.fanyi(word).decode())["trans_result"][0]["dst"]
    s=str(word)+str(u"  >---翻译--->  ")+str(z)
    print (s)
    #x.audioplay(s)

    while 1 :
        if sys.version_info < (3, 4):
            strkey=str(raw_input())
        else:
            strkey=str(input())
        strkey = strkey.replace("\n", "")
        if strkey:

            if strkey=="q":
                break;
            else:
                # os.system('clear')#linux
                os.system('cls')#windows
                # z=json.loads(x.fanyi(strkey))["trans_result"][0]["dst"]
                if sys.version_info < (3, 4) and 'gbk' in sys.getdefaultencoding():#gbk to utf8
                    z = json.loads(x.fanyi(strkey.decode("gbk").encode("utf8")).decode())["trans_result"][0]["dst"]
                else:
                    z=json.loads(x.fanyi(strkey).decode())["trans_result"][0]["dst"]
                s=str(strkey)+str(u"  >---翻译--->  ")+str(z)
                # if x.r:x.write(s)
                x.write(str(strkey)+":"+str(z))
                print (s)
