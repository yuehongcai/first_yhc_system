#coding: utf-8
from . import models
from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='用户名:',max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码:',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class CmdbServerAdd(forms.Form):
    add_ip = forms.GenericIPAddressField(label='远端机器IP地址',max_length=32,widget=forms.TextInput
    (attrs={'id':'add_agent_ip','name':'add_agent_ip','class':'form-control'}))
    add_username = forms.CharField(label='远程用户名',max_length=32,widget=forms.TextInput
    (attrs={'id':'add_agent_username','name':'add_agent_username','class':'form-control'}))
    add_password = forms.CharField(label='登陆密码',max_length=64,widget=forms.PasswordInput
    (attrs={'id':'add_agent_password','name':'add_agent_password','class':'form-control'}))
    add_port = forms.CharField(label='远程ssh端口',max_length=16,widget=forms.TextInput
    (attrs={'id':'add_agent_port','name':'add_agent_port','class':'form-control'}))

class MonitorAlertAdd(forms.Form):
    email_sender = forms.EmailField(required=False,widget=forms.TextInput
    (attrs={'name':'email_sender','class':'form-control','placeholder':'发件人邮箱'}))
    email_sender_password = forms.CharField(required=False,widget=forms.PasswordInput
    (attrs={'name':'email_sender_password','class':'form-control','placeholder':'发件人密码(可不填)'}))
    email_receiver = forms.EmailField(required=False,widget=forms.TextInput
    (attrs={'name':'email_receiver','class':'form-control','placeholder':'收件人邮箱'}))
    email_smtp_server = forms.EmailField(required=False,widget=forms.TextInput
    (attrs={'name':'email_smtp_server','class':'form-control','placeholder':'SMTP服务器：例如smtp.163.com'}))
    dingding_url = forms.CharField(required=False,label='钉钉机器人URL：',max_length=128,widget=forms.TextInput
    (attrs={'name':'dingding_url','class':'form-control','placeholder':'钉钉机器人URL'}))

    alert_level = forms.IntegerField(label='告警级别',required=False,widget=forms.Select(
            choices=(
                (1, '警告级别'),
                (2, '严重级别'),
    ),attrs={'class': 'form-control','name':'alert_level'}))
    alert_item = forms.IntegerField(label='监控项',required=False,widget=forms.Select(
           choices=(
               (0,'CPU利用率'),
               (1,'内存利用率'),
               (2,'磁盘利用率'),
               (3,'SWAP利用率'),
               (4,'网络丢包个数'),
               (5,'平均负载'),
    ),attrs={'class':'form-control','name':'alert_item'}))
    threhold = forms.FloatField(label='告警阈值',required=False,widget=forms.TextInput
    (attrs={'name':'threhold','class':'form-control'}))

class LogView(forms.Form):
    remote_host_lst = forms.IntegerField(label='远端主机列表',widget=forms.Select(
            attrs={'class':'form-control','name':'log_service'}))
    log_service = forms.IntegerField(label='日志种类',widget=forms.Select(
        choices=(
            (0,'messages系统日志'),
            (1,'mariadb数据库日志'),
            (2,'Nginx服务error日志'),
            (3,'dmesg硬件日志'),
        ),attrs={'class':'form-control','name':'log_service'}))

    line_count = forms.IntegerField(label='选择行数',widget=forms.Select(
        choices=(
            (20,'20'),
            (100,'100'),
            (500,'500'),
            (1000,'1000'),
            (2000,'2000'),
        ),attrs={'class':'form-control','name':'line_count'}))
    def __init__(self,*args,**kwargs): ## 让下拉框选取数据库的内容
        super(LogView,self).__init__(*args,**kwargs)
        self.fields['remote_host_lst'].widget.choices = [(host.id,host.ip) for host in models.CmdbServer.objects.all()]
        self.fields['log_service'].widget.choices = [ (service.id,service.name) for service in models.LogKind.objects.all()]