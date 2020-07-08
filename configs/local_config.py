# -*- coding: utf-8 -*-

"""本地配置"""

import os
import json
import traceback

from utils.logging_utils import log
from utils import file_utils, import_utils


class LocalConfig(object):
    # 程序数据文件存放根路径
    FIXED_ROOT_PATH = '/userdata'

    # 本地配置文件存放目录
    CONFIGS_BASE_PATH = os.path.join(FIXED_ROOT_PATH, 'configs')
    # 程序代码存放路径
    application_root_path = FIXED_ROOT_PATH
    # 数据保存根目录
    data_root_path = FIXED_ROOT_PATH

    @classmethod
    def get_local_config_path(cls):
        return os.path.join(cls.CONFIGS_BASE_PATH, "kino_stock_config.json")

    @classmethod
    def get_output_base_path(cls):
        return file_utils.mk_if_not_exists(os.path.join(cls.data_root_path, 'output_data'))

    @classmethod
    def get_logging_base_path(cls):
        return file_utils.mk_if_not_exists(os.path.join(cls.get_output_base_path(), 'logs'))

    @classmethod
    def get_log_file_path(cls, file_name):
        return os.path.join(cls.get_logging_base_path(), '{}.log'.format(file_name))


@log(log_args=True)
def load_local_config(setter_configs=False):
    config_file_path = LocalConfig.get_local_config_path()

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as f:
            config_data = json.load(f)
        if setter_configs:
            setter_config(config_data)
        return config_data


def setter_config(data):
    if data:
        obj_by_name = {}
        for key, value in data.items():
            try:
                obj_name, attr_name = key.split('.', maxsplit=1)

                if obj_by_name.__contains__(obj_name):
                    obj = obj_by_name.get(obj_name)
                else:
                    obj = obj_by_name.setdefault(obj_name, import_utils.import_configs_module(obj_name))

                if isinstance(value, str):
                    if value.startswith('[enum]'):
                        value = import_utils.import_enum(value.replace('[enum]', '', 1))

                setattr(obj, attr_name, value)
                print('--- setattr(obj={}, attr_name={}, value={})'.format(obj, attr_name, value))
            except Exception as e:
                traceback.print_exc()
                print('--- setter_config failed! e:{}. key:{}, value:{}'.format(e, key, value))


# 载入代码时默认加载一次
load_local_config(setter_configs=True)
