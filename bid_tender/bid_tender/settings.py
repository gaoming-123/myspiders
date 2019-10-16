# -*- coding: utf-8 -*-
from twisted.internet.error import TCPTimedOutError, ConnectionDone

SPIDER_MODULES = ['bid_tender.spiders']
NEWSPIDER_MODULE = 'bid_tender.spiders'

import random
import sys
import os

user_agent_list = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]
UA = random.choice(user_agent_list)
USER_AGENT = UA


# 配置开发开关
DEV_STATUS = True

if DEV_STATUS:
    # redis 配置
    REDIS_URL = 'redis://127.0.0.1:6379'
    REDIS_HOST = '127.0.0.1'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    DB = 12
    # mysql配置  测试数据库
    MYSQL_HOST = '*'
    MYSQL_USER = '*'
    MYSQL_PASSWORD = '*'
    MYSQL_CHATSET = 'utf8'
    MYSQL_PORT = 3306


    # 日志设置
    LOG_LEVEL = 'DEBUG'



    # LOG_FILE = "spider_test.txt"
else:
    # 此处为生产环境的配置
    REDIS_HOST = '*'
    REDIS_PASSWORD = '*'
    REDIS_PORT = 6379
    DB = 16
    # mysql配置  生产数据库
    MYSQL_HOST = '*'
    MYSQL_USER = '*'
    MYSQL_PASSWORD = '**'

    MYSQL_CHATSET = 'utf8'
    MYSQL_PORT = 3306

    # 日志设置
    LOG_LEVEL = 'DEBUG'

    cmd = "/sbin/ifconfig eth0 | grep 'inet ' | awk '{print $2}'"

    p = os.popen(cmd)
    rtn_str = p.read().strip()
    print(rtn_str)
    p.close()
    LOG_FILE = "/usr/local/service/spider_log/mySpider_" + rtn_str + ".log"

REDIS_PARAMS = {
    "password": REDIS_PASSWORD,
    'db': DB
}

# ====================以下为连接数据库配置=================
TJ_MYSQL_DB = "tj_tender_crawler"  # 天津
BJ_MYSQL_DB = "cq_tender_crawler"  # 北京
YN_MYSQL_DB = "yn_tender_crawler"  # 云南
WITHOUT_MYSQL_DB = "without_proxy"  # 初始链接添加库

SD_MYSQL_DB = "sd_tender_crawler"  # 山东
TENDER_MYSQL_DB = "tender_crawler"  # 四川
BT_MYSQL_DB = "bt_tender_crawler"  # 兵团
LN_MYSQL_DB = "ln_tender_crawler"  # 辽宁
# ====================以上为连接数据库配置=================


# 调度器组件设置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
# 配置125的redis
# REDIS_HOST = '118.190.82.125'  # 125外网，本地连

# 去重组件
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
DOWNLOAD_DELAY = 3
# 项目管道设置
ITEM_PIPELINES = {
    'bid_tender.pipelines.CommPipeline': 300,
}
# 日志设置
# LOG_LEVEL = 'DEBUG'
# 正式日志路径
# LOG_FILE = "/usr/local/service/bid_tender/log/mySpider.log"

#
# cmd = "/sbin/ifconfig eth0 | grep 'inet ' | awk '{print $2}'"
#
# p = os.popen(cmd)
# rtn_str = p.read().strip()
# print(rtn_str)
# p.close()
# LOG_FILE = "/usr/local/service/spider_log/mySpider_" + rtn_str + ".log"

# 获取数据时,随机等待0.5-1.5s的时间
RANDOMIZE_DOWNLOAD_DELAY = True
RETRY_ENABLED = True
RETRY_HTTP_CODES = [302, 307, 500, 503, 504, 400, 403, 404, 408, 429, 803]
RETRY_TIMES = 100

