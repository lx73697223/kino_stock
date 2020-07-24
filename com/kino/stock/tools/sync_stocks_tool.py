
"""获取股票列表，存到数据库"""

import os
import sys

from com.kino.stock.configs.local_config import LocalConfig
from com.kino.stock.repository.service import stock_service


if __name__ == '__main__':
    stocks_csv_path_format = sys.argv[1] if len(sys.argv) > 1 \
        else os.path.join(LocalConfig.get_output_base_path(), 'ks/tmp/stocks-%s.csv')
    is_hs = sys.argv[2] if len(sys.argv) > 2 else 'H'
    list_status = sys.argv[3] if len(sys.argv) > 3 else 'L'
    exchange = sys.argv[4] if len(sys.argv) > 4 else 'SSE'

    stocks_csv_path = stocks_csv_path_format % '-'.join((is_hs, list_status, exchange))

    stock_service.sync_stocks(
        is_hs=is_hs, list_status=list_status, exchange=exchange, stocks_csv_path=stocks_csv_path)
