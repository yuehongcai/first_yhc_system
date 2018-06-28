#coding: utf-8
import subprocess
import os,sys

def execute(remote_host,logpath):
    filename = __file__  ## 当前脚本名
    current_dir  = os.path.dirname(os.path.abspath(filename))
    BASE_DIR = os.path.dirname(current_dir)
    sys.path.append(BASE_DIR)
    from regular.ansible import playbook
    #res = subprocess.
    #play = playbook.AnsibleTask(host=ip,user=username,password=password,port=port)
