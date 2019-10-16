# -*- coding=utf-8 -*-
# gmj
# 配置说明

# 键：省份缩写_province
sd_province={
    # 网站类别 或者 表名     jyw  数据库中的表名为 sd_jyw
    'jyw':{
        # 键：原始数据表中 ywlx 和 xxlx 两个字段的值 使用 - 连接
        # 值：二元元组  ('目标表类 或 目标表 ','独立省份的解析方法')
        # 独立的解析方法可以为 空 '' 即可以为('zhaobiao','')
        # 目前 zhaobiao类 只有一张表 可以等同于表名    但 zhognbiao类 有四张表
        '工程建设-招标、资审公告':('zhaobiao','sd_jyw_gcjs'),
        # 如果需要单独进行解析字段控制 则需要使用 该键名称 后添加 1  来进行控制
        # 不需要无需添加，会自动读取默认的   目标表_fields_dict 的默认配置
        # 实例如下
        '工程建设-招标、资审公告1':{
            # 直接赋值字段名 对应源表字段名
            'link': 'lj',  # 采集来源url   link是目标字段  lj是源字段  会直接进行赋值操作
            'xmsd': 'cs',

            # 需要解析的字段
            'lx': '',# 类型
            'xmbh': '', # 项目编号
        },
    },

    'cgw':{

    }
}

def sd_jyw_gcjs(province, html, text, lines, table_line, table):
    """
    :param province:  省份缩写 可以用来控制省份分支  独立逻辑
    :param html:    度网页进行 html处理 使用xpath解析
    :param text:      网页文本 使用正则提取
                      处理中使用了re.sub(r'\s+', ' ', content)  replace('：', ':')
    :param lines:   列表  将网页每一行为列表的一项
    :param table_line:处理tr/td 得到   含有：的 k:v的行值
                      如果td中没有: 则不能识别
    :param table:   解析出规则的表单  并且每一行为一条数据
                    需要在代码中添加非第一列的列名 用于识别原始数据表的方向
    :return:  返回一个字典
    """
    # 该方法 提供
    res={}
    # 该方法内 为 需要独立解析的字段 的解析逻辑
    # 该方法内解析出来的字段将不会调用公用方法
    return res



# 字段解析方法名称 为 ：extract_字段名


# ===========字段解析的流程===========

# 如果存在就调用独立解析方法 --->  获取字段字典 --->  字典存在值 ---> 进行赋值
#                                  --->  字典值为空 ---> 字段不在独立解析结果中 ---> 调用独立的方法
# 独立的方法中也可以存在特定省份的解析逻辑  通过province值 来控制


