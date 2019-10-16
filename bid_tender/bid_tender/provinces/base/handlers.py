
# 此处列出可以被访问的方法，以省缩写开头，必须以_handler结尾
__all__=['base_jy_list_handler','base_jy_detail_handler','base_cg_list_handler','base_cg_detail_handler']
from .task_schedule import base_task_config, base_FIRST_CRAWL,province_name
from .utils import get_page_no
from bid_tender.common.utils import get_real_url_and_notice_id, make_rtn_data, get_selector_content, compare_date
from bid_tender.common.pur_name import PurName


def base_jy_list_handler(response):
    #get请求列表
    request_list = []
    #返回数据
    rtn_data = {}
    # 列表页的内容提取
    content_list = response.xpath("//tr[@height]")
    # print(content_list)
    now_url = response.url
    # 获取页码
    now_page, max_page = get_page_no(response)
    #读取配置参数
    day_max_page = bt_task_config['jy_list_parse'].get('page')
    day_period = bt_task_config['jy_list_parse'].get('period')
    # 全量与每日任务 控制逻辑
    control_page = max_page
    if day_max_page:
        control_page = day_max_page
    if bt_FIRST_CRAWL:
        control_page = max_page

    if now_page < control_page:
        next_page = now_page + 1
        next_page_url = now_url.replace(f'={now_page}', f'={next_page}')
        # 下一页请求
        request = {
            'url': next_page_url
        }
        request_list.append(request)
    #列表页的详情链接，及每项内容的一些内容传递
    base_url = 'http://ggzy.xjbt.gov.cn'
    for content in content_list:
        content_url = content.xpath(".//a/@href").extract_first()
        content_url = base_url + content_url
        xmsd = content.xpath(".//a/font/text()").extract_first()
        title = content.xpath(".//a/text()").extract_first()
        if xmsd:
            xmsd = xmsd.strip().replace('[', '').replace(']', '')
        else:
            xmsd = ''
        publish = content.xpath("./td[3]/text()").extract_first()
        publish = publish.strip().replace('[', '').replace(']', '')
        pattern = r'/(\d+)/(\d+)/'
        key1, key2 = re.findall(pattern, now_url)[0]
        item = {}
        # 项目归属地
        item['xmsd'] = xmsd

        # 发布时间
        item['fbsj'] = publish
        # 业务类型
        item['ywlx'] = jy_category_dict.get(key1)
        # 信息类型
        item['xxlx'] = jy_category_dict.get(key2)

        content_request = {
            'url': content_url,
            'meta': item
        }
        # print(content_request)
        # 详情url的控制逻辑
        if not bt_FIRST_CRAWL:
            if day_period:
                if compare_date(item['fbsj'], day_period):
                    request_list.append(content_request)
        else:
            request_list.append(content_request)
    # 返回数据   也可以调用make_rtn_data方法
    rtn_data['requests'] = request_list
    # print(rtn_data)
    return rtn_data



def base_jy_detail_handler(response):
    pass


def base_cg_list_handler(response):
    pass


def base_cg_detail_handler(response):
    pass
