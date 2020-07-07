
"""
扫描沪深股市所有的股票, 设置一个门槛, 如过滤交易额在5亿以下的，
监控资金量/交易量突然上涨的，目的是在中低位发现可能大涨的股票。
"""

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from feed_data.tushare_data_feeder import TushareDataFeeder


def run():
    pass


if __name__ == '__main__':
    scan_days = 30             # 扫描天数
    min_vol = 50000000         # 过滤小于min_vol的
    vol_factor = (10, 3)       # 连续3天交易量上涨10%以上
    amount_factor = (6, 3)     # 连续3天资金量上涨6%以上

    time_format = "%Y%m%d"
    now_time = datetime.now().timetuple()
    end_date = time.strftime(time_format, datetime.now().timetuple())
    start_date = time.strftime(time_format, (datetime.now() + relativedelta(days=-scan_days)).timetuple())

    data_feeder = TushareDataFeeder(tushare_token="311d0faf8bece0e369373c8ab8c6f52b0f2db20614a155cb20ec0ae9")

    # stocks_df = data_feeder.get_stocks(is_hs='H', list_status='L', exchange='SSE')
    # ts_codes = stocks_df['ts_code']
    # print(stocks_df)

    ts_codes = ['600000.SH']
    for ts_code in ts_codes:
        bar_df = data_feeder.get_bar(
            ts_code=ts_code, asset='E', freq='D', start_date=start_date, end_date=end_date, adj='qfq')
        print(bar_df)
