# coding=utf-8

import requests
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


def getmusic():
    url = 'http://rodvm.cloudapp.net/playmusic/playmusic.php'
    result = requests.post(url, headers=headers)
    result = result.text
    return result


def playover():
    url = 'http://rodvm.cloudapp.net/playmusic/playmusic.php?type=over'
    requests.get(url, headers=headers)


while True:
    try:
        music = getmusic()
        print(music)
        if(music):
            os.system('mpg123 -q "%s"' % music)
            playover()
    except:
        pass
