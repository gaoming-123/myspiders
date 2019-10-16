import re
import logging

# 开始字符串列表
START_STR_LIST = ['招标人:', '采购人:', '招标人名称:', '采购人名称:', '招标单位:', '招标人项目业主为', '招标人为', '项目业主为']
# 结束字符串列表（包含在所需要的字段内容）

END_CONTAINS_CHINESE = [
    '大学', '中学', '小学', '学校', '商学院', '学院',
    '有限公司', '有限责任公司', '公司',
    '水务局', '储备局', '保障局', '执法局', '公安局', '司法局', '规划局', '环境局', '管理局', '资源局', '教育局', '财政局', '审计局', '体育局', '商务局', '建设局',
    '委员会', '联合会', '管委会',
    '医院分院', '医院', '办公室', '某单位', '单位', '服务中心', '研究中心', '中心', '管理中心', '监测中心',
    '支队', '总队', '组织部', '某部',
    '监狱', '电视台', '管理处', '中心仓库', '检验所',
    '人民政府', '办事处', '网站', '支队',
    '养护处', '管理部', '办公厅', '什托洛盖镇', '憩园', '保障部', '水管处', '分院', '考试院', '农场', '党校',
    '设备站', '测试三', '幼儿园', '管理站', '烈士陵园', '煤矿', '武装部', '管理所', '广播电台', '园林管理所', '工作站', '殡仪馆', '研究院', '人民法院',
    '研究所', '卫生局', '民政局', '检察院', '推广站', '保护站', '艺术馆', '卫生院', '养护所', '博物馆', '电视局', '运输局', '团',
    '检测所', '公路处', '水利局', '档案局', '妇幼保健院', '工委', '福利院', '税务局', '工程处', '环境保护局', '时报', '发改委', '消防大队', '服务站', '总站', '园林局',
    '休养所',
    '五中', '管理段', '监理所', '村委会', '信息化厅'
]

# 结束字符串列表（不包含在所需要的字段内容）
END_WITHOUT_STR = ['二采购人地址:', '盖单位章招标代理:', '公章法定代表人:', '采购地址:', '招标代理机构:', '联系人:', '单位名称:', '招标单位联系人:', '招标人通信地址:','地点:'
                   '招标代理', '机关地址:', '本级地址:', '单位地址:', '联系地址:', '采购人地址:', '公章法定代表人:', '招标人地址:',
                   '代理机构:', '地址:', '联系人:', '建设资金', '项目编号:', '采购代理',
                   ]





# 先判断 招标人在网页中 使用招标人一套标准
JY_START = ['招标人:', '招标人名称:', '招标单位:', '招标人（项目业主）为', '招标人为', '项目业主为']

JY_END = END_WITHOUT_STR

# 先判断 采购人在网页中 使用采购人一套标准
CG_START = ['采购人:', '采购人名称:', '采购人为', '项目业主为','采购人:单位名称:']
CG_END = END_WITHOUT_STR


class PurName(object):
    """
    此类，是用于查找业主的,需要更新起始字符 和 结束字符(不包含在业主中的)
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

    def get_chinese(self, pattern="[\u4e00-\u9fa5|\uff1a|\u003a|\n]+"):
        """
        获取正文内容中想要的内容
        :param pattern: 正则表达式  "[\u4e00-\u9fa5|\uff1a|\u003a]+"  为查找中文字符内容以及冒号
        :return:
        """
        m = re.compile(pattern)
        list_ = re.findall(m, self.content)
        self.chinses_text = ''.join(list_)


    def get_pur_name_by_slice(self, starts:list, ends:list):
        """根据前后字符串来提取中间的内容"""
        result = ''
        log_txt = ''
        for start_str in starts:
            start_len = len(start_str)
            text_2 = self.content
            s = 0
            min_index=0
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
                        word_dict.setdefault(d,end)
                min_index=min(word_index)
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

    def find_pur_name(self, jy_start=JY_START, jy_end=JY_END, cg_start=CG_START, cg_end=CG_END, ):
        """
        根据前后关键字遍历 查找业主的名称
        :param jy_start: 交易网站 起始字符串列表
        :param jy_end:   交易网站 结束字符串列表
        :param cg_start: 采购网站 起始字符串列表
        :param cg_end:   采购网站 结束字符串列表
        :return:
        """

        self.get_content()
        self.get_chinese()
        pur_name=''
        if ('招标人' in self.content) or ('招标单位' in self.content):
            jy_start.sort(key=lambda x:-len(x))
            pur_name, log_txt = self.get_pur_name_by_slice(jy_start, jy_end)
        elif ('采购人' in self.content) or ('采购单位' in self.content):
            cg_start.sort(key=lambda x: -len(x))
            pur_name,log_txt=self.get_pur_name_by_slice(cg_start,cg_end)
        if pur_name:
            logging.info(log_txt)
            return pur_name
        logging.info(f'URL地址：{self.url}   未找到pur_name')
        return ''

    def get_pretty_content(self):
        content = self.selector.xpath('string(.)').extract_first().replace('：', ':').strip()
        content = re.sub(r' ', '', content)
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'\xa0', '', content)
        content = re.sub(r'\n[\t]+', '\n', content)
        content = re.sub(r'[\n]+', '\n', content)
        content = re.sub(r'\t', '', content)
        content = re.sub(r':\n', ':', content)
        content = re.sub(r'\n', '', content)
        self.content = re.sub(r'[*]+', '\n', content)
        self.content_list = self.content.split('\n')
        # return content_list

    def get_pur_name_by_content_line(self, starts: list):
        # 一行内容只有一条信息，获取该信息的方法
        for start in starts:
            for line in self.content_list:
                if start in line:
                    pur_name = line.strip().replace(start, '')
                    log_txt = f'URL地址 开始:{self.url}结束  开始: {start} 结束---开始: {pur_name} 结束---开始:  结束---开始: {line} 结束'
                    return pur_name, log_txt

    def find_pur_name3(self, jy_start=JY_START, cg_start=CG_START, ):
        """
        根据行内容来 查找业主的名称
        :param jy_start: 交易网站 起始字符串列表
        :param cg_start: 采购网站 起始字符串列表
        :return:
        """

        self.get_pretty_content()
        pur_name = ''
        if ('招标人' in self.content) or ('招标单位' in self.content):
            jy_start.sort(key=lambda x: -len(x))
            pur_name, log_txt = self.get_pur_name_by_content_line(jy_start)
        elif ('采购人' in self.content) or ('采购单位' in self.content):
            cg_start.sort(key=lambda x: -len(x))
            pur_name, log_txt = self.get_pur_name_by_content_line(cg_start)
        if pur_name:
            logging.info(log_txt)
            return pur_name
        logging.info(f'URL地址：{self.url}   未找到pur_name')
        return ''


