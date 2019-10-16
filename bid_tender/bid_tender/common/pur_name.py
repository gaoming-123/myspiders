import re
import logging

# 先判断 招标人在网页中 使用招标人一套标准
JY_START = ['招标人:', '招标人名称:', '招标单位:', ]

# 先判断 采购人在网页中 使用采购人一套标准
CG_START = ['采购人:', '采购人名称:', '采购人:单位名称:']

# 结束字符串列表（不包含在所需要的字段内容）
END_WITHOUT_STR = ['（二）采购人地址:', '盖单位章招标代理:', '公章法定代表人:', '采购地址:', '招标代理机构:', '联系人:', '单位名称:', '招标单位联系人:', '招标人通信地址:',
                   '地点:','招标代理', '机关地址:', '本级地址:', '单位地址:', '联系地址:', '采购人地址:', '公章法定代表人:', '招标人地址:',
                   '代理机构:', '地址:', '联系人:', '采购人', '建设资金', '项目编号:', '采购代理','项目类别','建设地点','办公地址']

# 以 为 字 确定的字符列表
WEI_LIST = ['采购人为', '项目业主为', '招标人为', '招标人（项目业主）为']


class PurName(object):
    """
    此类，是用于查找业主的
    """

    def __init__(self, response, pattern):
        # 该pattern 确保节点只能有一个
        self.selector = response.xpath(pattern)
        self.pur_name = ""
        self.url = response.url

    def get_content(self):
        """获取节点的正文内容"""
        content = self.selector.xpath('string(.)').extract_first().replace('：', ':').strip()
        html = re.sub(r'\s+', '', content)
        x = re.compile(r'<[^>]+>', re.S)
        self.content = x.sub('', html)  # 正文内容

    def get_pur_name_by_re(self, text):
        result = ''
        log_txt = ''
        if text in self.content:
            try:
                pattern = text + '(.*?)(，|,|。)'
                result = re.findall(pattern, self.content)[0][1].strip()
                log_txt = f'URL地址 开始:{self.url}结束  开始: {text} 结束---开始: {result} 结束---开始: ,|。结束---开始: ,|。 结束'
            except:
                pass
        return result, log_txt

    def get_pur_name_by_slice(self, starts: list, ends: list):
        """根据前后字符串来提取中间的内容"""
        result = ''
        log_txt = ''
        for start_str in starts:
            start_len = len(start_str)
            text_2 = self.content
            s = 0
            min_index = 0
            while 1:
                start = text_2.find(start_str)
                if start == -1:
                    break
                s = s + start + start_len
                text_2 = self.content[s:]
                word_index = []
                word_dict = {}
                for end in ends:
                    d = text_2.find(end)
                    if d > 0:
                        word_index.append(d)
                        word_dict.setdefault(d, end)
                min_index = min(word_index)
                if min_index > 30:
                    continue
            if min_index:
                result = self.content[s:s + min_index]
                break
            # logging.info(f'URL地址 开始:{self.url}结束  开始: {start_str} 结束---')
        if result:
            log_txt = f'URL地址 开始:{self.url}结束  开始: {start_str} 结束---开始: {result} 结束---开始: {word_dict.get(min_index)} 结束---开始: {text_2[:50]} 结束'
            # print(result)
        return result, log_txt

    def find_pur_name(self, jy_start=JY_START, cg_start=CG_START, end=END_WITHOUT_STR):
        """
        根据前后关键字遍历 查找业主的名称
        :param jy_start: 交易网站 起始字符串列表
        :param jy_end:   交易网站 结束字符串列表
        :param cg_start: 采购网站 起始字符串列表
        :param cg_end:   采购网站 结束字符串列表
        :return:
        """
        self.get_content()
        pur_name = ''
        # 根据带为字的值来取值
        for txt in WEI_LIST:
            if txt in self.content:
                pur_name, log_txt = self.get_pur_name_by_re(txt)
        if pur_name:
            logging.info(log_txt)
            return pur_name
        if ('招标人' in self.content) or ('招标单位' in self.content):
            jy_start.sort(key=lambda x: -len(x))
            pur_name, log_txt = self.get_pur_name_by_slice(jy_start, end)
        elif ('采购人' in self.content) or ('采购单位' in self.content):
            cg_start.sort(key=lambda x: -len(x))
            pur_name, log_txt = self.get_pur_name_by_slice(cg_start, end)

        if pur_name:
            logging.info(log_txt)
            return pur_name
        logging.info(f'URL地址：{self.url}   未找到pur_name')
        return ''

