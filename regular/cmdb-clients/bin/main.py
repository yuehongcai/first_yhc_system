#coding: utf-8
import os
import sys

filename = os.path.abspath(sys.argv[0])
current_dir = os.path.dirname(filename)
Parent_DIR = os.path.dirname(current_dir)
sys.path.append(Parent_DIR)  ##设置工作目录，使得包和模块能够正常导入
from core import handler

if __name__ == '__main__':
    handler.ArgvHandler(sys.argv)