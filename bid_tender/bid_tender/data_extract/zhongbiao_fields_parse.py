# -*- coding=utf-8 -*-
# gmj
# 中标字段解析方法文件

import re
from bid_tender.data_extract.utils import get_value_by_split_maohao, get_value_by_split_maohao2, find_tel, \
    get_data_from_table, get_value_by_next_td, get_value_by_table_line, deal_date_str, get_data_from_table2, \
    bt_get_value_by_next_td, get_finally_result, get_value_by_table_line2, get_value_by_next_td2, get_chapter_content
from bid_tender.data_extract.utils import get_xmyz_by_text


# =======================中标基本信息=======================


def extract_xmmc(province, html, text, lines, table_line, table):
    result = []
    # 项目及标段名称
    texts = ['项目名称', '标段名称']
    r1 = get_value_by_split_maohao2(lines, texts)
    if ':' not in r1: result.append(r1)
    get_value_by_table_line2(table_line, texts,result)
    get_value_by_next_td(html, '项目名称',result)
    get_value_by_next_td(html, '工程名称',result)
    try:
        result1 = \
            re.findall(r'(项目名称:|标段名称:)(.*?)(\s|，|。)', text, re.S)[0][1].strip()
        if len(result1) < 50:
            result1 = re.sub('&nbsp;', '', result1).replace('为', ' ').replace('：', ' ').strip()
            result.append(result1)
    except:
        pass
    res = get_finally_result(result)
    return res


# 类型 ok
def extract_type(province, html, text, lines, table_line, table):
    res = get_value_by_next_td(html, '工程类型')
    if not res:
        res = bt_get_value_by_next_td(html, '项目类别')
    return res


# 项目编号 ok
def extract_xmbh(province, html, text, lines, table_line, table):
    result = []
    if province == 'bt':
        try:
            res = get_data_from_table(table, '标段编号')[0]
            if res:result.append(res)
        except:
            pass
    pattern = r'(标段|项目|招标).*?编号:?([0-9a-zA-Z_-]+)'
    res = re.findall(pattern, text)
    if res: result.append(res[0][1])
    get_value_by_next_td(html, '工程编号',result)
    bt_get_value_by_next_td(html, '项目编号',result)
    get_value_by_split_maohao(lines,'项目编号',result)
    res = get_finally_result(result)
    return res


# 招标人
def extract_zbr(province, html, text, lines, table_line, table):
    result = []
    text_list = ['招标人', '招标单位']
    get_value_by_split_maohao2(lines, text_list,result)
    texts=['建设单位','招标单位']
    r = get_value_by_next_td2(html, texts,result)
    res = get_finally_result(result)
    return res


# 招标人联系电话
def extract_zbrdh(province, html, text, lines, table_line, table):
    phones = find_tel(text)
    if phones:
        return phones[0]
    else:
        return ''


# 招标代理机构
def extract_zbdl(province, html, text, lines, table_line, table):
    result = []
    try:
        result1 = \
            re.findall(r'(招标代理机构是:?|招?标?代理机?构?单?位?:|招标代理:|招标代理为)(.*?)(\s|，|。|地|统一|\s$|地.{0.4}址)', text,
                       re.S)[0][1].strip()
        if len(result1) < 50:
            result1 = re.sub('&nbsp;', '', result1).replace('为', ' ').replace('：', ' ').strip()
            if result1:result.append(result1)
    except:
        pass
    texts = ['招标代理单位', '代理单位', '代理机构', '招标代理']
    result2 = get_value_by_split_maohao2(lines, texts)
    if result2:
        if ':' not in result2:
            result.append(result2)
    texts = ['招标代理单位', '代理单位', '代理机构', '招标代理']
    get_value_by_next_td2(lines, texts,result)
    res = get_finally_result(result)
    return res


# 招标代理机构电话
def extract_zbdldh(province, html, text, lines, table_line, table):
    phones = find_tel(text)
    if len(phones) > 1:
        return phones[1]
    else:
        return ''


