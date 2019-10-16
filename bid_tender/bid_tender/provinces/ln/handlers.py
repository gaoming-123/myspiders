# 此处列出可以被访问的方法，以省缩写开头，必须以_handler结尾
__all__ = ['ln_jy_list_handler', 'ln_jy_detail_handler', 'ln_cg_list_handler', 'ln_cg_detail_handler']
import json
import re

from .task_schedule import ln_task_config, ln_FIRST_CRAWL, province_name
from .utils import get_page_no, compare_date
from bid_tender.common.utils import make_rtn_data, get_selector_content, is_have_attach_by_filename
from bid_tender.common.pur_name import PurName

jy_cate_dict = {
    '政府采购': 'Zfcg',
    '建设工程': 'Jsgc',
    '国有产权': 'Cqjy',
    '土地/矿产权': 'Tdjy',
    '医疗器械': '',
    '其他': '',
}

cg_cate_dict = {
    '1001': '采购公告',
    '1008': '单一来源公告',
    '1002': '结果公告',
    '1007': '采购文件公示',
    '1003': '更正公告',
}


def ln_jy_list_handler(response):
    try:
        cookie=response.headers.getlist('Set-Cookie')[0]
        for x in cookie.split(';'):
            if 'ASP' in x:
                cookie=x
    except:
        cookie = response.headers.getlist('Cookie')
    # print(set_cookie)
    # print(cookie)
    request_list = []
    form_request_list = []
    rtn_data = {}
    content_list = response.xpath("//tr[@valign='top']")
    over_period=False
    # print(content_list)
    now_page, max_page = get_page_no(response)
    # print('start_page,max_page',now_page,max_page)
    # print(f'取出页码{start_page}，{max_page}')
    # if start_page == max_page == 1:
    #     max_page = 5
    # day_max_page = ln_task_config['jy_list_parse'].get('page')
    day_period = ln_task_config['jy_list_parse'].get('period')

    # control_page = max_page
    # if day_max_page:
    #     control_page = day_max_page
    # if ln_FIRST_CRAWL:
    #     control_page = max_page
    # print(control_page)

        # print(f'meta中的page{now_page}')


    base_url = 'http://www.lnggzy.gov.cn'
    # print(base_url)
    for content in content_list:
        # print(content_url)
        xmsd = content.xpath(".//p/span[2]/text()").extract_first()
        ywlx = content.xpath(".//p/span[4]/text()").extract_first()
        xxlx = content.xpath(".//p/span[6]/text()").extract_first()
        title = content.xpath(".//a/text()").extract_first()
        content_url = content.xpath(".//a/@href").extract_first()
        content_url = content_url.replace('InfoDetail', 'ZtbInfo')
        content_url = content_url.replace('Default', jy_cate_dict.get(ywlx))
        content_url = base_url + content_url
        # print(title)
        if xmsd:
            xmsd = xmsd.strip()
        else:
            xmsd = ''
        publish = content.xpath(".//span/text()").extract_first()
        publish = publish.strip()
        item = {}
        # 项目归属地
        item['xmsd'] = xmsd
        # 标题
        item['title'] = title
        # 发布时间
        item['fbsj'] = publish
        # 业务类型
        item['ywlx'] = ywlx
        # 信息类型
        item['xxlx'] = xxlx

        content_request = {
            'url': content_url,
            'meta': item
        }
        # print(content_request)
        if not ln_FIRST_CRAWL:
            if day_period:
                if compare_date(item['fbsj'], day_period):
                    request_list.append(content_request)
                else:
                    over_period=True
        else:
            request_list.append(content_request)

    if not over_period:
        next_page = now_page + 1
        # print('now_page,next_page',now_page,next_page)

        __VIEWSTATE=response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
        __VIEWSTATEGENERATOR=response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        # print(__VIEWSTATEGENERATOR)
        # print('请求中的参数',next_page)
        form_request = {
            'url': response.url.split('&word=')[0],
            # 请求参数
            'post_params': {
                '__VIEWSTATE':__VIEWSTATE,
                '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
                '__EVENTTARGET': 'MoreInfoListjyxx1$Pager',
                '__EVENTARGUMENT': f'{next_page}',
                '__VIEWSTATEENCRYPTED':'',
                'MoreInfoListjyxx1$Pager_input':f'{now_page}',
            },
            'hd':{
                'Cookie':cookie,
            },
            # 'meta':meta  #需要传递的参数
        }
        # print(form_request)
        form_request_list.append(form_request)
    rtn_data['form_requests'] = form_request_list
    rtn_data['requests'] = request_list

    return rtn_data


