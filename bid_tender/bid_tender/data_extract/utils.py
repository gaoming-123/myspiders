# -*- coding=utf-8 -*-
# gmj
# 公用方法文件
import datetime
import re

# 先判断 招标人在网页中 使用招标人一套标准
import time
from collections import Counter

JY_START = ['招标人:', '招标人名称:', '招标单位:', ]

# 先判断 采购人在网页中 使用采购人一套标准
CG_START = ['采购人:', '采购人名称:', '采购人:单位名称:']

# 结束字符串列表（不包含在所需要的字段内容）
END_WITHOUT_STR = ['二采购人地址:', '盖单位章招标代理:', '公章法定代表人:', '采购地址:', '招标代理机构:', '联系人:', '单位名称:', '招标单位联系人:', '招标人通信地址:',
                   '地点:', '招标代理', '机关地址:', '本级地址:', '单位地址:', '联系地址:', '采购人地址:', '公章法定代表人:', '招标人地址:',
                   '代理机构:', '地址:', '联系人:', '采购人', '建设资金', '项目编号:', '采购代理', '采购项目子包']

# 以 为 字 确定的字符列表
WEI_LIST = ['采购人为', '项目业主为', '招标人为', '招标人（项目业主）为']

# 对列表进行 文本长度倒叙排列
JY_START.sort(key=lambda x: -len(x))
CG_START.sort(key=lambda x: -len(x))


def get_pur_name_by_re(content, text):
    result = ''
    if text in content:
        try:
            pattern = text + '(.*?)，|,|。'
            result = re.findall(pattern, content)[0].strip()
            if len(result)>30:
                return ''
        except:
            pass
    return result


def get_pur_name_by_slice(text, starts: list, ends: list):
    """根据前后字符串来提取中间的内容"""
    result = ''
    for start_str in starts:
        start_len = len(start_str)
        text_2 = text
        s = 0
        min_index = 0
        while 1:
            start = text_2.find(start_str)
            if start == -1:
                break
            s = s + start + start_len
            text_2 = text[s:]
            word_index = []
            word_dict = {}
            for end in ends:
                d = text_2.find(end)
                if d > 0:
                    word_index.append(d)
                    word_dict.setdefault(d, end)
            if word_index:
                min_index = min(word_index)
                if min_index > 30:
                    continue
        if min_index:
            result = text[s:s + min_index]
            break

    return result

# 根据文本获取项目业主
def get_xmyz_by_text(text, jy_start=JY_START, cg_start=CG_START, end=END_WITHOUT_STR):
    text = re.sub(r'\s+', '', text)
    text=text.replace('&nbsp;','')
    pur_name = ''
    # 根据带为字的值来取值
    for txt in WEI_LIST:
        if txt in text:
            pur_name = get_pur_name_by_re(text, txt)
    if pur_name:
        return pur_name
    if ('招标人' in text) or ('招标单位' in text):
        jy_start.sort(key=lambda x: -len(x))
        pur_name = get_pur_name_by_slice(text, jy_start, end)
    elif ('采购人' in text) or ('采购单位' in text):
        cg_start.sort(key=lambda x: -len(x))
        pur_name = get_pur_name_by_slice(text, cg_start, end)
    if pur_name:
        return pur_name
    return ''


# 判断是否为段落
def chapter_judge(text):
    """返回段落编号 或者 False"""
    chinese_num = {
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '十': 10,
    }
    chapter_word = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '.', '、', '1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '0']
    point = False
    chapter = 0
    chapter_chinese = False
    for i in range(5):
        chinese = False
        # print(text)
        s = text.strip()[i:i + 1]
        if s in chapter_word:
            if s in ['.', '、']:
                point = True
                continue
            try:
                num = int(s)
            except:
                num = chinese_num.get(s)
                chinese = True
                if not point:
                    chapter_chinese = True
            if not point:
                if chapter < 10:
                    chapter = chapter * 10 + num
                else:
                    chapter += num
            if point:
                if chinese:
                    break
                if num:
                    # chapter=f'{chapter}.{num}'
                    # 子段落  如 2.2
                    return False, False
        else:
            break
    return chapter, chapter_chinese


