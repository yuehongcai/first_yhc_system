#coding: utf-8
"""yhc_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include  #引入了二级路由机制
from django.contrib import admin
from devops import views
from . import settings
from django.views.static import serve

handler404 = "devops.views.page_not_found"
handler500 = "devops.views.page_error"
from django.conf.urls import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login',views.login),
    url(r'^index',views.monitor_dashboard),
    url(r'^$',views.login),
    url(r'^devops/',include('devops.urls')),
    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT,'show_indexes':True}),
]
