
"""
假设今天是7.8号
先计算6.6到7.6这一个月“上涨”的成交量取平均值，忽略K线是下跌的成交量数据 一个月貌似太长了 10日数据 (是否要考虑阴线的成交量)
用7.7号的成交量除以平均值，得到数值vol_chg 保存到数据库
如何使用: 根据vol_chg降序排列，观察到交易量有异动的股票。然后手工筛选股票，后续再开发进一步的规则
还要看分时图的情况 判断是否大资金在吸取筹码
"""

import pandas
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from configs.local_config import load_local_config
from repository.dao import stock_bar_dao, stock_dao
from strategy.base_strategy import BaseStrategy

pandas.set_option('expand_frame_repr', False)
pandas.set_option('display.max_rows', 200)


class ScanningMomentumStrategy(BaseStrategy):

    def get_signals(self):
        pass


if __name__ == '__main__':
    load_local_config()

    rolling_days = 10             # 天数
    use_ups_vol_avg = True     # 取上涨行情成交量平均值
    ts_codes = stock_dao.get_all_stocks()['ts_code']      # ['600000.SH']

    time_format = "%Y%m%d"
    now_time = datetime.now()
    end_date = time.strftime(time_format, now_time.timetuple())
    start_date = time.strftime(time_format, (now_time + relativedelta(days=-(rolling_days * 2))).timetuple())

    for ts_code in ts_codes:
        bar_df = stock_bar_dao.get_stock_bar(ts_codes=[ts_code], start_date=start_date, end_date=end_date,
                                             freq="D", adj="qfq", order_by='trade_date')
        if bar_df is None or len(bar_df) == 0:
            print('--- {} bar data is empty!'.format(ts_code))
            continue

        bar_df = bar_df[-rolling_days:]
        bar_df.loc[:, 'pct_vol'] = bar_df['vol'].pct_change(periods=1, fill_method='ffill')

        vol_avg = bar_df['vol'].mean()
        ups_vol_avg = bar_df.loc[bar_df['change'] > 0, 'vol'].mean()   # 上涨行情的成交量平均值
        print(bar_df)
        vol_chg = (ups_vol_avg if use_ups_vol_avg else vol_avg) / bar_df.iloc[-1]['vol']
        print('--- ups_vol_avg:', ups_vol_avg, '- vol_avg:', vol_avg, '- vol_chg:', vol_chg)

        print('--- bar_df: \n', bar_df)
