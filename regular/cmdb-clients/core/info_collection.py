#coding: utf-8
import sys
import platform

def linux_sys_info():
    from plugins.linux import sysinfo
    return sysinfo.collect()

def windows_sys_info():
    from plugins.windows import sysinfo as win_sys_info
    return win_sys_info.collect()

class InfoCollection(object):
    def collect(self):
        try:
            func = getattr(self,platform.system())
            info_data = func()
            formatted_data = self.build_report_data(info_data)
            return formatted_data
        except AttributeError:
            sys.exit('不支持当前操作系统: [%s]' % platform.system)

    def Linux(self): ##这个Linux必须大写，因为getattr上面返回的是Linux，需要调用该函数
        return linux_sys_info()

    def Windows(self):  ##同理
        return windows_sys_info()

    def build_report_data(self,data):
        return data

