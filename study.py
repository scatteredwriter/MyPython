# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
import time
import re


def Login():
    loginbut.click()
    uname = driver.find_element_by_name('uname')
    password = driver.find_element_by_name('password')
    numcode = driver.find_element_by_name('numcode')
    but = driver.find_element_by_class_name('zl_btn_right')
    # username = input('请输入账号: ')
    # password_p = input("请输入密码: ")
    yanzheng = input("请输入验证码: ")
    uname.clear()
    password.clear()
    numcode.clear()
    uname.send_keys('2015212856')
    password.send_keys('Scattered1')
    numcode.send_keys(yanzheng)
    but.click()
    print('登录完成')


def GetChapterIds():
    driver.get('http://mooc1.chaoxing.com/course/96522356.html')
    cellbgbluebgblue1wh = driver.find_element_by_css_selector(
        'div.cell.bgblue.bgblue1.wh')
    p20s = cellbgbluebgblue1wh.find_elements_by_css_selector(
        'div.p20.btdwh.btdwh1.fix')
    for p20 in p20s:
        mt10 = p20.find_element_by_class_name('mt10')
        mb15s = mt10.find_elements_by_css_selector(
            'li.mb15.course_section.fix')
        for mb15 in mb15s:
            link = mb15.find_element_by_css_selector('a.wh.wh1')
            href = link.get_attribute('href')
            pattern = re.compile('knowledgeId=\d+')
            match = pattern.search(href)
            if match:
                chapterids.append(match.group().replace('knowledgeId=', ''))
    print('所有章节数据已经获取完毕')
    driver.back()


def ChioceCourse():
    '选择课程'
    driver.switch_to_frame('frame_content')
    a = driver.find_element_by_partial_link_text('创新创业')
    url = a.get_attribute('href')
    driver.switch_to_default_content()
    return url


def ClickCourse():
    '点击任务点'
    global coursename
    timeline = driver.find_element_by_class_name('timeline')
    units = timeline.find_elements_by_class_name('units')
    for unit in units:
        leveltwos = unit.find_elements_by_class_name('leveltwo')
        for leveltwo in leveltwos:
            clearfix = leveltwo.find_element_by_class_name('clearfix')
            icon = clearfix.find_element_by_class_name('icon')

            # 判断该课程是否学习完成
            try:
                orange = icon.find_element_by_class_name('orange')
                if not orange:
                    continue
            except Exception as identifier:
                continue

            articlename = clearfix.find_element_by_class_name('articlename')
            but = articlename.find_element_by_tag_name('a')
            but.click()
            break
        break
    while True:
        PlayVideo()
    print('所有课程已经学习完成')


def EnteriFrame():
    '进入iFrame'
    driver.switch_to_default_content()
    driver.switch_to_frame('iframe')
    ans_attach_ct = driver.find_element_by_class_name('ans-attach-ct')
    _iframe = ans_attach_ct.find_element_by_tag_name('iframe')
    driver.switch_to_frame(_iframe)


def JundgeFinished():
    '判断是否播放完成'
    driver.switch_to_default_content()
    driver.switch_to_frame('iframe')
    try:
        finished = driver.find_element_by_css_selector(
            'div.ans-attach-ct.ans-job-finished')
        if finished:
            driver.switch_to_default_content()
            return True
        else:
            EnteriFrame()
            return False
    except Exception as identifier:
        EnteriFrame()
        return False


def StudyNext():
    '播放下一节'
    global url
    onetoone = driver.find_element_by_class_name('onetoone')
    ncells = onetoone.find_elements_by_class_name('ncells')
    i = 0
    for ncell in ncells:
        try:
            a = ncell.find_element_by_css_selector(
                'a[title={}]'.format(coursename))
            currents = a.find_element_by_class_name('currents')
            if currents:
                i += 1
                break
        except Exception as identifier:
            pass
        i += 1
        continue
    url = driver.current_url
    pattern = re.compile('enc=.+')
    match = pattern.search(url)
    if match:
        enc = match.group().replace('enc=', '')
        driver.get(studypage.format(chapterids[i], courseId, clazzid, enc))


def PlayVideo():
    '播放视频'
    global coursename
    driver.switch_to_default_content()
    main = driver.find_element_by_class_name('main')
    coursename = main.find_element_by_tag_name('h1').text
    EnteriFrame()
    reader = driver.find_element_by_id('reader')
    flash = None
    while not flash:
        try:
            flash = reader.find_element_by_css_selector(
                "object[type='application/x-shockwave-flash']")
        except Exception as identifier:
            pass
    print('正在学习:', coursename)
    size = flash.size
    try:
        chains.move_to_element_with_offset(
            flash, 10, size['height'] - 10).click(flash).perform()
    except Exception as identifier:
        pass
    while not JundgeFinished():
        try:
            # chains.move_to_element_with_offset(
            #     flash, 10, size['height'] - 10).click(flash).perform()
            # time.sleep(1)
            chains.release(flash).perform()
        except Exception as identifier:
            pass
    chains.reset_actions()
    print(coursename, "学习视频观看完毕，现在学习下一节")
    StudyNext()


driver = webdriver.Chrome()
chains = ActionChains(driver)
coursename = None
courseId = 96522356
clazzid = 1406028
studypage = 'https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId={}&courseId={}&clazzid={}&enc={}'

driver.get('http://cqupt.benke.chaoxing.com/')
loginbut = driver.find_element_by_class_name('zt_l_loading')
print('进行账号登录...')
Login()
print('\n获取课程章节数据...')
chapterids = []
GetChapterIds()
url = ChioceCourse()
driver.get(url)
print('\n开始学习...')
ClickCourse()
