"""
获取股票历史bar数据，存到数据库
"""

import sys

from com.kino.stock.utils import time_utils
from com.kino.stock.repository.dao import stock_bar_dao
from com.kino.stock.repository.service import stock_bar_service


if __name__ == '__main__':
    ts_codes = sys.argv[1].split(',') if len(sys.argv) > 1 else None
    adj = sys.argv[2] if len(sys.argv) > 2 else 'qfq'
    freq = sys.argv[3] if len(sys.argv) > 3 else 'D'
    # 交易日区间. 默认为数据库中最大的日期的下一天
    start_date = sys.argv[4] if len(sys.argv) > 4 else \
        time_utils.delta_and_format_time(stock_bar_dao.get_max_index('trade_date'), days=1, _format="%Y%m%d")
    end_date = sys.argv[5] if len(sys.argv) > 5 else time_utils.format_time(_format="%Y%m%d")

    stock_bar_service.sync_stock_bar(start_date=start_date, end_date=end_date, freq=freq, adj=adj, ts_codes=ts_codes,
                                     temp_to_csv=True)
