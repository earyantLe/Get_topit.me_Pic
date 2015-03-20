# coding=utf-8
import re, os, urllib, sys, socket
from itertools import count

def utf2defcode(mstring):  # 转换为本地编码，解决中文乱码问题
    defcode = sys.getfilesystemencoding()
    return mstring.decode('utf-8').encode(defcode)
def getHtml(url):  # 获取网页源代码
    page = urllib.urlopen(url)
    html = page.read()
    return html
def getTitle(html):  # 获取专辑名
    reg = r'<h2>(.+)</h2>'
    titleRe = re.compile(reg)
    title = re.findall(titleRe, html)
    return title[0]
def getImg(html, title):  # 下载图片到本地
    reg = r'src=\"(.+\.jpg)'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    x = 1
    for imgurl in imglist:
        urllib.urlretrieve(imgurl, os.getcwd() + '\\' + title + '\%s.jpg' % x)
        x += 1
    return imglist      
def createNewFolder(folderName):
    os.makedirs(folderName)
    
def getSecondPageList(html):  # 获取专辑里二级页面列表  
    reg = r'<a href="([^\s]*?item[^\s]*?)">'
    mre = re.compile(reg)
    pagelist = re.findall(mre, html)
    return pagelist
def getPic(html):  # 获取二级页面中图片URL
    reg = r'href="([^\s]*?jpg)"'
    mre = re.compile(reg)
    piclist = re.findall(mre, html)
    return piclist
def getAllFirstPageURL(html):
    reg = r'<a href="([^s]+?p=\d)">'
    mre = re.compile(reg)
    pagelist = re.findall(mre, html)
    return pagelist
    
socket.setdefaulttimeout(60)  # 防止网络延迟导致崩溃
 
albumURL = "http://www.topit.me/album/1353605"

html = getHtml(albumURL)
 
firstPagelist = [albumURL] + getAllFirstPageURL(html)
 
title = getTitle(html)
  
createNewFolder(utf2defcode(title))

firstPagelistLen = len(firstPagelist)

x = 1;

for k in range(0, firstPagelistLen):
    secondPagelist = getSecondPageList(getHtml(firstPagelist[k]))[::2]
    secondPagelistLen = len(secondPagelist)
    for i in range(0, secondPagelistLen):
        pichtml = getHtml(secondPagelist[i])
        picURL = ''.join(getPic(pichtml))
        mpwd = os.getcwd() + '\\' + title + '\\'
        mpwd = unicode(mpwd, 'utf8')
        print mpwd
        print "Download %s.jpg" % x
        urllib.urlretrieve(picURL, mpwd + '\%s.jpg' % x)
        x = x + 1
