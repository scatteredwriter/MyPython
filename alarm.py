# coding=utf-8

import requests
import json
import re
import os
import time
import datetime
import urllib.request


stu_num = '2015212856'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Referer': 'http://www.weather.com.cn/weather/101040100.shtml'}


def getWeather():
    url = 'http://wthrcdn.etouch.cn/weather_mini?citykey=101040100'
    result = requests.get(url, headers=headers)
    try:
        encoding = ''
        if result.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(result.text)
            if encodings:
                encoding = encodings[0]
            else:
                encoding = result.apparent_encoding
        encode_content = result.content.decode(
            encoding, 'replace').encode('utf-8', 'replace')
        result = encode_content.decode('utf-8')
    except:
        result = result.text
    result = json.loads(result)
    result = result['data']
    return '播报闹钟。现在是%s' % time.strftime("%Y-%m-%d %H:%M", time.localtime()) + '，%s今日温度为%s℃。' % (result['city'], result['wendu'])


def getCourses():
    url = 'https://wx.idsbllp.cn/api/kebiao'
    data = {'stu_num': stu_num}
    result = ''
    for i in range(3):
        try:
            result = requests.post(url, data=data)
            break
        except:
            pass
    result = result.text
    result = json.loads(result)
    data = result['data']
    week = datetime.datetime.now().weekday()
    courseMode = ''
    if(result['nowWeek'] % 2):
        courseMode = 'single'
    else:
        courseMode = 'double'
    courses = []
    for item in data:
        if(item['weekBegin'] <= result['nowWeek'] and item['weekEnd'] >= result['nowWeek'] and item['hash_day'] == week and(item['weekModel'] == 'all' or item['weekModel'] == courseMode)):
            courses.append(item)
    result = ''
    for item in courses:
        result += '第%s有%s，教室在%s。' % (item['lesson'],
                                     item['course'], item['classroom'])
    if(result):
        result = '今天' + result
    return result


def getVoice(text):
    text = urllib.parse.quote(text)
    tokenurl = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=Pp1PNrUVnECO7LH7Ki4uQxnx&client_secret=0b1ab78a06e3b571c8e76143849b85d5'
    result = requests.get(tokenurl, headers=headers)
    result = json.loads(result.text)
    url = 'http://tsn.baidu.com//text2audio?tex=%s&tok=%s&lan=zh&ctp=1&cuid=7808972&pit=5&vol=15&per=4' % (
        text, result['access_token'])
    os.system('mpg123 -q "%s"' % url)


weather = getWeather()
print(weather)
courses = getCourses()
print(courses)
getVoice(weather + courses)
