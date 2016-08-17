# -*-coding=utf-8-*-
import re, os, urllib, sys, socket, string, time, types, math, exceptions
from itertools import count
from os.path import join, getsize
from multiprocessing import TimeoutError
from lib2to3.pgen2.token import PERCENT
from random import choice


def setUTF8():  # 确保默认编码为UTF-8
    reload(sys)
    sys.setdefaultencoding("utf-8")  # 该方法在2.5版本以后被隐蔽，需重新装载sys模块才能使用，请无视eclipse错误


#     print "默认编码为： : " + sys.getdefaultencoding()

def getHtml(url):  # 获取网页源代码
    page = urllib.urlopen(url)
    html = page.read()
    return html


def rUnsupportChar(s):  # 替换不能作为目录名的字符 <> : * " ? |
    unSupChar = r'''
    <>:*"?|
    '''
    supChar = r'''
    ()-^~$-
    '''
    trans = string.maketrans(unSupChar, supChar)
    s = s.translate(trans, "")
    return s


def downLoadImg(imglist, title):  # 下载图片到本地
    tryTime = 1
    i = 0
    lenImageList = len(imglist)
    while (i < lenImageList):
        imgurl = imglist[i]
        if (type(imgurl) is types.ListType):  # 有时候同一张图片取到多个下载地址,最后一个为本站图片
            imgurl = imgurl[-1]
        picPath = os.getcwd() + '\\' + title + '\%s.jpg' % (i + 1)
        print "Downloading: " + picPath + " From-->> " + imgurl
        time.sleep(0.3 * math.pow(2, tryTime - 1))
        try:
            urllib.urlretrieve(imgurl, unicode(picPath), showProgress)
            if (getsize(unicode(picPath)) > 1000):  # 下载到的文件小于1kb认定为无效文件
                print u'下载成功!!!'
                tryTime = 1
            else:
                if (tryTime < 6):  # 下载失败时尝试重新下载次数
                    print u'下载失败，重新下载...'
                    tryTime += 1
                    i -= 1
                else:
                    print u'---------------------\n该文件无法下载，图片URL地址为： ' + unicode(imgurl) + "\n---------------------"
                    tryTime = 1
            i += 1;
        except Exception:
            print u'下载超时，重新下载...'
            tryTime += 2
            if (tryTime > 6):  # 下载失败时尝试重新下载次数
                print u'---------------------\n该文件无法下载，图片URL地址为： ' + unicode(imgurl) + "\n---------------------"
                tryTime = 1
                i += 1


def showProgress(a, b, c):  # 显示下载进度
    '''
    @a 已经下载的数据块数
    @b 数据块大小
    @c 总文件大小
    '''
    per = 100 * a * b / c
    if per > 100:
        per = 100
    if per % 10 == 0:
        print 'Progress: ' + '%.2f%%' % per


def createNewFolder(html, lenPic):  # 创建文件夹，返回文件夹名
    reg = r'<h2>(.+)</h2>'
    titleRe = re.compile(reg)
    title = re.findall(titleRe, html)
    title[0] = rUnsupportChar(title[0]) + " " + str(lenPic) + "P"
    dirPath = os.getcwdu() + unicode("\\") + unicode(title[0])
    if (os.path.exists(dirPath) == False):
        os.makedirs(unicode(title[0]))
        print "\n创建名称为：" + title[0] + " 的目录"
    else:
        print "名称为：" + title[0] + " 的目录已存在"
    return title[0]


def getItemsUrlList(url):  # 获取图片详情URL列表 
    html = getHtml(url)
    reg = r'href="([^\s]*?item/[\d]*?)">'
    mre = re.compile(reg)
    pagelist = re.findall(mre, html)
    return list(set(pagelist))


def getPicUrl(url):  # 获取图片URL
    html = getHtml(url)
    reg = r'href="([^\s]*?jpg)"'
    mre = re.compile(reg)
    picUrl = re.findall(mre, html)
    print picUrl
    return picUrl


