#-*-coding:utf-8 -*-
#!/usr/bin/python
import urllib
import urllib2
import cookielib
import requests
import re
import os


def login(loginURL):
    ID = raw_input("Please input your student ID:")
    Password = raw_input("Please input your password:")
    print 'Loading........'
    page = urllib2.urlopen(loginURL).read()
    postdata = urllib.urlencode({
      	    '__VIEWSTATE':getVIEW(page),   		
      	    'txtYhm':ID,				#std ID
     	    'txtMm':Password,			#password
            'rblJs':'学生',
            'btnDl':' 登录'})
    myRequest = urllib2.Request(loginURL, postdata,getheaders())

    loginPage = urllib2.urlopen(myRequest).read()
    page =  unicode(loginPage, 'gb2312').encode("utf-8") 
    try:
    	name = getName(page)
        logindata = (myRequest,name,ID)
        return logindata
    except IndexError, e:
    	print "User-name or password error, try again!"
	main()
	exit()
    else:
	pass
def getheaders(Request=None):  #为每次访问提供Headers
    headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'202.200.112.200',
            'Pragma':'no-cache',
            'Referer':'',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0 Iceweasel/44.7.36'
            }
    if Request != None:
        headers['Referer'] = Request.get_full_url() #获取上次的访问地址作为本次访问的Referer值
    return headers

def gethash(url):          # 获取第一次打开登录页时随机产生的hash码
	headers = requests.head(url).headers
        val = headers['location']
        return val[:28]

def getVIEW(Page):          # 获取页面访问状态
        view = r'name="__VIEWSTATE" value="(.+)" '
        view = re.compile(view)
        return view.findall(Page)[0]

def Print(Score_html):
    rules = "<tr.*?<td>([0-9\-]{9}).*?([1-2]).*?[0-9].*?<td>(.*?)</td.*?<td>.*?</td><td>([0-9\.]*)</td><td>.*?([0-9\.]*)</td><td>(.*?)</td>.*?</tr>"
    res = re.compile(rules,re.S)
    iteams = re.findall(res,Score_html)
    date = ('','')
    for iteam in iteams:
        if date != iteam[0:2]:
            date = iteam[0:2]
            print '-------------------------------------------------------------------'
            print  '\t\t学年：%s\t\t学期：%s' % date
            print '-------------------------------------------------------------------'
        print '\t%s\t%s\t%s\t%s' % iteam[2:6]

def getName(loginPage):		# 获取姓名
           Sname = r'<span id="xhxm">(.+)同学</span>'
           Sname = re.compile(Sname)
           try:
		return Sname.findall(loginPage)[0]
           except IndexError, e:
		raise e
		print "User-name or password error, try again!"
		main()
def main():
        URL = 'http://202.200.112.200' #登录网址
        hashcode = gethash(URL+'/default6.aspx')
        loginURL = URL+hashcode+'default6.aspx'
        logindata = login(loginURL) #登录成功后返回的信息
        MyRequest = logindata[0]
        name = logindata[1]
        print name
        ID = logindata[2]
        getdata = urllib.urlencode({
	'xh':ID,
	'xm':name,
	'gnmkdm': 'N121605'
        })
        accessURL = URL+hashcode+'xscj_gc.aspx?'+getdata
	MyRequest = urllib2.Request(accessURL,None,getheaders(MyRequest) ) #成绩查询页面
        loginPage=unicode(urllib2.urlopen(MyRequest).read(), 'gb2312').encode("utf-8")
	data = urllib.urlencode({
		"__VIEWSTATE":getVIEW(loginPage),
		"Button5":"按学年查询"
		})
       # print MyRequest.get_full_url()
       # print loginPage
	MyRequest= urllib2.Request(accessURL,data,getheaders(MyRequest))		#按学年查询页面
	html = urllib2.urlopen(MyRequest)
	result =  unicode(html.read(), 'gb2312').encode("utf-8")
#	print result
        Print (result)												# Score
if __name__ == '__main__':
    main()
