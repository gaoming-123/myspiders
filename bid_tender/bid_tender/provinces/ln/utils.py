# 该省份公用的方法

import datetime
import re
import time




def compare_date(date_str, period):
    """公告日期与采集起始日期比较，大于将返回True"""
    # 输入格式为'%Y-%m-%d'
    publish_time = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    before_time = datetime.datetime.strptime(now_time, '%Y-%m-%d') - datetime.timedelta(days=period)
    return publish_time > before_time


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


def get_start_date():
    bnow_time = datetime.datetime.now().strftime('%Y-%m-%d')
    bnow_time = bnow_time + ' 12:00:00'
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if time.strptime(str(now_time), '%Y-%m-%d %H:%M:%S') >= time.strptime(str(bnow_time), "%Y-%m-%d %H:%M:%S"):
        release_time = datetime.datetime.now() - datetime.timedelta(days=2)
        release_time = release_time.strftime('%Y-%m-%d')
    else:
        release_time = datetime.datetime.now() - datetime.timedelta(days=2)
        release_time = release_time.strftime('%Y-%m-%d')
    return release_time

def get_page_no(response):
    now_page_text = response.xpath('//span[@id="MoreInfoListjyxx1_ys"]/text()').extract_first()
    now_page, max_page = tuple(now_page_text.strip().split('/'))
    now_page = int(now_page)
    max_page = int(max_page)
    return now_page, max_page



