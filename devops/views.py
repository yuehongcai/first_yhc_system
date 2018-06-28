# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from forms import *
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from . import models  # 这句话比 from models import * 好
from cmdb_server import asset_handler
from monitor_server import monitor_handler
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from . import  forms
import os,sys
import socket,time
from monitor_server import alert_by_dingding,alert_by_email,threshold
import datetime
from devops.log_server import log_server,log_kind

def page_not_found(request):
    '''
    404报错页面
    '''
    return render(request,'devops/404.html')

def page_error(request):
    '''
    500报错页面
    '''
    return render(request,'devops/500.html')

@csrf_exempt
def login(request):
    if request.method == 'GET':
        userform = UserForm()
        return render(request,'devops/login.html',{'userform':userform})
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid(): # 先满足前端表单的条件
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return redirect('/index/')
            else:
                message = '用户密码不正确' ## message要想显示，需要在login.html定义{{ if message}}
                return render(request,'devops/login.html',locals())
        else:
                message = '表单输入有误'
                return render(request,'devops/login.html',locals())

@login_required
def index(request):
    return render(request,'devops/monitor/dashboard.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/login/')

'''
cmdb部分
'''
@csrf_exempt  ##跳过django的安全认证机制，处理客户端脚本和前端展示部分
def report(request):
    if request.method == 'POST': # request.POST本身是个dict对象，下面的是字典中的get方法
        asset_data = json.loads(request.body)  # 这是cmdb客户端脚本发过来的原始字典的键
        if not asset_data:
            print '没有资产数据！'
        if not issubclass(dict,type(asset_data)):
            print '数据必须为字典类型'

        '''以序列号SN作为资产的唯一识别码'''
        sn = asset_data.get('sn',None) # get方法获取该键值，如果有则返回，否则默认为空
        print sn
        if sn:
            asset_obj = models.CmdbServer.objects.filter(sn=sn)  # filter是把该字段该筛选出来
            if asset_obj: # 如果已经存在该资产，则进行更新该资产
                asset_handler.UpdateServer(request,asset_obj[0],asset_data) # 进入已上线的资产更新流程
                return HttpResponse('数据已经更新')
            else: # 如果不存在该资产，则进行创建新的资产
                asset_handler.NewServer(request,asset_data) # 类实例
                # response = new_asset.add_to_new_assets_zone()
                return HttpResponse('数据已经插入成功')
        else:
            print '没有资产序列号，请检查数据'
    else:
        return HttpResponse('客户端脚本，请运行main.py文件')

@csrf_exempt
def serverlist(request):
    pageSize = 10
    cmdb_server_lst = models.CmdbServer.objects.all().order_by('id')
    pageinator = Paginator(cmdb_server_lst, pageSize)   # 开始做分页
    if request.GET.get("page"):
        page = request.GET.get('page')
    else:
        page = 1
    data = pageinator.page(page)

    return render(request, 'devops/cmdb/serverlist.html',{'data':data,'cmdb/serverlist':cmdb_server_lst})

@csrf_exempt
@login_required
def serveradd(request): # 当用户点击部署按钮的时候才会触发此views
    if request.method == 'POST':
        cmdbserveradd_form = forms.CmdbServerAdd(request.POST)
        if cmdbserveradd_form.is_valid():
            ip = request.POST.get('add_ip')
            username = request.POST.get('add_username')
            password = request.POST.get('add_password')
            port = request.POST.get('add_port')
            print ip,username,password,port
            if check_ip(ip):  ## 检查IP地址的输入是否合法
                ip_list = models.CmdbServer.objects.values_list('ip',flat=True) #会直接出现IP地址列表，这个ip是Model字段
                if ip in ip_list:
                    msg = '你输入的节点IP地址已经部署了远程服务，请直接在主机信息列表查看'
                    print msg
                    return render(request,'devops/cmdb/serveradd.html',{'msg':msg,'cmdbserveradd_form':cmdbserveradd_form})
                else:
                    filename = __file__  ## 当前脚本名
                    current_dir  = os.path.dirname(os.path.abspath(filename))
                    BASE_DIR = os.path.dirname(current_dir)
                    sys.path.append(BASE_DIR)
                    from regular.ansible import playbook
                    play = playbook.AnsibleTask(host=ip,user=username,password=password,port=port)
                    yml_path = os.path.join(BASE_DIR,'regular','ansible','cmdb-agent.yml')
                    play.run_playbook(yml_path)
                    msg = 'OK，正在部署中，请稍等20秒...'
                    return render(request,'devops/cmdb/serveradd.html',{'msg':msg,'cmdbserveradd_form':cmdbserveradd_form})
            else:
                msg = '你输入的IP地址不合法，请重新输入'
                return render(request,'devops/cmdb/serveradd.html',{'msg':msg,'cmdbserveradd_form':cmdbserveradd_form})
    if request.method != 'POST': ## 当用户没有填入数据，直接访问页面的时候
        cmdbserveradd_form = forms.CmdbServerAdd()
        return render(request,'devops/cmdb/serveradd.html',locals())

