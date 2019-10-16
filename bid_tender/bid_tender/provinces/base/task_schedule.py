__all__=['province_weight']
from bid_tender.task.task_config import PROVINCES_DICT
# ======全量爬取的开关参数======
# 从全局配置文件中读取，没有将配置为全量爬取，用于开发测试
try:
    from bid_tender.task.task_config import base_FIRST_CRAWL
except:
    base_FIRST_CRAWL=True
#=====================

# 省份缩写及请求权重
try:
    province_name,province_weight=PROVINCES_DICT.get('省份名')
except TypeError:
    province_name, province_weight=0,0


# 配置handler任务的爬取控制方式，及爬取量参数的配置
# 每日任务控制配置    通过  (页码 或 天数 或 页码和天数) 三种配置来进行日常任务控制
# 控制逻辑写入list页的handler函数中
base_task_config={
    # 公共资源交易网
    'jy_list_parse':{
        # 控制爬取的page数
        'page':5,
        # 控制爬取的时间天数
        'period':2,
    },
    # 采购网
    'cg_list_parse':{
        # 控制爬取的page数
        'page':5,
        # 控制爬取的时间天数
        'period':2,
    },
}


