# 该模块用于处理log日志，将日志处理为每个人的错误归类，并将文本发送给开发人员，进行错误修改或检查
# 将该文件放入项目日志文件夹内 运行  或者自定义日志文件目录
import re
import datetime
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# ============================配置区==============================
# 开发人员的邮箱及任务分配
TASK_DICT_LIST = {
    # '名字': ['email', '网址', '网址2', ],
    'lzk':['**@qq.com',
           'http://www.jl.gov.cn','http://www.ccgp-jilin.gov.cn',
           ],
}
# 日志文件所在路径，如果为空，将会读取当前文件夹作为日志文件路径
LOG_DIR = ''

# 邮箱相关配置
FROM_ADDRESS = ''  # 公司邮箱  用来发送邮件的邮箱地址
PASSWORD = ''  # 邮箱密码或者是授权密码
SMTP_SERVER = ''  # 这里是SMTP服务器地址   例如：'smtp.sina.com'
# ===========================配置区========================


# 可自定义日志文件目录

if not LOG_DIR:
    LOG_DIR = os.path.dirname(os.path.abspath(__file__))

today = datetime.datetime.now().strftime('%Y-%m-%d')
today = today.replace('-', '')
today_file = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
today_file = today_file.replace('-', '')
# 建立错误字典，与任务人数相同数量的错误收集列表
errors_dict = {}
for k in TASK_DICT_LIST.keys():
    errors_dict.setdefault(k, [])
log_msg = []
pur_name_list=[]

def send_res_to_email(to_addr, file, theme='每日错误报告', contents='每日错误报告', content_type='plain'):
    from_addr = FROM_ADDRESS  # 用来发送邮件的邮箱地址
    password = PASSWORD  # 邮箱密码或者是授权密码
    # 目标邮箱地址
    smtp_server = SMTP_SERVER  # 这里是新浪的SMTP服务器地址
    # 发送的信息格式
    content = MIMEText(contents, content_type, 'utf-8')
    msg = MIMEMultipart()
    msg['From'] = Header(from_addr)  # 定义发件人
    msg['Subject'] = Header(theme, 'utf-8')  # 定义邮件名
    msg.attach(content)  # 加上邮件的内容
    # 构建邮件附件
    part_attach1 = MIMEApplication(open(file, 'rb').read())  # 打开附件
    part_attach1.add_header('Content-Disposition', 'attachment', filename=file)  # 为附件命名
    msg.attach(part_attach1)  # 添加附件
    server = smtplib.SMTP()
    try:
        server.connect(smtp_server, 25)  # 连接SMTP服务器
        # server.set_debuglevel(1)  # 打印调试信息
        server.login(from_addr, password)  # 登陆邮箱
        server.sendmail(from_addr, to_addr, msg.as_string())  # 发送邮件
        print(f"Send email to {to_addr}, successfully!")
    except smtplib.SMTPException as e:
        server.quit()  # 退出


def deal_log(file_re, split_str, contains_str, category_re='', del_re=''):
    """
    处理日志的方法
    :param file_str:   文件名所包含的特别信息，用于区分哪些文件需要处理
    :param split_str:  将日志文件进行分割的标志
    :param contains_str:  分割后，每段内容包含的特殊内容，用于区分日志文件段
    :param category_re:   用于分类信息的提取，传入的是提取分类信息的正则表达式
    :param del_re: 日志文件段内需要删除的数据，传入参数为正则表达式
    :return:
    """
    dir_list = os.listdir(LOG_DIR)
    for file_name in dir_list:
        file_path = os.path.join(LOG_DIR, file_name)
        if os.path.isfile(file_path):
            # 判断当天的日志
            file_match=re.findall(file_re,file_name)
            if file_match:
                if not file_name.startswith('_'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        log_txt = f.read()
                        logs = log_txt.split(split_str)
                        for log in logs:
                            if contains_str in log:
                                if del_re:
                                    content = re.findall(del_re, log, re.S)
                                    # 取出链接
                                    if content:
                                        log = log.replace(content[0], '')
                                if category_re:
                                    url = re.findall(category_re, log)
                                    url = url[0].strip()
                                    # 根据url来进行区分
                                    for k, v in TASK_DICT_LIST.items():
                                        for start_str in v:
                                            # 排除邮件
                                            if '@' in start_str:
                                                continue
                                            if url.startswith(start_str):
                                                log = f'==================================\n{log}\n=================================='
                                                errors_dict[k].append(log)

                                else:
                                    log_msg.append(log)

                    with open(file_path, 'r', encoding='utf-8') as fl:
                        file_lines=fl.readlines()
                        for line in file_lines:
                            if 'URL地址' in line:
                                pur_name_list.append(line)

def send_email_to_workers():
    # 发送邮件
    for p, ers in errors_dict.items():
        file_name = f'{p}_{today_file}_error.txt'
        with open(file_name, 'a+', encoding='utf-8') as er:
            er.write(f'===={today}共{len(ers)}条错误\n')
            er.writelines(ers)
        send_res_to_email(TASK_DICT_LIST[p][0], file_name)
        os.remove(file_name)


def send_pur_log_to_workers():
    # 发送pur_name采集日志邮件给gmj
    file_name = f'{today_file}_pur.txt'
    with open(file_name, 'a+', encoding='utf-8') as er:
        er.write(f'===={today}共{len(pur_name_list)}条错误\n')
        er.writelines(pur_name_list)
    send_res_to_email('451574449@qq.com', file_name)
    os.remove(file_name)

def create_error_file():
    # 创建文件
    for p, ers in errors_dict.items():
        with open(f'{p}_{today_file}_error.txt', 'a+', encoding='utf-8') as er:
            er.write(f'===={today}共{len(ers)}条错误\n')
            er.writelines(ers)


def create_one_file():
    # 创建单个文件
    with open(f'{today_file}_msg.txt', 'a+', encoding='utf-8') as er:
        er.write(f'===={today}共{len(log_msg)}条错误\n')
        er.writelines(log_msg)





if __name__ == '__main__':
    split_str = "INFO: parse start with url: "
    contains_str = 'Traceback'
    category_re = "INFO: start handle data for url:(.*?)\n"
    del_re = "'content':(.*?)'has_attach':"
    deal_log(file_re=today, split_str=split_str, contains_str=contains_str, category_re=category_re)
    # create_error_file()
    send_email_to_workers()
    send_pur_log_to_workers()