def deploy_cmdb_agent(request):
    pass
def check_ip(ipaddr):
    ipaddr = ipaddr.strip().split('.')
    if len(ipaddr) < 4:
        print ('IP地址输入有误！')
        return False
    for ip in range(len(ipaddr)):
        ipaddr[ip] = int(ipaddr[ip])
        if ipaddr[ip] > 0 and ipaddr[ip] < 255:
            pass
        else:
            print ('IP地址不能超过255！')
            return False
    return True


@login_required
def serverrecycle(request):
    pass
    return render(request,'devops/cmdb/serverrecycle.html')

'''
监控部分
'''
def check_host(ipaddr,port):
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ipaddr,port))
        return True
    except socket.error as e:
        return False
    finally:
        sock.close()

@csrf_exempt
def monitor_display(request):  ## 这个判断主机状态的不写入数据库，实时在页面ajax刷新看到
    ip_list = models.MonitorServer.objects.values_list('ip',flat=True)
    global server_status
    for ip in ip_list:
        if check_host(ip,22):
            server_status = 1
        else:
            server_status = 0
    pageSize = 10
    monitor_server_lst = models.MonitorServer.objects.all().order_by('id')
    pageinator = Paginator(monitor_server_lst, pageSize)   # 开始做分页
    if request.GET.get("page"):
        page = request.GET.get('page')
    else:
        page = 1
    data = pageinator.page(page)
    return render(request,'devops/monitor/display.html',{'data':data,
        'monitor_server_lst':monitor_server_lst,'server_status':server_status})

def monitor_dashboard(request):
    return render(request,'devops/monitor/dashboard.html',locals())

