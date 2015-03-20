#-*-coding=utf-8-*-
import re, os, urllib, sys, socket, string,time
reload(sys)
sys.setdefaultencoding('utf-8') 
print sys.getdefaultencoding()

def getHtml(url):  # 获取网页源代码
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getAllPageUrl(html):  # 获取专辑下所以分页URL列表
    reg = r'<a href="[^s]+?p=(\d*?)">'
    mre = re.compile(reg)
    numlist = re.findall(mre, html)
    pages=int(numlist[-1])
    pagelist=[]
    for i in range(1,pages+1):
        pagelist.append(albumURL+"?p="+str(i))
    return  pagelist

albumURL = "http://www.topit.me/album/1830217"  
print getAllPageUrl(getHtml(albumURL))
