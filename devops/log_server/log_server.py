#coding: utf-8
import redis  ## redis的作用是避免长连接，异步等待客户端的日志数据
from threading import Thread
import time

class RedisHelper(object):
    def __init__(self):
        self._conn = redis.Redis(host='192.168.42.129')
        self.host = '192.168.42.129'  ## 日志客户端主机
        self.log_path = '/var/log/messages'
        ##self.channel = "logs:{hostname}:{log_path}".format(hostname=self.host, log_path=self.log_path)"
        self.channel = 'monitor'
        self.count = 0
        #self.string = self._conn.get('self.channel:%d' %self.count)

    def get_redis_log(self):
        obj = self._conn.pubsub()
        obj.subscribe(self.channel)  ## 订阅客户端主机发过来的日志频道
        while True:
            #self.string = obj.parse_response(block=False) ## 设置非阻塞模式
            line = obj.parse_response()
            self.count += 1
            self._conn.set('%s:%d' %(self.channel,self.count),line)  ## redis的key是monitor:数字（行号）
            #self._conn.set(self.channel,line)  ## redis的key是monitor:数字（行号）
        return True

    def main(self):
        t = Thread(target=self.get_redis_log)  ##多线程必须存在，否则将会进行阻塞，网页无法刷新
        t.setDaemon(True)
        t.start()

'''
web browser ---> django server --> plugin(log_server.py) ---> redis <-- 远端主机

'''