# encoding: utf-8
# 采用redis发送日志
from __future__ import unicode_literals, division

import time
import sys,os
import signal
import urllib2
import math
import redis

FLAG = True

def get_last_lines(f, num=10):
	"""读取文件的最后几行
	"""
	size = 1000
	try:
		f.seek(-size, 2)
	except IOError:  # 文件内容不足size
		f.seek(0)
		return f.readlines()[-num:]

	data = f.read()
	lines = data.splitlines()
	n = len(lines)
	while n < num:
		size *= int(math.ceil(num / n))
		try:
			f.seek(-size, 2)
		except IOError:
			f.seek(0)
			return f.readlines()[-num:]
		data = f.read()
		lines = data.splitlines()
		n = len(lines)

	return lines[-num:]


def process_line(r,channel,line):
	r.publish(channel, line.strip())

def sig_handler(signum, frame):
	global FLAG
	FLAG = False

signal.signal(signal.SIGALRM, sig_handler) # 收到退出信号后，以比较优雅的方式终止脚本
signal.alarm(300) # 为了避免日志输出过多，浏览器承受不住，设置5分钟后脚本自动停止


def force_str(s):
	if isinstance(s, unicode):
		s = s.encode("utf-8")
	return s


def tail(remote_host,log_path,line_count=10):
	channel = '{%s:%s:%s}' %(remote_host,log_path,line_count)
	r = redis.Redis(host='127.0.0.1')
	if not os.path.exists(log_path):
		sys.exit('你输入的日志路径%s不存在！请检查是否是绝对路径') %log_path

	with open(log_path, 'r') as f:
		last_lines = get_last_lines(f, int(line_count))
		for line in last_lines:
			process_line(r, channel, force_str(line))
		try:
			while FLAG:  # 通过信号控制这个变量，实现优雅退出循环
				line = f.readline()
				if not line:  ## 如果此时没有实时日志输出了，则进行等待
					time.sleep(0.05)
					continue
				process_line(r, channel, force_str(line)) ## 如果又有新的日志出来了，则进行处理
		except KeyboardInterrupt:
			pass


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python %s log_path line_count" %(sys.argv[0])
        exit(1)

    tail(log_path=sys.argv[1],line_count=sys.argv[2])

'''
使用http发送日志
# encoding: utf-8
from __future__ import unicode_literals, division

import time
import sys,os
import signal
import urllib2
import math

FLAG = True
uri = '/devops/log/view/'
django_server_ip = '192.168.0.6' # 通过域名来实现，是为了后期扩展方便些，万一django双节点
django_server_port = 8080

def get_last_lines(f, num=10):
	"""读取文件的最后几行
	"""
	size = 1000
	try:
		f.seek(-size, 2)
	except IOError:  # 文件内容不足size
		f.seek(0)
		return f.readlines()[-num:]

	data = f.read()
	lines = data.splitlines()
	n = len(lines)
	while n < num:
		size *= int(math.ceil(num / n))
		try:
			f.seek(-size, 2)
		except IOError:
			f.seek(0)
			return f.readlines()[-num:]
		data = f.read()
		lines = data.splitlines()
		n = len(lines)

	return lines[-num:]


def process_line(line):
	url = 'http://%s:%s%s' %(django_server_ip,django_server_port,uri)
	try:
		request = urllib2.Request(url=url,data=line)
		print line
		response = urllib2.urlopen(request)
		message = '发送成功'
		print "\033[32;32;5m 发送成功，请登陆Devops运管平台进行审核 \033[0m"
	except Exception as e:
		message = '发送失败:%s' %e
		print '\033[31;1m发送失败，%s\033[0m' %e


def sig_handler(signum, frame):
	global FLAG
	FLAG = False

signal.signal(signal.SIGALRM, sig_handler) # 收到退出信号后，以比较优雅的方式终止脚本
signal.alarm(300) # 为了避免日志输出过多，浏览器承受不住，设置5分钟后脚本自动停止


def force_str(s):
	if isinstance(s, unicode):
		s = s.encode("utf-8")
	return s


def tail(log_path,line_count=10):
	if not os.path.exists(log_path):
		sys.exit('你输入的日志路径%s不存在！请检查是否是绝对路径') %log_path

	with open(log_path, 'r') as f:
		last_lines = get_last_lines(f, int(line_count))
		for line in last_lines:
			process_line(force_str(line))
		try:
			while FLAG:  # 通过信号控制这个变量，实现优雅退出循环
				line = f.readline()
				if not line:  ## 如果此时没有实时日志输出了，则进行等待
					time.sleep(0.05)
					continue
				process_line(force_str(line)) ## 如果又有新的日志出来了，则进行处理
		except KeyboardInterrupt:
			pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python %s log_path line_count" %(sys.argv[0])
        exit(1)
    tail(log_path=sys.argv[1],line_count=sys.argv[2])

'''''