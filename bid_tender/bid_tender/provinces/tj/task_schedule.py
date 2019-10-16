# 控制是否为首次爬取，即全量爬取
from bid_tender.task.task_config import PROVINCES_DICT
try:
    from bid_tender.task.task_config import tj_FIRST_CRAWL
    tj_FIRST_CRAWL=tj_FIRST_CRAWL
except:
    # 第一次全量爬取
    tj_FIRST_CRAWL=True


# 省份缩写
try:
    province_name,province_weight=PROVINCES_DICT.get('天津')
except TypeError:
    province_name, province_weight=0,0

# 配置handler任务的爬取控制方式，及爬取量参数的配置
# page 和period不能共存
tj_task_config={
    # handler的方法名，用于提取参数的键
    'jy_list_parse':{
        # 控制爬取的page数
        'page':20,
        # 控制爬取的时间天数
        'period':10,
    },
    'cg_list_parse': {
        # 控制爬取的page数
        'page': 5,
        # 控制爬取的时间天数
        'period': 2,
    },
}