# 开标地点
def extract_kbdd(province, html, text, lines, table_line, table):
    result = []
    # try:
    #     result1 = \
    #         re.findall(r'(资格审查地点:|开标地点:?|地点为:?|网上递交网址为|送达:|网址|开标方式:)(.*?)(）|\d+\.|。|，|\s)', text, re.S)[0][1]
    #     result1 = re.sub('&nbsp;', '', result1).strip().replace(':', '')
    #     if result1: result.append(result1)
    # except:
    #     pass
    get_value_by_split_maohao(lines, '开标地点',result)
    get_value_by_next_td(html, '开标地点',result)
    res = get_finally_result(result)
    return res


# 开标时间  date类型
def extract_kbsj(province, html, text, lines, table_line, table):
    res = ''
    result1, result2, result3 = None, None, None
    try:
        result1 = \
            re.findall(r'(开标时间:?|时间为:?)(.*?)(）|\d+\.|。|，|\s)', text, re.S)[0][1]
        result1 = result1.strip().replace(':', '')
    except:
        try:
            result1 = re.findall('于(.*?)进行开标', text)[0]
        except:
            pass
    result2 = get_value_by_next_td(html, '开标时间')
    if not result2:
        result2 = get_value_by_split_maohao(lines, '开标时间')
    if not res:
        if result2:
            res = result2
        else:
            res = result1
    res = deal_date_str(res)
    return res


# 公示期
def extract_gsq(province, html, text, lines, table_line, table):
    result = []
    try:
        r = re.findall('公示期为(.*?)(,|，|。)', text)[0][0]
        if r: result.append(r)
    except:
        pass
    try:
        gsq_start = get_value_by_next_td(html, '公示开始时间')
        gsq_end = get_value_by_next_td(html, '公示截止时间')
        if not gsq_end:
            gsq_end = get_value_by_next_td(html, '公示结束时间')
        if gsq_start:
            gsq = gsq_start + '-' + gsq_end
            result.append(gsq)
    except:
        pass
    texts=['公示时间','公示日期']
    get_value_by_split_maohao2(lines, texts,result)
    texts=['公示时间',]
    get_value_by_next_td(lines, texts,result)
    res = get_finally_result(result)
    return res


# 投标最高限价（元）
def extract_zgxj(province, html, text, lines, table_line, table):
    zgxj = ''
    if province == 'tj':
        try:
            zgxj = re.findall('投标最高限价(.*?元)', text)[0]
        except:
            pass
    return zgxj


# 投标最高限价（元）
def extract_zgxjw(province, html, text, lines, table_line, table):
    zgxj = None
    try:
        zgxj = re.findall('投标最高限价(.*?元)', text)[0]
    except:
        pass
    return zgxj


# 评审委员会成员名单
def extract_pscy(province, html, text, lines, table_line, table):
    res = get_value_by_table_line(table_line, '评标委员会')
    if not res:
        res=get_chapter_content(table_line,'委员会成员名单')
    return res


# 计划工期   int类型
def extract_jhgq(province, html, text, lines, table_line, table):
    result = []
    get_value_by_split_maohao(lines, '工期',result)

    result3 = get_data_from_table(table, '工期')

    if result3: result.append(result3[0])
    res = get_finally_result(result)
    if res:
        try:
            res = int(re.findall('\d+', res)[0])
        except:
            pass
    return res


# 第一投标报价
def extract_first_tbbjw(province, html, text, lines, table_line, table):
    res = None
    return res


# 有效家数
def extract_effective(province, html, text, lines, table_line, table):
    res = None
    return res


# 总投标家数
def extract_tbgs_count(province, html, text, lines, table_line, table):
    res = None
    return res


# ===========================中标公司表============================


def extract_zbmc(province, html, text, lines, table_line, table):
    # 中标名次1第一名2第二名3第三名4投标5双低10废标
    res = None
    return res


