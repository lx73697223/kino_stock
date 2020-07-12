
"""程序环境配置"""


class AppConfig(object):
    # 环境. dev、test、prod...
    profile = 'dev'
    # 机器标签. 用于区分同种环境不同类型, basic、docker1、docker2...
    machine_tag = 'basic'

    tushare_token = '311d0faf8bece0e369373c8ab8c6f52b0f2db20614a155cb20ec0ae9'
