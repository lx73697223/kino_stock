# -*- coding: utf-8 -*-

import importlib


def get_title_name(name):
    return name.title().replace('_', '')


def import_enum(name):
    """通过自定义字符串动态导入枚举值"""
    # [enum]repository.data_enums#DataExist.discard
    module_name, class_name = name.split("#", 1)
    class_name, value = class_name.split(".")
    return getattr(importlib.import_module(module_name), class_name)(value)


def import_configs_module(name):
    """通过模块名动态导入.configs包中的类"""
    return getattr(importlib.import_module("configs." + name), get_title_name(name))
