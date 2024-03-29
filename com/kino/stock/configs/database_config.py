"""
数据库配置
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker


class DatabaseConfig(object):
    engine_url = None
    echo = True
    autocommit = True

    stock_table_name_format = 't_stock'
    stock_bar_table_name_format = 't_stock_bar'

    @classmethod
    def create_connection(cls, engine_url=None, echo=None, autocommit=True):
        """创建数据库连接"""
        engine_url = engine_url or cls.engine_url
        echo = echo if echo is not None else cls.echo
        autocommit = autocommit if autocommit is not None else cls.autocommit

        engine = sqlalchemy.create_engine(engine_url, echo=echo)
        session = sessionmaker(bind=engine, autocommit=autocommit)()
        return engine, session

    @classmethod
    def get_stock_table_name(cls):
        return cls.stock_table_name_format

    @classmethod
    def get_stock_bar_table_name(cls):
        return cls.stock_bar_table_name_format
