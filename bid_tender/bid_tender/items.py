# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class WithoutProxyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()

class WithoutProxyLoader(ItemLoader):
    default_item_class = WithoutProxyItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()


class BaseItem(Item):
    """基础item模板"""
    link = Field()  # 采集来源url
    pur_name = Field()  # 业主
    content = Field()  # 详情网页内容
    xmbh = Field()  # 项目编号  从详情url中截取
    xmsd = Field()  # 项目属地
    sorce_web = Field()  # 数据源    只有 公共资源交易网 或者 政府采购网 两种
    ly=Field()         # 来源  来自网页内容
    title = Field()  # 项目名称(标题)
    ywlx = Field()  # 业务类型
    xxlx = Field()  # 信息类型
    fbsj = Field()  # 发布时间
    has_attach = Field()  # 是否有附件   0:没有, 1:有
    # 附件信息
    notice_id = Field()  # 公告下载链接
    attach_url_list = Field()  # 附件原链接
    attach_id_list = Field()  # 新生成的附件名字
    attach_location_list = Field()  # 附件本地存储路径

    pipeline_func = Field()  # 每一个item中都默认加上
    # pipline_func = Field()  # 每一个item中都默认加上

class AttachItem(Item):
    """  附件item  """
    notice_id = Field()
    fj_link = Field()
    fj_location = Field()
    fj_name = Field()