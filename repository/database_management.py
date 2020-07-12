# -*- coding: utf-8 -*-

"""
数据库
"""

import pandas

from core_utils.annotation import singleton
from core_utils.logging_utils import LoggingUtil
from core_utils import time_utils, sql_utils, iter_utils
from configs.database_config import DatabaseConfig
from data_enums import TableExist


@singleton(func_name="get_singleton_str")
class DatabaseManagement(object):

    def __init__(self):
        self.logger = LoggingUtil.get_default_logger()
        self.__engine, self.__session = DatabaseConfig.create_connection()

    @staticmethod
    def get_singleton_str(*args, **kw):
        return DatabaseConfig.engine_url

    def save_data_frame(self, data_frame, table_name, index_label=None, index=True, if_table_exists=TableExist.fail,
                        chunk_size=50, dtype=None, on_ignore_dup_key=False, unique_index_columns=None):
        """
        DataFrame to resource
        :param data_frame: save data
        :param table_name: table name
        :param index_label: index column name
        :param index: True or False
        :param if_table_exists: fail, append, replace, backup_replace(==table_rename & replace)
        :param chunk_size: insert multi values size
        :param dtype: {column:Type}
        :param on_ignore_dup_key: create IGNORE_DUP_KEY=ON unique index
        :param unique_index_columns: IGNORE_DUP_KEY=ON unique index column names
        """
        if data_frame is not None and len(data_frame) > 0:
            if if_table_exists == TableExist.backup_replace:
                self.table_rename(table_name)
                if_table_exists = TableExist.append

            if on_ignore_dup_key and if_table_exists != TableExist.fail \
                    and unique_index_columns is not None and len(unique_index_columns) > 0:
                if not self.__engine.has_table(table_name):
                    data_frame.iloc[:1].to_sql(name=table_name, index=index, index_label=index_label,
                                               dtype=dtype, con=self.__engine, if_exists=TableExist.append.value)
                    self.recreate_table_index_with_ignore_dup_key(table_name, unique_index_columns, index_label)

            data_frame.to_sql(name=table_name, if_exists=if_table_exists.value, index=index, index_label=index_label,
                              dtype=dtype, con=self.__engine, chunksize=chunk_size, method='multi')

    def query_data_frame_all(self, table_name, index_col=None, columns=None, chunk_size=None, parse_dates=None,
                             coerce_float=True, check_has_table=False):
        """read resource table into to DataFrame"""
        if not check_has_table or self.__engine.has_table(table_name):
            return pandas.read_sql_table(table_name=table_name, con=self.__engine, index_col=index_col, columns=columns,
                                         chunksize=chunk_size, parse_dates=parse_dates, coerce_float=coerce_float)
        else:
            self.logger.warning('{} not exist'.format(table_name))

    def query_data_frame_by_sql(self, sql, params=None, index_col=None, columns=None, chunk_size=None, parse_dates=None,
                                coerce_float=True):
        """read resource into to DataFrame"""
        return pandas.read_sql(sql=sql, con=self.__engine, index_col=index_col, coerce_float=coerce_float,
                               params=params, parse_dates=parse_dates, columns=columns, chunksize=chunk_size)

    def query_data_frame(self, table_name, sql_wheres=None, order_sql='', index_col=None, columns=None, params=None,
                         chunk_size=None, parse_dates=None, coerce_float=True, check_has_table=False):
        """read resource into to DataFrame"""
        if not check_has_table or self.__engine.has_table(table_name):
            columns_str = "[{}]".format('],['.join(columns)) if iter_utils.get_iter(columns) else "*"
            where_sql = sql_utils.where_sql_joiner(sql_wheres)
            sql = "SELECT {} FROM {} {} {}".format(columns_str, table_name, where_sql, order_sql)
            return self.query_data_frame_by_sql(sql, index_col=index_col, coerce_float=coerce_float, params=params,
                                                parse_dates=parse_dates, columns=columns, chunk_size=chunk_size)
        else:
            self.logger.warning('{} not exist'.format(table_name))

    def query_max_index(self, table_name, index_col, check_has_table=False):
        if not check_has_table or self.__engine.has_table(table_name):
            sql = "SELECT MAX([{}]) AS max_index FROM {}".format(index_col, table_name)
            return self.execute_sql(sql).scalar()
        else:
            self.logger.warning('{} not exist'.format(table_name))

    def delete_batch(self, table_name, wheres, check_has_table=False):
        """delete"""
        if wheres is None or len(wheres) == 0:
            self.logger.error('wheres cannot be empty')
            return
        if not check_has_table or self.__engine.has_table(table_name):
            self.execute_sql("DELETE {} {}".format(table_name, sql_utils.where_sql_joiner(wheres)))
        else:
            self.logger.warning('{} not exist'.format(table_name))

    def table_rename(self, table_name, new_table_name=None):
        """rename"""
        if not self.__engine.has_table(table_name):
            self.logger.warning('table rename failed. {} not exist'.format(table_name))
            return
        if self.__engine.has_table(new_table_name):
            self.logger.warning('table rename failed. {} already exist'.format(new_table_name))
            return
        if new_table_name is None:
            new_table_name = '{}_bak_{}'.format(table_name, time_utils.format_time(_format="%Y%m%d%H%M%S"))
            self.logger.info('table_name = {}, new_table_name = {}'.format(table_name, new_table_name))
        self.execute_sql("EXEC SP_RENAME '{}', '{}'".format(table_name, new_table_name))
        return new_table_name

    def recreate_table_index_with_ignore_dup_key(self, table_name, unique_index_columns, index_label=None):
        sql_list = []
        if index_label is not None:
            sql_list.append("DROP INDEX ix_{}_{} ON {};".format(table_name, index_label, table_name))
        if unique_index_columns is not None and len(unique_index_columns) > 0:
            sql_list.append("CREATE UNIQUE INDEX ix_{}_{}_unique ON {} ([{}]) WITH (IGNORE_DUP_KEY = ON);".format(
                table_name, '_'.join(unique_index_columns), table_name, '], ['.join(unique_index_columns)))
        self.execute_sql(sql_list)

    def execute_sql(self, sql):
        if sql:
            with self.__engine.begin() as conn:
                if iter_utils.get_iter(sql):
                    result = []
                    for s in sql:
                        result.append(conn.execute(s))
                else:
                    result = conn.execute(sql)
            return result

    def add_obj(self, obj):
        """添加"""
        self.__session.add(obj)
        self.__session.commit()  # 提交
        return obj

    def query_all(self, target_class, query_filter):
        """查询"""
        # query() 括号内必须是一个类(target_class), 如果是对象(obj), 需要改为(obj.__class__)
        result_list = self.__session.query(target_class).filter(query_filter).all()
        return result_list

    def update_by_filter(self, obj, update_hash, query_filter):
        """更新"""
        self.__session.query(obj.__class__).filter(query_filter).update(update_hash)
        self.__session.commit()

    def delete_by_filter(self, obj, query_filter):
        """删除"""
        self.__session.query(obj).filter(query_filter).delete()

    def close(self):
        """关闭session"""
        self.__session.close()
