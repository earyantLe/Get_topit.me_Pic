# -*-coding=utf-8-*-
import os
import re
import socket
import string
import sys
import urllib


def setUTF8():
    reload(sys)
    sys.setdefaultencoding("utf-8")


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getALLAlbum(homeURL):
    homeURL = getHtml(homeURL)
    reg = r'<a href="([^\s]*?album/[\d]*?)">'
    mre = re.compile(reg)
    numlist = re.findall(mre, homeURL)
    return numlist


def getItemUrlList(url):
    html = getHtml(url)
    reg = r'href="([\s]*?item/[\d]*?)">'
    mre = re.compile(reg)
    pageList = re.findall(mre, html)
    return list(set(pageList))


def getALLPageUrl(html, albumURL):
    reg = r'<a href="[^s]+?p=(\d*?)">'
    mre = re.compile(reg)
    numlist = re.findall(mre, html)
    if numlist:
        pages = int(numlist[-1])
    else:
        pages = 1
    pagelist = []
    for i in range(1, pages + 1):
        pagelist.append(albumURL + "?p=" + str(i))
        return pagelist


def getPicUrl(url):
    html = getHtml(url)
    reg = r'href="([^\s]*?jpg)"'
    mre = re.compile(reg)
    picUrl = re.findall(mre, html)
    print picUrl
    return picUrl


def rUnsupportChar(s):
    unSupChar = r'''
    <>:*"?|
    '''
    supChar = r'''
       ()-^~$-
       '''
    trans = string.maketrans(unSupChar, supChar)
    s = s.translate(trans, "")
    return s


def createNewFolder(html, lenPic):
    reg = r'<h2>(.+)</h2>'
    titleRe = re.compile(reg)
    title = re.findall(titleRe, html)
    title[0] = rUnsupportChar(title[0]) + "  " + str(lenPic) + "P"
    dirPath = os.getcwdu() + unicode("\\") + unicode(title[0])
    if (os.path.exists(dirPath) == False):
        os.mkdir(unicode(title[0]))
        print "\n创建名称为：" + title[0] + "的目录"
    else:
        print "名称为" + title[0] + "的目录已存在"
    return title[0]

def downLoadImg(imglist, title):  # 下载图片到本地
    tryTime =1
    i =0
    lenImgList=len(imglist):




# 下载一个专辑的所有图片到本地
def downloadOneAlbum(albumURL):
    #     获取html页面的源代码
    html = getHtml(albumURL)
    #     获取该专辑的所有分页
    pageList = getALLPageUrl(html, albumURL)

    #     遍历图片详情页
    imaDetailList = []
    for pageItem in pageList:
        imaDetailList += getItemUrlList(pageItem)
    lenPic = len(imaDetailList)
    print u"一共" + str(lenPic) + u'张图片'

    #     获取图片URL
    imgList = []
    print u'正在获取图片的URL地址'
    for imgList in imaDetailList:
        imgList += getPicUrl(imgList)
    # 创建专辑名为  的文件夹
    title = createNewFolder(html, lenPic)


#   下载图片
    downloadImg(imgList,title)

def downloadQurryAlbum(homeUrl):
    pageList = []
    homeURLContent = getHtml(homeUrl)
    reg = r'<a href="http://www.topit.me/albums/search\?query=[^s]+?&p=([1-9]\d*)">'
    mre = re.compile(reg)
    numlist = re.findall(mre, homeURLContent)
    if numlist:  # 判断空，防止只有一页的专辑
        pages = int(numlist[-1])
    else:
        pages = 1
    for i in range(1, pages + 1):
        albumURL = homeUrl + '&p=' + str(i)
        print albumURL
        pageList += getALLAlbum(albumURL)
    print  pageList
    for i in range(0, len(pageList)):
        print "\n=======" + u"下载搜索到的专辑" + pageList[i] + "======="
        downloadOneAlbum(pageList[i])


album = "http://www.topit.me/albums"
albumhot = "http://www.topit.me/albums/hot"
albumURL = "http://www.topit.me/album/1140304"
setUTF8()

# 设置默认防止网络延迟导致崩溃
socket.setdefaulttimeout(30)

choice = raw_input("请选择想下载的图片的模式：1为专辑，2为用户id，直接输入文字则下载有关文字的图片")

if choice.isdigit():
    if choice == '1':
        albumsId = raw_input("请输入专辑id")
        queryURL = r'http://www.topit.me/albums/' + albumsId
        downloadQurryAlbum(queryURL)
    elif choice == '2':
        userid = "请输入用户Id"
        queryURL = r"http: // www.topit.me/user/" + userid + "/albums"
        downloadQurryAlbum(queryURL)
else:
    queryURL = r'http://www.topit.me/albums/search?query=' + choice
    downloadQurryAlbum(queryURL)
