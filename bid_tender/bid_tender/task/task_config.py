##==========================================================
#   如果不进行某个省份的任务，将该省份在 PROVINCES_DICT 中注销

#   # 控制是否为首次爬取，即全量爬取
#   省份缩写_FIRST_CRAWL = True
#   # 控制是否进行每日爬取任务   True为需要修改，将不执行该省任务
#   省份缩写_HAVE_ERROR = False
##==========================================================

# 省份字典及权重配置
PROVINCES_DICT = {
    '兵团': ('bt', 100),
}

# ===============任务控制开始===================

#   兵团
bt_FIRST_CRAWL = False
bt_HAVE_ERROR = False

# =======================任务控制结束=========================


if __name__ == '__main__':

    for k, v in PROVINCES_DICT.items():
        # print('#  ',k)
        # print(f'{v}_FIRST_CRAWL = False')
        # print(f'{v}_HAVE_ERROR = False')
        # print(f"('{v}',100) # {k}")
        # print(f"'{k}':('{v}',100),")
        print(f"'{v[0]}':",f"'{k}',")
