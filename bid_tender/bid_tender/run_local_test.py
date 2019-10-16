
# 该文件是用于本地测试
import datetime
import time
from redis import StrictRedis
from scrapy.cmdline import execute

def get_release_time():
    bnow_time = datetime.datetime.now().strftime('%Y-%m-%d')
    bnow_time = bnow_time + ' 10:00:00'
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    release_time = ''
    if time.strptime(str(now_time), '%Y-%m-%d %H:%M:%S') >= time.strptime(str(bnow_time), "%Y-%m-%d %H:%M:%S"):
        release_time = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        release_time = datetime.datetime.now() - datetime.timedelta(days=1)
        release_time = release_time.strftime('%Y-%m-%d')
    return release_time


release_time=get_release_time()

# REDIS_URL = 'redis://127.0.0.1:6379'
# REDIS_HOST = '127.0.0.1'
# REDIS_PASSWORD = ''
# REDIS_PORT = 6379
# DB = 12
def add_start_url():
    # 测试的 起始url
    # task_url_map = {
    #
    #     # 安徽
    #     'ah_cgw': [
    #         'http://www.ccgp-anhui.gov.cn/cmsNewsController/getCgggNewsList.do?pageNum=1&numPerPage=20'
    #     ],
    #     'ah_jyw': [
    #         'http://ggzy.ah.gov.cn/dwr/call/plaincall/bulletinInfoDWR.getPackListForDwr1.dwr?page=1'
    #     ],
    #
    #
    # }

    test_urls = [
        # 天津采购网
        # 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1',
        # 天津市
        # 'http://ggzy.xzsp.tj.gov.cn/jyxxzfcg/index_1.jhtml',
        # 'http://ggzy.xzsp.tj.gov.cn/jyxxgcjs/index_1.jhtml',
        # 山东

        # 'http://ggzyjy.shandong.gov.cn/queryContent_1-jyxxgg.jspx?channelId=78',
        'http://ggzyjy.shandong.gov.cn/queryContent_1-jyxxgg.jspx?channelId=79',

        # 兵团公共资源

        # "http://ggzy.xjbt.gov.cn/TPFront/jyxx/004005/004005002/?paging=1",
        # 辽宁省交易网
        # 'http://www.lnggzy.gov.cn/lnggzy/showinfo/Morejyxx.aspx?timebegin=2019-09-30&timeend=2019-10-08&timetype=06&num1=000&num2=000000&jyly=005&word=',
        # 浙江
        # 'http://zjpubservice.zjzwfw.gov.cn/fulltextsearch/rest/getfulltextdata?format=json&sort=0&rmk1=002001001&pn=0&rn=20&idx_cgy=web',
        # 贵州
        # 'http://www.gzjyfw.gov.cn/gcms/queryContent.jspx?title=&businessCatalog=CE&businessType=ALL&inDates=800&ext=&origin=ALL'
        # 辽宁采购网
        # 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=goPubInfoList',
        # 兵团采购
        #  本级采购公告
        # 'http://cgw.xjbt.gov.cn/cggg/bjcggg/',
        # 本级变更公告
        # 'http://cgw.xjbt.gov.cn/cggg/bjgzgg/',
        # 本级中标/成交公告
        # 'http://cgw.xjbt.gov.cn/cggg/bjcjgg/',

    ]

    # for v in task_url_map.values():
    #     if isinstance(v,list):
    #         test_urls.append(v[0])
    #         # print(v[0])
    #     else:
    #         test_urls.append(v)
    #         # print(v)

    # print(len(test_urls))

    print('add start')
    redis_cli = StrictRedis(
        host='127.0.0.1',
        port=6379,
        password='',
        db=12
    )
    # redis_cli.delete('bid_tender:start_urls')
    redis_cli.flushdb()
    for url in test_urls:
        redis_cli.lpush('bid_tender:start_urls', url)
    print('add end')



if __name__ == '__main__':
    # execute(['scrapy', 'crawl', 'test_bid_tender_master'])
    add_start_url()
    # execute(['scrapy', 'crawl', 'test_bid_tender_master'])
    # 将打印信息保存到日志  需要更改日志文件名
    # execute(['scrapy', 'crawl', 'bid_tender','--logfile=my_test20190918ln_pur.log'])
    # 打印信息打印在窗口
    execute(['scrapy', 'crawl', 'bid_tender'])
#


