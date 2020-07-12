
import os
import pandas

from core_utils import time_utils
from core_utils.logging_utils import LoggingUtil
from configs.app_config import AppConfig
from repository.dao import stock_dao
from feed_data.tushare_data_feeder import TushareDataFeeder


logger = LoggingUtil.get_default_logger()


def sync_stocks(is_hs, list_status, exchange, stocks_csv_path=None):
    """
    同步股票列表
    :param is_hs:
    :param list_status:
    :param exchange:
    :param stocks_csv_path: 数据本地存储路径。
    存在此文件时直接从文件中读取，不存在时用tushare获取数据存到本地再存数据库。为None时直接从tushare获取并且不存到本地。
    :return:
    """
    if stocks_csv_path and os.path.exists(stocks_csv_path):
        stocks_df = pandas.read_csv(stocks_csv_path, index_col=0)
    else:
        tsd = TushareDataFeeder(tushare_token=AppConfig.tushare_token)
        stocks_df = tsd.get_stocks(is_hs=is_hs, list_status=list_status, exchange=exchange)
        if stocks_csv_path:
            stocks_df.to_csv(stocks_csv_path)

    stocks_df['created_time'] = time_utils.format_time()
    stocks_df['updated_time'] = time_utils.format_time()
    logger.info('stocks_df:\n%s', stocks_df)
    stock_dao.save_stock_df(stocks_df)
