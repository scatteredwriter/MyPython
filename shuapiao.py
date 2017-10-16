# coding=utf-8

from bs4 import BeautifulSoup
import requests
import re

addLists = []
dan = u''
dan2 = u''
index = -1
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
    'Referer': 'http://x3zl.17-g.com/a2/i1/67491503471904/index.asp?id=45774&uid=67491503471904'}


def getAddress():
    url = 'http://www.xicidaili.com/nt/'
    html = requests.get(url, headers=headers)
    html = html.text
    address = re.findall(r'(\d+\.\d+\.\d+\.\d+)</td>\s*<td>(\d+)</td>', html)
    for tr in address:
        addLists.append({'http': tr[0] + ':' + tr[1]})


def getDan():
    while True:
        try:
            url = 'http://x3zl.17-g.com/a2/zhulic.asp?id=45774&uid=67491503471904'
            html = requests.get(url, headers=headers)
            html = html.text
            dans = re.findall(
                r'/a2/plugin.asp\?id=45774&uid=67491503471904&dan=(\d+)&dan2=(\d+)\'', html)
            dan = dans[0][0]
            dan2 = dans[0][1]
            print dan, dan2
            return(dan, dan2)
        except:
            print u'获取dan失败！'


def shuaPiao((dan, dan2), ip):
    try:
        url = 'http://x3zl.17-g.com/a2/plugin.asp?id=45774&uid=67491503471904&dan={0}&dan2={1}'
        url = url.replace('{0}', dan).replace('{1}', dan2)
        result = requests.get(url, headers=headers,
                              proxies=ip, timeout=20)
        print result.text
    except:
        pass


def getIPtxt():
    txt = open(u'下载.txt')
    for line in txt:
        addLists.append({'https':  line.replace('\n', '')})


def getRanking():
    try:
        url = 'http://x3zl.17-g.com/a2/zhulix.asp?id=45774&uid=67491503471904'
        result = requests.get(url, headers=headers)
        result = result.text
        zhuli = re.findall(
            u">(\d+) ", result)
        ranking = re.findall(
            u">(\d+)</div>", result)
        print u'助力：' + zhuli[0] + u' 排名：' + ranking[0] + u' 热度：' + ranking[1] + '\n'
    except:
        pass


# getAddress()
getIPtxt()
print addLists
getRanking()
for ip in addLists:
    shuaPiao(getDan(), ip)
getRanking()
