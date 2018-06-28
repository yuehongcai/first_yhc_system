#coding: utf-8
#如下是monitorserver守护进程代码，而后进行告警
import alert_by_dingding,alert_by_email
from devops import models
import datetime

class CustomThreshold(object):
	def __init__(self,data):
		self.obj = models.CmdbServer.objects.get(sn=data.get('sn'))
		self.upload_threshold_warning = (self.obj.cpu_all_core) * 0.8
		self.upload_threshold_disaster = self.obj.cpu_all_core
		self.data = data
		self.host = data.get('ip')
		self._threshold_init()


	def _threshold_init(self):
		cpu_threshold_warning = 80
		mem_threshold_warning = 80
		disk_threshold_warning = 90
		swap_threshold_warning = 80
		errror_packet_threhold_warning = 500

		cpu_threshold_disaster = 95
		mem_threshold_disaster = 95
		disk_threshold_disaster = 95
		swap_threshold_disaster = 90
		errror_packet_threhold_disaster = 1000
		obj = models.AlertThreshold.objects.filter(template='common')  ## filter方法无法修改某个字段的值
		if not obj:  ## 如果本来没有改含有通用模板的记录，则进行创建
			models.AlertThreshold.objects.update_or_create(
				cpu_threshold_warning = cpu_threshold_warning,
				mem_threshold_warning = mem_threshold_warning,
				disk_threshold_warning = disk_threshold_warning,
				swap_threshold_warning = swap_threshold_warning,
				errror_packet_threhold_warning = errror_packet_threhold_warning,
				upload_threshold_warning = self.upload_threshold_warning,
				cpu_threshold_disaster = cpu_threshold_disaster,
				mem_threshold_disaster = mem_threshold_disaster,
				disk_threshold_disaster = disk_threshold_disaster,
				swap_threshold_disaster = swap_threshold_disaster,
				errror_packet_threhold_disaster = errror_packet_threhold_disaster,
				upload_threshold_disaster = self.upload_threshold_disaster
			)
		else:
			update_obj = models.AlertThreshold.objects.get(template='common')
			update_obj.upload_threshold_warning = self.upload_threshold_warning
			update_obj.upload_threshold_disaster = self.upload_threshold_disaster
			update_obj.save()

		warning_lst = [cpu_threshold_warning,mem_threshold_warning,disk_threshold_warning,swap_threshold_warning,errror_packet_threhold_warning,self.upload_threshold_warning]
		disaster_lst = [cpu_threshold_disaster,mem_threshold_disaster,disk_threshold_disaster,swap_threshold_disaster,errror_packet_threhold_disaster,self.upload_threshold_disaster]

		lst = ['cpu_util','mem_util','disk_util','swap_util','net_average_error','average_load']
		## 这是客户端脚本发送过来的，必须和上面的warning_lst和disaster_lst键保持一致
		if len(lst) == len(warning_lst) and len(warning_lst) == len(disaster_lst):  ## 保证键一致
			print 'before:%s' %datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			for i in range(len(lst)):
				if self.data.get(lst[i]) > disaster_lst[i]:
					if models.AlertConfig.objects.first().email_sender:
						obj = alert_by_email.Alert(host=self.host,item=lst[i],level='disaster')
						obj._alert()
					if 	models.AlertConfig.objects.first().dingding_url:
						alert_by_dingding._alert(alert_host=self.host,alert_level='disaster',alert_item=lst[i])
					models.MonitorAlert.objects.create(level=3,host=self.host,item=lst[i],value=self.data.get(lst[i]),ack=0)  ##产生告警信息表

				elif self.data.get(lst[i]) > warning_lst[i]:
					if models.AlertConfig.objects.first().email_sender:
						obj = alert_by_email.Alert(host=self.host,item=lst[i],level='warning')
						obj._alert()
					if 	models.AlertConfig.objects.first().dingding_url:
						alert_by_dingding._alert(alert_host=self.host,alert_level='warning',alert_item=lst[i])
					models.MonitorAlert.objects.create(level=2,host=self.host,item=lst[i],value=self.data.get(lst[i]),ack=0)
			print 'after:%s' %datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		else:
			print '检查代码的列表顺序是否一致'

