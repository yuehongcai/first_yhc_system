#coding: utf-8
from devops import models

class LogKindPreDefine(object):
    def __init__(self):
        self.predefine()

    def predefine(self):
        models.LogKind.objects.update_or_create(name='messages系统日志',logpath='/var/log/messages')
        models.LogKind.objects.update_or_create(name='mariadb数据库日志',logpath='/var/log/mariadb/mariadb.log')
        models.LogKind.objects.update_or_create(name='Nginx服务error日志',logpath='/var/log/nginx/error.log')
        models.LogKind.objects.update_or_create(name='dmesg硬件日志',logpath='/var/log/dmesg')

