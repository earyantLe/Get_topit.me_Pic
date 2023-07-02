import os
import re
import socket
import string
import sys

import math
import urllib

import time

from os.path import getsize


def setUTF8():
    reload(sys)
    sys.setdefaultencoding("utf-8")  # 该方法在2.5版本以后被隐蔽，需重新装载sys模块才能使用，请无视eclipse错误


setUTF8()

socket.setdefaulttimeout(30)

choice = raw_input("直接点击 y 随便下载热门推荐图片，或者输入要搜索的文字以下载相关图片\n")

album = r'http://www.topit.me/user/2443798/albums'


def getHtml(albumURL):
    page = urllib.urlopen(albumURL)
    html = page.read
    return html


def getALLAlbum(albumURL):
    albumURL = getHtml(albumURL)
    reg = r'<a href="([^\s]*?album/[\d]*?)">'
    mre = re.compile(reg)
    numList = re.findall(mre, albumURL)
    return numList


def getALLPageUrl(html, albumURL, maxPage=99):
    reg = r'<a href="[^s]+?p=(\d*?)">'
    mre = re.compile(reg)
    numList = re.findall(mre, html)
    if numList:
        pages = int(numList[-1])
    else:
        pages = 1
    if (pages > maxPage):
        pages = maxPage
    pageList = []
    for i in range(1, pages + 1):
        pageList.append(albumURL + "?p=" + str(i))
    return pageList


def getItemUrlList(url):
    html = getHtml(url)
    reg = r'href="([^\s]*?item/[\d]*?)">'
    mre = re.compile(reg)
    pageList = re.findall(mre, html)
    return list(set(pageList))


def getPicUrl(url):
    html = getHtml(url)
    reg = r'href="([^\s]*?jpg)"'
    mre = re.compile(reg)
    picUrl = re.findall(mre, html)
    print picUrl
    return picUrl


def rUnsupportChar(s):
    unSupChar = r'''
    ,.;*"?|
    '''
    supChar = r'''
    ()-^`$-
    '''
    trans = string.maketrans(unSupChar, supChar)
    s = s.translate(trans, "")
    return s


def createNewFolder(html, lenPic):
    reg = r'<h2>(.+)</h2>'
    titleRe = re.compile(reg)
    title = re.findall(titleRe, html)
    title[0] = rUnsupportChar(title[0] + "  " + str(lenPic) + "P")
    dirPath = os.getcwdu() + unicode("\\") + unicode(title[0])
    if os.path.exists(dirPath) == False:
        os.makedirs(unicode(title[0]))
        print "\n创建名称为：" + title[0] + "的目录"
    else:
        print "名称为：" + title[0] + "的目录已存在"
    return title[0]


def showProgress(a, b, c):
    #     显示下载进度
    per = 100 * a * b / c
    if per > 100:
        per = 100
    if per % 10 == 0:
        print 'Progress:' + '%.2f%%' % per


def downloadImg(imgList, title):
    tryTime = 1
    i = 0
    lenImageList = len(imgList)
    while (i < lenImageList):
        imgUrl = imgList[i]
        if type(imgUrl) is type.ListType:
            imgUrl = imgUrl[-1]
        picPath = os.getcwd() + '\\' + title + '\%s.jpg' % (i + 1)
        print "downloading........." + picPath + " From-->>" + imgUrl
        time.sleep(0.3 * math.pow(2, tryTime - 1))
        try:
            urllib.urlretrieve(imgUrl, unicode(picPath), showProgress)
            if getsize(unicode(picPath)) > 1000:
                print u'下载成功'
                tryTime = 1
            else:
                if tryTime < 3:
                    print u'下载失败，重新下载。。。'
                    tryTime += 1
                    i -= 1
                else:
                    print u'-------\n该文件无法下载，图片Url为：' + unicode(imgUrl) + "\n---"
                    tryTime = 1
            i += 1
        except Exception:
            print u'下载超市，重新下载...'
            tryTime += 2
            print  u'---\n 盖恩建无法下载，图片地址为：' + unicode(imgUrl) + "\n------"
            tryTime = 1
            i += 1


def downloadOneAlbum(albumURL, maxPage=99):
    # 获取html页面源代码
    html = getHtml(albumURL)

    # 获取专辑的分页url
    pageList = getALLPageUrl(html, albumURL, maxPage)

    # 遍历图片详情页URL
    imgDetialList = []
    for pageitem in pageList:
        imgDetialList += getItemUrlList(pageitem)
    lenPic = len(imgDetialList)
    print r"一共" + str(lenPic) + u'张图片'

    imgList = []
    print u'正在获取图片URL地址'
    for imgitem in imgDetialList:
        imgList += getPicUrl(imgitem)

    # 创建专辑名的文件夹
    title = createNewFolder(html, lenPic)

    # 下载图片
    downloadImg(imgList, title)


def downloadALLAlbum(album, maxPage=100):
    p = int(math.ceil(float(maxPage) / 40))
    pageList = []
    for i in range(1, p + 1):
        albumURL = album + '?p=' + str(i)
        pageList += getALLAlbum(albumURL)
    for i in range(0, maxPage):
        print "\n=========" + u'下载专辑' + pageList[i] + "=========="
        downloadOneAlbum(pageList[i])


if choice == 'y' or choice == 'Y':
    downloadALLAlbum(album);
