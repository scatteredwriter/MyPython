import requests
import json
import os
import platform


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

def getMusicList(keyword, p):
    get_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json=1&aggr=1&cr=1&catZhida=1&p=%d&n=20&w=%s&format=jsonp&inCharset=utf8&outCharset=utf-8'
    get_url = get_url % (p, keyword)
    result = requests.get(get_url).text
    result = json.loads(result[9:-1])
    musicList = result['data']['song']['list']
    musics = []
    for item in musicList:
        albumName = item['album']['title']
        singerName = ''
        for singer in item['singer']:
            singerName += '/' + singer['title']
        singerName = singerName[1:]
        songName = item['title']
        songMid = item['mid']
        mediaMid = item['file']['media_mid']
        albumMid = item['album']['mid']
        musics.append({
            'singerName': singerName,
            'albumName': albumName,
            'songName': songName,
            'songMid': songMid,
            'mediaMid': mediaMid,
            'albumMid': albumMid
        })
    return musics


def getVkey(songMid, mediaMid=None):
    if mediaMid is None:
        mediaMid = songMid
    get_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&uin=0&songmid=%s&filename=M500%s.mp3&guid=9391879250'
    get_url = get_url % (songMid, mediaMid)
    result = requests.get(get_url).text
    result = json.loads(result)
    return result['data']['items'][0]['vkey']


def getMusic(music, fileType=None):
    typeList = [
        'M800',
        'M500',
    ]
    if fileType is None:
        fileType = typeList[0]
    elif int(fileType) <= len(typeList):
        fileType = typeList[int(fileType)]
    else:
        fileType = typeList[1]
    music_url = 'http://dl.stream.qqmusic.qq.com/%s%s.mp3?vkey=%s&guid=9391879250&fromtag=27'
    albumImg_url = 'https://y.gtimg.cn/music/photo_new/T002R500x500M000%s.jpg?max_age=2592000'
    songMid = music['songMid']
    albumMid = music['albumMid']
    mediaMid = music['mediaMid']
    vkey = getVkey(songMid, mediaMid)
    if len(vkey) == 0:
        vkey = getVkey('003OUlho2HcRHC')
    music_url = music_url % (fileType, mediaMid, vkey)
    albumImg_url = albumImg_url % albumMid
    return (music_url, albumImg_url)


def downloadFile(music, musicInfo):
    music_url = musicInfo[0]
    musicImg_url = musicInfo[1]
    musicFile_base_url = ''
    musicImgFile_base_url = ''
    if platform.system() == 'Windows':
        musicFile_base_url = os.path.expanduser('~/Music')
        musicImgFile_base_url = os.path.expanduser('~/Pictures')
    else:
        musicFile_base_url = os.path.expanduser('~/Music')
        musicImgFile_base_url = os.path.expanduser('~/Pictures')

    musicFile_url = os.path.join(musicFile_base_url, (
        '%s - %s.mp3' % (music['singerName'], music['songName'])))
    musicImgFile_url = os.path.join(musicImgFile_base_url, (
        '%s - %s.jpg' % (music['singerName'], music['albumName'])))

    _file = requests.get(music_url, headers=headers)
    if _file.status_code is not 200:
        return False
    with open(musicFile_url, 'wb') as code:
        code.write(_file.content)
    _file = requests.get(musicImg_url)
    with open(musicImgFile_url, 'wb') as code:
        code.write(_file.content)
    return True


def mainFun():
    while(True):
        musics = []
        begin = 0
        p = 0
        keyword = input(
            '请输入要查询的关键字:(%sq或Q%s取消):' % (Color.WARNING, Color.ENDC))
        if keyword == 'q' or keyword == 'Q':
            exit()
        while(True):
            p += 1
            newMusics = getMusicList(keyword, p)
            if len(newMusics) == 0:
                print('%s已到最后一页!%s' % (Color.FAIL, Color.ENDC))
            else:
                musics.extend(newMusics)
                for i in range(begin, len(musics)):
                    realI = i
                    print(
                        '[%s].%s:%s\t%s:%s\t%s:%s' % (Color.OKGREEN + str(realI) + Color.ENDC,
                                                      Color.OKGREEN +
                                                      '歌曲' + Color.ENDC,
                                                      Color.BOLD +
                                                      musics[realI]['songName'] +
                                                      Color.ENDC,
                                                      Color.OKGREEN +
                                                      '歌手' + Color.ENDC,
                                                      Color.BOLD +
                                                      musics[realI]['singerName'] +
                                                      Color.ENDC,
                                                      Color.OKGREEN +
                                                      '专辑' + Color.ENDC,
                                                      Color.BOLD +
                                                      musics[realI]['albumName'] +
                                                      Color.ENDC
                                                      ))
            selected = input('请输入要下载的歌曲%s序号%s(支持多选，用%s空格%s分割序号，%s回车%s查看下一页，输入%sq或Q%s重新搜索):' % (
                Color.WARNING, Color.ENDC, Color.WARNING, Color.ENDC, Color.WARNING, Color.ENDC, Color.WARNING, Color.ENDC))
            if selected == 'q' or selected == 'Q':
                break
            elif len(selected) == 0:
                begin = len(musics)
                continue
            selecteds = selected.split(' ')
            for selectIndex in selecteds:
                music = musics[int(selectIndex)]
                music_info = getMusic(music, 0)
                print('歌曲:%s - %s\n歌曲链接:%s\n专辑图片:%s' % (Color.OKBLUE + music['singerName'], music['songName'] +
                                                        Color.ENDC, Color.OKBLUE + music_info[0] + Color.ENDC, Color.OKBLUE + music_info[1] + Color.ENDC))
                command = input(
                    '输入任意键下载(%sq或Q%s取消):' % (Color.WARNING, Color.ENDC))
                if command == 'q' or command == 'Q':
                    continue
                print('开始下载 %s - %s ...' % (Color.OKGREEN + music[
                      'singerName'], music['songName'] + '.mp3' + Color.ENDC))
                isSucc = downloadFile(music, music_info)
                if not isSucc:
                    print('%s下载失败，正在重试...%s' % (Color.FAIL, Color.ENDC))
                    music_info = getMusic(music, 1)
                    print('歌曲:%s - %s\n歌曲链接:%s\n专辑图片:%s' % (Color.OKBLUE + music['singerName'], music['songName'] +
                                                            Color.ENDC, Color.OKBLUE + music_info[0] + Color.ENDC, Color.OKBLUE + music_info[1] + Color.ENDC))
                    isSucc = downloadFile(music, music_info)
                    if not isSucc:
                        print('%s下载失败!%s' % (Color.FAIL, Color.ENDC))
                        break
                print('%s下载完成!%s' % (Color.OKGREEN, Color.ENDC))
            break


if __name__ == '__main__':
    mainFun()
