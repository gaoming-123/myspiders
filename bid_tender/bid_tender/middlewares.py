import os

import time
from random import random
import random
import re
import json
from urllib.parse import urlparse

from fake_useragent import UserAgent
from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
from selenium.webdriver import DesiredCapabilities
from lxml import etree
from twisted.internet.error import TCPTimedOutError

from .settings import USER_AGENT
import requests
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.http import HtmlResponse
from selenium import webdriver
from w3lib.html import remove_tags, replace_escape_chars


class NoProxyMiddware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PhantomJSMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        # 四川交易网链接
        pat1 = 'http://ggzyjy.sc.gov.cn/(.*?)'
        sc = re.match(pat1, request.url)
        # 重庆交易网链接
        pat1 = 'https://www.cqggzy.com/(.*?)'
        cq = re.match(pat1, request.url)
        if cq is None and sc is None:
            if 'PhantomJS' in request.meta:
                webpath = os.path.abspath(os.path.dirname(__file__))
                # exepath = os.path.join(webpath, 'phantomjs')
                exepath = os.path.join(webpath, 'phantomjs.exe')
                driver = webdriver.PhantomJS(executable_path=exepath)
                driver.get(request.url)
                time.sleep(random() * 5)
                driver.set_page_load_timeout(5)
                driver.set_script_timeout(5)
                content = driver.page_source
                driver.quit()
                return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        elif cq is not None:
            request.headers['user-agent'] = USER_AGENT

class JSPageMiddleware(object):
    # 请求动态网页
    def process_request(self, request, spider):
        hd = {
            'Connection': 'keep-alive',
            'Host': 'ggzyjy.sc.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2854.400'
        }
        try:
            if self.check_pat(request.url):
                i = 0
                while True:
                    urll = 'http://ggzyjy.sc.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
                    try:
                        if request.url == urll or request.url == urll + '?1':
                            brower = requests.post(url=request.url, headers=hd, data=request.body, timeout=10)
                            break
                        else:
                            brower = requests.get(request.url, timeout=10)
                            break
                    except Exception as e:
                        print(e)
                        i = i + 1
                        if i >= 5:
                            print('失效链接:' + request.url)
                            break
                        print('访问失败重试:' + request.url)
                        pass
                input_source = brower.text
                return HtmlResponse(url=request.url, body=input_source, encoding="utf-8", request=request)
        except:
            url = request.url
            return HtmlResponse(url=url, encoding="utf-8", request=request)

    def check_pat(self, url):
        pat1 = 'http://ggzyjy.sc.gov.cn/jyxx/.*?|http://ggzyjy.sc.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData.*?'
        s1 = re.match(pat1, url)
        if s1 is None:
            return False
        else:
            return True

    def get_title(self, html):
        html = etree.HTML(html)
        i = 1
        titles = set()
        while True:
            try:
                title = html.xpath('//ul[@class="listDmn"]/following-sibling::div[' + str(i) + ']/div/text()')[0]
                titles.add(self.strip_all(str(title)))
                i = i + 1
            except Exception:
                break
        return list(titles)

    def strip_all(self, value):
        # 去除空格和标签,换行符
        try:
            value = remove_tags(value)
            value = replace_escape_chars(value)
        finally:
            value = value.strip()
        return value


class RandomUserAgent(object):
    """
    随机user-agent中间件
    @author: bob.liu
    """

    def process_request(self, request, spider):
        """
        发送请求前会调用此方法
        :param request: 请求对象
        :param spider: 爬虫对象
        :return:
        """
        from scrapy.utils.project import get_project_settings as param
        request.headers["User-Agent"] = random.choice(
            param().get("USER_AGENT_LIST", ["Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"]))
        # print(u'发送请求前, 使用user-agent: %s' % request.headers)
        # spider.logger.info(u'发送请求前, 使用user-agent: %s' % request.headers)


import base64
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import time


class BidTenderRetryMiddleware(RetryMiddleware):
    """
    如果是贵州的域名报错了进来的, 在用代理去重试请求
    """
    def __init__(self, settings):
        super(BidTenderRetryMiddleware, self).__init__(settings)
        self.retry_http_use_proxy = dict(settings.get('RETRY_HTTP_USE_PROXY', {}))
        self.retry_exception_use_proxy = dict(settings.get('RETRY_EXCEPTION_USE_PROXY', {}))
        self.dont_retry = dict(settings.get('DONT_RETRY', {}))
        # print('************', self.retry_http_use_proxy)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response

        domain_name = urlparse(request.url).netloc  # 获取url中的域名

        # 配置了不重试的域名及状态码
        dont_retry_codes = self.dont_retry.get(domain_name, ())
        if dont_retry_codes and (response.status in set(int(x) for x in dont_retry_codes)):
            return response

        if response.status in self.retry_http_codes:
            # 需要加代理重试的
            use_proxy_code = self.retry_http_use_proxy.get(domain_name, ())
            if use_proxy_code and (response.status in set(int(x) for x in use_proxy_code)):
                _add_proxy(request)

            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    # 异常情况需要加代理重试的
    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):

            # 需要加代理重试的
            domain_name = urlparse(request.url).netloc  # 获取url中的域名
            use_proxy_exception = self.retry_exception_use_proxy.get(domain_name, ())
            if use_proxy_exception and isinstance(exception, use_proxy_exception):
                _add_proxy(request)

            return self._retry(request, exception, spider)

# def get_proxy():
#     return requests.get("http://127.0.0.1:5010/get/")


# class ProxyMiddleware(object):
#     def precess_request(self, request, spider):
#         # print(request.url)
#         # print(get_proxy())
#         request.meta['proxy'] = 'http://'+get_proxy()


def _add_proxy(request):
    """
    给请求加代理, 阿布云ip代理配置，包括账号密码
    :param request: 请求对象
    :return: None
    """
    proxy_user = "*"
    proxy_pass = "*"

    request.meta["proxy"] = "http://http-dyn.abuyun.com:9020"
    request.headers["Proxy-Authorization"] = "Basic " + base64.urlsafe_b64encode(
        bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")
