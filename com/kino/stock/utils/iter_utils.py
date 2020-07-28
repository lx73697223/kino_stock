"""
迭代类工具函数
"""

from collections.abc import Iterable

from com.kino.stock.utils.logging_utils import LoggingUtil


logger = LoggingUtil.get_default_logger()


def get_iter(obj):
    """
    判断是否是可迭代类型，如果不是则转为list
    :param obj: 对象
    :return:    可迭代对象
    """
    if obj is None:
        return []
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, Iterable):
        return list(obj)
    return [obj]


def merge_map_list(src_map, extra_map, ignore_duplicate=True):
    """
    合并两个value类型为数组的map, 并保证value数组顺序不乱
    :param src_map: 源map
    :param extra_map: 需要追加的map
    :param ignore_duplicate: list是否去重
    """
    for extra_key in extra_map:
        extra_values = extra_map.get(extra_key, [])
        src_values = src_map.get(extra_key, [])
        src_values.extend(extra_values)

        if ignore_duplicate:
            ignore_duplicate_values = list(set(src_values))
            ignore_duplicate_values.sort(key=src_values.index)
            src_values = ignore_duplicate_values

        src_map[extra_key] = src_values

