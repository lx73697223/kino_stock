
"""
使用 Tushare 获取数据
文档：https://tushare.pro/document/2
"""

import tushare as ts


if __name__ == '__main__':
    print('---', ts.__version__)

    # 设置用户tocken, 在 https://tushare.pro/user/token 页面获取
    ts.set_token('311d0faf8bece0e369373c8ab8c6f52b0f2db20614a155cb20ec0ae9')

    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    print('---', data)
