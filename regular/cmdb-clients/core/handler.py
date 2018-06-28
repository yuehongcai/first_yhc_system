#coding: utf-8
import json
import time
import urllib2
from core import info_collection
from conf import settings

class ArgvHandler(object):
    def __init__(self,args):
        self.args = args
        self.parse_args()

    def parse_args(self):
        if len(self.args) > 1 and hasattr(self,self.args[1]):
            func = getattr(self,self.args[1])  ##获取其内存地址
            func()
        else:
            self.help_msg()
            
    @staticmethod
    def help_msg():
        msg = '''
        collect_data 注：collect_data方法用来收集数据，并打印在屏幕上用于测试
        report_data  注：向django服务器发送数据，并且更新到资产平台系统中
        '''
        print msg

    @staticmethod
    def collect_data():  ##collect_data方法用来收集数据，并打印在屏幕上用于测试
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        print asset_data

    @staticmethod  ##普通方法，跟实例没有什么关系，不用传参self了
    def report_data():  ##report_data方法用来发送数据到服务器，从而实现自动化展示
        info = info_collection.InfoCollection()
        asset_data = info.collect() ## asset_data是字典对象
        print asset_data
        url = "http://%s:%s%s" %(settings.Params['server'],settings.Params['port'],settings.Params['url'])
        print ('正在将数据发送至:[%s].....' %url)
        json_data = json.dumps(asset_data)
        try:
            request =  urllib2.Request(url,json_data)
            print "\033[36;36;5m 发送完毕 \033[0m"  # 输出蓝色字体
            response = urllib2.urlopen(request)
            message = 'tst'
            print "\033[32;32;5m 发送成功，请登陆Devops运管平台进行审核 \033[0m"
        except Exception as e:
            message = '发送失败'
            print '\033[31;1m发送失败，%s\033[0m' %e
        with open(settings.PATH,'ab') as f:
            string = '发送时间：%s \t 服务器地址：%s \t 返回结果：%s \n' %(time.strftime('%Y-%m-%d %H:%M:%S'),url,message)
            f.write(string)
            print '日志记录成功！日志在clinets/log/目录下'