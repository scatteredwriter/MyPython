# coding=utf-8
import math

courses = {
    1: '电工学',
    2: '高等数学(上)',
    3: '大学英语3',
    4: 'C语言程序设计'
}
data = {
    '曽钦威': {
        courses[1]: 81,
        courses[2]: 77,
        courses[3]: 80,
        courses[4]: 95
    },
    '张晓阳': {
        courses[1]: 75,
        courses[2]: 60,
        courses[3]: 65,
        courses[4]: 75
    },
    '周杰': {
        courses[1]: 77,
        courses[2]: 90,
        courses[3]: 89,
        courses[4]: 82
    },
    '庄智': {
        courses[1]: 87,
        courses[2]: 61,
        courses[3]: 50,
        courses[4]: 90
    }
}


def sim_distance(datas, person1, person2):
    '通过计算欧氏距离得出两者的相似度'
    si = {}
    for item in datas[person1]:
        if item in datas[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0

    # 计算两者的欧氏距离
    sum_of_squares = sum([pow(datas[person1][item] - datas[person2][item], 2)
                          for item in datas[person1] if item in datas[person2]])

    # 返回值越接近1则代表两者的相似度越大
    return 1 / (1 + math.sqrt(sum_of_squares))


def sim_pearson(datas, person1, person2):
    '通过皮尔逊相关系数得出两者的相关程度'
    si = {}
    for item in datas[person1]:
        if item in datas[person2]:
            si[item] = 1
    if len(si) == 0:
        return 1
    # 计算person1所有item评分之和
    sum1 = sum([datas[person1][item] for item in si])
    sum2 = sum([datas[person2][item] for item in si])
    sum_of_1x2 = sum([datas[person1][item] * datas[person2][item]
                      for item in si])
    sum_of_square1 = sum([pow(datas[person1][item], 2) for item in si])
    sum_of_square2 = sum([pow(datas[person2][item], 2) for item in si])
    n = len(si)
    try:
        result = (sum_of_1x2 - (sum1 * sum2) / n) / math.sqrt((sum_of_square1 -
                                                               (pow(sum1, 2) / n)) * (sum_of_square2 - (pow(sum2, 2) / n)))
    except Exception as identifier:
        return 0
    return result


def get_result(person1, person2, fun):
    '计算相关度'
    result = fun(data, person1, person2)
    if fun == sim_distance:
        print('你们的相似度有%f哦' % result)
    elif fun == sim_pearson:
        if result > 0.0:
            print('你们两个人的学习情况非常相似哦！')
        elif result == 0.0:
            print('你们两个人的学习情况看起来没有什么关系')
        elif result < 0.0:
            print('你们真的是一点关系都没有...')


c = input('请选择使用哪种方式计算相关关系：\n1.欧氏距离\n2.皮尔逊相关度\n')
p1 = input('请输入第一位学生的名字：')
p2 = input('请输入第二位学生的名字：')
if c == '1':
    get_result(p1, p2, sim_distance)
elif c == '2':
    get_result(p1, p2, sim_pearson)
