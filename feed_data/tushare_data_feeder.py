
"""
使用 Tushare 获取数据
文档：https://tushare.pro/document/2
"""

import sys
import pandas
import tushare as ts

from base_data_feeder import BaseDataFeeder

pandas.set_option('expand_frame_repr', False)   # 打印时不要折叠列
pandas.set_option('display.max_rows', 200)      # 打印最多200行数据


class TushareDataFeeder(BaseDataFeeder):

    def __init__(self, tushare_token):
        # 设置用户token. https://tushare.pro/user/token 页面可获取token
        ts.set_token(tushare_token)

        # tushare需要足够的积分才能使用相应的接口: https://tushare.pro/document/1?doc_id=108
        self.__pro_api = ts.pro_api()

    def get_trading_calendar(self, exchange='SSE', start_date='20200701', end_date='20200706', is_open='1'):
        """
        获取各大交易所交易日历
        :param exchange:        交易所 SSE 上交所,SZSE 深交所,CFFEX 中金所,SHFE 上期所,CZCE 郑商所,DCE 大商所,INE 上能源,IB 银行间,XHKG 港交所
        :param start_date:      开始日期 (YYYYMMDD)
        :param end_date:        结束日期 (YYYYMMDD)
        :param is_open:         是否交易 '0'休市, '1'交易
        :return: DataFrame
        """
        return self.__pro_api.trade_cal(
            exchange=exchange, start_date=str(start_date), end_date=str(end_date), is_open=is_open)

    def get_stocks(self, is_hs=None, list_status='L', exchange=None, fields=None):
        """
        获取股票列表
        https://tushare.pro/document/2?doc_id=25
        :param is_hs:       是否沪深港通标的，N 否 H 沪股通 S 深股通
        :param list_status: 上市状态： L上市 D退市 P暂停上市，默认L
        :param exchange:    交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
        :param fields:       需要的属性名称, 不填是返回所有属性
        :return: DataFrame
        """
        return self.__pro_api.stock_basic(exchange=exchange, is_hs=is_hs, list_status=list_status, fields=fields or [])

    def get_bar(self, ts_code, asset='E', freq='D', start_date=None, end_date=None, adj=None, adjfactor=True,
                factors=None, ma=None):
        """
        获取复权行情 (1.2.26版本以上才有此接口)
        https://tushare.pro/document/2?doc_id=109
        :param ts_code:      证券代码
        :param asset:        资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
        :param freq:         数据频度 1MIN表示1分钟（1/5/15/30/60分钟） D日线 W周线 M月线，默认为D
        :param start_date:   开始日期 (YYYYMMDD)   取指定范围内的历史行情
        :param end_date:     结束日期 (YYYYMMDD)   取指定范围内的历史行情
        :param adj:          复权行情 (只针对股票)  qfq:前复权; hfq:后复权; 为空时不复权 默认None
        :param factors:      股票因子 (asset='E'时有效)  tor换手率 vr量比
        :param adjfactor:    复权因子 (v1.2.33) 在复权数据时，如果此参数为True，返回的数据中则带复权因子，默认为True
        :param ma:           均线 list 支持任意合理int数值 如 [5, 20, 50]
        :return: DataFrame
        """
        return ts.pro_bar(ts_code=ts_code, asset=asset, freq=freq, start_date=start_date, end_date=end_date,
                          adj=adj, adjfactor=adjfactor, factors=factors, ma=ma, api=self.__pro_api)

    def get_daily_basic(self, ts_code=None, trade_date=None, start_date=None, end_date=None):
        """
        获取每日重要的基本面指标
        https://tushare.pro/document/2?doc_id=32
        :param ts_code:      股票代码 (ts_code/trade_date 两个参数二选一)
        :param trade_date:   交易日期 (YYYYMMDD)   取某一天
        :param start_date:   开始日期 (YYYYMMDD)   取指定范围
        :param end_date:     结束日期 (YYYYMMDD)   取指定范围
        :return: DataFrame
        """
        return self.__pro_api.query(
            'daily_basic', ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date)

    def get_daily_md(self, codes, start_date=None, end_date=None, trade_date=None):
        """
        获取日线行情 (交易日每天15点～16点之间。本接口是未复权行情，停牌期间不提供数据)
        https://tushare.pro/document/2?doc_id=27
        :param codes:        股票代码列表
        :param trade_date:   交易日期 (YYYYMMDD)   取历史某一天的历史行情
        :param start_date:   开始日期 (YYYYMMDD)   取指定范围内的历史行情
        :param end_date:     结束日期 (YYYYMMDD)   取指定范围内的历史行情
        :return: DataFrame
        """
        ts_code = ','.join(codes)
        return self.__pro_api.query(
            'daily', ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date)

    def get_weekly_md(self, ts_code, start_date=None, end_date=None, trade_date=None):
        """
        获取周线行情 (交易日每天15点～16点之间。本接口是未复权行情，停牌期间不提供数据)
        :param ts_code:      股票代码 (ts_code/trade_date 两个参数任选一)
        :param trade_date:   交易日期 (YYYYMMDD)   取历史某一天的历史行情
        :param start_date:   开始日期 (YYYYMMDD)   取指定范围内的历史行情
        :param end_date:     结束日期 (YYYYMMDD)   取指定范围内的历史行情
        :return: DataFrame
        """
        return self.__pro_api.query(
            'weekly', ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date)

    def get_moneyflow(self, start_date=None, end_date=None, trade_date=None):
        """
        获取资金流向
        :param start_date:   开始日期 (YYYYMMDD)   取指定范围      (start_date/trade_date 两个参数二选一)
        :param end_date:     结束日期 (YYYYMMDD)   取指定范围
        :param trade_date:   交易日期 (YYYYMMDD)   取某一天
        :return: DataFrame
        """
        return self.__pro_api.query('moneyflow_hsgt', trade_date=trade_date, start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    print(ts.__version__)

    token = sys.argv[1] if len(sys.argv) > 1 else '311d0faf8bece0e369373c8ab8c6f52b0f2db20614a155cb20ec0ae9'

    ts_data_feeder = TushareDataFeeder(tushare_token=token)

    data = ts_data_feeder.get_stocks(is_hs='H', list_status='L', exchange='SSE')
    print('---', data)

    """
    data = ts_data_feeder.get_trading_calendar()
    print('---', data)

    data = ts_data_feeder.get_daily_md(codes=['000001.SZ', '688566.SH'], start_date='20200701', end_date='20200706')
    print('---', data)

    data = ts_data_feeder.get_weekly_md(ts_code='000001.SZ', start_date='20200301', end_date='20200706')
    print('---', data)

    data = ts_data_feeder.get_bar(ts_code='000001.SZ', start_date='20200301', end_date='20200706', adj='qfq')
    print('---', data)
    """
