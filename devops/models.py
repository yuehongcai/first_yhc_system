# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

'''下面是cmdb数据模型'''

class CmdbServer(models.Model):
    sn = models.CharField(max_length=128,unique=True,verbose_name='资产序列号',db_column='序列号')
    ip = models.GenericIPAddressField(null=True,blank=True,verbose_name='管理IP地址')
    hostname = models.CharField(max_length=64,null=True,blank=True,verbose_name='主机名',db_column='主机名')
    manufacturer = models.CharField(max_length=64,null=True,verbose_name='产商',db_column='产商')
    product_model = models.CharField(max_length=64,null=True,verbose_name='服务器型号',db_column='服务器型号')
    cpu_all_core = models.PositiveSmallIntegerField(blank=True, null=True,verbose_name='物理CPU个数*每CPU核数（无超线程）')
    mem_size = models.FloatField(blank=True, null=True,verbose_name='内存大小(GB)',db_column='内存(GB)')
    disk_size = models.FloatField(blank=True, null=True,verbose_name='本地所有磁盘总和(GB)',db_column='磁盘总和(GB)')
    asset_type_choice = (
        ('server','物理服务器'),
        ('virtual','虚拟机'),
        ('other','其他'),
    )
    asset_type = models.CharField(choices=asset_type_choice,max_length=64,default='server',verbose_name='资产类型')
    os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)
    created_by_choice = (
        ('auto','自动添加'),
        ('manual','手工录入'),
    )
    created_by = models.CharField(choices=created_by_choice,max_length=32,default='auto',verbose_name='添加方式')
    update_time = models.DateField(auto_now=True)  ## 自动添加时间，不需要单独处理该字段就会插入数据库中

'''
下面是监控部分
cpu利用率，服务进程状态，空闲内存,服务进程状态和磁盘空间使用率，以及网络接口丢包率
'''
class MonitorServer(models.Model):
    sn = models.CharField(max_length=128,null=True,verbose_name='系统序列号')
    hostname = models.CharField(max_length=64,null=True,blank=True,verbose_name='主机名',db_column='主机名')
    ip = models.GenericIPAddressField(unique=True,db_column='被监控节点IP') # 被监控节点的IP地址
    boot_time = models.CharField(max_length=64,null=False)
    cpu_util = models.FloatField(max_length=16,db_column='CPU利用率',default=0)  # CPU利用率
    mem_util = models.FloatField(max_length=16,db_column='已用内存比例',default=0)  # 剩余内存/总内存比例
    disk_util = models.FloatField(max_length=16,db_column='磁盘空闲利用率',default=0)
    swap_util = models.FloatField(max_length=16,db_column='swap利用率',default=0)
    average_load = models.FloatField(db_column='平均负载',default=0)
    average_iops = models.IntegerField(db_column='IOPS',null=True,blank=True,default=0)
    io_read_throughput = models.IntegerField(db_column='IO读吞吐量',default=0)
    io_write_throughput = models.IntegerField(db_column='IO写吞吐量',default=0)
    nic_average_throughput = models.IntegerField(db_column='网络收发吞吐量',default=0)
    net_average_error= models.FloatField(db_column='收发丢包个数',default=0)
    update_time = models.DateTimeField(auto_now=True)  ## 自动添加时间，不需要单独处理该字段就会插入数据库中


class Service(models.Model):
    sn = models.CharField(max_length=128,null=True,verbose_name='系统序列号')  # 绝对不能是唯一约束
    service_name = models.CharField(max_length=32,verbose_name='服务名称')
    status = (
           (0,'down'),
           (1,'active'),
    )
    service_status = models.SmallIntegerField(choices=status,verbose_name='服务状态',default=1)

'''
告警部分
'''
class MonitorAlert(models.Model): ##存放告警的所有动态信息
    alert_status = (
        (1,'info'),
        (2,'warning'),
        (3,'disaster'),
    )
    level = models.SmallIntegerField(choices=alert_status,db_column='监控级别',default=1)
    time = models.DateTimeField(auto_now=True,db_column='告警时间')
    info = models.CharField(max_length=128,db_column='告警详细信息',default='无') ## 由用户手工备注
    item = models.CharField(max_length=64,db_column='监控项',null=True)  ## 一台主机可以有多个监控项进行告警
    value = models.FloatField(null=True) #监控值
    host = models.CharField(max_length=64,db_column='被监控节点')  ## 被监控节点，可以是IP或主机名
    ack_status = (
        (0,'未确认'),
        (1,'已确认'),
    )
    ack = models.SmallIntegerField(choices=ack_status,db_column='确认状态',default=0)


class AlertConfig(models.Model):  ##存放告警的静态信息
    email_sender = models.EmailField(db_column='发件人邮箱')
    email_sender_password = models.CharField(max_length=16,db_column='发件人密码')
    email_receiver = models.EmailField(db_column='接收人邮箱')
    email_smtp_server = models.CharField(max_length=64,db_column='SMTP服务器')
    dingding_url = models.CharField(max_length=128,db_column='钉钉URL地址',null=True,blank=True)


class AlertThreshold(models.Model): ##阈值数据表，实际采集的数据需要这个表的数据进行比对
    template = models.CharField(max_length=32,unique=True,db_column='监控模板',default='common')  #如web或mysql或者common
    cpu_threshold_warning = models.IntegerField()
    mem_threshold_warning = models.IntegerField()
    disk_threshold_warning = models.IntegerField()
    swap_threshold_warning = models.IntegerField()
    upload_threshold_warning = models.FloatField()
    errror_packet_threhold_warning = models.IntegerField()

    cpu_threshold_disaster = models.IntegerField()
    mem_threshold_disaster = models.IntegerField()
    disk_threshold_disaster = models.IntegerField()
    swap_threshold_disaster = models.IntegerField()
    upload_threshold_disaster = models.FloatField()
    errror_packet_threhold_disaster = models.IntegerField()

class LogKind(models.Model):
    #value = models.IntegerField(auto_created=True) ##对应form表单的choices数值
    logpath = models.CharField(max_length=256,db_column='日志路径')
    name = models.CharField(max_length=32,db_column='显示名称')
