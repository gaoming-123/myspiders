# 招标字段解析的方法文件
import re
from bid_tender.data_extract.utils import get_value_by_split_maohao2, get_xmyz_by_text, get_value_by_split_maohao, \
    get_chapter_content, get_value_by_next_td2, get_data_from_table, find_tel, get_value_by_next_td, deal_date_str, \
    get_chapter_content2, get_data_from_table2

__all__ = ['extract_bxry', 'extract_cgr', 'extract_xmbh', 'extract_zbdl', 'extract_jsgm',
           'extract_zjly', 'extract_tel', 'extract_zgys_ff', 'extract_zgys_hq', 'extract_zgys_dj',
           'extract_zgyq', 'extract_kbdd', 'extract_zbtj', 'extract_spjg', 'extract_gk_zbfw', 'extract_zzxs',
           'extract_cgnr', 'extract_ssd', 'extract_zblb', 'extract_tb_jzrq', 'extract_jzrq', 'extract_tbfs',
           'extract_jbqk', 'extract_zbr_tel', 'extract_zbdl_tel']


# 项目业主  招标的项目业主
def extract_bxry(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''

    result1 = get_xmyz_by_text(text)
    # 正则匹配
    try:
        result3 = \
            re.findall(
                r'(.*采购人:|招标单位:|.*招\s*标\s*人：|招标人为|项目业主为|项目.业主|招标人（项目业主）)(.*?)(\s|\d+|招标代理|。|[，,]|；|\s$|地址)',
                text, re.S)[0][1]
        if len(result3) <= 50:
            result3 = re.sub('&nbsp;', '', result3).replace('为', ' ').replace('：', ' ').strip()
            if result3.startswith('）'):
                result3 = result3[1:].strip()
            elif result3.startswith('（'):
                result3 = result3[1:].strip()
    except:
        pass

    text_list = ['招标人', '招标单位','采购人','采购单位']

    result = get_value_by_next_td2(html, text_list)
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
        if result: return result
        return result1


# 采购人  采购项目的业主
def extract_cgr(province, html, text, lines, table_line, table):
    result1 = get_xmyz_by_text(text)
    if len(result1)>30:
        result1=''
    texts=['采购人','采购单位']
    result2 = get_value_by_split_maohao2(lines, texts)
    if result2:
        if ':' not in result2:
            return result2
    else:
        return result1


# 项目编号
def extract_xmbh(province, html, text, lines, table_line, table):
    if province == 'bt':
        try:
            res = get_data_from_table(table, '标段编号')[0]
            return res
        except:
            return ''
    pattern = r'项目.*?编号:?([0-9a-zA-Z_-]+)'
    res = re.findall(pattern, text)
    if res:
        return res[0]
    else:
        return ''


# 招标代理              招标代理
def extract_zbdl(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    try:
        result1 = \
            re.findall(r'(招标代理机构是:?|招?标?代理机?构?单?位?:|招标代理:|招标代理为)(.*?)(（|\(|\s|，|。|地|统一|\s$|地.{0.4}址)', text,
                       re.S)[0][1].strip()
        if len(result1) < 50:
            result1 = re.sub('&nbsp;', '', result1).replace('为', ' ').replace('：', ' ').strip()
        else:
            result1 = ''
    except:
        pass

    texts = ['招标代理单位', '代理单位', '代理机构', '招标代理']
    result3 = get_value_by_next_td2(html, texts)
    result2 = get_value_by_split_maohao2(lines, texts)
    if result2:
        if ':' not in result2:
            return result2
    else:
        if result3:
            return result3
        return result1


# 建设规模   总投资
def extract_jsgm(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    try:
        result1 = re.findall(
            r'(招标范围及内容|规模|拟建规模|内容和规模|招标项目简介:|建设概况:|工程规模:|项目概况:|工程内容及规模:|项目规模:|建设规模.|建设内容及规模|建设内容:)(.*?)(2[.]2|2[.]3|2[.]4|2[.]5|招标范围|建设地点)',
            text, re.S)[0][1]
        result1 = re.sub('&nbsp;', '', result1).strip()
    except:
        pass
    result2 = get_value_by_split_maohao(lines, '规模')
    if result2:
        return result2
    return result1


# 资金来源                                                   资金来源
def extract_zjly(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    try:
        result1 = re.findall('建设资金|建设资金来自|建设资金来源|资金来源为[:]|资金由(.*?)\s|[，,]|。', text)[0].strip()
        if len(result1) <= 50:
            result1 = re.sub('&nbsp;', '', result1).replace('为', ' ').replace(':', ' ').replace('来自', '').strip()
        else:
            result1 = ''
    except:
        pass
    result2 = get_value_by_split_maohao(lines, '资金来源')
    if result2:
        if ':' not in result2:
            return result2
    else:
        return result1


# 联系方式
def extract_tel(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    try:
        result1 = \
            re.findall(r'(联系方式:?|所有与本次招投标活动有关的事宜请按下列通讯联系)(.*?)(暂时没有信息|特别提醒|相关公告|网站声明|$|.platform_new)', text, re.S)[0][
                1]
        result1 = re.sub('&nbsp;', '', result1).strip()
    except:
        pass
    result2 = get_chapter_content(lines, '联系')
    if result2:
        return result2
    else:
        return result1


# 资格预审的方法（公共资源交易网铁路工程）（发布公告的媒介）
def extract_zgys_ff(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    # try:
    #     result1 = re.findall(r'媒介(.*?)(联系方式|所有与本次招投标活动有关的事宜请按下列通讯联系)', text, re.S)[0][0]
    #     result1 = re.sub('&nbsp;', '', result1).strip()
    # except:
    #     pass
    result2 = get_chapter_content(lines, '媒介')
    if result2:
        return result2
    else:
        return result1


# 资格预审文件的获取（公共资源交易网铁路工程）（招标文件的获取）
def extract_zgys_hq(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    # try:
    #     result1 = re.findall(r'(.文件.?获取|获取资格预审文件)(.*?)(.文件的递交|异议|其他要求)', text, re.S)[0][1]
    #     result1 = re.sub('&nbsp;', '', result1).strip()
    # except:
    #     pass
    texts = ['获取', '领取']
    result2 = get_chapter_content2(lines, texts)
    if result2:
        return result2
    else:
        return result1


# 资格预审文件的递交（公共资源交易网铁路工程）（投标文件的递交）
def extract_zgys_dj(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    # try:
    #     result1 = re.findall(r'(.投标文件的递交及相关事宜|.文件的递交)(.*?)(发布公告的媒介|资格审查|联系方式)', text, re.S)[0][1]
    #     result1 = re.sub('&nbsp;', '', result1).strip()
    # except:
    #     pass
    result2 = get_chapter_content(lines, '递交')
    if result2:
        return result2
    else:
        return result1


# 资格要求
def extract_zgyq(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    # try:
    #     result1 = re.findall(r'(.资格?质?.要求|投标人资格[和及]业绩要求)(.*?)(招标文件的获取|资格方法|技术成果经济补偿|资格预审方法|投标保证金)', text, re.S)[0][1]
    #     result1 = re.sub('&nbsp;', '', result1).strip()
    # except:
    #     pass
    texts = ['资格条件', '资格要求']
    result2 = get_chapter_content2(lines, texts)
    if result2:
        return result2
    else:
        return result1


# 开标地点
def extract_kbdd(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    # try:
    #     result1 = \
    #         re.findall(r'(资格审查地点:|开标地点:?|地点为:?|网上递交网址为|送达:|开标方式:)(.*?)(）|\d+\.|。|，|\s)', text, re.S)[0][1]
    #     result1 = re.sub('&nbsp;', '', result1).strip().replace(':', '')
    # except:
    #     pass
    result2 = get_value_by_split_maohao(lines, '开标地点')
    if not result2:
        result2 = get_value_by_next_td(html, '开标地点')
    if result2:
        return result2
    else:
        return result1


# 招标条件（公共资源交易网和建设网）
def extract_zbtj(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    try:
        result1 = re.findall(r'招标条件(.*?)(.招标范围|项目概况、招标范围及发包价|项目概况与招标范围|工程概况|项目概括)', text, re.S)[0][0]
        result1 = re.sub('&nbsp;', '', result1).strip()
    except:
        pass
    result2 = get_chapter_content(lines, '招标条件')
    if not result2:
        result2 = get_value_by_split_maohao(lines, '招标条件')
    if not result2:
        result2 = get_chapter_content(lines, '投标条件')

    if result2:
        if ':' not in result2:
            return result2
    else:
        return result1


# 审批机关
def extract_spjg(province, html, text, lines, table_line, table):
    try:
        spjg = re.findall(r'(机关名称为?|.经?由?|以)(.*?)(行?政?审批|批准建设|备案建设|完成了项目备案|批准|备案|核准)', text, re.S)[0][1].strip()
        if len(spjg) <= 50:
            spjg = re.sub('&nbsp;', '', spjg).replace(':', ' ').strip()
        else:
            spjg = ''
    except:
        spjg = ''
    return spjg


# 项目概况与招标范围    招标范围
def extract_gk_zbfw(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    try:
        result1 = re.findall(r'(项目概括|.与招标范围|项目概况.)(.*?)(资格人要求|.资格要求|.资格及要求|.业绩要求)', text, re.S)[0][1]
        result1 = re.sub('&nbsp;', '', result1).strip()
    except:
        pass
    result2 = get_chapter_content(lines, '项目概况')
    if not result2:
        result2 = get_chapter_content(lines, '招标范围')
    if not result2:
        result2 = get_chapter_content(lines, '项目基本情况')
    if not result2:
        result2 = get_value_by_split_maohao(lines, '概况')
        # result2+=get_value_by_split_maohao(lines, '招标范围')
    if result2:
        return result2
    else:
        return result1


# 招标组织形式
def extract_zzxs(province, html, text, lines, table_line, table):
    try:
        zzxs = re.findall(r'招标组织形式为(.*?)(。|，)', text, re.S)[0][0]
        if len(zzxs) < 50:
            zzxs = re.sub('&nbsp;', '', zzxs).replace('为', ' ').replace(':', ' ').strip()
        else:
            zzxs = None
    except:
        zzxs = ''
    return zzxs


# 招标人电话
def extract_zbr_tel(province, html, text, lines, table_line, table):
    phones = find_tel(text)
    if phones:
        return phones[0]
    else:
        return ''


# 招标代理电话
def extract_zbdl_tel(province, html, text, lines, table_line, table):
    phones = find_tel(text)
    if len(phones) > 1:
        return phones[1]
    else:
        return ''


# 项目基本情况
def extract_jbqk(province, html, text, lines, table_line, table):
    result1, result2, result3 = '', '', ''
    # try:
    #     result1 = re.findall(r'(项目概括|.与招标范围|项目概况.)(.*?)(资格人要求|.资格要求|.资格及要求|.业绩要求)', text, re.S)[0][1]
    #     result1 = re.sub('&nbsp;', '', result1).strip()
    # except:
    #     pass
    result2 = get_chapter_content(lines, '项目概况')
    if not result2:
        result2 = get_chapter_content(lines, '招标范围')
    if not result2:
        result2 = get_value_by_split_maohao(lines, '概况')
        # result2+=get_value_by_split_maohao(lines, '招标范围')
    if result2:
        return result2
    else:
        return result1


# 投标方式
def extract_tbfs(province, html, text, lines, table_line, table):
    res = ''
    return res


# 截止日期
def extract_jzrq(province, html, text, lines, table_line, table):
    res = get_value_by_split_maohao(lines, '截止日期')
    res = deal_date_str(res)
    return res


# 投标截止日期
def extract_tb_jzrq(province, html, text, lines, table_line, table):
    res = get_value_by_split_maohao(lines, '投标截止')
    if not res:
        res = get_value_by_next_td(html, '投标截止')
    res = deal_date_str(res)
    return res


# 招标类别
def extract_zblb(province, html, text, lines, table_line, table):
    res = ''
    if '招标' in text:
        res = '交易'
    if '采购' in text:
        res = '采购'
    return res


# 建设地点
def extract_ssd(province, html, text, lines, table_line, table):
    texts = ['招标项目所在地区', '建设地点']
    res = get_value_by_split_maohao2(lines, texts)
    if not res:
        res = get_value_by_next_td(html, '建设地点')
    return res


# 采购内容
def extract_cgnr(province, html, text, lines, table_line, table):
    if '采购' in text:
        texts = ['采购目录','名称']
        res = get_data_from_table2(table, texts)
        if res:
            res = ','.join(res)
        else:
            res = ''
        return res