# 根据 段落名称包含字符  来获取该段落的文本
def get_chapter_content(lines, txt):
    """以章标题为准"""
    content = []
    # 段落编号是中文 还是数字
    chapter_chinese = False
    content_chapter = 0
    # txt_start=False
    for line in lines:
        chapter, chinese = chapter_judge(line)
        if chapter and chinese and (txt in line):
            chapter_chinese = True
        if content_chapter:
            if chapter and chinese == chapter_chinese:
                break
            if '暂时没有信息' in line:
                continue
            if '附件' in line:
                continue
            content.append(line)
        if (txt in line) and chapter:
            content_chapter = chapter
            # content.append(line)
    return '\n'.join(content)


# 多个文本获取
def get_chapter_content2(lines, txts: list):
    # 通过多个值来获取一段文字内容
    res = ''
    for txt in txts:
        res = get_chapter_content(lines, txt)
        if res:
            break
    return res


# 通过 ：来切分 得到字段的值  example:  通过:切分 ==> 通过 ':' 切分 ==> ['通过','切分']
def get_value_by_split_maohao(lines, txt,result:list=None):
    res = ''
    for line in lines:
        if txt in line:
            try:
                pattern = f'{txt}.*?:'
                s_t = re.findall(pattern, line)[0]
                if len(s_t) > 20:
                    continue
                res = line.strip().split(s_t, 1)[1]
                if len(res) > 30:
                    res = ''
                if res:
                    break
            except:
                pass
    if isinstance(result,list):
        if res:
            result.append(res.strip())
    else:
        return res.strip()


# 通过 ：来切分 得到字段的值  传入值为列表  当取得一个值时就结束并返回
def get_value_by_split_maohao2(content, txts: list,result:list=None):
    res = ''
    for line in content:
        for txt in txts:
            if txt in line:
                try:
                    pattern = f'{txt}.*?:'
                    s_t = re.findall(pattern, line)[0]
                    if len(s_t) > 20:
                        continue
                    res = line.strip().split(s_t, 1)[1]
                    if len(res) > 30:
                        res = ''
                    if res:
                        break
                except:
                    pass
        if res:
            break
    if isinstance(result,list):
        if res:
            result.append(res.strip())
    else:
        return res.strip()


# 通过文本切分 来获 取值  example:  通过文本切分 ==> 通过 '文本' 切分 ==> ['通过','切分']
def get_value_by_split_text(content, txt,result:list=None):
    res = ''
    for line in content:
        if txt in line:
            try:
                res = line.strip().split(txt)[1]
            except:
                pass
    if isinstance(result,list):
        if res:
            result.append(res)
    else:
        return res.strip()


# 通过td下一个td标签来选择文本内容
def get_value_by_next_td(html, txt,result:list=None):
    res = ''
    try:
        res = html.xpath(f'//td[contains(text(),"{txt}")]')[0].xpath("./following-sibling::td")[0].xpath(
            'string()').strip()
    except:
        pass
    if isinstance(result,list):
        if res:
            result.append(res)
    else:
        return res.strip()


# 兵团交易网 td下个td取值方法  td标签下含有div标签
def bt_get_value_by_next_td(html, txt,result:list=None):
    res = ''
    try:
        res = html.xpath(f'//td/div[contains(text(),"{txt}")]/../following-sibling::td[1]/div/text()')
        if len(res) == 1:
            return res[0]
        else:
            res=''
    except:
        pass
    if isinstance(result,list):
        if res:
            result.append(res)
    else:
        return res
