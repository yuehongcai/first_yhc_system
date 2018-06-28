from django.conf.urls import *
from devops import views

app_name = 'devops'

urlpatterns = [
    url(r'^logout/$',views.logout),
    url(r'^cmdb/report/$',views.report),
    url(r'^cmdb/list',views.serverlist),
    url(r'^cmdb/add',views.serveradd),
    url(r'^cmdb/recycle/$',views.serverrecycle),
    url(r'^monitor/dashboard/$',views.monitor_dashboard),
    url(r'^monitor/display',views.monitor_display),
    url(r'^monitor/writedb/$',views.monitor_writedb),
    url(r'^monitor/addnode/$',views.monitor_addnode),
    url(r'^monitor/alert',views.monitor_alert),
    url(r'^monitor/info',views.monitor_info),
    url(r'^log/view',views.logview),
    url(r'^log/search',views.from_redis_get_log),
]