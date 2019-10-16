# encoding: utf-8
# author:  gao-ming
# time:  2019/7/23--18:15
# desc:
import datetime
import json
import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import logging

if not os.path.exists('log.txt'):
    try:
        file = open('log.txt', 'w')
        file.close()
    except:
        pass

logging.basicConfig(filename='log.txt', filemode="a+",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

logger = logging.getLogger('HaiDai')

email = ['563267935@qq.com']


def start_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def get_cookie(driver, username, pwd):
    url = 'http://hd.ecs8080.com/login'
    driver.get(url)

    zhanghao = driver.find_element_by_xpath('//*[@id="username"]')
    zhanghao.send_keys(username)
    time.sleep(1)

    mima = driver.find_element_by_xpath('//*[@id="password"]')
    mima.send_keys(pwd)
    time.sleep(1)

    deng_lu = driver.find_element_by_xpath('//*[@id="btnLogin"]')
    deng_lu.click()

    cookie = driver.get_cookies()
    driver.delete_all_cookies()
    # print(cookie)
    return cookie[0]


def one_account(username, cookie_value):
    url = 'http://hd.ecs8080.com/channeljson/loan/user/list'
    cookie = {
        'JSESSIONID': cookie_value,
    }
    fang_kuan = []
    pageSize = 10
    page = 1
    while 1:
        data = {
            'pageSize': pageSize,
            'pageNumber': page,
            'sortOrder': 'asc',
        }
        res = requests.post(url, data=data, cookies=cookie)
        # print(res.text)
        res = json.loads(res.text)
        total = res['total']
        # print(total)
        content_list = res['rows']
        with open('haidai.csv', 'a+', encoding='utf-8') as fw:
            for c in content_list:
                # print(content)
                if c['mobile']:
                    text = f"{c['mobile']},{c['realName']},{c['channelName']},{c['status']},{c['createTime'].split(' ')[0]}\n"
                    if c['status'] == '已放款':
                        fang_kuan.append(text)
                    else:
                        fw.write(text)
        logger.info('complete %s page %d' % (username, page))
        if total - pageSize * page >= pageSize:
            page += 1
            time.sleep(0.1)
            # print(total,page)
        else:
            break
    with  open('fangkuan.csv', 'a+', encoding='utf-8') as ff:
        ff.write(fang_kuan)
    # print(content['mobile'],content['realName'],content['channelName'],content['status'])


def send_res_to_email(to_addr: list, theme='hello', contents='请接收附件！', content_type='plain', files=None):
    """
    :param to_addr: 目标邮件
    :param theme: 主题
    :param contents: 正文内容
    :param content_type: 内容格式 txt形式：plain , html格式：html
    :param files: :附件 {'file_path':['file_name',]}多个
    :return:
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication

    from_addr = 'gaomingjiang123@sina.com'  # 用来发送邮件的邮箱地址
    password = 'gaomingjiang'  # 邮箱密码或者是授权密码
    # 目标邮箱地址
    smtp_server = 'smtp.sina.com'  # 这里是新浪的SMTP服务器地址
    # 发送的信息格式
    content = MIMEText(contents, content_type, 'utf-8')
    msg = MIMEMultipart()
    msg['From'] = Header(from_addr)  # 定义发件人
    msg['Subject'] = Header(theme, 'utf-8')  # 定义邮件名
    msg.attach(content)  # 加上邮件的内容

    if not files:
        for (f_path, f_name) in files.items():
            if isinstance(f_name, list):
                for f_name_l in f_name:
                    part = MIMEApplication(open('%s/%s' % (f_path, f_name_l), 'rb').read())
                    part.add_header('Content-Disposition', 'attachment', filename=f_name_l)
                    msg.attach(part)
            else:
                part = MIMEApplication(open('%s/%s' % (f_path, f_name), 'rb').read())
                part.add_header('Content-Disposition', 'attachment', filename=f_name)
                msg.attach(part)

    try:
        server = smtplib.SMTP()
        server.connect(smtp_server, 25)  # 连接SMTP服务器
        # server.set_debuglevel(1)  # 打印调试信息
        server.login(from_addr, password)  # 登陆邮箱
        server.sendmail(from_addr, to_addr, msg.as_string())  # 发送邮件
        print("Send successfully!")
    except smtplib.SMTPException as e:
        server.quit()  # 退出


if __name__ == '__main__':
    try:
        os.remove('haidai.csv')
        os.remove('fangkuan.csv')
    except Exception as FileNotFoundError:
        pass
    username_pwd = {
        '武汉饼王': 123456,
        '阿栋短信1': 123456,
        '阿栋短信2': 123456,
        '阿栋短信3': 123456,
        '阿栋短信4': 123456,
    }
    driver = start_driver()

    for k, v in username_pwd.items():
        complete_cookie = get_cookie(driver, k, v)
        cookie_value = complete_cookie.get('value')
        one_account(k, cookie_value)
        # print(cookie_value)

    driver.close()

    today = str(datetime.date.today())
    send_res_to_email(email, theme=f'{today}结果', files={'./': ['haidai.csv', 'fangkuan.csv']})
