# 这是省份文件的模板文件，

base_rules=[
    #
    {
        're': '',
        'func': 'base_jy_list_handler',
        'use_js': False,
    },
]
# 导入所有的pipeline方法
from .pipelines import *
# 导入所有的item类
from .items import *
# 导入所有的handler方法
from .handlers import *
# 从任务配置文件导入参数     province_weight 为该省的请求权重
from .task_schedule import province_weight
#  每天的任务链接及权重
base_everyday_task=[
    # # # # #(  url地址 , 权重值  )
    ###========= 公共资源交易网==============###
    ('', province_weight),
    ###=========   采购网   ============###
]

