import os
import random
import hashlib
import requests

# from bid_tender.common.download import thread_download
from bid_tender.config.download import thread_download
from ..settings import BASE_PATH

from Crypto.Cipher import AES
import base64
import logging
import datetime
import re
import time

FILE_END = ['doc', 'zip', 'pdf', 'docx', 'xls', 'rar', 'jpg']


# 加密部分代码
def _add_to_16(s):
    while len(s) % 16 != 0:
        s += (16 - len(s) % 16) * chr(16 - len(s) % 16)
    return str.encode(s)  # 返回bytes


# 加密部分代码
def _get_secret_url(text, key='qnbyzzwmdgghmcnm'):
    aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器，本例采用ECB加密模式
    encrypted_text = str(base64.encodebytes(aes.encrypt(_add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
    encrypted_text = encrypted_text.replace('/', "^")
    return encrypted_text[:-2]


# 获得真实的url
def get_real_url_and_notice_id(org_url, key):
    aa = org_url.split('/')
    aaa = len(aa)
    bbb = aa[aaa - 1].split('.')
    ccc = bbb[0]
    secret_text = _get_secret_url(ccc, key=key)
    return org_url.replace(ccc, secret_text), ccc


# 获取正文内容
def get_selector_content(selector):
    """传入正文 选择器 """
    content = selector.xpath('string(.)').extract_first().replace('\n', '').replace(
        '\r', '').replace('\t', '').replace('&nbsp', '').replace('：', ':').replace('，', ',').strip()
    html = re.sub(r'\s+', '', content)
    x = re.compile(r'<[^>]+>', re.S)
    content = x.sub('', html)  # 正文内容
    return content


# def get_content_xpath()

# 较早版本的 业主获取  pur_name
def get_pur_name(response, content_pattern):
    """
    :param response: 响应
    :param content_pattern: 正文的正则表达式
    :return:
    """
    pre_replace_words = [',', ' ', '地址', '及电话', '联系', '']
    replace_words = [',', ' ', '地址', '及电话', '联系', '']
    try:
        content = response.xpath(content_pattern).extract_first()
    except:
        content = ''
    x = re.compile(r'<[^>]+>', re.S)
    try:
        txt = x.sub('', content).replace('：', ':').replace('，', ',').replace('。', ',').replace(' ', '')
    except:
        txt = content
    try:
        txt = txt.strip()
    except:
        txt = ''
    try:
        xmyz = re.search(
            '招标人:(.*?)公司|招标人名称:(.*?)公司|招标人:(.*?)中心|招标人:(.*?)政府|招 标 人:(.*?)中心|招 标 人:(.*?)政府|采购人名称:(.*?)中心|采购人名称:(.*?)政府|招标人:(.*?)小组|采购人:(.*?)院|采购人名称:(.*?)院|采购人名称:(.*?)电视台|采购人名称:(.*?)学|采购人名称:(.*?)宣传部|招标人:(.*?)管理局|采购人名称:(.*?)局|采购人名称:(.*?)委员会|采购人名称:(.*?)会|招标人:(.*?)局|招标人:(.*?)办事处|招 标 人:(.*?)公司|采购人名称:(.*?)公司',
            txt, re.S).group(0).split(':')[1].replace('开标时间', '').replace('联系人', '').replace('联系电话', '').replace('地址',
                                                                                                                 '').replace(
            '招标代理机构', '').strip()
    except:
        xmyz = ''
    if xmyz == '':
        try:
            xmyz = re.search(
                '招标人（项目业主）为(.*?)(?=建设资金)|招标人为(.*?)(?=建设资金)|招标人（项目业主）为(.*?)(?=,)|招标人为(.*?)(?=,)|招标人（项目业主）为(.*?)公司|招标人为(.*?)公司|项目业主为(.*?)(?=,)',
                txt, re.S).group(0).strip().split('为')[1].replace('.', '').replace('_', '').strip()
        except:
            xmyz = ''
    try:
        xmbh = re.search('项目编号:(.*?)\n', txt, re.S).group(0).split(':')[1].strip()
    except:
        xmbh = ''

    return xmyz, xmbh


# 通过后缀来区分附件
def is_have_attach_by_filename(response, province):
    """
    :param response:  响应
    :param province:  省份(的保存文件名)
    :return:
    """
    base_url = '/'.join(response.url.split('/')[0:3])
    a_list = response.xpath('//a')
    # print(a_list)
    attach_path = os.path.join(BASE_PATH, 'attachments', province)
    if not os.path.exists(attach_path):  # 路径是否存在, 不存在就创建
        os.makedirs(attach_path)
    # print(attach_path)
    file = '0'
    attach_url_list, attach_id_list, attach_location_list = [], [], []
    for a in a_list:
        # print(a)
        texts = a.xpath('string(.)').extract()
        a_text = ''.join([t.strip() for t in texts])
        # print(a_text)
        a_href = a.xpath('./@href').extract_first()
        if a_text and ('.' in a_text):
            try:
                file_ = a_text.split('.')[-1]
                if file_.lower() in FILE_END:
                    file = '1'
                    # 附件原地址 用于附件表中的  fj_link
                    if a_href.startswith('http'):
                        fj_link = a_href
                    elif a_href.startswith('./'):
                        fj_link = base_url + a_href.replace('./', '/')
                    else:
                        fj_link = base_url + a_href
                    attach_url_list.append(fj_link)
                    # 用于附件表的   fj_name
                    fj_name = hashlib.md5()
                    fj_name.update(a_href.split('/')[-1].encode('utf-8'))
                    fj_name = fj_name.hexdigest()
                    # print(fj_name)
                    # 用于附件本地保存地址  fj_location
                    save_name = fj_name + '.' + file_.lower()
                    # print(save_name)
                    attach_id_list.append(save_name)
                    fj_location = os.path.join(attach_path, save_name)
                    attach_location_list.append(fj_location)
                    thread_download(a_href, fj_location)
            except:
                pass
    return file, attach_url_list, attach_id_list, attach_location_list


# 通过链接来区分附件
def is_have_attach_by_href(response, province, key_word='download'):
    """
    :param response:  响应
    :param province:  省份(的保存文件名)
    :param key_word:  在url中的特殊字符串，用于区分是否为下载链接
    :return:
    """
    base_url = '/'.join(response.url.split('/')[0:3])
    a_list = response.xpath('//a')
    # print(a_list)
    attach_path = os.path.join(BASE_PATH, 'attachments', province)
    if not os.path.exists(attach_path):  # 路径是否存在, 不存在就创建
        os.makedirs(attach_path)
    file = '0'
    attach_url_list, attach_id_list, attach_location_list = [], [], []
    for a in a_list:
        # print(a)
        texts = a.xpath('string(.)').extract()
        a_text = ''.join([t.strip() for t in texts])
        # print(a_text)
        a_href = a.xpath('./@href').extract_first()
        if key_word in a_href.lower():
            try:
                file = '1'
                # 附件原地址 用于附件表中的  fj_link
                if a_href.startswith('http'):
                    fj_link = a_href
                else:
                    fj_link = base_url + a_href
                attach_url_list.append(fj_link)
                # 用于附件表的   fj_name
                fj_name = hashlib.md5()
                fj_name.update(a_href.split('/')[-1].encode('utf-8'))
                fj_name = fj_name.hexdigest()
                file_ = a_text.split('.')[-1]
                # 用于附件本地保存地址  fj_location
                save_name = fj_name + '.' + file_.lower()
                attach_id_list.append(save_name)
                fj_location = os.path.join(attach_path, save_name)
                attach_location_list.append(fj_location)
                # thread_download(a_href, fj_location)
            except:
                pass
    return file, attach_url_list, attach_id_list, attach_location_list


# 构造返回值
def make_rtn_data(data: list = None, requests: list = None, form_requests: list = None, json_requests: list = None,
                  item_cfg=None):
    """
    requests:list example:
        [{
            'url':url,   地址链接
            'meta':meta, #需要传递的参数
            }]
    form_requests:
        [{
        'url':url,   地址链接
        'post_params':post_params,# 请求参数
        'meta':meta  #需要传递的参数
            }]
    json_requests：
        [{
        'url':url,   地址链接
        'post_params':post_params,# 请求参数
            }]
    items:
        [{
            'item_cfg':'',   # 单独配置item类
            'data':[
                        {
                            'item_cfg':'', # 单独配置pipeline类
                            'k':'v'  # 要返回的数据字典
                        }
                    ],
        }]
    params data:传入的为单一条数据
    :return: 返回的数据值
    """
    rtn_data, item = {}, {}
    if requests:
        rtn_data['requests'] = requests
    if form_requests:
        rtn_data['form_requests'] = form_requests
    if requests:
        rtn_data['json_requests'] = json_requests
    # 单独配置item类
    if item_cfg:
        item['item_cfg'] = item_cfg
    if data:
        item['data'] = data
        rtn_data['items'] = [item]
    return rtn_data

# 获取user_agent
def get_user_agent():
    user_agent_list = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]

    return random.choice(user_agent_list)


def get_local_proxy():
    return requests.get("http://127.0.0.1:5010/get/")


# 比较日期 返回真假
def compare_date(date_str, period):
    """公告日期与采集起始日期比较，大于将返回True"""
    # 输入格式为'%Y-%m-%d'
    publish_time = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    before_time = datetime.datetime.strptime(now_time, '%Y-%m-%d') - datetime.timedelta(days=period)
    # print(before_time)
    return publish_time > before_time


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


# 获取页码
def get_page_no(response):
    now_page_text = response.xpath("//a[contains(text(),'条记录')]/text()").extract_first()
    page = re.findall('共\d+条记录(.*?)/(\d+)页', now_page_text)[0]
    now_page = int(page[0].strip())
    max_page = int(page[1])
    return now_page, max_page
