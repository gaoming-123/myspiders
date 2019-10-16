from bid_tender.task.task_config import PROVINCES_DICT

try:
    from bid_tender.task.task_config import ln_FIRST_CRAWL
except:
    # 第一次全量爬取
    ln_FIRST_CRAWL = True

# 省份缩写
try:
    province_name, province_weight = PROVINCES_DICT.get('辽宁')
except TypeError:
    province_name, province_weight = 0, 0

# 配置handler任务的爬取控制方式，及爬取量参数的配置
# page 和period不能共存
ln_task_config = {

    'jy_list_parse': {
        # 控制爬取的page数
        'page': 40,
        # 控制爬取的时间天数
        'period': 2,
    },
    'cg_list_parse': {
        # 控制爬取的page数
        'page': 15,
        # 控制爬取的时间天数
        'period': 2,
    },
}


