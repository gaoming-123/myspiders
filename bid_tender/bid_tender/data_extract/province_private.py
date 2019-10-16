# -*- coding=utf-8 -*-
# Author: gmj
# Date  : 2019/9/29 16:43
# Desc  : 省份独立解析方法集合文件
import re
from bid_tender.data_extract.utils import get_value_by_table_line, get_data_from_table, get_value_by_next_td, \
    deal_date_str, get_data_from_table2, get_value_by_split_maohao2, get_value_by_split_maohao, get_value_by_next_td2, \
    bt_get_value_by_next_td, get_chapter_content, ah_get_value_by_next_td


# 兵团交易网 工程建设 招标公告
def bt_jyw_zbgc(province, html, text, lines, table_line, table):
    res = {}

    return res


# 兵团交易网 工程建设 中标候选人公告
def bt_jyw_zbhxr(province, html, text, lines, table_line, table):
    res = {}
    # res['xmmc'] = bt_get_value_by_next_td(html, '工程名称')
    res['zbr'] = bt_get_value_by_next_td(html, '建设单位')

    # jhgq = bt_get_value_by_next_td(html, '工期')
    # res['jhgq'] = jhgq if jhgq else None
    company = get_data_from_table(table, '中标单位')
    if len(company) == 1:
        company = company[0]
    res['company'] = company
    res['gsmc'] = company
    res['tbbj'] = bt_get_value_by_next_td(html, '小写')
    res['name'] = bt_get_value_by_next_td(html, '建造师姓名')
    res['jb'] = bt_get_value_by_next_td(html, '注册级别')
    res['zsbh'] = bt_get_value_by_next_td(html, '证书编号')

    return res


# 兵团交易网 工程建设 中标结果公告
def bt_jyw_zbjggg(province, html, text, lines, table_line, table):
    res = {}
    res['xmbh'] = bt_get_value_by_next_td(html, '项目编号')
    res['type'] = bt_get_value_by_next_td(html, '项目类别')
    res['zbr'] = bt_get_value_by_next_td(html, '招标人')
    # res['xmmc'] = bt_get_value_by_next_td(html, '项目名称')
    company = get_data_from_table(table, '中标单位')
    if len(company) == 1:
        company = company[0]
    res['company'] = company
    res['gsmc'] = company

    # jhgq = get_data_from_table(table, '工期')
    # res['jhgq'] = jhgq if jhgq else None
    res['name'] = get_data_from_table(table, '项目经理')
    gsq_start = get_value_by_next_td(html, '公示开始时间')
    gsq_end = get_value_by_next_td(html, '公示结束时间')
    res['gsq'] = gsq_start + '-' + gsq_end if gsq_start else None

    return res


# 兵团采购网 采购公告 全部分类
def bt_cgw_cggg(province, html, text, lines, table_line, table):
    res = {}

    cgnr = get_data_from_table(table, '名称')
    if cgnr: res['cgnr'] = ','.join(cgnr)
    res['zgyq'] = get_chapter_content(lines, '资格条件')
    return res


# 山东交易结果解析
def sd_jyw_gcjg(province, html, text, lines, table_line, table):
    res = {}
    # res['xmmc'] = get_value_by_table_line(table_line, '项目名称')
    res['xmbh'] = get_value_by_table_line(table_line, '项目编号')
    res['kbsj'] = get_value_by_table_line(table_line, '开标时间')
    res['zbdl'] = get_value_by_table_line(table_line, '代理机构')
    res['pscy'] = get_value_by_table_line(table_line, '评标委员会')
    res['company'] = get_data_from_table(table, '中标单位')

    return res


