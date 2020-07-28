from com.kino.stock.utils import sql_utils
from com.kino.stock.configs.database_config import DatabaseConfig
from com.kino.stock.repository.data_enums import TableExist
from com.kino.stock.repository.database_management import DatabaseManagement


def save_stock_bar_df(df):
    DatabaseManagement(engine_url=DatabaseConfig.engine_url).save_data_frame(
        df, table_name=DatabaseConfig.get_stock_bar_table_name(), index=False, if_table_exists=TableExist.append)


def get_stock_bar(ts_codes, start_date, end_date, freq="D", adj="qfq", columns=None, order_by=None):
    sql_wheres = sql_utils.range_where(start_date, end_date, "trade_date")
    sql_wheres.append("ts_code in ({})".format(','.join(["'%s'" % s for s in ts_codes])))
    sql_wheres.append("freq = '{}'".format(freq))
    sql_wheres.append("adj = '{}'".format(adj))

    order_sql = "order by {}".format(order_by) if order_by else ''

    return DatabaseManagement(engine_url=DatabaseConfig.engine_url).query_data_frame(
        DatabaseConfig.get_stock_bar_table_name(), columns=columns, sql_wheres=sql_wheres, order_sql=order_sql)


def get_max_index(index_col="trade_date"):
    return DatabaseManagement(engine_url=DatabaseConfig.engine_url).query_max_index(
        DatabaseConfig.get_stock_bar_table_name(), index_col=index_col)
