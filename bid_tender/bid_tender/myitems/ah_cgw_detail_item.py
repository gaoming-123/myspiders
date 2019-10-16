from scrapy import Item, Field


class ah_cgw_detail_item(Item):
    xmbh = Field()  # 项目编号
    title = Field()  # 项目名称
    pur_name = Field()  # 项目业主
    content = Field()  # 详情原文件
    link = Field()  # 采集来源url
    sorce_web = Field()  # 来源网站名
    cgpmmc = Field()  # 采购品目名称
    ly = Field()  # 来源
    ywlx = Field()  # 业务类型
    xxlx = Field()  # 信息类型
    fbsj = Field()  # 发布时间
    xmsd = Field()  # 项目属地
    fj_list = Field()
    has_attach = Field()
    items = Field()
    pipline_func = Field()  # 每一个item中都默认加上