import pymysql
from bid_tender import settings
from bid_tender.items import AttachItem
import logging


# 连接数据库
def get_cnn_cursor(db, cursorclass=pymysql.cursors.Cursor):
    conn = pymysql.connect(
        host=settings.MYSQL_HOST,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        db=db,
        charset=settings.MYSQL_CHATSET,
        port=settings.MYSQL_PORT,
        cursorclass=cursorclass
    )
    return conn, conn.cursor()


# 保存到数据库
def try_save_to_db(sql_s, conn, cursor):
    """
    为保存函数，执行纯sql语句
    :param sql_s: 纯sql语句  为 单个sql语句  或者  多个sql语句的列表
    :param conn:  mysql连接
    :param cursor:  sql游标
    :return:
    """
    try:
        if isinstance(sql_s, list):
            # 存入多条数据
            for sql in sql_s:
                cursor.execute(sql)
        else:
            cursor.execute(sql_s)
        conn.commit()
        return 1
    except Exception as e:
        conn.rollback()
        logging.info('save data error: %s' % e)


# 保存url到数据库
def save_url(conn, cursor, province, link):
    sql_txt = f'INSERT INTO {province}_tender_crawler.{province}_url_list(link) VALUES ("{link}");'
    url_result = try_save_to_db(sql_txt, conn, cursor)
    if url_result != 1:
        logging.info(f'save to {province}_url_list error: {url_result}')


# 获得插入部分的纯sql语句
def get_part_sql_txt(item, data, ex_fields: list = []):
    """获取存入的sql字符串"""
    field_list = []
    field_value = []
    for fe in item.fields:
        if fe in ex_fields:
            continue
        if fe == 'content':
            # 将内容字段中的 ' 单引号 进行替换，便于后面的插入语句生成   因此，如果后续需要进行数据处理，可能需要先进行反替换处理
            data[fe] = data[fe].replace("'", "\\'")
        field_list.append(fe)
        field_value.append(f"'{data[fe]}'")
    return f"({','.join(field_list)}) values ({','.join(field_value)})"


# 获得更新部分的sql语句
def get_update_sql(item, data: dict, ex_fields: list = []):
    """获得更新的sql字符串"""
    field_k_v = []
    for fe in item.fields:
        if fe in ex_fields:
            continue
        if fe == 'content':
            # 将内容字段中的 ' 单引号 进行替换，便于后面的插入语句生成
            data[fe] = data[fe].replace("'", "\\'")
        k_v = f"{fe}='{data[fe]}'"
        field_k_v.append(k_v)

    return ' ON DUPLICATE KEY UPDATE ' + ','.join(field_k_v)


# 获得全部的sql语句
def get_insert_sql_txt(province, category, data, item, ex_fields):
    """
    :param province: 省份缩写，最好从task/task_config.py中的PROVINCES_DICT中获取
    :param category: 类别 目前分为  交易-->'jy'  采购 -->'cg'
    :param data: 要保存处理数据
    :param item: 与保存数据相关的item类
    :param ex_fields: 不保存到数据库的字段列表
    :return:
    """
    sql_txt = f"INSERT INTO {province}_tender_crawler.{province}_{category}w"
    sql_txt += get_part_sql_txt(item=item, data=data, ex_fields=ex_fields)
    sql_txt += get_update_sql(item=item, data=data, ex_fields=ex_fields)
    return sql_txt


def get_sql_txt_and_value(province, category, data, item, ex_fields, update=True):
    """构造sql语句 并返回 对应的数据字典 """
    sql_txt = f"INSERT INTO {province}_tender_crawler.{province}_{category}w"
    field_list = []
    field_site = []
    field_update = []
    fields_value = {}
    for fe in item.fields:
        if fe in ex_fields:
            continue
        if fe in data.keys():
            field_list.append(fe)
            field_site.append(f'%({fe})s')
            field_update.append(f"{fe}=%({fe})s")
            if isinstance(data[fe], list):
                try:
                    fields_value[fe] = data[fe][0]
                except:
                    fields_value[fe] = ''
            else:
                fields_value[fe] = data[fe]
            # print(fe,data[fe])
    # 插入sql语句
    sql = sql_txt + f"({','.join(field_list)}) values ({','.join(field_site)}) "
    # 更新sql语句
    if update:
        sql += f" on duplicate key update {','.join(field_update)}"
    # print(sql)
    return sql, fields_value


def try_save_to_db2(sql_s, values, conn, cursor):
    # 通过sql语句 和 值 保存数据
    try:
        cursor.execute(sql_s, values)
        conn.commit()
        return 1
    except Exception as e:
        conn.rollback()
        logging.info('save data error: %s' % e)


# 获取 保存附件的sql语句
def make_attach_sql_list(province, data):
    """
    将附件存入附件表的函数，由于字段固定，因此封装此方法
    :param province: 省份缩写，最好从task/task_config.py中的PROVINCES_DICT中获取
    :param data: 要处理的数据
    :return:
    """
    attach_sql_list = []
    notice_id = data.get('notice_id')
    for fj_link, fj_location, fj_name in zip(data['attach_url_list'], data['attach_location_list'],
                                             data['attach_id_list']):
        attach_data = {
            'notice_id': notice_id,
            'fj_link': fj_link,
            'fj_location': fj_location,
            'fj_name': fj_name
        }
        attach_sql = f"INSERT INTO {province}_tender_crawler.{province}_attachment"
        attach_sql += get_part_sql_txt(item=AttachItem, data=attach_data)
        attach_sql += get_update_sql(item=AttachItem, data=attach_data)
        attach_sql_list.append(attach_sql)
    return attach_sql_list
