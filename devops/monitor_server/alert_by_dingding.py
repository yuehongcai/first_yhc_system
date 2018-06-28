#coding: utf-8
import urllib2
import time
import json
from devops import models
import requests
#dingding_url = 'https://oapi.dingtalk.com/robot/send?access_token=b5258c4335ed8ab792075013c965efcbf4f8940f92e7bd936cdc7842d3bf9405'
# 钉钉机器人token使用参考文档：http://www.pc6.com/infoview/Article_108931.html

def config(url):
    dingding_url = url
    config_obj = models.AlertConfig.objects.first()  ##取出第一条记录
    config_obj.dingding_url = dingding_url
    config_obj.save()


def _alert(alert_host,alert_level,alert_item):
    if alert_level == 'warning' or alert_level == 'disaster': ##告警
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "告警信息",
                "text": "### %s\n" % time.strftime("%Y-%m-%d %X") +
                "> #### 主机：%s \n\n" % alert_host +
                "> #### 监控项：%s \n\n" % alert_item +
                "> #### 程度：%s \n\n" % alert_level
            }
        }
        send(data)

def send(data):
    headers = {'Content-Type':'application/json;charset=UTF-8'}
    send_data = json.dumps(data).encode('utf-8')
    config_obj = models.AlertConfig.objects.first()
    dingding_url = config_obj.dingding_url
    print dingding_url
    requests.post(url=dingding_url,data=send_data,headers=headers)
