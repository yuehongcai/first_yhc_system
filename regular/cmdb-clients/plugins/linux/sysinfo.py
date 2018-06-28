#coding: utf-8
# 注意！本脚本经测试只针对CentOS 7系列，其他版本的系统不一定适合
import subprocess
import psutil
import socket
import platform

def collect():
    filter_keys = ['Manufacturer','Serial Number','Product Name']
    raw_data = {}

    for key in filter_keys:
        # 注意：不要使用sudo命令执行任务，可能造成数据不正常
        res = subprocess.Popen("dmidecode -t system |grep '%s'" %key,
                               stdout=subprocess.PIPE,shell=True)
        result = res.stdout.read().decode()
        data_list = result.strip().split(':')
        if len(data_list) > 1:
            raw_data[key] = data_list[1].strip()

    data = dict()
    data['asset_type'] = 'server'
    data['manufacturer'] = raw_data['Manufacturer']
    data['sn'] = raw_data['Serial Number']
    data['product_model'] = raw_data['Product Name']

    data.update(get_os_info())
    data.update(get_cpu_info())
    data.update(get_ram_info())
    data.update(get_nic_info())
    data.update(get_disk_info())
    return data

def get_os_info():
    data_dic = {
        'os_release':platform.platform().split('-')[-3] +''+ platform.platform().split('-')[-2],  ## 打印出centos 7.2.1511的格式，在前端减少空间大小
        'os_type': platform.system(),
        'hostname': socket.gethostname()
     }
    return data_dic

def get_cpu_info():
    base_cmd = 'cat /proc/cpuinfo'
    raw_data = {
        'cpu_model': "%s |grep 'model name'|head -1 " % base_cmd,
        'cpu_count': "%s |grep 'processor'|wc -l " % base_cmd,
        'cpu_core_count':"%s |grep 'cpu cores'|awk -F: '{SUM += $2} END {print SUM}' " % base_cmd,
    }

    for key,cmd in raw_data.items():
        try:
            cmd_res = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            raw_data[key] = cmd_res.stdout.read().decode().strip()
        except Exception as e:
            print (e)
            raw_data[key] = ""
    data = {
        'cpu_count':raw_data["cpu_count"],
        'cpu_core_count':raw_data['cpu_core_count'],
    }
    cpu_model = raw_data['cpu_model'].split(":")
    if len(cpu_model) > 1:
        data['cpu_model'] = cpu_model[1].strip()
    else:
        data['cpu_model'] = -1
    return data
'''
def get_ram_info():
    # raw_data 是服务器本身原始所有内存条的总和，raw_list是原始内存信息列表
    raw_data = subprocess.Popen("dmidecode -t memory|grep 'Installed Size'",stdout=subprocess.PIPE,shell=True)
    raw_list = raw_data.stdout.read().decode().split("\n")
    输出结果如下
    Installed Size: 8 MB (Single-bank Connection)
    Installed Size: Not Installed'

    mem_size = 0 # 内存大小,单位
    for line in raw_list:
        if line:
            if line.split(':')[1].split()[0].strip() != 'Not':  # 如果此卡槽没有装内存条
                mem_size += int(line.split(':')[1].split()[0].strip())
    mem_size = round(mem_size / 1024.0 , 2)  ##必须是1024.0，因为如果是512 / 1024 = 0，round保留两位小数
    return {'memory_size':mem_size}
'''

def get_ram_info():
    with open('/proc/meminfo') as mem_open:
        mem_size = int(mem_open.readline().split()[1])
        mem_size = round(mem_size /1024/1024.0 , 2)  ##必须是1024.0，因为如果是512 / 1024 = 0，round保留两位小数
    return {'memory_size':mem_size}


def get_nic_info():
    '''
    网卡名称（包括loop口和虚拟网桥）、IP地址、掩码、MAC地址、带宽速率、
    '''
    nic_dict = {}
    ''' psutil.net_if_addrs()['eth0'] 输出结果如下
    [snic(family=2, address='192.168.0.10', netmask='255.255.255.0', broadcast='192.168.0.255', ptp=None), snic(family=10, address='fe80::332:aa6b:e407:ed8f%eth1', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snic(family=17, address='00:0c:29:f0:79:4f', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)]
    '''
    for key,value in psutil.net_if_addrs().items():
        # value[0]是IP地址栏元组，value[1]是IPv6地址栏元组，value[2]是MAC地址栏元组
        nic_dict[key] = {}  # 字典中嵌套字典
        nic_dict[key]['ip'] = value[0][1]   # ip地址
        nic_dict[key]['netmask'] = value[0][2]   # 掩码
        if len(value) >= 3: # (注：docker0等虚拟网桥无MAC地址元组，故需要判断总长度)
            nic_dict[key]['mac'] = value[2][1]  # MAC地址
        else:
            nic_dict[key]['mac'] = 'null'

        command = subprocess.Popen("ethtool %s|grep Speed" %key,stdout=subprocess.PIPE,shell=True)
        res = command.stdout.read() # 注意，此命令只会执行一次才出来结果，所以需要保存变量的值
        if res: # 因为lo和虚拟网桥没有工作速率speed，需要注意列表越界
            nic_speed = res.split(':')[1].strip()
            nic_dict[key]['speed'] = nic_speed
        else:
            nic_dict[key]['speed'] = 0

    return nic_dict

def get_disk_info():
    disk_data = subprocess.Popen("lsblk|grep disk",stdout=subprocess.PIPE,shell=True)
    disk_list = disk_data.stdout.read().decode().split('\n')
    '''输出结果如下
    [u'sda                     8:0    0   20G  0 disk ', u'sdb                     8:16   0   10G  0 disk ', u'']
    '''
    disk_dict = {}
    disk_size = 0
    for line in disk_list:
        if line:
            disk_dict[line.split()[0]] = line.split()[3]  ## sda:20G,sdb:4T
            if line.split()[3].endswith('G'):
                disk_size += int(line.split()[3].strip('G'))
            if line.split()[3].endswith('T'):
                disk_size += int(line.split()[3].strip('T')) * 1024
            if line.split()[3].endswith('K'):
                disk_size += int(line.split()[3].strip('K')) / 1024
    disk_dict.update({'disk_size':disk_size})
    return disk_dict

if __name__ == "__main__":
    # 收集信息功能测试
    d = collect()
    print d
