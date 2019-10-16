import datetime
import re
import pymysql
from bid_tender.config.ah_cgw import *


def ah_cgw(response):
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset=MYSQL_CHATSET,
        port=MYSQL_PORT
    )
    cursor = conn.cursor()
    rtn_data = {}
    sql = 'select id from ah_cgw_list where url = %s'
    if 'requests' not in rtn_data:
        rtn_data['requests'] = []
    list = response.xpath('//div[@class="zc_contract_top"]')[1].xpath('./table/tr')
    for li in list:
        url = 'http://www.ccgp-anhui.gov.cn' + li.xpath('./td/a/@href').extract_first()
        title = li.xpath('./td/a/@title').extract_first()
        fbsj = li.xpath('./td[2]/a/text()').extract_first().strip().replace('[', '').replace(']', '')
        par = [url]
        conn.ping(reconnect=True)
        cursor.execute(sql, [par])
        cont_id = cursor.fetchone()
        if not cont_id:
            rtn_data['requests'].append({
                'url': url,
                'meta': {
                    'title': title,
                    'fbsj': fbsj
                }
            })
    page = int(response.url.split('pageNum=')[1].split('&')[0])
    maxpages = response.xpath('//div[@class="pg"]/ul/li[last()-1]//text()').extract_first()
    maxpage = int(re.findall(r'共(.*?)页', maxpages)[0].strip().split(' ')[-1])
    qstime = response.url.split('pubDateStart=')[1].split('&')[0]
    if page < maxpage:
        url = 'http://www.ccgp-anhui.gov.cn/cmsNewsController/getCgggNewsList.do?pageNum=' + str(
            page + 1) + '&numPerPage=20&pubDateStart=' + qstime + '&channelCode=cggg'
        rtn_data['requests'].append({
            'url': url
        })
    cursor.close()
    conn.close()
    return rtn_data