# 是否为疑似中标，1是，0不是
def extract_is_yszb(province, html, text, lines, table_line, table):
    # 中标候选人第一个 即是
    res = 0
    return res


# 中标候选人名称
def extract_company(province, html, text, lines, table_line, table):
    text_list = ['中标候选人', '单位名称']
    res = get_data_from_table2(table, text_list)
    if not res:
        try:
            res = re.findall('中标候选人.*?投标人名称:(.*?)(\s|（)', text, re.S)[0][0]
        except:
            pass
    if not res:
        r = get_value_by_split_maohao(lines, '第一中标')
        if r: res.append(r)
        r = get_value_by_split_maohao(lines, '第二中标')
        if r: res.append(r)
        r = get_value_by_split_maohao(lines, '第三中标')
        if r: res.append(r)
    return res


# 投标报价（元）/否决投标依据条款
def extract_tbbj(province, html, text, lines, table_line, table):
    res = get_data_from_table(table, '报价')
    if not res:
        try:
            res = re.findall('中标候选人.*?投标报价:(.*?)(\s|（)', text, re.S)[0][0]
        except:
            pass
    return res


# 投标报价（万元）
def extract_tbbjw(province, html, text, lines, table_line, table):
    if '万元' in text:
        res = get_data_from_table(table, '报价')
        return res
    else:
        return 0


# 经评审的投标价（元）/否决投标理由
def extract_psbj(province, html, text, lines, table_line, table):
    res = ''
    return res


# 经评审的投标价（万元）
def extract_psbjw(province, html, text, lines, table_line, table):
    res = 0
    return res


# 综合评标得分/备注
def extract_zhpf(province, html, text, lines, table_line, table):
    # 得分
    res = get_data_from_table(table, '得分')
    return res


# 最低下浮
def extract_zdxf(province, html, text, lines, table_line, table):
    res = None
    return res


# 最低下浮的计算方式是否准确，准或约
def extract_is_zq(province, html, text, lines, table_line, table):
    res = None
    return res


# 废标原因类型
def extract_fbyy_str(province, html, text, lines, table_line, table):
    res = None
    return res


# 废标原因类型对应的字典值
def extract_fbyy_dict(province, html, text, lines, table_line, table):
    res = None
    return res


# 前台查询字段
def extract_money(province, html, text, lines, table_line, table):
    res = None
    return res


# 1未转换，2已转换
def extract_flag(province, html, text, lines, table_line, table):
    res = 1
    return res


# ========================中标人员表=============================

def extract_gsmc(province, html, text, lines, table_line, table):
    # 关联公司名称
    res = get_data_from_table(table, '中标单位')
    return res


# 姓名
def extract_name(province, html, text, lines, table_line, table):
    res = get_data_from_table(table, '姓名')
    if not res:
        res = get_data_from_table(table, '项目负责人')
    if not res:
        res = bt_get_value_by_next_td(html, '项目经理')
    return res


# 证书名称
def extract_zsmc(province, html, text, lines, table_line, table):
    res = None
    text_list = ['注册资格', '证书']
    res = get_data_from_table2(table, text_list)
    return res


# 证书编号
def extract_zsbh(province, html, text, lines, table_line, table):
    res = get_data_from_table(table, '编号')
    return res


# 职称
def extract_zc(province, html, text, lines, table_line, table):
    res = None
    return res


# 职称专业
def extract_zczy(province, html, text, lines, table_line, table):
    res = get_data_from_table(table, '专业')
    return res


# 级别
def extract_jb(province, html, text, lines, table_line, table):
    res = None
    return res


# 职务
def extract_zw(province, html, text, lines, table_line, table):
    res = None
    return res


# ============================中标业绩===========================


