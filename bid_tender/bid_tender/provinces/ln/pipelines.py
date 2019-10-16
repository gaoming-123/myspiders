# 此处列出可以被访问的方法，必须以省缩写开头，以_pipeline结尾
__all__=['ln_jy_detail_pipeline','ln_cg_detail_pipeline',]

from bid_tender.settings import LN_MYSQL_DB
from bid_tender.common.sql_utils import get_cnn_cursor, make_attach_sql_list, try_save_to_db, get_insert_sql_txt, \
    save_url, get_sql_txt_and_value, try_save_to_db2
from .task_schedule import province_name
from .items import ln_jy_detail_item,ln_cg_detail_item


def ln_jy_detail_pipeline(data):
    print('---------ln_jy_detail_pipeline----------')
    conn, cursor = get_cnn_cursor(LN_MYSQL_DB)
    # 保存附件信息
    if int(data['has_attach']):
        attach_sql_list = make_attach_sql_list(province=province_name, data=data)
        try_save_to_db(attach_sql_list, conn, cursor)
    # 保存详情
    sql_txt,values = get_sql_txt_and_value(province=province_name, category='jy', data=data, item=ln_jy_detail_item,
                                 ex_fields=['notice_id', 'attach_url_list', 'attach_location_list', 'attach_id_list',
                                            'pipeline_func'])
    result = try_save_to_db2(sql_txt,values, conn, cursor)
    # 详情存成功了, 如果是完结了的, 就保存连接到url list, 下次就不会再请求这个连接了
    if result == 1:
        save_url(conn, cursor, province=province_name, link=data.get('link'))
    cursor.close()
    conn.close()

def ln_cg_detail_pipeline(data):
    print('---------ln_cg_detail_pipeline----------')
    conn, cursor = get_cnn_cursor(LN_MYSQL_DB)
    # 保存附件信息
    if int(data['has_attach']):
        attach_sql_list = make_attach_sql_list(province=province_name, data=data)
        try_save_to_db(attach_sql_list, conn, cursor)
    # 保存详情
    sql_txt,values = get_sql_txt_and_value(province=province_name, category='cg', data=data, item=ln_cg_detail_item,
                                 ex_fields=['notice_id', 'attach_url_list', 'attach_location_list', 'attach_id_list',
                                            'pipeline_func'])
    result = try_save_to_db2(sql_txt,values, conn, cursor)
    # 详情存成功了, 如果是完结了的, 就保存连接到url list, 下次就不会再请求这个连接了
    if result == 1:
        save_url(conn, cursor, province=province_name, link=data.get('link'))
    cursor.close()
    conn.close()


