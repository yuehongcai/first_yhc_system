#coding: utf-8

from devops import models

class UpdateInfo(object):

	def __init__(self,request,mon_obj,data): # mon_obj代表具体哪个设备
		self.request = request
		self.mon_obj = mon_obj
		self.data = data
		self.sn = data.get('sn')
		self.update()

	def update(self):
		self.mon_obj.ip = self.data.get('ip')
		self.mon_obj.boot_time = self.data.get('boot_time')
		self.mon_obj.hostname = self.data.get('hostname')
		self.mon_obj.cpu_util = self.data.get('cpu_util')
		self.mon_obj.mem_util = self.data.get('mem_util')
		self.mon_obj.disk_util = self.data.get('disk_util')
		self.mon_obj.swap_util = self.data.get('swap_util')
		self.mon_obj.average_load = self.data.get('average_load')
		self.mon_obj.average_iops = self.data.get('average_iops')
		self.mon_obj.io_read_throughput = self.data.get('io_read_throughput')
		self.mon_obj.io_write_throughput = self.data.get('io_write_throughput')
		self.mon_obj.nic_average_throughput = self.data.get('nic_average_throughput')
		self.mon_obj.net_average_error = self.data.get('net_average_error')
		self.mon_obj.save()
		self.update_service()

	def update_service(self):
		for k,v in self.data.get('service_data').items():  # 如httpd:0 , mariadb:1
			if k != 'sn':  ##传过来的key有是sn的，但是我们需要的key是服务名
				service_obj = models.Service.objects.get(sn=self.sn,service_name=k)
				service_obj.service_status = v
				service_obj.save()

class AddInfo(object):

	def __init__(self,request,data):
		self.request = request
		self.data = data
		self.sn = data.get('sn')
		self.add()

	def add(self):
		defaults = {
			'ip': self.data.get('ip'),
			'hostname': self.data.get('hostname'),
			'boot_time': self.data.get('boot_time'),
			'cpu_util': self.data.get('cpu_util'),
			'mem_util' : self.data.get('mem_util'),
			'disk_util' : self.data.get('disk_util'),
			'swap_util' : self.data.get('swap_util'),
			'average_load' : self.data.get('average_load'),
			'average_iops' : self.data.get('average_iops'),
			'io_read_throughput': self.data.get('io_read_throughput'),
			'io_write_throughput': self.data.get('io_write_throughput'),
			'nic_average_throughput' : self.data.get('nic_average_throughput'),
			'net_average_error' : self.data.get('net_average_error')
		}
		models.MonitorServer.objects.update_or_create(sn=self.sn,defaults=defaults)  ## update_or_create防止重复记录插入
		for k,v in self.data.get('service_data').items(): # 下列是入库Service表
			if k != 'sn':
				models.Service.objects.update_or_create(service_name=k,service_status=v,sn=self.sn)