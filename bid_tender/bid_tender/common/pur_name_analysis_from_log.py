# 该模块用于处理log日志，将日志处理为每个人的错误归类，并将文本发送给开发人员，进行错误修改或检查
import re
import datetime
import os

import jieba
from collections import Counter

log_file_dir = 'E:\\works\projects\\bid_tender\\bid_tender\\my_test20190903ln_pur.log'
END_CONTAINS_CHINESE = ['有限公司',
                        '幼儿园', '五中', '服务中', '财政局', '训练仪', '工会', '人民检察院', '农业股', '农村厅', '分校', '建设局', '总会', '保障局', '发改委', '赵守前',
                        '广播电视局', '小学', '管理局', '事务局', '图书馆', '中波站', '教育局', '司法厅', '戒毒所', '总工会', '中心', '办公厅',
                        '本级', '管理段', '研究院', '自然资源局', '支队', '农村局', '草原局', '福利院', '监狱', '环保局', '水文局', '卫生院', '市委党校',
                        '学校', '建设厅', '分院', '看守所', '大学', '发展局', '粮食局', '交通运输局', '执法局', '学院', '中学', '改革局', '单位', '卫生局',
                        '商务局', '联合社', '高中', '人民政府', '生态环境厅', '交通局', '青年宫', '气象局', '医院', '招商局', '抚顺战犯管理所', '机关', '总站',
                        '办公', '管修处', '联合会', '园林处', '高喜文', '乡政府', '王志强', '大队', '健康局', '福建', '公安局', '项目', '妇幼保健院', '生态环境局',
                        '委员会', '环境保护局', '司法局', '组织部', '殡仪馆', '监察局', '水利局', '消防局', '办事处', '垃圾处理场', '中心站', '管理区', '管理处',
                        '博物馆', '研究所', '乐团', '保障部', '集团', '电视台', '民政局', '人民法庭', '人民法院', '公司', '旅游局',
                        '档案馆', '宣传部', '村委会', '监理所', '雷锋纪念馆', '办公室', '分局', '监督所', '信息化厅', '中心校', '广播局'
                        # '政治部', '民族文化宫', '分局', '教育局', '总工会', '公司', '委员会', '管理处', '学院', '税务局', '中学', '体育局', '消防局', '通信局', '老干部局', '学校', '天津海关', '人民政府', '中心', '成套局', '二所', '开发局', '档案馆', '办公室', '交通局', '总公司', '办事处', '检查局', '医院', '展览馆', '分公司', '服务站', '环境保护局', '寝园', '项目', '管理所', '作家协会', '小学', '旅游局', '管理局', '图书馆', '公用事业局', '公路处', '供应站', '戒毒所', '大学', '人民法院', '三所', '水务局', '支行', '气象局', '年鉴社', '一所', '发展局', '防治院'
                        # '大学', '中学', '小学', '学校', '商学院', '学院',
                        # '有限公司', '有限责任公司', '公司', '分局',
                        # '水务局', '储备局', '保障局', '执法局', '公安局', '司法局', '规划局', '环境局', '管理局', '资源局', '教育局', '财政局', '审计局', '体育局', '商务局', '建设局',
                        # '事务局', '农村局', '交通局',
                        # '委员会', '联合会', '管委会', '交通厅', '监察局',
                        # '医院分院', '医院', '领导小组办公室', '办公室', '某单位', '单位', '服务中心', '研究中心', '管理中心', '监测中心', '中心血站', '中心',
                        # '支队', '总队', '组织部', '某部', '领导小组',
                        # '监狱', '电视台', '管理处', '中心仓库', '检验所', '农科院',
                        # '政府', '办事处', '网站', '支队', '福利院'
                        # '养护处', '管理部', '办公厅', '什托洛盖镇', '憩园', '保障部', '水管处', '分院', '考试院', '农场', '党校',
                        # '设备站', '测试三', '幼儿园', '管理站', '烈士陵园', '煤矿', '武装部', '管理所', '广播电台', '管理所', '工作站', '殡仪馆', '研究院', '人民法院',
                        # '研究所', '卫生局', '民政局', '检察院', '推广站', '保护站', '艺术馆', '卫生院', '养护所', '博物馆', '电视局', '运输局', '团',
                        # '五中', '管理段', '监理所', '村委会', '信息化厅'
                        ]

