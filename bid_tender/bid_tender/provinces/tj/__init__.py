tj_rules=[
    # 天津公共资源交易网 列表页
    {
        're': r'http://ggzy.xzsp.tj.gov.cn/.*?/index_\d+\.jhtml',
        'func': 'tj_jy_list_handler',
        'use_js': False,
    },
    # 天津公共资源交易网 详情页
    {
        're': r'http://ggzy.xzsp.tj.gov.cn:80/.*?/.*?.jhtml',
        'func': 'tj_jy_detail_handler',
        'use_js': False,
    },
# 天津市政府采购网
#     # get请求 列表  第一次请求页
#     {
#         're': r'http://www.ccgp-tianjin.gov.cn/portal/topicView.do[?]method=view&view=Infor&id=1665&ver=2&st=1',
#         'func': 'tj_cg_list_handler',
#         'use_js': False,
#     },
#     # post请求 表页
#     {
#         're': r'http://www.ccgp-tianjin.gov.cn/portal/topicView.do',
#         'func': 'tj_cg_list_handler',
#         'use_js': False,
#     },
#     # 详情页
#     {
#         're': r'http://www.ccgp-tianjin.gov.cn/portal/documentView.do[?]method=view&id=\d+&ver=\d+',
#         'func': 'tj_cg_detail_handler',
#         'use_js': False,
#     },
]
from .pipelines import *
from .items import *
from .handlers import *
from .task_schedule import province_weight
#  每天的任务链接及权重
tj_everyday_task=[
    #(  url地址 , 权重值  )
# 天津市公共资源交易网
    # 政府采购
    ('http://ggzy.xzsp.tj.gov.cn/jyxxzfcg/index_1.jhtml', province_weight),
    # 工程建设
    ('http://ggzy.xzsp.tj.gov.cn/jyxxgcjs/index_1.jhtml', province_weight),
    # 土地使用权
    ('http://ggzy.xzsp.tj.gov.cn/jyxxky/index_1.jhtml', province_weight),
    # 国有产权
    ('http://ggzy.xzsp.tj.gov.cn/jyxxcq/index_1.jhtml', province_weight),
    # 农村产权
    ('http://ggzy.xzsp.tj.gov.cn/jygknccq/index_1.jhtml', province_weight),
    # 医药采购
    ('http://ggzy.xzsp.tj.gov.cn/jyxxyy/index_1.jhtml', province_weight),
    # 矿业权交易
    ('http://ggzy.xzsp.tj.gov.cn/jyxxkyq/index_1.jhtml', province_weight),
    # 其他
    ('http://ggzy.xzsp.tj.gov.cn/jyxxqt/index_1.jhtml', province_weight),

# 采购网
#     ('http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1', province_weight),
    # # 区
    # (f'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=find&name=&ldateQGE=&ldateQLE=&id=1994&view=Infor&type=&fd=&typeIn=?sj={get_release_time()}type1=page&page=1', province_weight),

]

