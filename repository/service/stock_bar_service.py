
import os
import pandas

from core_utils.logging_utils import LoggingUtil
from configs.app_config import AppConfig
from configs.local_config import LocalConfig
from repository.dao import stock_dao, stock_bar_dao
from feed_data.tushare_data_feeder import TushareDataFeeder


logger = LoggingUtil.get_default_logger()


def sync_stock_bar(start_date, end_date, freq='D', adj='qfq', ts_codes=None, temp_to_csv=True):
    """
    同步股票K线数据
    :param start_date:
    :param end_date:
    :param freq:
    :param adj:
    :param ts_codes: 需要同步的股票代码列表。为None时拉取股票列表中所有股票
    :param temp_to_csv: 是否暂存到csv文件然后再上传到数据库。股票K线数据本地存储路径格式 => csv_path_format % ts_code
    :return:
    """
    if ts_codes is None:
        ts_codes = stock_dao.get_all_stocks(columns=['ts_code'])['ts_code']
        logger.info('ts_codes:\n%s', ts_codes)

    if ts_codes is not None and len(ts_codes) > 0:
        tsd = None
        csv_path_format = LocalConfig.get_stock_bar_csv_tmp_path_format(
            adj=adj, freq=freq, start_date=start_date, end_date=end_date) if temp_to_csv else None

        for ts_code in ts_codes:
            csv_path = csv_path_format % ts_code if csv_path_format else None

            if not csv_path or not os.path.exists(csv_path):
                tsd = tsd or TushareDataFeeder(tushare_token=AppConfig.tushare_token)
                bar_df = tsd.get_bar(ts_code=ts_code, freq=freq, adj=adj, start_date=start_date, end_date=end_date)
                if csv_path:
                    bar_df['freq'] = freq
                    bar_df['adj'] = adj
                    bar_df.to_csv(csv_path)
            else:
                bar_df = pandas.read_csv(csv_path, index_col=0)

            logger.info('bar_df:\n%s', bar_df)
            stock_bar_dao.save_stock_bar_df(bar_df)
