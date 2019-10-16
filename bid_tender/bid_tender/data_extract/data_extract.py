# 数据解析执行文件

import copy
import time

import pymysql
from bid_tender.data_extract.config import *
import logging
from lxml import etree
import pandas as pd
# 导入全部的字段解析函数
from bid_tender.data_extract.utils import get_start_date
from bid_tender.data_extract.zhaobiao_fields_parse import *
from bid_tender.data_extract.zhongbiao_fields_parse import *
from bid_tender.data_extract.config import zhaobiao_fields_dict, zhongbiao_fields_dict, provinces_dict
from bid_tender.data_extract.fields_extract_cfg import *
from bid_tender.data_extract.province_private import *


# 执行解析数据的类，从一个源数据库到目标数据库的全流程执行
class DataExtract(object):
    """数据提取的类"""

    def __init__(self, db_from, db_to, cursor_class=pymysql.cursors.Cursor):
        self.cursor_class = cursor_class
        # 源数据库
        self.db_from = db_from
        # 目标数据库
        self.db_to = db_to
        self.cnn, self.cursor = self._connect()
        self.to_cnn, self.to_cursor = self._des_connect()
        # 保存错误的数据
        self.error_jy = []
        self.error_cg = []

    def _connect(self):
        # 连接原始数据 数据库
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=self.db_from,
            charset=MYSQL_CHATSET,
            port=MYSQL_PORT,
            cursorclass=self.cursor_class
        )
        return conn, conn.cursor()

    def _des_connect(self):
        # 链接目标数据库
        conn = pymysql.connect(
            host=DES_MYSQL_HOST,
            user=DES_MYSQL_USER,
            password=DES_MYSQL_PASSWORD,
            db=self.db_to,
            charset=DES_MYSQL_CHATSET,
            port=DES_MYSQL_PORT,
            cursorclass=self.cursor_class,
            use_unicode=True
        )
        return conn, conn.cursor()

    def extract(self, web_cate='jyw',index=None):
        # 传入表名  sd_jyw
        self._extract_data(web_cate,index=index)

    def _extract_data(self, web_cate, num=100,index=None):
        start_time = time.time()
        province = self.db_from.split('_')[0]
        org_table = f'{province}_{web_cate}'

        # org_sql = f'select * from {org_table} where created > "{get_start_date()}" and flag=1'

        if index:
            org_sql = f'select * from {org_table} where id={index}'
        else:
            org_sql = f'select * from {org_table} where created > "{get_start_date()}" and flag=1'
        self.cursor.execute(org_sql)
        # print(self.cursor.rowcount)
        columns = self.cursor.description
        columns = [field[0] for field in columns]
        # print(columns)
        org_wrong_num = 0
        org_total = 0
        no_deal = 0
        logging.info(f'start extract table of {org_table} data')
        print(f'start extract table of {org_table} data')
        while 1:
            data = self.cursor.fetchmany(num)
            print('开始处理间隔时间：', time.time() - start_time)
            for d in data:
                # 执行单条数据提取
                try:
                    data_extract = OneDataExtract(columns, d, province, web_cate)
                    # 得到数据
                    result, des_table = data_extract.extract()
                    # print(result)
                    if result:
                        # 设置省份字段
                        result.setdefault('sf', provinces_dict.get(province))
                        result.setdefault('area', provinces_dict.get(province))
                        # 保存数据
                        save_res = self._save_extract_data(des_table, result, update=True)
                        if save_res:
                            # self._change_flag(org_table, d[0])

                            logging.info(f'save data to {des_table} success')
                        else:
                            org_wrong_num += 1
                            logging.info(f'save data to {des_table} failed')
                    else:
                        if result is None:
                            no_deal += 1
                        else:
                            org_wrong_num += 1
                            logging.info(f'save data to {des_table} failed')
                except:
                    org_wrong_num += 1
                    logging.info(f'save data to {des_table} failed')
            org_total += len(data)
            if len(data) < num:
                break
        logging.info(
            f'finish extract table of {org_table} data,源数据：{org_total}条，成功:{org_total-no_deal-org_wrong_num}. 失败:{org_wrong_num}.未处理：{no_deal}')
        logging.info(f'处理{self.db_from}.{org_table}共耗时：', time.time() - start_time)
        print(
            f'finish extract table of {org_table} data,源数据：{org_total}条，成功:{org_total-no_deal-org_wrong_num}. 失败:{org_wrong_num}.未处理：{no_deal}')
        print(f'处理{self.db_from}.{org_table}共耗时：', time.time() - start_time)

    def _change_flag(self, table, pk):
        sql = f'update {self.db_from}.{table} set flag=2 where id={pk}'
        self.cursor.execute(sql)
        self.cnn.commit()

    def _save_extract_data(self, table, data, update=True):
        if table == 'zhongbiao':
            return self.save_zhongbiao(data, update=update)
        if table == 'zhaobiao':
            return self.save_zhaobiao(data, update=update)
        else:
            return self.save_des_table(table, data, update=update)

    def save_zhaobiao(self, data, update):
        # 保存招标数据
        return self.save_des_table('qg_zhaobiao', data, update=update)

    def save_des_table(self, table_name, res_data: dict, other_data: dict = None, update=True):
        """将结果保存到目标数据库目标表"""
        if other_data is None:
            other_data = {}
        columns = self.get_des_columns(table_name)
        data = dict(res_data, **other_data)
        # print(data)
        sql_txt, values = self._get_sql_txt(table_name, columns, data, update=update)
        try:
            self.to_cursor.execute(sql_txt, values)
            self.to_cnn.commit()
            return self.to_cursor.lastrowid
        except Exception as e:

            print(e)
            print(data)
            self.to_cnn.rollback()
            logging.info(f'save data to {table_name} failed. the error: {e}')
            return False

    def save_zhongbiao(self, data, update=True):
        # 保存中标数据
        # 查找招标id
        # zhaobiao_id = ''
        # other_data = {'zhaobiao_id': 11, }
        # res = self.save_des_table('qg_zhongbiao', data, other_data=other_data, update=update)
        res = self.save_des_table('qg_zhongbiao', data, update=update)
        # print('res',res)
        if res:
            other_data = {'zhongbiao_id': res, }
            # 中标公司表
            if isinstance(data['company'], list):
                company_num = len(data['company'])
                for i in range(company_num):
                    if not data['company'][i]:
                        continue
                    one_data = {}
                    one_data['company'] = data['company'][i]
                    one_data['zbmc'] = i + 1
                    one_data['is_yszb'] = 1 if i == 0 else 0
                    try:
                        one_data['tbbj'] = data['tbbj'][i]
                    except:
                        one_data['tbbj'] = ''
                    try:
                        one_data['zhpf'] = data['zhpf'][i]
                    except:
                        one_data['zhpf'] = ''
                    self.save_des_table('qg_zhongbiao_gs', one_data, other_data=other_data, update=update)
            else:
                self.save_des_table('qg_zhongbiao_gs', data, other_data=other_data, update=update)
            # 中标人员表
            if isinstance(data['name'], list):
                name_num = len(data['name'])
                for i in range(name_num):
                    if not data['name'][i]:
                        continue
                    one_data = {}
                    for field in ['name', 'zsms', 'zsbh', 'zc', 'zczy', 'jb', 'zw', 'gsmc']:
                        try:
                            if field == 'gsmc':
                                one_data[field] = data['company'][i]
                            else:
                                one_data[field] = data[field][i]
                        except:
                            one_data[field] = ''

                    self.save_des_table('qg_zhongbiao_ry', one_data, other_data=other_data, update=update)
            else:
                self.save_des_table('qg_zhongbiao_ry', data, other_data=other_data, update=update)
            # 中标业绩表
            self.save_des_table('qg_zhongbiao_yj', data, other_data=other_data, update=update)
        return res

    def get_des_columns(self, table):
        """获取目标表的列属性"""
        sql = f'select * from {table } order by id desc limit 1'
        self.to_cursor.execute(sql)
        columns = self.to_cursor.description
        columns = [field[0] for field in columns]
        return columns

    def _get_sql_txt(self, table, columns, data, update):
        """构造sql语句"""
        sql_txt = f"INSERT INTO {self.db_to}.{table}"
        field_list = []
        field_site = []
        field_update = []
        fields_value = {}
        for fe in columns:
            if fe == 'id':
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

    def __del__(self):
        # 关闭连接
        self.cursor.close()
        self.cnn.close()
        self.to_cursor.close()
        self.to_cnn.close()


