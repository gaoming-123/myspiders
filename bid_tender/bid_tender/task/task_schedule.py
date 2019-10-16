# 该文件是 框架全部改成省份模式时，使用的任务添加运行文件
import os
from bid_tender.common.sql_utils import get_cnn_cursor
from bid_tender.settings import WITHOUT_MYSQL_DB
from bid_tender.provinces import *
from bid_tender.settings import BASE_PATH
from .task_config import *
import pymysql
import datetime

# 收集任务的函数
def collect_provinces_tasks():
    """获取全部的rules规则"""
    # cate_list=['everyday_task','FIRST_CRAWL','HAVE_ERROR']
    all_result = []
    province_dir = os.path.join(BASE_PATH, 'bid_tender', 'provinces')
    dir_list = os.listdir(province_dir)
    for dir_name in dir_list:
        if dir_name.startswith('_'):
            dir_list.remove(dir_name)

    for province in dir_list:
        if os.path.isdir(os.path.join(province_dir, province)):
            # 通过该值来控制省份的任务是否添加
            if province not in PROVINCES_DICT.values():
                break
            try:
                # 通过task_config文件中的HAVE_ERROR属性值控制是否跳过该省份
                error_task = f'{province}_HAVE_ERROR'
                if eval(error_task):
                    break
            except:
                pass
            try:
                everyday_tasks = f'{province}.{province}_everyday_task'
                everyday_tasks=eval(everyday_tasks)
                all_result += eval(everyday_tasks)
            except:
                print(f'{province}省份，任务添加失败，请查明原因！')
    return all_result

# 任务主程序
def task_main():
    # 每天的任务获取
    all_everyday_tasks = collect_provinces_tasks()

    # 连接task数据库
    task_conn, task_cursor = get_cnn_cursor(WITHOUT_MYSQL_DB, cursorclass=pymysql.cursors.DictCursor)
    # 连接tender数据库
    # tender_conn,tender_cursor=get_cnn_cursor(TENDER_MYSQL_DB)

    #  对 任务url 去重后的列表
    url_list = list(set(all_everyday_tasks))
    sql = "insert ignore into task_tender(url,pri_level) values(%s,%s)"
    par = url_list
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\n', sql, '添加', len(url_list), '条')
    try:
        task_cursor.executemany(sql, par)
        task_conn.commit()
    except Exception as e:
        print(e)

    task_cursor.close()
    task_conn.close()


# tender_cursor.close()
# tender_conn.close()
if __name__ == '__main__':
    task_main()