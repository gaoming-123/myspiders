# 添加招标任务
import os
import pymysql
import sys
import platform
import time
import datetime

# 连接task数据库

if platform.system() == 'Linux':
    cfg_path = "/usr/local/service/bid_tender/"
    sys.path.append(cfg_path)
else:
    cfg_path = "E:\works\projects\\bid_tender"
    sys.path.append(cfg_path)
from bid_tender.settings import PRO_BASE_PATH
from bid_tender.task.task_config import PROVINCES_DICT
from bid_tender.provinces import *

if platform.system() == 'Linux':
    cfg_path = "/usr/local/service/bid_tender/bid_tender/config"
    sys.path.append(cfg_path)
    from without import *
else:
    from bid_tender.config.without import *
task_conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DB,
    charset=MYSQL_CHATSET,
    port=MYSQL_PORT,
    cursorclass=pymysql.cursors.DictCursor  # 以字典形式返回数据
)
task_cursor = task_conn.cursor()

# 连接tender数据库
if platform.system() == 'Linux':
    cfg_path = "/usr/local/service/bid_tender/bid_tender/config"
    sys.path.append(cfg_path)
    from tender import *
else:
    from bid_tender.config.tender import *

tender_conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DB,
    charset=MYSQL_CHATSET,
    port=MYSQL_PORT
)
tender_cursor = tender_conn.cursor()

# 采集类型，方式1、全部：all，2、单独的某个：cgw，3、逗号拼接的多个：cgw,bxw
if len(sys.argv) > 1:
    sync_type = sys.argv[1]
else:
    sync_type = 'all'

bnow_time = datetime.datetime.now().strftime('%Y-%m-%d')
bnow_time = bnow_time + ' 10:00:00'
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
release_time = ''

if time.strptime(str(now_time), '%Y-%m-%d %H:%M:%S') >= time.strptime(str(bnow_time), "%Y-%m-%d %H:%M:%S"):
    release_time = datetime.datetime.now().strftime('%Y-%m-%d')
else:
    release_time = datetime.datetime.now() - datetime.timedelta(days=1)
    release_time = release_time.strftime('%Y-%m-%d')


# 所有任务对应的优先级
task_level_map = {

    # 安徽
    'ah_cgw': 100,
    'ah_jyw': 100,
}
task_url_map = {}

# 开启任务的省份列表
TASK_PROVINCES = [p[0] for p in PROVINCES_DICT.values()]


# 获取task任务
def push_task(type_list, cate='str'):
    # print(type_list)
    if cate == 'list':
        for row in type_list:
            if row in task_level_map:
                level = task_level_map[row]
            else:
                level = 0
            get_url(row, level)
    else:
        if sync_type in task_level_map:
            level = task_level_map[sync_type]
        else:
            level = 0
        get_url(sync_type, level)


# 查询初始的url
def get_url(task_type, level):
    # 重载 task_url_map
    task_url_map = {
        # 采购网,分省级跟市级
        'hn_cgw': [
            'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&bz=1&pageSize=20&pageNo=1&sj=' + str(
                release_time),
            'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&bz=2&pageSize=20&pageNo=1&sj=' + str(
                release_time),
            'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=1&pageSize=20&pageNo=1&sj=' + str(
                release_time),
            'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=2&pageSize=20&pageNo=1&sj=' + str(
                release_time),
            'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0103&bz=1&pageSize=20&pageNo=1&sj=' + str(
                release_time),
            'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0103&bz=2&pageSize=20&pageNo=1&sj=' + str(
                release_time),
        ],
        # 吉林
        'jl_jyw': [
            'http://was.jl.gov.cn/was5/web/search'
        ],
        'jl_cgw': [
            'http://www.ccgp-jilin.gov.cn/shopHome/morePolicyNews.action'
        ]

    }

    if task_type in task_url_map:
        task_url = task_url_map[task_type]
        if isinstance(task_url, list):
            for url in task_url:
                url_list.append([url, level])
        else:
            url_list.append([task_url, level])
    else:
        if task_type in TASK_PROVINCES:
            # 添加provinces文件下的单省份任务
            everyday_tasks = f'{task_type}.{task_type}_everyday_task'
            everyday_tasks = eval(everyday_tasks)
            url_list.extend(everyday_tasks)
        else:
            print(f"{task_type}省份任务未打开！")


# # 获取任务最大发布时间
# def max_release_time(task_type,level):
#     if isinstance(task_type,list):
#         for i in task_type:
#             if i in tender_rw_sql_map:
#                 for i in tender_rw_sql_map[i]:
#                     tender_cursor.execute(tender_sql_map[i])
#                     release_time_map[i] = tender_cursor.fetchall()[0][0]
#                     if release_time_map[i] == None:
#                         release_time_map[i] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#     else:
#         if task_type in tender_rw_sql_map:
#             for i in tender_rw_sql_map[task_type]:
#                 tender_cursor.execute(tender_sql_map[i])
#                 release_time_map[i] = tender_cursor.fetchall()[0][0]
#                 if release_time_map[i] == None:
#                     release_time_map[i] = time.strftime('%Y-%m-%d', time.localtime(time.time()))

# 处理数据

url_list = []
print('添加任务：', sync_type)
if sync_type == 'all':
    type_list = [
        'hn_cgw', 'jl_jyw', 'jl_cgw', 'sd', 'tj', 'ln', 'bt'
    ]
    # max_release_time(type_list,'list')
    push_task(type_list, 'list')
elif ',' in sync_type:
    type_list = sync_type.split(',')
    # max_release_time(type_list, 'list')
    push_task(type_list, 'list')
else:
    # max_release_time(sync_type, 'str')
    push_task(sync_type, 'str')

# 收集任务的函数

# def collect_provinces_tasks():
#     """获取全部的rules规则"""
#     # cate_list=['everyday_task','FIRST_CRAWL','HAVE_ERROR']
#     all_result = []
#     # province_dir = os.path.join('E:\works\projects\\bid_tender', 'bid_tender', 'provinces')
#     province_dir = os.path.join(PRO_BASE_PATH, 'bid_tender', 'provinces')
#     dir_list = os.listdir(province_dir)
#     for dir_name in dir_list:
#         if dir_name.startswith('_'):
#             dir_list.remove(dir_name)
#
#     for province in dir_list:
#         if os.path.isdir(os.path.join(province_dir, province)):
#             # 通过该值来控制省份的任务是否添加
#             if province not in PROVINCES_DICT.values():
#                continue
#             try:
#                 # 通过task_config文件中的HAVE_ERROR属性值控制是否跳过该省份
#                 error_task = f'{province}_HAVE_ERROR'
#                 if eval(error_task):
#                     continue
#             except:
#                 pass
#             try:
#                 everyday_tasks = f'{province}.{province}_everyday_task'
#                 everyday_tasks=eval(everyday_tasks)
#                 all_result += eval(everyday_tasks)
#             except:
#                 print(f'{province}省份，任务添加失败，请查明原因！')
#     return all_result
#
# provinces_url_list=collect_provinces_tasks()
# url_list.extend(provinces_url_list)

# 插入任务表
if url_list:
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    url_list = list(set(tuple(r) for r in url_list))
    sql = "insert ignore into task_tender(url,pri_level) values(%s,%s)"
    par = url_list
    print(now, '\n', sql, '添加', len(url_list), '条')
    try:
        task_cursor.executemany(sql, par)
        task_conn.commit()
    except Exception as e:
        print(e)

task_cursor.close()
task_conn.close()
tender_cursor.close()
tender_conn.close()
# if __name__ == '__main__':
# push_task('sd')
