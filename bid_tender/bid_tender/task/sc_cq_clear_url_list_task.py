"""
清理四川和重庆的url_list表
暂定每月清理一次url_list表, 里面保留一个月内的数据
"""
import sys
import platform
import time

import pymysql

if platform.system() == 'Linux':
    cfg_path = "/usr/local/service/bid_tender/bid_tender/config"
    sys.path.append(cfg_path)
    from without import *
else:
    from bid_tender.config.without import *


def __get_db_obj():
    """
    获取数据库连接
    :return: (conn, cursor)
    """
    # 连接task数据库
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset=MYSQL_CHATSET,
        port=MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor  # 以字典形式返回数据
    )
    cursor = conn.cursor()
    return conn, cursor


def __close_db(conn, cursor):
    """
    关闭数据库连接
    :return: None
    """
    if cursor:
        cursor.close()
    if conn:
        cursor.close()


def __clear_data(conn, cursor, clear_data_sql):
    """
    删除数据库里面历史数据, 只保留date时间范围内的数据
    :param conn: 数据库连接对象
    :param cursor: 数据库游标对象
    :param interval: 间隔月数, 默认1个月
    :return: 影响行数
    """
    try:
        cursor.execute(query=clear_data_sql)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        print('some error when save the data into db: %s' % e)


def do_main():
    # sql 语句, 保存一个月内的所有数据
    sc_clear_data_sql = "DELETE FROM tender_crawler.sc_url_list WHERE created <= DATE_SUB(NOW(),INTERVAL 1 MONTH);"
    cq_clear_data_sql = "DELETE FROM cq_tender_crawler.cq_url_list WHERE created <= DATE_SUB(NOW(),INTERVAL 1 MONTH);"

    conn, cursor = __get_db_obj()

    # 清理sc_url_list
    sc_clear_cnt = __clear_data(conn, cursor, sc_clear_data_sql)
    print('%s - tender_crawler.sc_url_list 本次清理数据: [%s] 条' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), sc_clear_cnt))
    time.sleep(2)
    # 清理cq_url_list
    cq_clear_cnt = __clear_data(conn, cursor, cq_clear_data_sql)
    print('%s - cq_tender_crawler.cq_url_list 本次清理数据: [%s] 条' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), cq_clear_cnt))

    __close_db(conn, cursor)


if __name__ == '__main__':
    do_main()

