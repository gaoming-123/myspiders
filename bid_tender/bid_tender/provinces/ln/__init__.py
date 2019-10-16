# 这是省份文件的模板文件，


ln_rules=[
    # 辽宁省公共资源列表页
    {
        're': r'http://www.lnggzy.gov.cn/lnggzy/showinfo/Morejyxx.aspx[?]timebegin.*?',
        'func': 'ln_jy_list_handler',
        'use_js': False,
    },
    # 辽宁省公共资源详情页
    {
        're': r'http://www.lnggzy.gov.cn/lnggzy/.*?/.*?[?]InfoID=.*?',
        'func': 'ln_jy_detail_handler',
        'use_js': False,
    },
    # 采购网  get页  即第一次请求
    {
        're': r'http://www.ccgp-liaoning.gov.cn/portalindex.do[?]method=goPubInfoList',
        'func': 'ln_cg_list_handler',
        'use_js': False,
    },
    #采购网  form-request页
    {
        're': r'http://www.ccgp-liaoning.gov.cn/portalindex.do[?]method=getPubInfoList&t_k=null',
        'func': 'ln_cg_list_handler',
        'use_js': False,
    },
    #
    {
        're': r'http://www.ccgp-liaoning.gov.cn/portalindex.do[?]method=getPubInfoViewOpen&infoId=.*?',
        'func': 'ln_cg_detail_handler',
        'use_js': False,
    },
]
from .pipelines import *
from .items import *
from .handlers import *
from .task_schedule import province_weight
from .utils import get_release_time,get_start_date
#  每天的任务链接及权重
ln_everyday_task=[
    #(  url地址 , 权重值  )
    # 公共资源网  取两天时间
    (f'http://www.lnggzy.gov.cn/lnggzy/showinfo/Morejyxx.aspx?timebegin={get_start_date()}&timeend={get_release_time()}&timetype=06&num1=000&num2=000000&jyly=005&word=', province_weight),
    # 采购网
    ('http://www.ccgp-liaoning.gov.cn/portalindex.do?method=goPubInfoList',province_weight)

]

