import gevent
from gevent import monkey

monkey.patch_all()  # 猴子补丁

import json
from redis import Redis
import http
import os
import threading
import time
from contextlib import closing
from http.client import IncompleteRead

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import sys

if sys.platform.lower() == 'linux':
    cfg_path = "/usr/local/service/bid_tender/bid_tender"
    sys.path.append(cfg_path)
    import settings as config
else:
    from bid_tender import test_settings as config


class _ControlDownload(object):
    """
    协程下载 -- 单利模式
    """
    __instrance = None  # 单利
    __lock = threading.RLock()

    def __new__(cls, *args, **kwargs):  # 单利模式
        # 1.判断类属性是否为None
        if cls.__instrance is None:
            # 2.如果对象还没有被创建，就调用父类的方法为第一个对象分配空间
            cls.__instrance = super().__new__(cls)
        # 3.把类属性中保存的引用返回给Python的解释器
        return cls.__instrance

    def __init__(self, server=None, key='attachments'):
        self.__server = server
        if not self.__server:
            self.__server = Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PASSWORD,
                db=config.DB
            )
        self.__key = key
        self.__current_sub_thread = None

    @property
    def current_sub_thread(self):
        return self.__current_sub_thread

    @current_sub_thread.setter
    def current_sub_thread(self, thread_obj):
        if isinstance(thread_obj, threading.Thread):
            self.__current_sub_thread = thread_obj

    @property
    def lock(self):
        return self.__lock

    @property
    def rds_server(self):
        return self.__server

    @property
    def rds_key(self):
        return self.__key

    def do_download(self):
        gevent.joinall([gevent.spawn(self.__download, **each) for each in self._pop()])

    def __download(self, file_url, save_path, chunk_size=2048):
        """
        下载附件
        :param chunk_size: 按块下载的大小, 2的11次方貌似要快点(网上看到的)
        :param file_url: 附件下载连接
        :param save_path: 附件保存路径
        :return:
        """

        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        # 判断附件是否下载过
        if os.path.isfile(save_path) and 0 < os.path.getsize(save_path):
            return

        # 开始下载文件
        try:
            response = requests.get(
                url=file_url,
                headers={
                    'User-Agent': r'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'},
                timeout=8000,
                verify=False,
                stream=True  # 按块读取
            )

            print('%s - %s - %s - [%s] - downloading file ......' % (
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                self.current_sub_thread.name if self.current_sub_thread else threading.currentThread().name,
                gevent.getcurrent().name,
                os.path.split(save_path)[-1]
            ))

            with closing(response) as stm:
                with open(save_path, "wb") as ft:
                    # 按块下载
                    try:
                        for chunk in stm.iter_content(chunk_size=chunk_size):
                            if chunk:
                                ft.write(chunk)  # 按块保存
                        ft.flush()
                    except http.client.IncompleteRead as http_e:
                        print('there throw `http.client.IncompleteRead`: %s' % http_e)
                    except Exception as e:
                        print('there throw exception: %s' % e)
        except Exception as e:
            raise Exception('download_attachment error: %s' % e)

    def _pop(self, start=0, end=9):
        pipe = self.__server.pipeline()
        pipe.multi()
        with self.__lock:
            pipe.zrange(self.__key, start, end).zremrangebyrank(self.__key, start, end)
            results, count = pipe.execute()
        return list(map(lambda ele: json.loads(ele), results)) if results else []


control = _ControlDownload()


def start_download_task():
    """
    阻塞
    :return:
    """
    _current_thread = threading.currentThread()
    if _current_thread.name == 'MainThread':
        print('主线程使用中, 会阻塞主线程.......')

    if control.current_sub_thread \
            and control.current_sub_thread.is_alive() \
            and control.current_sub_thread.name is not 'MainThread':
        print('下载任务线程还存活, 不用再开启新的线程.....', control.current_sub_thread)
        return

    control.current_sub_thread = _current_thread
    note = control.rds_server.zcard(control.rds_key)

    while note > 0:
        control.do_download()
        time.sleep(1)
        note = control.rds_server.zcard(control.rds_key)


def put_to_redis(file_url, save_path, score=0):
    """
    把下载信息加入到redis中, 这里使用有序集合
    :param file_url: 附件下载连接
    :param save_path: 附件保存路径
    :param score: 下载优先级, 数字越大越排在前面
    :return:
    """
    with control.lock:
        print('排队下载, redis数据库key为: [ %s ] ' % control.rds_key)
        control.rds_server.execute_command('ZADD', control.rds_key, -int(score),
                                           json.dumps(dict(file_url=file_url, save_path=save_path)))


thread_download = put_to_redis

if __name__ == '__main__':
#     for i in range(1, 50):
#         thread_download(
#             file_url='https://ztb.cqggzy.com/CQTPBidder/jsgcztbmis2/pages/zbfilelingqu_hy/cQZBFileDownAttachAction.action?cmd=download&AttachGuid=656f8488-bd97-4f39-987a-3f8fb757bfe4&FileCode=J076&ClientGuid=bb24ac2d-5fe4-438c-a430-a61e06a783d5',
#             save_path='./attaches/%saa.gef' % i
#         )
#     g1 = gevent.spawn(func1, 'http://www.baidu.com')
#     g2 = gevent.spawn(func2, 'http://www.baidu.com')
#     gevent.joinall([g1, g2])
#     threading.Thread(target=start_download_task).start()
#     a = 1
#     while a:
#         a += 1
#         time.sleep(0.5)
#         print('**********************', a)
        start_download_task()
