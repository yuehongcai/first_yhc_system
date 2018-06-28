=======本系统基于Python 2.7+ Django1.1 + MySQL开发====

1、登陆前需要进行python manage.py makegrations; python manage.py migrate;python manage.py createsuperuser ，用户名和密码如设置所示
2、pip install requests
   pip install ansible
   pip install redis
3、在regular/monitor-clients/monitor_agent.py中定义django服务器的django_server_ip，请自行改为
   自己的域名和IP地址即可
4、这是在pycharm中编写的代码，缩进都是TAB键，注意移植到其他平台，缩进变成4个空格的问题