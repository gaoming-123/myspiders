# -*- coding=utf-8 -*-
# gmj
# 目标数据库的item类，即需要解析的字段列表


from scrapy import Item, Field


# 招标信息表
class ZhaoBiao(Item):
    bt = Field()  # 标题               已有


# 中标基本信息
class ZhongBiao(Item):
    zhaobiao_id = Field()  # 对应的招标ID
    xmmc = Field()  # 项目及标段名称


# 中标公司表
class ZhongBiaoGS(Item):
    zhongbiao_id = Field()  # 中标公示基本信息表id


# 中标人员表
class ZhongBiaoRY(Item):
    zhongbiao_id = Field()  # 中标公示基本信息表id


# 中标业绩
class ZhongBiaoYJ(Item):
    zhongbiao_id = Field()  # 中标公示基本信息表id
    gs_id = Field()  # 后台唯一公司id（关联）