@csrf_exempt
def monitor_writedb(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        raw_keys = ['sn','ip','boot_time','mem_util','cpu_util','average_load','io_read_throughput','io_write_throughput','disk_util','swap_util','average_iops','nic_average_throughput','net_avarage_error']
        a = set(req.keys()) - set(raw_keys) # 得到诸如httpd,cobblerd等服务的信息
        service_dict = {'sn':req.get('sn')}
        for line in list(a):
            if req[line] == 'active':
                d = {line: 1}  # 写成0和1的形式，方便前端进行绿色或红色的展示
            if req[line] == 'down':
                d = {line: 0}
            service_dict.update(d)
        mon_data = {
            'service_data': service_dict,
            'sn': req.get('sn'),
            'ip': req.get('ip'),
            'boot_time': req.get('boot_time'),
            'hostname': req.get('hostname'),
            'cpu_util': req.get('cpu_util'),
            'mem_util': req.get('mem_util'),
            'disk_util': req.get('disk_util'),
            'swap_util': req.get('swap_util'),
            'average_load': req.get('average_load'),
            'average_iops': req.get('average_iops'),
            'io_read_throughput': req.get('io_read_throughput'),
            'io_write_throughput': req.get('io_write_throughput'),
            'nic_average_throughput': req.get('nic_average_throughput'),
            'net_average_error': req.get('net_average_error'),
        }
        sn = mon_data.get('sn',None)
        print 'send:%s' %datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        threshold.CustomThreshold(mon_data)  ## 客户端发过来的数据去执行判断是否超过阈值进行告警
        if sn:
            mon_obj = models.MonitorServer.objects.filter(sn=sn)
            if mon_obj:  ## 如果存在该sn的记录
                for k,v in service_dict.items():
                    service_obj = models.Service.objects.filter(sn=sn,service_name=k)
                    if service_obj:
                        monitor_handler.UpdateInfo(request,mon_obj[0],mon_data)
                    else:  ## 对于在客户端监控脚本新增的服务名称
                        monitor_handler.AddInfo(request,mon_data)

                return HttpResponse('数据已经更新')
            else:
                monitor_handler.AddInfo(request,mon_data)  ## 如果不存在该sn记录，直接去增加该记录
                return HttpResponse('数据已经插入记录OK')
        else:
            return HttpResponse('没有设备序列号，请检查客户端系统')
    else:
        return HttpResponse('客户端脚本错误，必须是POST')

@csrf_exempt
def monitor_addnode(request):
     return render(request,'devops/monitor/addnode.html',locals())

@csrf_exempt
def monitor_alert(request):
    if request.method == 'POST':
        monitor_alert_form = forms.MonitorAlertAdd(request.POST)
        email_alert = request.POST.get('email_alert')
        dingding_alert = request.POST.get('dingding_alert')
        print email_alert,dingding_alert

        if email_alert == 'on':
            sender = request.POST.get('email_sender')
            password = request.POST.get('email_sender_password')
            receiver = request.POST.get('email_receiver')
            smtp_server = request.POST.get('email_smtp_server')
            alert_by_email.Config(sender,password,receiver,smtp_server) ##这是类
        if dingding_alert == 'on':
            dingding_url = request.POST.get('dingding_url')
            alert_by_dingding.config(dingding_url)  ## 这是函数

        return render(request,'devops/monitor/alertset.html',locals())
    else:
        monitor_alert_form = forms.MonitorAlertAdd()
        return render(request,'devops/monitor/alertset.html',locals())


@login_required
@csrf_exempt
def monitor_info(request):
    pageSize = 10
    not_ack_lst = models.MonitorAlert.objects.filter(ack=0).order_by('id')
    pageinator = Paginator(not_ack_lst, pageSize) ## 数据列表，每页记录数，它是对象
    if request.GET.get("page"):
        page = request.GET.get('page')
    else:
        page = 1
    data = pageinator.page(page)
    return render(request,'devops/monitor/alertinfo.html',{'data':data,'not_ack_lst':not_ack_lst})

'''
日志部分
'''
@csrf_exempt
def logview(request):
    if request.method == 'POST':
        logview_form = forms.LogView(request.POST)
        if logview_form.is_valid():
            all_data = logview_form.clean()
            host_id,log_id =  all_data['remote_host_lst'],all_data['log_service']
            remote_host = models.CmdbServer.objects.get(id=host_id).ip
            log_service = models.LogKind.objects.get(id=log_id).logpath
            line_count = all_data['line_count']
            print remote_host,log_service,line_count
            return render(request,'devops/log/logview.html',locals())
        else: ##表单无效
            message = '表单无效，请重新选择'
            return render(request,'devops/log/logview.html',locals())
    if request.method == 'GET':
        log_kind.LogKindPreDefine()
        logview_form = forms.LogView()
        return render(request,'devops/log/logview.html',locals())

@csrf_exempt
def from_redis_get_log(request):
    r = log_server.RedisHelper()
    r.main()
    if request.POST.get('id'):  ##防止id是none的情况
        id = int(request.POST.get('id'))
        string = r._conn.get('%s:%d' %(r.channel,id))
        #print '第%s条:%s' %(id,string)
        if string :  ## 确保redis的get有东西（包括空字符串）才处理
            string = eval(string)  ## 传过来的是字符串'['subscribe', 'monitor', 1L] '
            if string[2] != 1:  ## 不要返回['subscribe', 'monitor', 1L]垃圾内容
                return HttpResponse(string[2])
        else: ## 如果redis没有客户端发日志过来，返回点
            return HttpResponse('.')
    else: ##ajax传递过来的id是None
        return HttpResponse('.')


