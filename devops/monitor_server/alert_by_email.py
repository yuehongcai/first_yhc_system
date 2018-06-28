#coding: utf-8
import smtplib
from email.mime.text import MIMEText
from devops import models

class Config(object):
    def __init__(self,sender,password,receiver,smtp_server):
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.smtp_server = smtp_server
        models.AlertConfig.objects.update_or_create(email_sender=self.sender,email_sender_password=self.password,
                                         email_receiver=self.receiver,email_smtp_server=self.smtp_server)

class Alert(object):
    def __init__(self,level,host,item):
        self.string = '告警! The %s has occured host %s , its item is %s' %(level,host,item)
        self.msg = MIMEText(self.string,'plain','utf-8') #正文
        self.sender = models.AlertConfig.objects.first().email_sender
        self.receiver = models.AlertConfig.objects.first().email_receiver
        self.password = models.AlertConfig.objects.first().email_sender_password
        self.smtp_server = models.AlertConfig.objects.first().email_smtp_server

    def _alert(self):
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver
        self.msg['Subject'] = '邮件发送测试工作'  ##标题
        port = 25
        server = smtplib.SMTP(self.smtp_server,port)
        server.login(self.sender,self.password)
        server.sendmail(self.sender,self.receiver,self.msg.as_string())
        server.quit()


'''
网易邮箱使用案例
    sender = '15706107661@163.com'
    password = 'yhc199510'  ## 网易授权码，需要在网易邮箱设置
    receiver = '2424013264@qq.com'
    smtp_server = 'smtp.163.com'
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = '邮件发送测试工作'
    port = 25

    server = smtplib.SMTP(smtp_server,port)
    server.login(sender,password)
    server.sendmail(sender,receiver,msg.as_string())
    server.quit()
'''