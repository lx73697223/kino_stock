
"""
扫描沪深股市所有的股票, 设置一个门槛, 如过滤交易额在5亿以下的，
监控资金量/交易量突然上涨的，目的是在中低位发现可能大涨的股票。
"""

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from configs.local_config import LocalConfig
from configs.app_config import AppConfig
from core_utils import time_utils
from repository.dao import stock_dao, stock_bar_dao
from strategy.base_strategy import BaseStrategy


class ScanningMomentumStrategy(BaseStrategy):

    def run(self):
        pass


if __name__ == '__main__':
    scan_days = 30             # 扫描天数
    min_vol = 50000000         # 过滤小于min_vol的
    vol_factor = (10, 3)       # 连续3天交易量上涨10%以上
    amount_factor = (6, 3)     # 连续3天资金量上涨6%以上
    ts_codes = ['600000.SH']

    time_format = "%Y%m%d"
    now_time = datetime.now().timetuple()
    end_date = time.strftime(time_format, datetime.now().timetuple())
    start_date = time.strftime(time_format, (datetime.now() + relativedelta(days=-scan_days)).timetuple())

    for ts_code in ts_codes:
        pass
        # bar_df = data_feeder.get_bar(
        #     ts_code=ts_code, asset='E', freq='D', start_date=start_date, end_date=end_date, adj='qfq')
        # print(bar_df)
