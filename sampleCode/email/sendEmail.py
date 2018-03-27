#coding:utf8
'''
日报
'''
import email
import smtplib
import os
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# python3 设置发件人昵称
from email.utils import formataddr

class EmailSender:
    def __init__(self):
        self.user = 'xxx@xxx.com'
        self.passwd = 'xxx'
        self.to_list = ['',]
        self.cc_list = ['',]
        self.tag = '安卓自动打包邮件，请勿回复！'
        self.doc = None


    def send(self):
        '''
        发送邮件
        '''
        try:
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com",port=465)
            server.login(self.user,self.passwd)
            server.sendmail(self.user, self.to_list, self.get_attach())
            server.close()
            print( "send email successful")
        except Exception as e:
            print( "send email failed %s"%e)
    def get_attach(self):
        '''
        构造邮件内容
        '''
        attach = MIMEMultipart()

        #添加邮件内容
        #txt = MIMEText(self.content, 'plain', 'utf-8')
        txt  = MIMEText(self.content, 'html', 'utf-8')
        attach.attach(txt)  

        if self.tag is not None:
            #主题,最上面的一行
            attach["Subject"] = Header(self.tag, 'utf-8')
        if self.user is not None:
            #显示在发件人
            attach['From'] = formataddr(["前端-安卓组", self.user])
        if self.to_list:
            #收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            #抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            #估计任何文件都可以用base64，比如rar等
            #文件名汉字用gbk编码代替
            name = os.path.basename(self.doc).encode("gbk")
            f = open(self.doc,"rb")
            doc = MIMEText(f.read(), "base64", "gb2312")
            doc["Content-Type"] = 'application/octet-stream'
            doc["Content-Disposition"] = 'attachment; filename="'+name+'"'
            attach.attach(doc)
            f.close()
        return attach.as_string()


if __name__=="__main__":
    my = EmailSender()
    
    my.user = 'xxx@xxx.com'
    my.passwd = 'xxx'
    my.to_list = ["xxx@163.com",'xxx@qq.com']
    my.cc_list = ["",]
    my.tag = "安卓最新测试包(本邮件是程序自动下发的，请勿回复！)"

    my.content = """
<p>  hi all:</p>
<p>安卓最新测试包，请点击下面链接查看详情，或扫描二维码直接下载。</p>
<p><a href="https://www.pgyer.com/jzUL">App详情页</a></p>
<p> App二维码：</p>
<p><img src="https://www.pgyer.com/app/qrcode/jzUL"></p>
"""

    my.send()


