#!/usr/bin/python
#coding=utf8
 
import httplib
import md5
import urllib
import random
import json,re
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf8')
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
            self.fromLang,self.toLang = 'en', 'zh'
        else:
            self.fromLang,self.toLang = 'zh', 'en'

        sign = self.appid+self.q+str(self.salt)+self.secretKey
        self.m1 = md5.new()
        self.m1.update(sign)
        sign = self.m1.hexdigest()
        self.myurl = self.myurl+'?appid='+self.appid+'&q='+urllib.quote(self.q)+'&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(self.salt)+'&sign='+sign
    def reques(self):
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
    def setq(self,q):
        self.q=q
        return self.q

    def fanyi(self,q=""):
        if q: self.setq(q)
        self.createstr()
        return self.reques()

    def getSpeech(self, text):
        url = 'http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=' + str(self.spd) + '&text='
        return url + str(text)

    def audioplay(self, text):
        subprocess.call(["mplayer", self.getSpeech(text)], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def dicts(self,keys):
        key1=keys[0]
        var=(keys[1:]).strip()
        def abc(var):
            var=int(var)
            if var:self.spd=var

        def bcd(var):
            pass
        def cde(var):
            pass
        setdict = {"s": abc(var), "f": bcd(var), "c": cde(var)}
        dicr=setdict[key1]
        return dicr

if __name__=="__main__":
    word = sys.argv
    delk=word.pop(0)
    word=" ".join(word)
    selects=word.split(" --")
    word=selects.pop(0)
    x = fanyi()
    # for i in selects:
    #     d = x.dicts(i)
    z=json.loads(x.fanyi(word))["trans_result"][0]["dst"]
    s=str(word)+str("  -->翻译为--->  ")+str(z)
    print s
    x.audioplay(s)
