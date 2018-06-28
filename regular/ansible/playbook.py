#coding: utf-8
import subprocess
import sys
import logging

'''
hello.yml使用样例,需要实现pip install ansible

---
- hosts: temp   ## 这个主机组是固定的，写playbook必须指定组为temp
  tasks:
  - name: shell command
    shell: echo hello world `date` by `hostname` >/tmp/hello.log
'''

#定义打印日志,#通过logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(filename='task_exec_ansible.log',format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',datefmt='%Y-%m-%d %H:%M:%S %p',level=10)

class AnsibleTask():
    def __init__(self,host=None,connection='ssh',user=None,password=None,port=22, extra_vars=None):
        self.host = host
        self.connection = connection
        self.user = user
        self.password = password
        self.port = port

        self.hostgroup = 'temp'
        self._validate()
        self.hosts_file = 'ansible_hosts.txt'
        self.generate_hosts_file()


    def _validate(self):
            if not self.host or not self.user or not self.password:
                    raise Exception('主机的IP，用户名，密码均不能为空')

    def generate_hosts_file(self):
        string = '''[%s] \n%s ansible_connection=%s ansible_ssh_user=%s ansible_ssh_pass=%s ansible_ssh_port=%s  ''' %(self.hostgroup,self.host,self.connection,self.user,self.password,self.port)
        with open(self.hosts_file,'w') as f:
            f.write(string+'\n')

    def run_command(self):
        res = subprocess.Popen('ansible %s -m ping --inventory=%s '%(self.hostgroup,self.hosts_file),stdout=subprocess.PIPE,shell=True)
        result = res.stdout.read().decode()
        if len(result) >= 48:
            response_status = result[-48:].split()[-1].split('=')[-1]  ## 过滤的是failed
            '''
            result[-48:] = 'ok=2    changed=1    unreachable=0    failed=0 \n'
            '''
            if response_status == '0':  ## 如果执行成功，则进行info日志记录
                logging.info(result)
            else:
                logging.error(result)


    def run_playbook(self,playbook):
        res = subprocess.Popen('ansible-playbook %s --inventory=%s '%(playbook,self.hosts_file),stdout=subprocess.PIPE,shell=True)
        result = res.stdout.read().decode()
        if len(result) >= 48:
            response_status = result[-48:].split()[-1].split('=')[-1]  ## 过滤的是failed
            '''
            result[-48:] = 'ok=2    changed=1    unreachable=0    failed=0 \n'
            '''
            if response_status == '0':  ## 如果执行成功，则进行info日志记录
                logging.info(result)
            else:
                logging.error(result)


if __name__ == '__main__':
    obj = AnsibleTask(host='192.168.42.130',connection='ssh',user='root',password='passw0rd',port=22)
    #obj.run_command()
    obj.run_playbook('hello.yml')