def extract_xmyz(province, html, text, lines, table_line, table):
    # 项目业主
    result1, result2, result3 = '', '', ''

    result1 = get_xmyz_by_text(text)
    # 正则匹配
    try:
        result3 = \
            re.findall(
                r'(.*采购人[：:]|招标单位[:：]|.*招\s*标\s*人：|招标人为|项目业主为|项目.业主|招标人（项目业主）)(.*?)(\s|\d+|招标代理|。|[，,]|；|\s$|地址)',
                text, re.S)[0][1]
        if len(result3) <= 50:
            result3 = re.sub('&nbsp;', '', result3).replace('为', ' ').replace('：', ' ').strip()
            if result3.startswith('）'):
                result3 = result3[1:].strip()
            elif result3.startswith('（'):
                result3 = result3[1:].strip()
    except:
        pass
    text_list = ['招标人', '建设单位', '招标单位','采购单位']
    result2 = get_value_by_split_maohao2(lines, text_list)

    if result2:
        if ':' not in result2:
            return result2
    else:
        if result1 and result3:
            if len(result1) <= len(result3):
                return result1
            else:
                return result3
        if result1: return result1
        if result3: return result3
        return result1


# 暂不采集字段
"""
# 业绩关联类型
def extract_yjgllx(province, html, text, lines, table_line, table):
    res = None
    return res


# 业绩类型
def extract_yjlx(province, html, text, lines, table_line, table):
    res = None
    return res


# 业绩类型大类名称
def extract_yjlx_main_str(province, html, text, lines, table_line, table):
    res = None
    return res


# 业绩类型大类字典值
def extract_yjlx_main_dict(province, html, text, lines, table_line, table):
    res = None
    return res


# 业绩类型子类名称
def extract_yjlx_sub_str(province, html, text, lines, table_line, table):
    res = None
    return res


# 业绩类型子类字典值
def extract_yjlx_sub_dict(province, html, text, lines, table_line, table):
    res = None
    return res
"""


# 开工时间
def extract_kgrq(province, html, text, lines, table_line, table):
    res = None
    try:
        res = re.findall('工期要求:(.*?)开工', text)[0]
    except:
        pass
    return res


# 交工日期
def extract_jiao_rq(province, html, text, lines, table_line, table):
    res = None
    return res


# 竣工日期
def extract_jun_rq(province, html, text, lines, table_line, table):
    res = None
    try:
        res = re.findall('至(.*?)竣工', text)[0]
        if len(res)>20:
            res=None
    except:
        pass
    return res


# 建设规模
def extract_jsgm(province, html, text, lines, table_line, table):
    result=[]
    # try:
    #     result1 = re.findall(
    #         r'(招标范围及内容|规模|拟建规模|内容和规模|招标项目简介:|建设概况:|工程规模:|项目概况:|工程内容及规模:|项目规模:|建设规模.|建设内容及规模|建设内容:)(.*?)(2[.]2|2[.]3|2[.]4|2[.]5|招标范围|建设地点)',
    #         text, re.S)[0][1]
    #     result1 = re.sub('&nbsp;', '', result1).strip()
    # except:
    #     pass
    get_value_by_split_maohao(lines, '规模',result)
    get_value_by_next_td(html,'规模',result)
    res=get_finally_result(result)
    return res


# 合同价格（元）
def extract_htjg(province, html, text, lines, table_line, table):
    res = None
    try:
        res = get_data_from_table(table, '元')
    except:
        pass
    if not res:
        res = get_value_by_split_maohao('中标标价', text)
    return res


# 合同价格（万元）
def extract_htjgw(province, html, text, lines, table_line, table):
    res = 0
    try:
        res = get_data_from_table(table, '万元')
        if not res:
            res = 0
    except:
        pass
    return res


# 合同价格字符
def extract_htjgzf(province, html, text, lines, table_line, table):
    res = None
    return res


# 项目负责人
def extract_xmfzr(province, html, text, lines, table_line, table):
    texts = ['项目经理', '项目负责人']
    res = get_data_from_table2(table, texts)
    return res


# 技术负责人
def extract_jsfzr(province, html, text, lines, table_line, table):
    texts = ['技术负责人']
    res = get_data_from_table2(table, texts)
    return res
