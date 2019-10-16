# 该省份公用的方法

import datetime
import re
import time

def get_release_time():
    bnow_time = datetime.datetime.now().strftime('%Y-%m-%d')
    bnow_time = bnow_time + ' 10:00:00'
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    release_time = ''
    if time.strptime(str(now_time), '%Y-%m-%d %H:%M:%S') >= time.strptime(str(bnow_time), "%Y-%m-%d %H:%M:%S"):
        release_time = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        release_time = datetime.datetime.now() - datetime.timedelta(days=1)
        release_time = release_time.strftime('%Y-%m-%d')
    return release_time

def get_page_no(response):
    """获取页码"""
    pass
