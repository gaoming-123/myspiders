# -*- coding=utf-8 -*-
# Author: gmj
# Date  : 2019/9/29 16:40
# Desc  : 省份数据解析配置文件


# 兵团网
bt_province = {
    'jyw': {
        '工程建设-招标公告': ('zhaobiao', ''),
        '工程建设-中标候选人公告': ('zhongbiao', 'bt_jyw_zbhxr'),
        '工程建设-中标结果公告': ('zhongbiao', 'bt_jyw_zbjggg'),
        # '工程建设-资格预审公示':('zhaobiao',''),
        # '工程建设-变更公告':('zhaobiao',''),
    },

    'cgw': {
        '采购公告-本级采购公告': ('zhaobiao', ''),
        # '采购公告-本级变更公告': ('zhaobiao', ''),
        '采购公告-本级中标/成交公告': ('zhongbiao', ''),
        # '采购公告-本级废标/终止公告': ('zhaobiao', ''),
        # '采购公告-本级澄清解答': ('zhaobiao', ''),

        '采购公告-师市采购公告': ('zhaobiao', ''),
        # '采购公告-师市变更公告': ('zhaobiao', ''),
        '采购公告-师市中标/成交公告': ('zhongbiao', ''),
        # '采购公告-师市废标/终止公告': ('zhaobiao', ''),
        # '采购公告-师市澄清解答': ('zhaobiao', ''),
    },
}

# 辽宁省
ln_province = {
    'jyw': {
        '建设工程-招标、资审公告': ('zhaobiao', ''),
        '建设工程-中标候选人公示': ('zhongbiao', 'ln_jyw_zbhxr'),
        '建设工程-中标结果公示': ('zhongbiao', 'ln_jyw_zbjggs'),
    },

    'cgw': {
        '采购公告-竞争性磋商公告': ('zhaobiao', ''),
        '采购公告-公开招标公告': ('zhaobiao', ''),
        '采购公告-询价公告': ('zhaobiao', ''),
        '单一来源公示-单一来源公示': ('zhaobiao', ''),
        '结果公告-中标公告': ('zhongbiao', ''),
    },
}

# 山东省
sd_province = {
    'jyw': {
        '工程建设-招标/资审公告': ('zhaobiao', ''),
        '工程建设-交易结果公示': ('zhongbiao', ''),
        '工程建设-中标候选人公示': ('zhongbiao', ''),
    },
    # 'cgw': {},
}

# 天津市
tj_province = {
    'jyw': {
        '工程建设-招标公告': ('zhaobiao', ''),
        '工程建设-中标结果公示': ('zhongbiao', 'tj_jyw_zbjggs'),
    },
    # 'cgw': {
    # },
    'contract_cgw': {
        '合同及验收公告-采购信息':('zhaobiao','')
    },
    'corrections_cgw': {
        '更正公告-采购信息':('zhaobiao','')
    },
    'demand_cgw': {
        '采购需求征求意见-采购信息':('zhaobiao','')
    },
    'purchase_cgw': {
        '采购公告-采购信息':('zhaobiao','')
    },
    'result_cgw': {
        '采购结果公告-采购信息':('zhongbiao','')
    },
    'source_cgw': {
        '单一来源公示-采购信息':('zhaobiao','')
    },
}

# 湖北省
# hubei_province={
#     'candidate_jyw':{
#         '工程建设-中标候选人':('zhongbiao',''),
#     },
#     'cgw':{
#     },
#
# }

# 安徽省
ah_province = {
    'jyw': {
        '工程招标-交易公告': ('zhaobiao', ''),
        '工程招标-结果公告': ('zhongbiao', 'ah_jyw_jyjg'),
    },
    # 'cgw': {'':('zhaobiao','')},
}


