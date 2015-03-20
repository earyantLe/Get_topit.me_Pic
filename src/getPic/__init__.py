# -*- coding=utf-8 -*-
import re, os, urllib, sys, socket, string
from itertools import count

def getHtml(url):  # 获取网页源代码
    page = urllib.urlopen(url)
    html = page.read()
    return html

def rUnsupportChar(s):  # 替换不能作为目录名的字符 <> : * " ? |
    unSupChar = r'''
    <>:*"?\
    '''
    supChar=r'''
    ()-^~$-
    '''
    trans=string.maketrans(unSupChar,supChar)
    s = s.translate(trans, "")
    return s

def downLoadImg(imglist,title):  # 下载图片到本地
    x=1
    for imgurl in imglist:
        picPath=os.getcwd() + '\\' + title + '\%s.jpg' % x
        print "Downloading: "+picPath
        urllib.urlretrieve(imgurl, unicode(picPath))
        x += 1


def createNewFolder(html,lenPic):  # 创建文件夹，返回文件夹名
    reg = r'<h2>(.+)</h2>'
    titleRe = re.compile(reg)
    title = re.findall(titleRe, html)
    title[0]=rUnsupportChar(title[0])+" "+str(lenPic)+"P"
    dirPath = os.getcwdu() + unicode("\\") + unicode(title[0])
    if(os.path.exists(dirPath) == False):
        os.makedirs(unicode(title[0]))
    return title[0]
    
def getItemsUrlList(url):  # 获取图片详情URL列表 
    html = getHtml(url)
    reg = r'<a href="([^\s]*?item/[\d]*?)">'
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

def getAllPageUrl(html):  # 获取专辑下所以分页URL列表
    reg = r'<a href="([^s]+?p=\d)">'
    mre = re.compile(reg)
    pagelist = re.findall(mre, html)
    return [albumURL, ] + pagelist
  

#防止网络延迟导致崩溃   
socket.setdefaulttimeout(60)        
  
albumURL = "http://www.topit.me/album/1230349"  #find no Url
albumURL = "http://www.topit.me/album/1225451"  #find no Url
albumURL = "http://www.topit.me/album/1228963"  # can not retrive all page 
  
#获取html页面源代码
html = getHtml(albumURL)

#获取该专辑的所以分页URL
pageList=getAllPageUrl(html)
  
#遍历图片详情页URL
imgDetialList=[]
for pageitem in pageList:
    imgDetialList+=getItemsUrlList(pageitem)
lenPic=len(imgDetialList)
print imgDetialList
print u"一共"+str(lenPic)+u"张图片"

#获得图片URL
imgList=[]
print u"正在获取图片URL地址..."
for imgitem in imgDetialList:
    imgList+=getPicUrl(imgitem)

#创建专辑名为名的文件夹
title=createNewFolder(html,lenPic)
   
#下载图片
downLoadImg(imgList, title)


