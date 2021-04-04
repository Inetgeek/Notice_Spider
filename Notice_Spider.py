#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import datetime
import urllib.request
import requests
import json
from bs4 import BeautifulSoup

def getTitle (url):
    headers = ('User-Agent',"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
    bs = BeautifulSoup(html,'html.parser')
    Title_links = bs.select('.Article_Title > a')
    return Title_links

def getDate (url):
    headers = ('User-Agent',"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
    bs = BeautifulSoup(html,'html.parser')
    Date_links = bs.select('.Article_PublishDate')
    return Date_links

def getNowDate():
    now_time = datetime.datetime.now()
    yes_time = now_time+datetime.timedelta(days=-3)
    current_time = yes_time.strftime('%Y-%m-%d')
    return current_time

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

for date,text, link, in zip(dates, contents, links):
    data = date+' '+text+':http://xxx.xxx.com'+link
    if date == Now_Date:
        send_data = send_data+data+'\n\n'

print('\n')
print(send_data)

import smtplib
from email import (header)
from email.mime import (text, multipart)
import time

def sender_mail():
    smtp_Obj = smtplib.SMTP_SSL('smtp.qq.com',465) # 连接qq邮箱SMTP服务器，端口是25
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

sender_mail()

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
if len(send_data) > 0:
    res = requests.post(url,data=body,headers=headers)
    #sender_mail()
    print(res.status_code)
    print(res.text)
    #print(send_data)

