# 此处列出可以被访问的方法，以省缩写开头，必须以_handler结尾


__all__ = ['tj_jy_list_handler', 'tj_jy_detail_handler', 'tj_cg_list_handler', 'tj_cg_detail_handler']
from .task_schedule import tj_task_config, tj_FIRST_CRAWL, province_name
from bid_tender.common.utils import get_real_url_and_notice_id, make_rtn_data, get_selector_content, \
    is_have_attach_by_filename, compare_date
from .utils import get_page_no
from bid_tender.common.pur_name import PurName
import re
tj_key = 'qnbyzzwmdgghmcnm'

cg_city_cate_dict = {
    '1662': '采购需求征求意见',
    '1665': '采购公告',
    '1663': '更正公告',
    '2014': '采购结果公告',
    '2015': '合同及验收公告',
    '2033': '单一来源公示',
}
cg_area_cate_dict = {
    '1994': '采购需求征求意见',
    '1664': '采购公告',
    '1666': '更正公告',
    '2013': '采购结果公告',
    '2016': '合同及验收公告',
    '2034': '单一来源公示',
}
cg_site_list_name = {
    '2': '和平区',
    '3': '河东区',
    '4': '河西区',
    '5': '南开区',
    '6': '河北区',
    '7': '红桥区',
    '8': '东丽区',
    '9': '西青区',
    '10': '津南区',
    '11': '北辰区',
    '12': '武清区',
    '13': '宝坻区',
    '14': '宁河区',
    '15': '静海区',
    '16': '蓟州区',
    '17': '滨海新区',
    '18': '开发区',
    '19': '保税区',
    '20': '滨海高新区',
    '21': '中新天津生态城',
    '22': '中心商务区',
    '23': '东疆保税港区',
    '24': '临港经济区',
    '25': '天津海河教育园区',
}


def tj_jy_list_handler(response):
    request_list = []
    rtn_data = {}
    to_next_page = True
    content_list = response.xpath("//ul[@class='article-list2']/li")
    if not content_list:
        to_next_page=False
    now_url = response.url
    now_page, max_page = get_page_no(response)
    day_period = tj_task_config['jy_list_parse'].get('period')
    for content in content_list:
        content_url = content.xpath(".//a/@href").extract_first()
        content_url, notice_id = get_real_url_and_notice_id(content_url, key=tj_key)
        publish = content.xpath(".//div[@class='article-list3-t']/div[@class='list-times']/text()").extract_first()
        item = {}
        item['xmsd'] = "天津市"
        item['notice_id'] = notice_id
        item['fbsj'] = publish.split(' ')[0].strip()
        content_request = {
            'url': content_url,
            'meta': item
        }
        if not tj_FIRST_CRAWL:
            if compare_date(item['fbsj'], day_period):
                request_list.append(content_request)
            else:
                to_next_page=False
        else:
            request_list.append(content_request)
    rtn_data['requests'] = request_list

    if to_next_page:
        if now_page< max_page:
            next_page = now_page + 1
            next_page_url = now_url.replace(f'_{now_page}', f'_{next_page}')
            request = {
                'url': next_page_url
            }
            request_list.append(request)

    # print(rtn_data)
    return rtn_data


def tj_jy_detail_handler(response):
    sitemap = response.xpath("//div[@class='sitemap']/a/text()").extract()
    title = response.xpath("//div[@class='content-title']/text()").extract_first()
    # print(title)
    ywlx = sitemap[-2]
    xxlx = sitemap[-1]
    content_selector = response.xpath("//div[@class='content-article']")[-1]
    org_source = response.xpath("//a[@class='originUrl']/text()").extract_first()
    content = content_selector.extract().strip()
    # content='test_wrong'
    has_attach, attach_url_list, attach_id_list, attach_location_list = is_have_attach_by_filename(response,
                                                                                                   province_name)
    # pur_name,info_id=get_pur_name(response,"//div[@class='content']")
    # print('==========================以前的 pur_name',pur_name)
    purName = PurName(response, pattern="//div[@class='content']")
    pur_name = purName.find_pur_name()

    # print('==========================现在的 pur_name', pur_name)
    item = {}
    item['link'] = response.url
    item['pur_name'] = pur_name
    item['ywlx'] = ywlx
    item['xxlx'] = xxlx
    item['title'] = title
    xmbh = response.url.split('/')[-1]
    item['xmbh'] = xmbh.split('.')[0]
    item['ly'] = org_source.strip()
    item['sorce_web'] = '天津公共资源交易网'
    item['content'] = content
    item['has_attach'] = has_attach
    item['attach_url_list'] = attach_url_list
    item['attach_id_list'] = attach_id_list
    item['attach_location_list'] = attach_location_list

    rtn_data = make_rtn_data(data=[
        dict(item, **response.meta['meta'])
    ])
    return rtn_data


