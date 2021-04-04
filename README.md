### 概述
此项目为学院级网站解决自动化推送所开发，专为懒人设计(~作者~)，防止错过重要通知。
代码作者：InetGeek
版权申明：完全开放源代码。但使用或转发保存该项目代码时请备注原作者（INetGeek）信息
### 原理
该代码通过获取header包头模拟浏览器向网站发送请求，获得网站数据加载到本地进行解析，从而抓取到所需要的对应标签或者类或ID下的元素属性或内容，通过切片方式将数据进行重组和存储，最后通过邮件系统和微信推送系统进行推送。
### 库的安装
所要使用到的python库有：**time**/**datetime**/**requests**/**beautifulsoup**/**smtplib**等
其中第三方库为：**requests**/**beautifulsoup**。安装方法：
```
pip install beautifulsoup4
pip install requests
```
### 推送方式
push+ / QQ邮箱
### 云服务器定时执行程序
shell脚本
```
/usr/bin/python /www/server/panel/class/sendmail.py
```
### 作者
作者：InetGeek 版权归作者所有
CSDN博客：[InetGeek](https://blog.csdn.net/qq_34532102)
个人博客：[Digran's Blog](https://www.digran.cn)
