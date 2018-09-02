# coding=utf-8

import requests
import json
import re
import os
import time
import urllib.request


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


def gettext():
    url = 'http://rodvm.cloudapp.net/broadcast/text.php'
    result = requests.get(url, headers=headers)
    result = result.text
    return result


def getVoice(text):
    text = urllib.parse.quote(text)
    tokenurl = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=Pp1PNrUVnECO7LH7Ki4uQxnx&client_secret=0b1ab78a06e3b571c8e76143849b85d5'
    result = requests.get(tokenurl, headers=headers)
    result = json.loads(result.text)
    url = 'http://tsn.baidu.com//text2audio?tex=%s&tok=%s&lan=zh&ctp=1&cuid=7808972&pit=5&vol=15&per=4' % (
        text, result['access_token'])
    os.system('mpg123 -q "%s"' % url)


while True:
    try:
        text = gettext()
        print(text)
        if(text):
            getVoice(text)
    except:
        pass
