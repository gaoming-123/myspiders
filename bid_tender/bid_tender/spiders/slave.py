from gevent import monkey
monkey.patch_all()  # 猴子补丁
import os
import datetime

import re
import json

import scrapy
from scrapy import Request, FormRequest
from scrapy_redis.spiders import RedisSpider

from bid_tender import settings
from bid_tender.myhandlers import *
from bid_tender.myitems import *



from bid_tender.provinces import *

PROVINCES_DIR_LIST=[]

def get_all_rules():
    """获取全部的rules规则"""
    all_rules = []
    # province_rules = []
    province_dir = os.path.join(settings.PRO_BASE_PATH, 'bid_tender', 'provinces')
    dir_list = os.listdir(province_dir)
    for dir_name in dir_list:
        if os.path.isdir(os.path.join(province_dir, dir_name)):
            # 不导入模板文件的rules
            if dir_name=='base':
                continue
            # 排除__pycache__文件夹
            if not dir_name.startswith('_'):
                PROVINCES_DIR_LIST.append(dir_name)
                dir_name = f'{dir_name}.{dir_name}_rules'
                all_rules += eval(dir_name)
    return all_rules


provinces_rules = get_all_rules()
print(PROVINCES_DIR_LIST)
all_rules=settings.rules
all_rules.extend(provinces_rules)
# print(all_rules)

# provinces文件下有的省份，但是在旧框架下运行的handler方法列表
tj_cgw_handler=[
                # 天津采购网
                'tj_cgw_area_url_list',
                'tj_cgw_city_url_list',
                'tj_contract_cgw_detail',
                'tj_corrections_cgw_detail',
                'tj_demand_cgw_detail',
                'tj_purchase_cgw_detail',
                'tj_result_cgw_detail',
                'tj_source_cgw_detail',
                # 山东采购网
                'sd_cgw_detail',
                'sd_cgw_url',]

class NoproxySpider(RedisSpider):
    """Spider that reads urls from redis queue (bid_tender:start_urls)."""
    name = 'bid_tender'
    redis_key = 'bid_tender:start_urls'

    # allowed_domains = ['cnblogs.com']

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(NoproxySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        self.logger.info('parse start with url: ' + response.url)
        start = datetime.datetime.now()
        found_rule = False
        use_js = False
        for rule in all_rules:
            # print(rule)
            pattern = re.compile(rule['re'])
            ret = re.search(pattern, response.url)
            # print(rule['re'], response.url, ret)
            if (ret):
                found_rule = True
                use_js = rule['use_js']
                # print(rule['func'])
                break
        if found_rule:
            # 按配置做解析动作
            self.logger.info("start handle data for url: " + response.url)
            province_status = False
            if rule['func'] in tj_cgw_handler:
                data = eval(rule['func'] + '.' + rule['func'] + '(response)')
            else:
                province = rule['func'].split('_')[0]

                if province in PROVINCES_DIR_LIST:  # 添加在provinces文件下的省文件名
                    province_status=True
                    data = eval(province + '.' + rule['func'] + '(response)')
                else:
                    data = eval(rule['func'] + '.' + rule['func'] + '(response)')

            # data = eval(rule['func'] + '.' + rule['func'] + '(response)')
            # print(data)
            self.logger.info("handled data for url: " + response.url)
            self.logger.info("return data: " + str(data))
            # print(str(data))
            self.logger.info("start yield requests: " + response.url)
            if 'requests' in data:
                for url in data['requests']:
                    if use_js:
                        yield Request(
                            url=url['url'],
                            dont_filter=True,
                            headers=url.get('hd', '') if url.get('hd', '') else {},
                            meta={'PhantomJS': url['PhantomJS']}
                        )
                    else:
                        yield Request(
                            url=url['url'],
                            dont_filter=True,
                            headers=url.get('hd', '') if url.get('hd', '') else {},
                            meta={'meta': url.get('meta', '')} if url.get('meta', '') else {}
                        )
            # print('meta = ', response.meta)
            self.logger.info("end yield requests: " + response.url)
            self.logger.info("start yield form requests: " + response.url)
            if 'form_requests' in data:
                for post in data['form_requests']:
                    yield FormRequest(
                        url=post['url'],
                        # headers=post.get('meta', ''),
                        formdata=post['post_params'],
                        headers=post.get('hd', '') if post.get('hd', '') else {},
                        meta={'post_params': post['post_params'], 'meta': post.get('meta', '')},
                        dont_filter=True
                    )
            self.logger.info("end yield form requests: " + response.url)
            self.logger.info("start yield items: " + response.url)
            if 'json_requests' in data:
                for post in data['json_requests']:
                    hd = {
                        'Content-Type': 'application/json;charset=UTF-8',
                    }
                    yield FormRequest(
                        url=post['url'],
                        method="POST",
                        body=json.dumps(post['post_params']),
                        headers=hd,
                        meta={'post_params': post['post_params']},
                        dont_filter=True
                    )
            self.logger.info("end yield json requests: " + response.url)
            self.logger.info("start yield items: " + response.url)
            if ('items' in data):
                for tmp_items in data['items']:
                    # print(tmp_items)
                    if province_status:
                        for tmp_item in tmp_items['data']:
                            # for item_key in tmp_item:
                            #     item[item_key] = tmp_item[item_key]
                            item = tmp_item
                            if ('item_cfg' in tmp_items):
                                item['pipeline_func'] = province + '.' + tmp_items['item_cfg'].replace('handler','pipeline')
                            else:
                                item['pipeline_func'] = province + '.' + rule['func'].replace('handler', 'pipeline')

                            yield item
                    else:
                        if ('item_cfg' in tmp_items):
                            item = eval(tmp_items['item_cfg'] + '_item.' + tmp_items['item_cfg'] + '_item()')
                        else:
                            item = eval(rule['func'] + '_item.' + rule['func'] + '_item()')
                        for tmp_item in tmp_items['data']:
                            for item_key in tmp_item:
                                item[item_key] = tmp_item[item_key]
                                if ('item_cfg' in tmp_items):
                                    item['pipline_func'] = tmp_items['item_cfg'] + '_pipline.' + tmp_items[
                                        'item_cfg'] + '_pipline'
                                else:
                                    item['pipline_func'] = rule['func'] + '_pipline.' + rule['func'] + '_pipline'
                            # print(item)
                            yield item
            self.logger.info("end yield items for url: " + response.url)
        else:
            self.logger.warning('no rule matched for url: ' + response.url)
        end = datetime.datetime.now()
        self.logger.info("parse end for url: " + response.url + ', cost ' + str((end - start).seconds) + ' seconds')
