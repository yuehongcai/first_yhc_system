#coding: utf-8
# 客户端脚本，用systemd守护进程实现
import datetime
import psutil
import urllib2
import time
import json
import subprocess
import os
import socket
import datetime

django_server_ip = '192.168.10.161' # 通过域名来实现，是为了后期扩展方便些，万一django双节点
django_server_port = 8080
uri = '/devops/monitor/writedb/'  # 发送到django对应的url
agent_dict = {}


def collect():   ## 动态数据，需要每隔10秒钟获取一次，然后取三次的平均值，总耗时20秒
	agent_dict['boot_time'] = datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H:%M")
	agent_dict['cpu_util'] = psutil.cpu_percent()
	agent_dict['mem_util'] = psutil.virtual_memory().percent  ##已用内存比例
	agent_dict['disk_util'] = psutil.disk_usage('/').percent
	agent_dict['swap_util'] = psutil.swap_memory().percent  ## vm利用率
	agent_dict['average_load'] = os.getloadavg()[-1]
	## 15分钟的平均负载
	agent_dict['average_iops'] = (psutil.disk_io_counters().read_count + psutil.disk_io_counters().write_count) / 2
	agent_dict['io_read_throughput'] = psutil.disk_io_counters().read_bytes/1024/1024
	agent_dict['io_write_throughput'] = psutil.disk_io_counters().write_bytes/1024/1024
	agent_dict['nic_average_throughput'] =  (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv ) /2/1024/1024  ##单位GB
	agent_dict['net_average_error'] = (psutil.net_io_counters().dropin + psutil.net_io_counters().dropout ) /2

	return agent_dict

def send_to_django():
	mon_dict  = dict()
	res1 = collect()
	time.sleep(10)
	res2 = collect()
	time.sleep(10)
	res3 = collect()

	mon_dict['cpu_util'] = round((res1['cpu_util']+ res2['cpu_util'] + res3['cpu_util']) / 3,2)
	mon_dict['mem_util'] = round((res1['mem_util'] + res2['mem_util'] + res3['mem_util'] ) / 3,2)
	mon_dict['disk_util'] = round((res1['disk_util']  + res2['disk_util']  + res3['disk_util'] ) / 3,2)
	mon_dict['swap_util'] = round((res1['swap_util']+ res2['swap_util']+ res3['swap_util']) / 3,2)
	mon_dict['average_load'] = round((res1['average_load'] + res2['average_load'] + res3['average_load']) / 3,2)
	mon_dict['average_iops'] = round((res1['average_iops'] + res2['average_iops'] + res3['average_iops']) / 3,2)
	mon_dict['io_read_throughput'] = round((res1['io_read_throughput']+ res2['io_read_throughput'] + res3['io_read_throughput']) / 3,2)
	mon_dict['io_write_throughput'] = round((res1['io_write_throughput'] + res2['io_write_throughput'] + res3['io_write_throughput']) / 3,2)
	mon_dict['nic_average_throughput'] = round((res1['nic_average_throughput']+ res2['nic_average_throughput'] + res3['nic_average_throughput']) / 3,2)
	mon_dict['net_average_error'] = round((res1['net_average_error'] + res2['net_average_error'] + res3['net_average_error']) / 3,2)

	res = subprocess.Popen("dmidecode -t system |grep 'Serial Number'" ,stdout=subprocess.PIPE,shell=True)
	result = res.stdout.read().decode()
	mon_dict['sn'] = result.split(':')[1].strip()
	mon_dict['hostname'] = socket.gethostname()
	mon_dict['ip'] = psutil.net_if_addrs()['eth0'][0][1]
	mon_dict['boot_time'] = datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H:%M")
	mon_dict.update(get_service())

	print mon_dict
	json_data = json.dumps(mon_dict)
	url = 'http://%s:%s%s' %(django_server_ip,django_server_port,uri)
	print '正在将数据发送至:[%s].....' %url
	try:
		request = urllib2.Request(url=url,data=json_data)
		print "\033[36;36;5m 发送完毕 \033[0m"  # 输出蓝色字体
		response = urllib2.urlopen(request)
		message = '发送成功'
		print "\033[32;32;5m 发送成功，请登陆Devops运管平台进行审核 \033[0m"
	except Exception as e:
		message = '发送失败:%s' %e
		print '\033[31;1m发送失败，%s\033[0m' %e


def get_service():  ## 获取指定服务的运行状态
	monitor_name = set(['httpd','mysqld','cobblerd','haproxy','docker-containerd','dnsmasq'])  # 用户指定监控的服务进程名称,这个psutil跟常规检测进程破ps -aux看到的结果不同
	service_dict = {}
	proc_name = set()  # 系统检测到的进程名称

	for proc in psutil.process_iter(attrs=['pid','name']):
		proc_name.add(proc.info['name'])

	proc_stop = monitor_name - proc_name  # 通过集合的形式来找出停掉的进程名,前者有但是后者没有的
	if proc_stop: # 如果确实有监控的进程停掉了
		for p in proc_stop:
			service_status = 'down'
			service_name = p
			service_dict[p] = service_status

	proc_ok = monitor_name & proc_name # 对于状态好的进程依然要记录
	if proc_ok:
		for p in proc_ok:
			service_status = 'active'
			service_name = p
			service_dict[p] = service_status

	return service_dict

if __name__ == '__main__':
	while True:
		send_to_django()