END_OUT_CHINESE = ['二采购人地址:', '盖单位章招标代理:', '招标人地址:', '公章法定代表人:', '采购人地址:', '办公地址:','采购地址:', '招标代理机构:',
                   '联系人:', '地址:', '单位名称:','招标单位联系人:','招标人通信地址:','联系方式:',
                   '地点:','采购代理机构:','采购项目内容:','联系地址:','项目联系人:','招标代理人:','项目名称:','名称:'
                   # '公章法定代表人:', '联系人:', '公章招标代理机构:', '招标单位联系人:', '盖单位章招标代理:', '招标代理机构:', '招标人地址:', '地址:','联系电话:','建设资金','代理机构:',
                   #                '招标项目编号为:','项目编号:','招标项目编号为:'
                   # '招标代理', '机关地址:', '单位地址:', '联系地址:', '公章法定代表人:', '招标人地址:', '地址:', '地点:', '项目联系人:', '联系人:', '采购人', '建设资金', '项目编号:',
                   # '采购代理',
                   ]

start=['采购人:单位名称:']

class PurNameAnalysis(object):
    """对业主字段进行分析的类，初始化完成，调用analysis方法，需要将数据导出，调用保存类的方法即可"""

    def __init__(self, log_file_dir, already_end_words, end_out_words):
        """
        :param log_file_dir:   日志文件路径
        :param already_end_words:  业主字段包含的结束字符串
        :param end_out_words:  业主字段不包含的结束字符串
        """
        self.log_file_dir = log_file_dir
        self.already_end_words = already_end_words
        self.end_out_words = end_out_words
        # self.my_content = []
        # 保存日志中找到业主的url及其提取信息
        self.pur_name_content = []
        # 未找到业主的url
        self.not_find_pur = []
        # 保存未成功匹配的业主网页
        self.pur_name_error = []
        # 根据现有的结束词来判断出确定的结束字符串
        self.new_sure_end_words = set(end_out_words)
        self.sure_end_contain = set(already_end_words)
        self.sure_end_contain_dict = {}
        self.final_end_contain=dict()
        self.final_end_words=dict()
        self.final_error=[]


    def read(self):
        """读取日志文件，将匹配到业主，和未匹配到业主的url分开"""
        with open(self.log_file_dir, 'r', encoding='utf-8') as f:
            # 按行读取
            logs = f.readlines()
            for log in logs:
                if 'URL地址' in log:
                    # self.my_content.append(log)
                    find_list = re.findall('开始:(.*?)结束', log)
                    if find_list:
                        self.pur_name_content.append(f"{','.join(find_list)},\n")
                    else:
                        find_list = re.findall('URL地址：(.*?)未找', log)
                        self.not_find_pur.append(f'{find_list[0].strip()},\n')

    def get_ends_words(self, pur_name):
        """
        找出业主字段结尾字符串，
        如果结尾在已知的列表中，将返回(0，结尾字符串),
        如果结尾不在已知的列表中，将返回(1,结尾字符串)
        :param pur_name: 业主字符串
        :return:
        """
        # 特殊字符，在切分的业主字符串尾部出现的特殊字符，例如：锦州医科大学附属第三医院二   中的 ‘二’
        # special_words = [':', '二']
        end_pur = self.get_end_word(pur_name)
        # print(end_pur)
        for word in self.already_end_words:
            if end_pur.endswith(word):
                # end_pur = word
                return 0, end_pur
        # 不是已知的结尾 将打印
        # print('=end_pur=', end_pur)
        return 1, end_pur

    def deal_pur_name(self):
        """处理业主字段"""
        error_num = 0
        total = 0
        contain_end_words = []
        out_end_words = []
        for content in self.pur_name_content:
            total += 1
            # print('one====start')
            # res 是pur_name  业主字符串
            pur_name = content.split(',')[2].strip()
            print('取出的pur_name:', pur_name)
            # 结尾字符串
            end_str = content.split(',')[3].strip()
            print('生产中的切分词：', end_str)
            # 根据已有的结尾字符串得到的有效结果，跳过
            # if end_str not in self.end_out_words:
            # pur_name = pur_name + end_str
            try:
                # 获取状态，结尾字符串
                status, end_word = self.get_ends_words(pur_name)
            except:
                continue
            # 结尾字符串不在已知的列表中，将对50字符串重新切分，
            if status:
                # print(pur_name)
                # 对业主重新切分，得到新的业主
                success, word = self.endswith_contains_word(pur_name)
                if success:
                    end_word = word
                else:
                    # 没有重新切分成功，将原结束字符串添加到新的列表中
                    contain_end_words.append(end_word)
            try:
                # res_text 是招标人后的50字符串
                # 取out_word字符串
                res_text1 = content.split(',')[4]
                print('******原生：', res_text1)
                res_text = res_text1.split(end_word)[1]
                out_end_word, cut_list = self.get_out_word(res_text)
                if out_end_word == end_str:
                    contain_end_words.append(end_word)
                else:
                    error_num += 1

                    print(cut_list)
                    print('切分词:', end_word)
                    print('添加的：', out_end_word)
                all_words = end_word + out_end_word
                # print(all_words)
                # print(all_words in res_text)
                if all_words in res_text:
                    print('结束词与切分词连续！ok！')
                out_end_words.append(out_end_word)
                # print('new_end_str:', out_end_word)
                # print(res_text)
                # print(out_end_word)
                self.pur_name_error.append(content)
            except:
                print(f"{content}数据切分有问题,请检查！")
                self.pur_name_error.append(content)
        print('有问题的个数：', error_num)
        print('总数个数：', total)

        contain_end_words, out_end_words = list(set(contain_end_words)), list(set(out_end_words))
        self.new_contain_end_words = list(set(contain_end_words) - set(self.already_end_words))
        self.new_out_end_words = list(set(out_end_words) - set(self.end_out_words))

    def analysis(self):
        """主函数方法"""
        self.read()
        self.deal_pur_name()

        return self.new_contain_end_words, self.new_out_end_words

    def get_out_word(self, text):
        """对字符串进行切分，获得 外结束字符串"""
        cut_ = jieba.cut(text, cut_all=False)
        cut_list = list(cut_)
        # print(cut_list)
        if len(cut_list[0]) == 1:
            out_end_word = cut_list[1] + cut_list[2]
        else:
            out_end_word = cut_list[0] + cut_list[1]

        if out_end_word + ':' in text:
            out_end_word = out_end_word + ':'
        # print('查找出的：', out_end_word)
        return out_end_word, cut_list

    def endswith_contains_word(self, pur_name):
        """判断是否以 已存在的结束字符串结尾  """
        for a_word in END_CONTAINS_CHINESE:
            if a_word in pur_name:
                end_word = a_word
                return 1, end_word
        return None, None

    def parse_by_jieba(self, text):
        """
        找出业主字段结尾字符串，
        :param pur_name: 业主字符串
        :return:
        """
        # 获取结束字符串
        out_end = self.get_end_word(text)
        # out_end=out_end+':'
        # 获取pur_name结束词
        pur_name = text.replace(out_end, '')
        end_pur = self.get_end_word(pur_name)
        return pur_name, end_pur, out_end

    def get_end_by_jieba_contains_word(self, text):
        cut_ = jieba.cut(text.strip(), cut_all=False)
        cut_list = list(cut_)
        cut_len = len(cut_list)

        # print(cut_list)
        # jieba切分列表的 结束词
        num = 0
        while 1:
            num += -1
            if num + cut_len < 0:
                break
            end_ = cut_list[num]
            if not end_:
                continue
            end_word = ''.join(cut_list[num:])
            if len(end_word) > 10:
                continue
            # print(end_word)
            for word in self.already_end_words:
                long_word = word + end_word
                # print(long_word)
                if long_word in text:
                    if long_word + ':' in text:
                        end_word += ':'
                    self.new_sure_end_words.add(end_word)
                    # self.ok+=1
                    # print(text)
                    # print(word,end_word)
                    return end_word

    def get_contains_word_by_end_word(self, text):
        """通过确定的结束字符串 来查找结束词"""
        sure_end_words = list(self.new_sure_end_words)
        sure_end_words.sort(key=lambda x: -len(x))
        # print(sure_end_words)
        # print(text)
        word_index = []
        word_dict = {}
        for word in sure_end_words:
            index = text.find(word)
            if index > 0:
                word_index.append(index)
                word_dict.setdefault(index, word)
        try:
            min_index = min(word_index)

            contain_word = word_dict[min_index]
            pur_name = text.split(contain_word)[0]
        except:
            pur_name = ''
        if not pur_name:
            return ''
        # print('***',text)
        # print('****',contain_word)
        # print('*****',pur_name)
        # print(pur_name)
        # print(pur_name)
        end_contains = self.get_end_word(pur_name)
        self.sure_end_contain.add(end_contains.strip())
        self.sure_end_contain_dict.setdefault(end_contains, text)
        # self.ok+=1
        # print(text)
        # print(end_contains,contain_word)
        return end_contains

    def get_end_word(self, text):
        """通过分词来获得结束词 """
        cut_ = jieba.cut(text.strip(), cut_all=False)
        cut_list = list(cut_)
        # jieba切分列表的 结束词
        while 1:
            end_ = cut_list[-1]
            del cut_list[-1]
            if not end_:
                continue
            if len(end_) > 1:
                pass
            else:
                end_ = cut_list[- 1] + end_
            return end_

    def dev_deal_pur_name(self):
        """处理业主字段"""

        error_num = 0
        total = 0
        contain_end_words = []
        out_end_words = []
        for content in self.pur_name_content:

            res_text1 = content.split(',')[4].strip()
            print('******原生：', res_text1)
            if ':' not in res_text1:
                # 当文本中没有: 时，需要原切割字符串。
                print('需要人工识别', content)
                continue
            if res_text1.startswith(':'):
                res_text = res_text1.split(':')[1]
            else:
                res_text = res_text1.split(':')[0]
            # for word in ['公章']:
            #     res_text=res_text.replace(word,'')
            print(res_text)
            jie_pur, jie_end, jie_end_out = self.parse_by_jieba(res_text)
            print(jie_pur, '**', jie_end, '**', jie_end_out)
            sure_pur, sure_end, sure_end_out = self.get_out_word_by_split(res_text)
            print(sure_pur, '**', sure_end, '**', sure_end_out)
            contain_end_words.append(jie_end)
            if jie_end_out + ':' in res_text1:
                jie_end_out = jie_end_out + ':'
            out_end_words.append(jie_end_out)

            if sure_pur:
                contain_end_words.append(sure_end)
                if sure_end_out + ':' in res_text1:
                    sure_end_out = sure_end_out + ':'
                out_end_words.append(sure_end_out)
            # if jie_end_out==sure_end_out:
            #     print('')
            total += 1

        # print('有问题的个数：', error_num)
        print('总数个数：', total)
        r1 = Counter(contain_end_words)
        print(r1)
        r2 = Counter(out_end_words)
        print(r2)
        contain_end_words, out_end_words = list(set(contain_end_words)), list(set(out_end_words))
        self.new_contain_end_words = list(set(contain_end_words) - set(self.already_end_words))
        self.new_out_end_words = list(set(out_end_words) - set(self.end_out_words))

    def dev_deal_pur_name_cycle(self):
        """处理业主字段"""
        len1 = 0
        len2 = 0
        total_set = set()
        t = 0
        result = {}
        while 1:
            t += 1
            print(t)
            len1 = len(self.sure_end_contain)
            len2 = len(self.new_sure_end_words)
            for content in self.pur_name_content:
                url = content.split(',')[0].strip()
                total_set.add(url)
                res_text1 = content.split(',')[4].strip()
                if res_text1.startswith(':'):
                    res_text = res_text1.split(':')[1]
                else:
                    res_text = res_text1.split(':')[0]
                if res_text + ':' in res_text1:
                    res_text += ':'
                # print(content)
                # print('**',res_text)
                end_contains = self.get_contains_word_by_end_word(res_text)
                if end_contains:
                    # print(end_contains)
                    result.setdefault(url, 1)
                end_word = self.get_end_by_jieba_contains_word(res_text)
                # print(end_word)
                # print(res_text)
            if len1 == len(self.sure_end_contain) and len2 == len(self.new_sure_end_words):
                break
        sure_end_contain_list = list(self.sure_end_contain)
        sure_end_contain_list.sort(key=lambda x: len(x))
        sure_end_words_list = list(self.new_sure_end_words)
        sure_end_words_list.sort(key=lambda x: len(x))
        # print(sure_end_words_list)
        total_url_num = len(total_set)
        ok_num = len(result.keys())
        print(f"共有{ len(self.pur_name_content)}条数据！共{total_url_num}条url")
        print(f'合格{ok_num}条，不合格{total_url_num-ok_num}')
        # 打印处理不合格的数据，进行人工分析
        # print('====不合格数据如下：')
        # for content in self.pur_name_content:
        #     url = content.split(',')[0].strip()
        #     res_text1 = content.split(',')[4].strip()
        #     if res_text1.startswith(':'):
        #         res_text = res_text1.split(':')[1]
        #     else:
        #         res_text = res_text1.split(':')[0]
        #     if res_text + ':' in res_text1:
        #         res_text += ':'
        #     if url not in result.keys():
        #         print(content)
        # print('================')
        # 打印 新结束词 对应的 pur_name内容段
        # for k, v in self.sure_end_contain_dict.items():
        #     print(v)
        #     print(k)

        # print(self.sure_end_contain)
        # 处理相似的结束词，将其删除
        self.rm_similar(self.sure_end_contain)
        self.rm_similar(self.new_sure_end_words)


        # print(len(self.sure_end_contain))
        # print(self.new_sure_end_words)
        # 新添加的结尾词
        new_contain_end_words = list(self.sure_end_contain - set(self.already_end_words))
        # 新结束字符串
        new_out_end_words = list(self.new_sure_end_words - set(self.end_out_words))

        print('新增结尾词:',new_contain_end_words)
        print('新增结束字符串:',new_out_end_words)

    def rm_similar(self,l):
        """去除相似的词"""
        for s_word in list(l):
            if len(s_word) > 3:
                # print(s_word)
                cut_ = jieba.cut(s_word.strip(), cut_all=True)
                cut_list = list(cut_)
                end_ = cut_list[-1]
                if len(end_) == 2:
                    if end_ in l:
                        l.remove(s_word)
                else:
                    end_ = s_word[-3:]
                    if end_ in l:
                        l.remove(s_word)

    def dev_analysis(self):
        """主函数方法"""
        self.read()
        self.dev_deal_pur_name()

        return self.new_contain_end_words, self.new_out_end_words

    def dev_cycle_analysis(self):
        self.read()
        self.dev_deal_pur_name_cycle()
        self.last_check()

    def get_out_word_by_split(self, text):
        """对字符串进行切分，获得 外结束字符串"""
        word_index = []
        word_dict = {}
        for word in self.already_end_words:
            index = text.find(word)
            if index > 0:
                word_index.append(index)
                word_dict.setdefault(index, word)
        try:
            max_index = max(word_index)
            contain_word = word_dict[max_index]
            out_end_word = text.split(contain_word)[1]
            pur_name = text.replace(out_end_word, '')
            out_end = self.get_end_word(pur_name)
        except:
            pur_name, out_end, out_end_word = None, None, None
        return pur_name, out_end, out_end_word

    def _to_csv(self, file, header: list, content: list):
        """保存到csv"""
        with open(file, 'a+', encoding='utf-8') as er:
            er.write(f'{",".join(header)},\n')
            er.writelines(content)

    def _today(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.today = today.replace('-', '')

    def not_find_pur_to_csv(self):
        """导出未找到业主的url地址"""
        self._to_csv(file=f'{self.today}_not_find_pur_analysis.csv',
                     header=['未找到业主的url地址'], content=self.not_find_pur)

    def error_pur_to_csv(self):
        """导出未成功匹配的url"""
        self._to_csv(file=f'{self.today}_error_pur_analysis.csv',
                     header=['url地址,起始字符串', 'pur_name', 'end_str', '50字符'],
                     content=self.pur_name_error)

    def last_check(self):
        error_num=0
        for content in self.pur_name_content:
            res_text = content.split(',')[4].strip()
            word_index = []
            word_dict = {}
            for end_out_ in self.new_sure_end_words:
                for in_word in self.sure_end_contain:
                    index=res_text.find(in_word+end_out_)
                    i_index=res_text.find(':')
                    if i_index < index:
                        continue
                    if index >0:
                        word_index.append(index)
                        word_dict.setdefault(index,(in_word,end_out_))
            try:
                min_index=min(word_index)
            except:
                min_index=0
            if min_index:

                # print(res_text)
                # print(word_dict[min_index])
                # if self.final_end_contain.has_key(word_dict[min_index][0]):

                self.final_end_contain.setdefault(word_dict[min_index][0],content)
                self.final_end_words.setdefault(word_dict[min_index][1],content)
                pass
            else:
                error_num+=1
                # print(content)
                self.final_error.append(content)
        print(f'==============共有{error_num}处错误===============')
        print('最终结尾词新增值:',list(set(self.final_end_contain.keys())-set(self.already_end_words)))
        print('最终结束字符新增值:', list(set(self.final_end_words.keys()) - set(self.end_out_words)))
        for k,v in self.final_end_contain.items():
            print(k)
            print(v)
        for k,v in self.final_end_words.items():
            print(k)
            print(v)
        print('问题如下:')
        for i in self.final_error:
            print(i)

p = PurNameAnalysis(log_file_dir=log_file_dir, already_end_words=END_CONTAINS_CHINESE, end_out_words=END_OUT_CHINESE)
# l1, l2 = p.dev_analysis()
# print(len(l1))
# print(l1)
# print(len(l2))
# print(l2)
p.dev_cycle_analysis()
# 读取日志

# 业主字段 切分字段 原始字段

# 判断业主的结束词 在已经有的结束词列表中

# 没有 将进行分词 取得结束词 添加 新增结束词列表中

# 根据新增的结束词 对原始字符串进行切分，取得新增out结束字符串

# 对原始字符进行切分':'
# 取第一个，对其进行结束词查找
# 以最后一个结束词进行切分，取[1] 得到新增out结束字符串

# 或者以分词来查找新增out结束字符串


ln_end_contains=['国土资源局', '地址', '党校', '处理厂', '规划局', '指挥部', '监测站', '宗教事务', '文学院', '人民武装部',
                 '传输台', '一中', '内容', '日报社', '财政金融局', '南关校', '信息化局', '社会保障厅', '先生', '科学技术局',
                 '服务', '分局中', '建局', '信访局', '兽医局', '林业局', '管委会', '渔业局', '协会', '体育局', '工作室',
                 '审批局', '交通运输厅', '管理所', '档案局', '水务局', '税务局', '转播站', '交警队', '园林局', '公用事业局',
                 '部队', '种畜场', '实验学校物', '执法队', '小学校', '管理站', '监督站', '新闻出版局', '歌剧院', '基地', '法定代表人',
                 '镇政府', '审计局', '人事局', '教育局', '画院', '残联', '水土保持局', '环卫处', '事业']

ln_end_words=['代理机构:', '李秋实集中采购机构:', ':', '采购招标代理:', '资金来源:', '预算金额:', '废标原因:',
              '集中采购机构:', '变更澄清或修改事项:', '吴迪集中采购机构:', '王侃集中采购机构:', '其他内容不变联系人:', '齐岩集中采购机构:',
              '二采购人地址:', '盖单位章招标代理:', '招标人地址:', '公章法定代表人:', '采购人地址:', '办公地址:', '采购地址:', '招标代理机构:',
              '联系人:', '地址:', '单位名称:', '招标单位联系人:', '招标人通信地址:', '联系方式:',
              '地点:', '采购代理机构:', '采购项目内容:', '联系地址:', '项目联系人:', '招标代理人:', '项目名称:', '名称:'
              ]