# 数据解析的具体执行类，执行单条数据的具体执行
class OneDataExtract(object):
    """单条数据提取的类"""

    def __init__(self, columns, org_data, province, web_cate):
        # 原始数据  元组
        self.org_data = org_data
        self.province = province
        # 网站类型
        self.web_cate = web_cate
        # 返回的最终数据
        self.columns = columns
        # 业务类型
        self.yw_cate = self._get_yw_cate()
        # self._get_content()
        # 按行存储的网页内容
        # self._get_content_line()
        # print(extract_method)

    def extract(self):
        result, des_table = self._pro_yw_cate_extract()
        return result, des_table

    def _pro_yw_cate_extract(self):
        # 省份 业务类别网页解析
        # 该省份 该类别的解析控制字典
        province_dict = eval(f'{self.province}_province')
        # 网站类型
        pro_web_cate = province_dict.get(self.web_cate)
        try:
            des_table, extract_method = pro_web_cate.get(self.yw_cate)

            # 按行存储的网页内容
            self._get_content_line()
            # 正文文本内容保存
            self._get_content()
            # 进行表格处理
            self._table_extract()
        except:
            return None, None
        # 获取提取字段的控制字典
        extract_res = {}
        if extract_method:
            # 得到解析结果
            extract_res = eval(
                extract_method + '(self.province,self.html,self.content,self.content_list,self.table_line,self.tables)')
        yw_cate_dict = pro_web_cate.get(f'{self.web_cate}1')
        if not yw_cate_dict:
            # 如果取不到值，则读取默认值
            yw_cate_dict = eval(f"{des_table}_fields_dict")
        # 复制一份数据字典 用于保存解析结果
        pro_cate_dict = copy.deepcopy(yw_cate_dict)
        for k, v in yw_cate_dict.items():
            # 对于字段 如果有自定义的方法则调用该方法，否则，调用公用方法
            if v:
                # 直接取值 ，表示该字段值不需要解析
                f_num = self.columns.index(v)
                data = self.org_data[f_num]
                if isinstance(data, str):
                    data = data.strip()
                pro_cate_dict[k] = data
            else:
                # 没有在独立解析结果中，则调用共用的方法
                if k not in extract_res:
                    pro_cate_dict[k] = eval(
                        f'extract_{k}' + '(self.province,self.html,self.content,self.content_list,self.table_line,self.tables)')
        if extract_res:
            pro_cate_dict = dict(pro_cate_dict, **extract_res)
        return pro_cate_dict, des_table

    def _get_yw_cate(self):
        # 获得网页类别区分值  两个字段值相加得到
        f_num = self.columns.index('ywlx')
        f_num2 = self.columns.index('xxlx')
        return self.org_data[f_num] + '-' + self.org_data[f_num2]

    def _get_content(self):
        """获取节点的正文内容"""
        # 去掉b标签
        # content = content.replace('<b>', '').replace('</b>', '').replace('&nbsp;', '')
        # 将网页切成列表
        # self.html = etree.HTML(content)
        content = self.html.xpath('string(.)').replace('：', ':').replace(' ', '').strip()
        # print('content11',content)
        content = re.sub(r'\s+', ' ', content)
        # print('content222',content)
        x = re.compile(r'<[^>]+>', re.S)
        # self.content = x.sub('', html)
        self.content = x.sub('', content)
        # print(self.content)

        # 能够直接使用的原始数据，进行直接赋值

    def _get_content_line(self):
        f_num = self.columns.index('content')
        content = self.org_data[f_num]
        # 处理可能转义的文本
        html = etree.HTML(content)
        content1 = html.xpath('string(.)')
        content1=self.deal_content(content1)
        # print('++++++', content)
        content = self.deal_content(content)
        content_list = content.split('\n')
        content_list1=content1.split('\n')
        # 取对网页处理成功的列表
        if len(content_list)< len(content_list1):
            content_list=content_list1
            content1 = content1.replace('<b>', '').replace('</b>', '').replace('&nbsp;', '')
            self.html=etree.HTML(content1)
        else:
            content = content.replace('<b>', '').replace('</b>', '').replace('&nbsp;', '')
            self.html = etree.HTML(content)
        self.content_list = []
        for line in content_list:
            if line.startswith(':'):
                line = line[1:]
            self.content_list.append(line)
        if len(content_list) < 3:
            print('id', self.org_data[0], '网页行数：', len(content_list))

    def deal_content(self, content):
        if '</p>' in content:
            content = content.replace('</p>', '******</p>')
        if '<br>' in content:
            content = content.replace('<br>', '******')
        if '</tr>' in content:
            content = content.replace('</tr>', '******</tr>')
        if '</th>' in content:
            content = content.replace('<th>', '******<th>')
            content = content.replace('</th>', ':</th>')
        if '</td>' in content:
            content = content.replace('</td>', '******</td>')
            content = content.replace('</td>', ':</td>')
        if '</div>' in content:
            content = content.replace('</div>', '******</div>')
        html = etree.HTML(content)
        contents = html.xpath('string(.)').replace('：', ':').replace('::', ':').strip()
        # contents = html.xpath('string(.)').replace('：', ':').strip()
        pattern_list = [r' ', r'\u3000', r'\xa0', r'\s+', r'\x09', r'\x0d']
        for pattern in pattern_list:
            contents = re.sub(pattern, '', contents)
        # print(contents)
        contents = contents.replace(':******', ':')
        contents = re.sub(r'[*]+', '\n', contents)
        contents = re.sub(r':\n+:', '###', contents)
        # contents = re.sub(r':', '', contents)
        contents = re.sub(r'###', ':', contents)
        content = re.sub(r':+', ':', contents)
        # print(content)
        return content

    def _table_extract(self):
        """
        # 列表数据 可以通过键 ： 切分得到值
        :return: 表格网页的数据列表  以及 横向表格数据
        """
        f_num = self.columns.index('content')
        text = self.org_data[f_num]
        if ('&lt;' in text) and ('&gt;' in text):
            html = etree.HTML(text)
            text = html.xpath('string(.)')
        tes_txt = text.replace('</td>', '++</td>')
        tes_txt = tes_txt.replace('</th>', '+h+</th>')
        tes_txt = re.sub('\s', '', tes_txt)
        html = etree.HTML(tes_txt)
        tr_txt_list = []
        tr_data_list = []
        data_lines = []
        tr_list = html.xpath('//tr')
        # print(len(tr_list))
        for tr in tr_list:
            tr_2 = tr.xpath('.//tr')
            if tr_2:
                pass
            else:
                content = tr.xpath('string(.)')
                content = content.replace(' ', '')

                if content != '+' * len(content):
                    tr_txt_list.append(tr)
        # print(len(tr_txt_list))
        for txt in tr_txt_list:
            content = txt.xpath('string(.)').replace('：', ':').strip()
            content = content.replace(' ', '')
            # 删除开头的++
            if content.startswith('+'):
                while 1:
                    if content.startswith('+'):
                        content = content[1:]
                    else:
                        break
            tr_data_list.append(content[:-2])
        # 将含有：的多个td拆分为 k:v 形式 的行
        self._td_to_lines(data_lines, tr_data_list)
        # 处理整体文本 分理处k v 键值对行   与 表table数据
        self._to_lines_and_table(data_lines)

    def _to_lines_and_table(self, data_lines):
        # 处理整体文本 分理处k v 键值对行   与 表table数据
        k_v_line = []
        table_dict = {}
        for line in data_lines:
            if line.startswith('table'):
                table_name_org = re.findall('tableh?\d+-', line)[0]
                table_name = table_name_org.replace('h', '')
                if table_name in table_dict:
                    # table_dict[table_name].append(line.replace(table_name_org,'')+'\n')
                    table_dict[table_name].append(line.replace(table_name_org, ''))
                else:
                    table_dict.setdefault(table_name, [line.replace(table_name_org, ''), ])
            else:
                k_v_line.append(line)
        for k, v in table_dict.items():
            table_data = [t_l.split('++') for t_l in v]
            table_dict[k] = pd.DataFrame(table_data)
            # print(table_dict[k])
        table_data = {}
        for k in table_dict:
            df = table_dict[k]
            rows, columns = df.shape
            if rows != 1:
                # 判断表格的方向
                # 用于判断表格方向的表头，非第一行或者第一列表头 的集合
                head = ['工期', '金额', '中标价', '业绩', '废标原因', '负责人','预算']
                index = self._judge_index(df, head)
                if index == '0':
                    # 将表格转置为横向表
                    df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
                table_data[k] = df
        # 返回结果为k_v键值对的列表  以及 横向表的字典
        self.tables = table_data
        self.table_line = k_v_line

    def _td_to_lines(self, data_lines, tr_data_list):
        # 将含有：的多个td拆分为 k:v 形式 的行
        table_num = 0
        table_columns = 1
        for content in tr_data_list:
            # 以多个键值对存在的行，将数据处理为单个按键值对的行
            if '+h+' in content:
                if '++' in content:
                    table_columns = 1
                    # th td 混编
                    tr_content_l = content.split('++')
                    for th_td in tr_content_l:
                        th_td = th_td.replace('+h+', ':')
                        th_td = re.sub(':+', ':', th_td)
                        data_lines.append(th_td)
                else:
                    # 全是表头的情况
                    tr_content_l = content.split('+h+')
                    columns = len(tr_content_l)
                    if columns != table_columns:
                        table_num += 1
                        table_columns = columns
                        # 给行数据做标记  有表头的表n
                        content = f'tableh{table_num}-' + content
                        data_lines.append(content)
            if ':++' in content:
                # td:td 键值对
                table_columns = 1
                tr_content_l = content.split('++')
                for i in range(0, len(tr_content_l), 2):
                    td_k_v = ''.join(tr_content_l[i:i + 2])
                    data_lines.append(td_k_v)
            elif '++' in content:
                # td/td/td
                tr_content_l = content.split('++')
                columns = len(tr_content_l)
                if columns != table_columns:
                    table_num += 1
                    table_columns = columns
                    # 给行数据做标记
                    content = f'table{table_num}-' + content
                    data_lines.append(content)

                else:

                    data_lines.append(f'table{table_num}-' + content)
            else:
                data_lines.append(content)
                table_columns = 1

    def _judge_index(self, df, head):
        # 判断表的方向
        # 默认竖向表
        index = '0'
        # 根据表头来判断
        for name in head:
            # name = '工期'
            # 第一列数据
            for row_name in df.iloc[:, 0]:
                if name in row_name:
                    index = '0'
            # 第一行数据
            for col_name in df.iloc[0, :]:
                if name in col_name:
                    index = '1'
        columns = df.shape[1]
        # 通过 数据 (公司)  来判断
        for i in range(columns):
            comp_num = 0
            for name in df.iloc[:, i]:
                if name.endswith('公司'):
                    comp_num += 1
            if comp_num > 1:
                # 横向表
                index = '1'
        return index


if __name__ == '__main__':
    # data_extract = DataExtract(db_from=LN_MYSQL_DB, db_to=DES_MYSQL_DB)
    # data_extract.extract(web_cate='jyw')
    # data_extract.extract(web_cate='cgw')
    # data_extract.extract(web_cate='cgw',index=127673)
    data_extract = DataExtract(db_from=TJ_MYSQL_DB, db_to=DES_MYSQL_DB)
    data_extract.extract(web_cate='result_cgw',index=5)
    # data_extract.extract(web_cate='contract_cgw')
    pass
