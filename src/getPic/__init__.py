#-*-coding=utf-8-*-
import re, os, urllib, sys, socket, string,time,types,math
from itertools import count
from os.path import join, getsize  
from multiprocessing import TimeoutError

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
    tryTime=1                     
    i=0
    lenImageList=len(imglist)
    while(i<lenImageList):
        imgurl=imglist[i]
        if(type(imgurl) is types.ListType):  #有时候同一张图片取到多个下载地址,最后一个为本站图片     
            imgurl=imgurl[-1]
        picPath=os.getcwd() + '\\' + title + '\%s.jpg' % (i+1)
        print "Downloading: "+picPath+" From-->> "+imgurl
        time.sleep(0.3*math.pow(2, tryTime-1))
        try:
            urllib.urlretrieve(imgurl, unicode(picPath))
            if(getsize(unicode(picPath))>1000): # 下载到的文件小于1kb认定为无效文件
                print u'下载成功!!!'
                tryTime=1
            else:
                if(tryTime<6):                   # 下载失败时尝试重新下载次数
                    print u'下载失败，重新下载...'
                    tryTime+=1
                    i-=1
                else:
                    print u'---------------------\n该文件无法下载，图片URL地址为： '+unicode(imgurl)+"\n---------------------"
                    tryTime=1
            i+=1;
        except TimeoutError:
            print u'下载超时，重新下载...'
            tryTime+=2
            if(tryTime>6):                   # 下载失败时尝试重新下载次数
                    print u'---------------------\n该文件无法下载，图片URL地址为： '+unicode(imgurl)+"\n---------------------"
                    tryTime=1
                    i+=1
            


def createNewFolder(html,lenPic):  # 创建文件夹，返回文件夹名
    reg = r'<h2>(.+)</h2>'
    titleRe = re.compile(reg)
    title = re.findall(titleRe, html)
    title[0]=rUnsupportChar(title[0])+" "+str(lenPic)+"P"
    dirPath = os.getcwdu() + unicode("\\") + unicode(title[0])
    if(os.path.exists(dirPath) == False):
        os.makedirs(unicode(title[0]))
        print "创建名称为："+title[0]+" 的目录"
    else:
                print "名称为："+title[0]+" 的目录已存在"
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
    reg = r'<a href="[^s]+?p=(\d*?)">'
    mre = re.compile(reg)
    numlist = re.findall(mre, html)
    pages=int(numlist[-1])
    pagelist=[]
    for i in range(1,pages+1):
        pagelist.append(albumURL+"?p="+str(i))
    return  pagelist

#确保编码方式为UTF-8
reload(sys)
sys.setdefaultencoding("utf-8") #该方法在2.5以后被隐蔽，需重新装载sys模块才能使用，请无视eclipse错误
print "Encoding: "+sys.getdefaultencoding()

#防止网络延迟导致崩溃   
socket.setdefaulttimeout(30)        
  
albumURL = "http://www.topit.me/album/1230349"  #find no Url brcause thee colum
albumURL = "http://www.topit.me/album/1225451"  #find no Url brcause three colum
albumURL = "http://www.topit.me/album/126073"  

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


