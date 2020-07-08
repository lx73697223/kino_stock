# -*- coding: utf-8 -*-

import importlib


def get_title_name(name):
    return name.title().replace('_', '')


def import_enum(name):
    module_name, class_name = name.split("#", 1)
    class_name, value = class_name.split(".")
    return getattr(importlib.import_module(module_name), class_name)(value)


def import_configs_module(name):
    return getattr(importlib.import_module("configs." + name), get_title_name(name))
