#coding: utf-8
import os
import sys

Params = {
    'server': '192.168.0.15',
    'port': 8080,
    'url': '/devops/cmdb/report/',   # 注意django的urls.py一些要写成'cmdb/report/$'的形式
}

file = os.path.abspath(sys.argv[0])
current_dir = os.path.dirname(file)
parent_dir = os.path.dirname(current_dir)

PATH = os.path.join(parent_dir,'log','cmdb.log')