def getAllPageUrl(html, albumURL, maxPage=99):  # 获取所有分页URL列表
    reg = r'<a href="[^s]+?p=(\d*?)">'
    mre = re.compile(reg)
    numlist = re.findall(mre, html)
    if numlist:  # 判断空,防止只有一页的专辑
        pages = int(numlist[-1])
    else:
        pages = 1
    if (pages > maxPage):
        pages = maxPage
    pagelist = []
    for i in range(1, pages + 1):
        pagelist.append(albumURL + "?p=" + str(i))
    return pagelist


def getAllAlbum(homeURL):
    homeURL = getHtml(homeURL)
    reg = r'<a href="([^\s]*?album/[\d]*?)">'
    mre = re.compile(reg)
    numlist = re.findall(mre, homeURL)
    return numlist


def downloadALLAlbum(homeURL, maxPage=20):  # 下载所有推荐专辑或者热门专辑,默认下载20个专辑
    p = int(math.ceil(float(maxPage) / 40))
    pageList = []
    for i in range(1, p + 1):
        albumURL = homeURL + '?p=' + str(i)
        pageList += getAllAlbum(albumURL)
    for i in range(0, maxPage):
        print "\n=======================" + u'下载专辑  ' + pageList[i] + "======================="
        downloadOneAlbum(pageList[i])


def downloadQurryAlbum(homeURL, maxPage=20):  # 下载所有搜索到的专辑,默认下载20个专辑
    pageList = []
    homeURLContent = getHtml(homeURL)
    reg = r'<a href="http://www.topit.me/albums/search\?query=[^s]+?&p=([1-9]\d*)">'
    mre = re.compile(reg)
    numlist = re.findall(mre, homeURLContent)
    if numlist:  # 判断空,防止只有一页的专辑
        pages = int(numlist[-1])
    else:
        pages = 1
    for i in range(1, pages + 1):
        albumURL = homeURL + '&p=' + str(i)
        print albumURL
        pageList += getAllAlbum(albumURL)
    print pageList
    # for i in range(0, maxPage):
    for i in range(0, len(pageList)):
        print "\n====================" + u'下载搜索到的专辑  ' + pageList[i] + "====================="
        downloadOneAlbum(pageList[i])


def downloadOneAlbum(albumURL, maxPage=99):  # 下载一个专辑所有图片到本地文件夹
    # 获取html页面源代码
    html = getHtml(albumURL)

    # 获取该专辑的所以分页URL
    pageList = getAllPageUrl(html, albumURL, maxPage)

    # 遍历图片详情页URL
    imgDetialList = []
    for pageitem in pageList:
        imgDetialList += getItemsUrlList(pageitem)
    lenPic = len(imgDetialList)
    print u"一共" + str(lenPic) + u"张图片"

    # 获得图片URL
    imgList = []
    print u"正在获取图片URL地址..."
    for imgitem in imgDetialList:
        imgList += getPicUrl(imgitem)

    # 创建专辑名为名的文件夹
    title = createNewFolder(html, lenPic)

    # 下载图片
    downLoadImg(imgList, title)


album = "http://www.topit.me/albums"
albumhot = "http://www.topit.me/albums/hot"
albumURL = "http://www.topit.me/album/1140304"

setUTF8()

# 设置默认防止网络延迟导致崩溃   
socket.setdefaulttimeout(30)

choice = raw_input("直接点击 y 随便下载热门推荐图片，或者输入要搜索的文字以下载相关图片\n")

if (choice == 'y' or choice == 'Y'):
    num = raw_input("输入您要下载的专辑数量，直接点击y默认为20，建议低于60\n")
    if (not num.isdigit()):
        print ur'输入的内容不是数字或者y,程序已退出'
        exit()
    if num == 'y':
        num = 20
    downloadALLAlbum(album, int(num))
else:
    queryURL = r'http://www.topit.me/albums/search?query=' + choice
    num = raw_input("输入您要下载的专辑数量，直接点击y默认为20，建议低于60\n")
    if (not num.isdigit()):
        print ur'输入的内容不是数字或者y,程序已退出'
        exit()
    if num == 'y':
        num = 20
    downloadQurryAlbum(queryURL, int(num))
