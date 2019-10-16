# -*- coding=utf-8 -*-
# gmj
# 数据库配置文件

##===================源数据的数据库配置===============
# 测试数据库配置
# MYSQL_HOST = '*'
# MYSQL_USER = '*'
# MYSQL_PASSWORD = '*'
# MYSQL_CHATSET = 'utf8'
# MYSQL_PORT = 3306

# 生产数据库配置


##=====================end=============================


##================目标数据库的配置======================
DES_MYSQL_HOST = '*'
DES_MYSQL_USER = '*'
DES_MYSQL_PASSWORD = '*'
DES_MYSQL_CHATSET = 'utf8'
DES_MYSQL_PORT = 3306

DES_MYSQL_DB = "*"


##===================end==================================


# ====================以下为连接数据库配置=================
TJ_MYSQL_DB = "tj_tender_crawler"  # 天津

BT_MYSQL_DB = "bt_tender_crawler"  # 兵团
LN_MYSQL_DB = "ln_tender_crawler"  # 辽宁

AH_MYSQL_DB='ah_tender_crawler'  #安徽
# ====================以上为连接数据库配置=================


zhaobiao_fields_dict = {
    'lj': 'link',  # 采集来源url
    'cs': 'xmsd',  # 项目属地/城市
    'ly': 'ly',  # 来源  来自网页内容
    'bt': 'title',  # 项目名称(标题)
    'fbsj': 'fbsj',  # 发布时间
    'nr': 'content',  # 内容

    'xmbh': '',  # 项目编号
    'bxry': '',  # 项目业主
    'zbdl': '',  # 招标代理              招标代理
    'jsgm': '',  # 建设规模   总投资
    'zjly': '',  # 资金来源                                                   资金来源
    'tel': '',  # 联系方式
    'zgys_ff': '',  # 资格预审的方法（公共资源交易网铁路工程）（发布公告的媒介）
    'zgys_hq': '',  # 资格预审文件的获取（公共资源交易网铁路工程）（招标文件的获取）
    'zgys_dj': '',  # 资格预审文件的递交（公共资源交易网铁路工程）（投标文件的递交）
    'zgyq': '',  # 资格要求                                                   资格要求
    'kbdd': '',  # 开标地点                                                   开标地点
    'zbtj': '',  # 招标条件（公共资源交易网和建设网）
    'spjg': '',  # 审批机关
    'gk_zbfw': '',  # 项目概况与招标范围    招标范围
    'zzxs': '',  # 招标组织形式

    'zbr_tel': '',  # 招标人电话
    'zbdl_tel': '',  # 招标代理电话
    'jbqk': '',  # 项目基本情况
    'tbfs': '',  # 投标方式
    'jzrq': '',  # 截止日期
    'tb_jzrq': '',  # 投标截止日期
    'zblb': '',  # 招标类别
    'ssd': '',  # 建设地点
    'cgr': '',  # 采购人
    'cgnr': '',  # 采购内容
}

zhongbiao_fields_dict = {
    'fbsj': 'fbsj',  # 官网发布时间
    'txt': 'content',  # 源文件
    'link': 'link',  # 网站链接
    'city': 'xmsd',  # 城市
    # 'area':'', # 省份
    # 'sf': '',  # 省份
    # 需要解析的字段
    'xmmc': 'title',  # 项目及标段名称
    'type': '',  # 类型
    'xmbh': '',  # 项目编号

    'zbr': '',  # 招标人
    'zbrdh': '',  # 招标人联系电话
    'zbdl': '',  # 招标代理机构
    'zbdldh': '',  # 招标代理机构电话
    'kbdd': '',  # 开标地点
    'kbsj': '',  # 开标时间
    'gsq': '',  # 公示期
    'zgxj': '',  # 投标最高限价（元）
    'zgxjw': '',  # 投标最高限价（万元）
    'first_tbbjw':'',# 第一投标报价
    'pscy': '',  # 评审委员会成员名单
    'effective':'',# 有效家数
    'tbgs_count':'',# 总投资家数

    # 'jhgq': '',  # 计划工期
    'zbmc': '',  # 中标名次1第一名2第二名3第三名4投标5双低10废标
    'is_yszb': '',  # 是否为疑似中标，1是，0不是
    'company': '',  # 中标候选人名称
    'tbbj': '',  # 投标报价（元）/否决投标依据条款
    'tbbjw': '',  # 投标报价（万元）
    'psbj': '',  # 经评审的投标价（元）/否决投标理由
    'psbjw': '',  # 经评审的投标价（万元）
    'zhpf': '',  # 综合评标得分/备注
    'zdxf': '',  # 最低下浮
    'is_zq': '',  # 最低下浮的计算方式是否准确，准或约
    'fbyy_str': '',  # 废标原因类型
    'fbyy_dict': '',  # 废标原因类型对应的字典值
    'money': '',  # 前台查询字段
    'flag': '',  # 1未转换，2已转换

    'gsmc': '',  # 关联公司名称
    'name': '',  # 姓名
    'zsmc': '',  # 证书名称
    'zsbh': '',  # 证书编号
    'zc': '',  # 职称
    'zczy': '',  # 职称专业
    'jb': '',  # 级别
    'zw': '',  # 职务

    'xmyz': '',  # 项目业主
    # 'yjgllx': '',  # 业绩关联类型
    # 'yjlx': '',  # 业绩类型
    # 'yjlx_main_str': '',  # 业绩类型大类名称
    # 'yjlx_main_dict': '',  # 业绩类型大类字典值
    # 'yjlx_sub_str': '',  # 业绩类型子类名称
    # 'yjlx_sub_dict': '',  # 业绩类型子类字典值
    'kgrq': '',  # 开工时间
    'jiao_rq': '',  # 交工日期
    'jun_rq': '',  # 竣工日期
    'jsgm': '',  # 建设规模
    'htjg': '',  # 合同价格（元）
    'htjgw': '',  # 合同价格（万元）
    'htjgzf': '',  # 合同价格字符
    'xmfzr': '',  # 项目负责人
    'jsfzr': '',  # 技术负责人

}

# 省份字典
provinces_dict = {
    'tj': '天津市',
    'ln': '辽宁省',
    'ah': '安徽省',

}
