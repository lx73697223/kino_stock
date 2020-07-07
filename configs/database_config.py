# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.orm import sessionmaker


class DatabaseConfig(object):
    database_engine_url = None
    database_engine_echo = True
    database_engine_fast_executemany = True

    @classmethod
    def create_connection(cls, engine_url=None, echo=None, fast_executemany=None, autocommit=True):
        """创建数据库连接"""
        engine_url = engine_url or cls.database_engine_url
        echo = echo if echo is not None else cls.database_engine_echo
        fast_executemany = fast_executemany if fast_executemany is not None else cls.database_engine_fast_executemany
        engine = sqlalchemy.create_engine(engine_url, echo=echo, fast_executemany=fast_executemany)
        session = sessionmaker(bind=engine, autocommit=autocommit)()
        return engine, session
