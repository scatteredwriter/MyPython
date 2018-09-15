import requests
import json


def SearchStudent(searchkey):
    url = 'http://jwzx.cqu.pt/data/json_StudentSearch.php?searchKey=%s'
    url = url % searchkey
    response = requests.get(url)
    response = json.loads(response.text)
    for i in range(len(response['returnData'])):
        print('第%i位：姓名：%s\t年级：%s\t性别：%s\t学号：%s\t班级：%s\t专业：%s\t学院：%s' % (
            i, response['returnData'][i]['xm'], response['returnData'][i]['nj'], response['returnData'][i]['xb'], response['returnData'][i]['xh'], response['returnData'][i]['bj'], response['returnData'][i]['zym'], response['returnData'][i]['yxm']))
    try:
        choose = input('\n请选择一项进行查询：')
        if int(choose) > len(response['returnData']) or int(choose) < 0:
            print('输入错误！')
            exit

        return response['returnData'][int(choose)]['xh']
    except:
        print('输入错误！')
        exit


def GetStudentPhoto(studentId):
    url = 'http://jwzx.cqu.pt/showstuPic.php?xh=%s'
    print('学生照片：' + url % studentId)


def GetCETPhont(studentId):
    url = 'http://172.22.80.212.cqu.pt/PHOTO0906CET/%s.JPG'
    print('CET照片：' + url % studentId)


while True:
    searchkey = input('\n请输入关键字：')
    studentId = SearchStudent(searchkey)
    GetStudentPhoto(studentId)
    GetCETPhont(studentId)
