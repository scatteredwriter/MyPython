# coding=utf-8

import requests
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


def changemusic():
    url = 'http://rodvm.cloudapp.net/playmusic/changemusic.php'
    result = requests.post(url, headers=headers)
    result = result.text
    if(result):
        os.system(
            'kill $(ps aux | grep -m 2 %s | awk \'{print $2}\')' % result)


while True:
    try:
        changemusic()
    except:
        pass
