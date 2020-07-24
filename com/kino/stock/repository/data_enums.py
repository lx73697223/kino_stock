# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class DataExist(Enum):
    discard = 'discard'
    replace = 'replace'
    backup_replace = 'backup_replace'


@unique
class TableExist(Enum):
    fail = 'fail'
    append = 'append'
    # replace = 'replace'  不使用直接替换表，改用备份替换
    backup_replace = 'backup_replace'
