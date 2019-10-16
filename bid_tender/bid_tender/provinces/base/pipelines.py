# 此处列出可以被访问的方法，必须以省缩写开头，以_pipeline结尾
__all__=['base_jy_detail_pipeline','base_cg_detail_pipeline']

from bid_tender.settings import BASE_MYSQL_DB
from bid_tender.common.sql_utils import get_cnn_cursor, make_attach_sql_list, try_save_to_db, get_insert_sql_txt, save_url
from .task_schedule import province_name


def base_jy_detail_pipeline(data):
    print('---------base_jy_detail_pipeline----------')
    # 传入连接数据库
    conn, cursor = get_cnn_cursor(BT_MYSQL_DB)
    # 保存附件信息
    if int(data['has_attach']):
        attach_sql_list = make_attach_sql_list(province=province_name, data=data)
        try_save_to_db(attach_sql_list, conn, cursor)
    # 保存详情
    # 传入省份缩写，类别，数据，要存储的item，不进行保存的字段，获取sql语句
    sql_txt = get_insert_sql_txt(province=province_name, category='jy', data=data, item=bt_jy_detail_item,
                                 ex_fields=['notice_id', 'attach_url_list', 'attach_location_list', 'attach_id_list',
                                            'pipeline_func'])
    result = try_save_to_db(sql_txt, conn, cursor)
    # 详情存成功了, 如果是完结了的, 就保存连接到url list, 下次就不会再请求这个连接了
    if result == 1:
        save_url(conn, cursor, province=province_name, link=data.get('link'))
    cursor.close()
    conn.close()


def base_cg_detail_pipeline(data):
    print('---------base_cg_detail_pipeline----------')
    pass