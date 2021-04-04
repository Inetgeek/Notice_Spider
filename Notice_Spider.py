#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import datetime
import urllib.request
import requests
import json
from bs4 import BeautifulSoup
#模拟浏览器对网站发出请求并解析获得级网文章发表标题等信息
def getTitle (url):
    headers = ('User-Agent',"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
    bs = BeautifulSoup(html,'html.parser')
    Title_links = bs.select('.Article_Title > a')
    return Title_links
#模拟浏览器对网站发出请求并解析获得级网文章发表时间等信息
def getDate (url):
    headers = ('User-Agent',"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
    bs = BeautifulSoup(html,'html.parser')
    Date_links = bs.select('.Article_PublishDate')
    return Date_links
#获取当前日期(-3表示今日往前推3天)
def getNowDate():
    now_time = datetime.datetime.now()
    yes_time = now_time+datetime.timedelta(days=-3)
    current_time = yes_time.strftime('%Y-%m-%d')
    return current_time
#获取文章标题、时间、链接等
url = 'http://xxx.xxx.com'
linklist_Title = getTitle(url)
linklist_Date = getDate(url)
contents = []
links = []
dates = []
send_data = ''
Now_Date = getNowDate()
for link in linklist_Title:
    contents.append(link.text.strip())
    links.append(link.get('href'))

for date in linklist_Date:
    dates.append(date.text.strip())
#获取指定日期的文章信息
for date,text, link, in zip(dates, contents, links):
    data = date+' '+text+':http://xxx.xxx.com'+link
    if date == Now_Date:
        send_data = send_data+data+'\n\n'

print('\n')
print(send_data)
#群发邮件，邮件系统为qq的，端口为465的ssl加密传输
import smtplib
from email import (header)
from email.mime import (text, multipart)
import time

def sender_mail():
    smtp_Obj = smtplib.SMTP_SSL('smtp.qq.com',465) # 连接qq邮箱SMTP服务器，端口是465
    sender_addrs = 'xxx@foxmail.com'       # 发件人邮箱账号
    password = "uaxxxxxxxxxxxge"           # 发件人邮箱密码  即配置生成的授权码
    smtp_Obj.login(sender_addrs, password)
    receiver_addrs = ['yyy@foxmail.com','zzz@foxmail.com']  #群发的收件人
    for email_addrs in receiver_addrs:
        try:
            msg = multipart.MIMEMultipart()
            msg['From'] = "InetGeek"
            msg['To'] = email_addrs
            msg['subject'] = header.Header('今日级网更新通知', 'utf-8')
            msg.attach(text.MIMEText('今日:['+getNowDate()+']级网最新通知如下:\n\n'+send_data, 'plain', 'utf-8'))  #邮件内容
            smtp_Obj.sendmail(sender_addrs, email_addrs, msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
            print('成功发送给%s' % ( email_addrs))
        except Exception as e:
            continue
    smtp_Obj.quit() #退出

#sender_mail()
#用json格式向push+推送文章
token = '4bxxxxxxxxxxxxxxxxxxxxxxx5'
title= '今日级网更新通知'
content = send_data 
url = 'http://pushplus.hxtrip.com/send'
data = {
    "token":token,
    "title":title,
    "content":content
}
body=json.dumps(data).encode(encoding='UTF-8')
headers = {'Content-Type':'application/json'}
#判断是否有更新内容，有则发送
if len(send_data) > 0:
    res = requests.post(url,data=body,headers=headers)
    sender_mail()
    print(res.status_code)
    print(res.text)
    #print(send_data)