def tj_cg_list_handler(response):
    rtn_data = {}
    form_request_list = []
    request_list = []

    if response.url == 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1':
        for id in cg_city_cate_dict.keys():
            form_request = {
                'url': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do',
                'post_params': {
                    'method': 'view',
                    'page': '1',
                    'id': id,
                    'step': '1',
                    'view': 'Infor',
                    'st': '1', }
            }

            form_request_list.append(form_request)

        for id in cg_area_cate_dict.keys():
            for area_num in cg_site_list_name.keys():
                form_request = {
                    'url': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do',
                    'post_params': {
                        'method': 'find',
                        'id': id,
                        'page': '1',
                        # 'name':'',
                        'view': 'Infor',
                        'siteLists': area_num, }
                }
                form_request_list.append(form_request)
        rtn_data['requests'] = request_list
        rtn_data['form_requests'] = form_request_list
        return rtn_data
    else:
        content_list = response.xpath("//ul[@class='dataList']/li")
        max_page = response.xpath("//span[@class='countPage']/b/text()").extract_first()
        max_page = int(max_page)
        post_params = response.meta['post_params']
        now_page = int(post_params['page'])
        day_max_page = tj_task_config['cg_list_parse'].get('page')
        day_period = tj_task_config['cg_list_parse'].get('period')
        control_page = max_page
        if day_max_page:
            control_page = day_max_page
        if tj_FIRST_CRAWL:
            control_page = max_page

        if now_page < control_page:
            next_page = now_page + 1
            post_params['page'] = str(next_page)
            form_request = {
                'url': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do',
                'post_params': post_params
            }

            form_request_list.append(form_request)
        xmsd = post_params.get('siteLists')

        if xmsd:
            xmsd = cg_site_list_name[xmsd]
        else:
            xmsd = '市级'
        msg_type = post_params.get('id')
        if msg_type in cg_city_cate_dict:
            msg_type = cg_city_cate_dict[msg_type]
        else:
            msg_type = cg_area_cate_dict[msg_type]
        base_url = 'http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&'
        for content in content_list:
            sec_url = content.xpath('./a/@href').extract_first()
            content_url = base_url + sec_url.split('?')[-1]
            title = content.xpath('./a/text()').extract_first()
            fbsj = content.xpath('./span/text()').extract_first().strip()
            item = {}
            # 项目归属地f
            item['xmsd'] = f'天津市{xmsd}'
            # 标题
            item['title'] = title
            # 发布时间
            item['fbsj'] = fbsj
            # 业务类型
            item['ywlx'] = '采购信息'
            # 信息类型
            item['xxlx'] = msg_type
            content_request = {
                'url': content_url,
                'meta': item
            }
            if not tj_FIRST_CRAWL:
                if day_period:
                    if compare_date(item['fbsj'], day_period):
                        request_list.append(content_request)
            else:
                request_list.append(content_request)

        rtn_data['requests'] = request_list
        rtn_data['form_requests'] = form_request_list
        # print(rtn_data)
        return rtn_data


def tj_cg_detail_handler(response):
    content_selector = response.xpath("//div[@id='pageContent']")
    content = content_selector.extract().strip()
    has_attach, attach_url_list, attach_id_list, attach_location_list = is_have_attach_by_filename(response,
                                                                                                   province_name)
    purName = PurName(response, pattern="//div[@id='pageContent']")
    pur_name = purName.find_pur_name()
    xmbh = re.findall(r'id=(.*?)&ver', response.url)[0]
    # print('==========================现在的 pur_name', pur_name)
    item = {}
    item['link'] = response.url
    item['pur_name'] = pur_name
    item['sorce_web'] = '天津市政府采购网'
    item['ly'] = ''
    item['xmbh'] = xmbh
    item['content'] = content
    item['has_attach'] = has_attach
    item['attach_url_list'] = attach_url_list
    item['attach_id_list'] = attach_id_list
    item['attach_location_list'] = attach_location_list
    rtn_data = make_rtn_data(data=[
        dict(item, **response.meta['meta'])
    ])
    return rtn_data