# 需要代理去重新请求的情况(目前只有贵州需要用到~2019-07-03加)
RETRY_HTTP_USE_PROXY = {
    # 格式
    # {域名: 重试状态码(元组或列表, 且里面的code需要在 RETRY_HTTP_CODES 中存在)}
    "www.gzjyfw.gov.cn": (500, 503, 504),
    "www.ccgp-guizhou.gov.cn": (500, 503, 504),
    "www.hnsggzy.com": (403, 500), "changsha.hnsggzy.com": (403, 500), "zhuzhou.hnsggzy.com": (403, 500),
    "xiangtan.hnsggzy.com": (403, 500), "hengyang.hnsggzy.com": (403, 500), "zhaoyang.hnsggzy.com": (403, 500),
    "yueyang.hnsggzy.com": (403, 500), "changde.hnsggzy.com": (403, 500),
    "zhangjiajie.hnsggzy.com": (403, 500), "yiyang.hnsggzy.com": (403, 500), "loudi.hnsggzy.com": (403, 500),
    "chengzhou.hnsggzy.com": (403, 500), "yongzhou.hnsggzy.com": (403, 500), "huaihua.hnsggzy.com": (403, 500),
    "xiangxi.hnsggzy.com": (403, 500),
    'www.ccgp-yunnan.gov.cn': (503,), 'www.ggzy.ah.gov.cn': (302, 307),
}
# 请求报异常, 需要重试, 并且需要用到代理的配置
RETRY_EXCEPTION_USE_PROXY = {
    # 格式{域名:(异常类名, )}
    # 可选类名: defer.TimeoutError, TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone,
    #  ConnectError, ConnectionLost, TCPTimedOutError, ResponseFailed IOError, TunnelError (ps: 记得导包)
    "202.61.88.152:9002": (TCPTimedOutError,),
    "202.61.88.152:9004": (TCPTimedOutError,),
    "202.61.88.152:8006": (TCPTimedOutError,),
    "202.61.88.152:8007": (TCPTimedOutError,),
    "www.ccgp-sichuan.gov.cn": (TCPTimedOutError,),
    "www.ccgp-yunnan.gov.cn": (TCPTimedOutError,),
    "zz.fjzfcg.gov.cn": (TCPTimedOutError,),
    "www.sczbbx.com": (TCPTimedOutError,),
    "www.xzggzy.gov.cn:9090": (TCPTimedOutError,),
    'ggzyjy.shandong.gov.cn': (ConnectionDone,),
}

# 下列域名配置不做重试
DONT_RETRY = {
    # 格式{域名:(code, )}
    "www.ccgp-jiangsu.gov.cn": (404,),
    "www.ccgp-beijing.gov.cn": (404,),
    "ggzyjy.gansu.gov.cn:81": (500,),
}

# 设置中间件
DOWNLOADER_MIDDLEWARES = {
    # 'my_test.middlewares.MyTestDownloaderMiddleware': 543,
    # 'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    #  'bid_tender.middlewares.RequestsUserAgentmiddware': 543,
    'bid_tender.middlewares.PhantomJSMiddleware': 543,
    'bid_tender.middlewares.RandomUserAgent': 544,

    'bid_tender.middlewares.JSPageMiddleware': 1,
    'bid_tender.middlewares.BidTenderRetryMiddleware': 550,  # 覆盖系统默认的重试中间件
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'bid_tender.middlewares.MyRetryMiddleware': 80,
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None
}

DOWNLOAD_TIMEOUT = 30
# ROBOTSTXT_OBEY = True

# 本地文件存放根目录
BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))) if sys.platform == 'win32' else "/nfs/bid_tender/"

# 项目文件根目录


# 项目文件根目录

PRO_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 处理规则
rules = [
    # 安徽公共资源交易
    {
        're': 'http://ggzy.ah.gov.cn/dwr/call/plaincall/bulletinInfoDWR.getPackListForDwr1.dwr',
        'func': 'ah_jyw',
        'use_js': False
    },
]
