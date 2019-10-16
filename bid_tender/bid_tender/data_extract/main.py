# -*- coding=utf-8 -*-
# Author: gmj
# Date  : 2019/10/15 13:13
# Desc  : 解析运行主文件


from bid_tender.data_extract.data_extract import DataExtract

from bid_tender.data_extract.config import *
#
from bid_tender.data_extract.fields_extract_cfg import *
#
for i in ['bt','ah','sd','ln','tj']:
    dic=eval(f'{i}_province')
    data_e=DataExtract(db_from=eval(f'{i.upper()}_MYSQL_DB'), db_to=DES_MYSQL_DB)
    for x in dic.keys():
        data_e.extract(web_cate=x)