def ln_jy_detail_handler(response):
    # 正文选择器
    content_selector = response.xpath("//div[@class='ewb-clearfix']")[0]
    # print(content_selector.xpath('string(.)').extract_first())
    content = content_selector.extract().strip()
    # content='test_wrong'
    has_attach, attach_url_list, attach_id_list, attach_location_list = is_have_attach_by_filename(response,
                                                                                                   province_name)
    # pur_name,info_id=get_pur_name(response,"//div[@class='content']")
    # print('==========================以前的 pur_name',pur_name)
    purName = PurName(response, pattern="//div[@class='ewb-clearfix']")
    pur_name = purName.find_pur_name()
    # print('==========================现在的 pur_name', pur_name)
    item = {}
    item['link'] = response.url
    item['pur_name'] = pur_name
    item['sorce_web'] = '辽宁省公共资源交易网'
    item['ly'] = ''
    item['xmbh'] = re.findall('InfoID=(.*?)&', response.url)[0]
    item['content'] = content
    item['has_attach'] = has_attach
    # 用于附件存储时的notice_id
    item['notice_id'] = response.url
    item['attach_url_list'] = attach_url_list
    item['attach_id_list'] = attach_id_list
    item['attach_location_list'] = attach_location_list

    rtn_data = make_rtn_data(data=[
        dict(item, **response.meta['meta'])
    ])
    # print(rtn_data)
    return rtn_data


def ln_cg_list_handler(response):
    rtn_data = {}
    form_request_list = []
    request_list = []
    if response.url == 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=goPubInfoList':
        # 第一次post请求
        for v in cg_cate_dict.keys():
            form_request = {
                'url': 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList&t_k=null',
                # 请求参数
                'post_params': {
                    'current': str(1),
                    'rowCount': str(20),
                    'searchPhrase': '',
                    'infoTypeCode': v,
                },
            }
            form_request_list.append(form_request)
    else:
        json_res = json.loads(response.text)
        total_num = json_res.get('total')
        now_page = json_res.get('current')
        rowCount = json_res.get('rowCount')
        day_max_page = ln_task_config['cg_list_parse'].get('page')
        day_period = ln_task_config['cg_list_parse'].get('period')
        post_params = response.meta.get('post_params')
        next_page = None
        if ln_FIRST_CRAWL:
            if rowCount * now_page < total_num:
                next_page = now_page + 1
        else:
            if now_page < day_max_page:
                next_page = now_page + 1
        content_list = json_res.get('rows')
        if len(content_list)== 20:
            # 翻页操作
            if next_page:
                post_params['current'] = str(next_page)
                form_request = {
                    'url': 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList&t_k=null',
                    # 请求参数
                    'post_params': post_params,
                }
                # print('第几页：',next_page)
                form_request_list.append(form_request)
        request_list = []
        ywlx = post_params.get('infoTypeCode')
        base_url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpen&infoId='
        for content in content_list:
            content_url = base_url + content['id']
            item = {}
            # 项目归属地
            item['xmsd'] = '辽宁省' + content['districtName']
            # 标题
            item['title'] = content['title']
            # 发布时间
            item['fbsj'] = content['releaseDate']
            # 业务类型
            item['ywlx'] = cg_cate_dict.get(ywlx)
            # 信息类型
            item['xxlx'] = content['infoTypeName']
            item['xmbh'] = content['id']
            content_request = {
                'url': content_url,
                'meta': item
            }
            # print(content_request)
            if not ln_FIRST_CRAWL:
                if day_period:
                    if compare_date(item['fbsj'], day_period):
                        request_list.append(content_request)
            else:
                request_list.append(content_request)
    rtn_data['form_requests'] = form_request_list
    rtn_data['requests'] = request_list
    return rtn_data


def ln_cg_detail_handler(response):
    # 正文选择器
    content_selector = response.xpath("//div[contains(@class,'textcenter')]")[0]
    content = content_selector.extract().strip()
    has_attach, attach_url_list, attach_id_list, attach_location_list = is_have_attach_by_filename(response,
                                                                                                   province_name)
    purName = PurName(response, pattern="//div[contains(@class,'textcenter')]")
    pur_name = purName.find_pur_name()
    # print('==========================现在的 pur_name', pur_name)
    item = {}
    item['link'] = response.url
    item['pur_name'] = pur_name
    item['sorce_web'] = '辽宁省政府采购网'
    item['ly'] = ''
    item['content'] = content
    item['has_attach'] = has_attach
    # 用于附件存储时的notice_id
    item['notice_id'] = response.url
    item['attach_url_list'] = attach_url_list
    item['attach_id_list'] = attach_id_list
    item['attach_location_list'] = attach_location_list

    rtn_data = make_rtn_data(data=[
        dict(item, **response.meta['meta'])
    ])
    # print(rtn_data)
    return rtn_data
