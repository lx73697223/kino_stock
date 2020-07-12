
from configs.database_config import DatabaseConfig
from repository.data_enums import TableExist
from repository.database_management import DatabaseManagement


def save_stock_df(df):
    DatabaseManagement().save_data_frame(
        df, table_name=DatabaseConfig.get_stock_table_name(), index=False, if_table_exists=TableExist.append)


def get_all_stocks(columns=None):
    return DatabaseManagement().query_data_frame_all(DatabaseConfig.get_stock_table_name(), columns=columns)