# 安徽交易网 td下个td取值方法  td标签下含有div标签
def ah_get_value_by_next_td(html, txt,result:list=None):
    res = ''
    try:
        res = html.xpath(f'//td/p/span[.="{txt}"]/../following-sibling::td[1]/p/span/text()')
        if len(res) == 1:
            return res[0]
        else:
            res=''
    except:
        pass
    if isinstance(result,list):
        if res:
            result.append(res)
    else:
        return res

# 通过td下一个td标签来选择文本内容
def get_value_by_next_td2(html, txts,result:list=None):
    res = ''
    for txt in txts:
        try:
            res = html.xpath(f'//td[contains(text(),"{txt}")]')[0].xpath("./following-sibling::td")[0].xpath(
                'string()').strip()
            if res:
                break
        except:
            pass
    if isinstance(result,list):
        if res:
            result.append(res)
    else:
        return res


# 通过th下一个td标签来选择文本内容
def get_value_by_th_td(html, txt,result:list=None):
    res = ''
    try:
        res = html.xpath(f'//th[contains(text(),"{txt}")]')[0].xpath('./following-sibling::td')[
            0].xpath('string()').extract_first().strip()
    except:
        pass
    if isinstance(result,list):
        if res:
            result.append(res)
    else:
        return res


# 查找电话号码，对其前后排序，一般业主电话在前，代理电话在后
def find_tel(text):
    phones = re.findall('(1[3-9]\d{9}|\d{3,4}-\d{7,14}|电话:\d{8})[^\d]', text)
    phones = list(set(phones))
    phones.sort(key=lambda x: text.find(x))
    return phones


# 从表单，通过列名提取数据  传入单个列名
def get_data_from_table(table_data: dict, column_name):
    """
    :param table_data: 网页的表处理结果
    :param column_name: 表列名中包含的名称
    :return: 如果找到，返回数据列表，未找到，返回空列表
    """
    # print(table_data)
    res = []
    try:
        for k in table_data:
            df = table_data[k]
            # print(df)
            columns_name = df.iloc[0, :]
            for index, name in enumerate(columns_name):
                if column_name in name:
                    new_res = list(df.iloc[1:, index])
                    # 取值最多的列表
                    if len(new_res) > len(res):
                        res = new_res
    except:
        pass
    return res


# 从表单，通过列名提取数据  传入列名列表
def get_data_from_table2(table_data: dict, column_names: list):
    # 多个列名 为同一个值得情况使用
    res = []
    for name in column_names:
        res = get_data_from_table(table_data, name)
        if res:
            break
    return res


# 通过关键字从表 行数据中提取数据
def get_value_by_table_line(table_lines: list, txt: str,result:list=None):
    res = ''
    for line in table_lines:
        if txt in line:
            try:
                pattern = f'{txt}.*?:'
                s_t = re.findall(pattern, line)[0]
                if len(s_t) > 20:
                    continue
                res = line.strip().split(s_t)[1]
            except:
                pass
    if isinstance(result,list):
        if res:
            result.append(res.strip())
    else:
        return res.strip()


# 传入多个值，进行尝试提取数据
def get_value_by_table_line2(table_lines: list, txts: list,result:list=None):
    res = None
    for txt in txts:
        res = get_value_by_table_line(table_lines, txt)
        if res:
            break
    if isinstance(result,list):
        if res:
            result.append(res.strip())
    else:
        return res


# 将日期转换为标准字符串
def deal_date_str(text):
    if not text:
        return None
    if '年' in text:
        da = re.findall('(\d{4})年(\d+)月(\d+)日', text)[0]
        return '-'.join([str(i) for i in da])
    if '-' in text:
        try:
            ss = re.findall('\d{4}-\d{1,2}-\d{1,2}', text)[0]
            return ss
        except:
            return None


# 获取最后的结果
def get_finally_result(result: list):
    """通过统计频率来获取值"""
    res_dict = Counter(result)
    res = res_dict.most_common(1)
    if res:
        return res[0][0]


def get_start_date():
    release_time = datetime.datetime.now() - datetime.timedelta(days=2)
    release_time = release_time.strftime('%Y-%m-%d')
    return release_time