# 辽宁交易网 中标候选人公示
def ln_jyw_zbhxr(province, html, text, lines, table_line, table):
    res = {}
    # res['xmmc'] = get_value_by_next_td(html, '工程名称')
    res['type'] = get_value_by_next_td(html, '工程类别')
    res['xmbh'] = get_value_by_next_td(html, '编号')
    res['zbr'] = get_value_by_next_td(html, '建设单位')
    res['gsmc'] = get_data_from_table(table, '单位名称')
    # jhgq = get_data_from_table(table, '工期')
    # if not jhgq:
    #     jhgq = None
    # res['jhgq'] = jhgq
    res['tbbj'] = get_data_from_table(table, '报价')
    res['name'] = get_data_from_table(table, '项目负责人')
    text_list = ['注册资格', '证书']
    res['zsmc'] = get_data_from_table2(table, text_list)
    res['zsbh'] = get_data_from_table(table, '证书编号')
    gsq_start = get_value_by_next_td(html, '公示开始时间')
    gsq_end = get_value_by_next_td(html, '公示截止时间')
    if not gsq_end:
        gsq_end = get_value_by_next_td(html, '公示结束时间')
    res['gsq'] = gsq_start + '-' + gsq_end
    return res


# 辽宁交易网 中标结果公示
def ln_jyw_zbjggs(province, html, text, lines, table_line, table):
    res = {}
    # txts = ['项目名称', '工程名称', '标段名称']
    # res['xmmc'] = get_value_by_next_td2(html, txts)
    res['xmbh'] = get_value_by_next_td(html, '标段编号')
    res['type'] = get_value_by_next_td(html, '工程类别')
    res['zbdl'] = get_value_by_next_td(html, '代理机构')
    res['zbr'] = get_value_by_next_td(html, '建设单位')
    kbsj = get_value_by_next_td(html, '开标日期')
    res['kbsj'] = deal_date_str(kbsj)
    # res['jhgq'] = get_value_by_next_td(html, '有效工期')
    res['gsmc'] = get_value_by_next_td(html, '中标单位')
    res['xmyz'] = get_value_by_next_td(html, '建设单位')
    res['htjg'] = get_value_by_next_td(html, '中标价')
    res['name'] = get_value_by_next_td(html, '项目负责人姓名')
    res['jb'] = get_value_by_next_td(html, '中标负责人级别')
    return res


# 天津市交易网 中标结果公示
def tj_jyw_zbjggs(province, html, text, lines, table_line, table):
    res = {}
    # jhgq = re.findall('工期:(\d+)日历天', text)
    # if not jhgq:
    #     jhgq = get_value_by_split_maohao(lines, '中标工期')
    # if not jhgq:
    #     jhgq = None
    # res['jhgq'] = jhgq
    res['zbr'] = get_value_by_split_maohao(lines, '招标人')
    res['zbdl'] = get_value_by_split_maohao(lines, '招标代理')
    htjg = re.findall('投标报价:(.*?)元', text)
    if not htjg:
        text_list = ['中标标价', '中标价']
        htjg = get_value_by_split_maohao2(lines, text_list)
    res['htjg'] = htjg
    gsmc = re.findall('投标人名称:(.*?)（', text)
    if not gsmc:
        text_list = ['中标单位', '中标人名称']
        gsmc = get_value_by_split_maohao2(lines, text_list)
    res['gsmc'] = gsmc
    name, zsmc, zsbh = '', '', ''
    persons = re.findall('项目经理:(.*?)，(.*?)（(.*?)）', text)
    if persons:
        name = [x[0] for x in persons]
        zsmc = [x[1] for x in persons]
        zsbh = [x[2] for x in persons]
    res['name'] = name
    res['zsmc'] = zsmc
    res['zsbh'] = zsbh
    return res


def ah_jyw_jyjg(province, html, text, lines, table_line, table):
    res={}
    res['xmmc']=ah_get_value_by_next_td(html,'项目名称')
    res['xmbh']=ah_get_value_by_next_td(html,'项目编号')
    res['zbr']=ah_get_value_by_next_td(html,'招标人')
    res['zbdl']=ah_get_value_by_next_td(html,'代理机构')
    res['kbsj']=ah_get_value_by_next_td(html,'开标时间')
    res['company']=ah_get_value_by_next_td(html,'名称')
    return res