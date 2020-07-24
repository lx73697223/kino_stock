# -*- coding: utf-8 -*-

"""
文件操作工具函数
"""

import os
import time
import shutil
import pandas
import zipfile
import tarfile
import traceback

import time_utils
from logging_utils import LoggingUtil, log


logger = LoggingUtil.get_default_logger()


def get_file_base_name(path):
    """
    获取文件名，不含后缀类型
    :param path: 路径
    :return: 名称 例：
    "/userdata/futures-common-libs/common_2_utils" ==> common_2_utils
    "/userdata/futures-common-libs/common_2_utils/file_utils.py" ==> file_utils
    """
    return os.path.splitext(os.path.basename(path))[0]


def get_file_mtime(path):
    """
    获取文件最后修改时间
    :param path: 路径
    :return: 修改时间
    """
    return pandas.to_datetime(time_utils.format_time(time.localtime(os.stat(path).st_mtime)))


def get_last_line(path, index=-1):
    """
    获取文件最后一行. 使用指针的方式实现
    :param path: 文件路径
    :param index: 默认为倒数第一行
    :return: last line or None for empty file
    """
    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            if file_size > 0:
                with open(path, 'rb') as f:     # to use seek from end, must use mode 'rb'
                    offset = -8                 # initialize offset
                    while -offset < file_size:   # offset cannot exceed file size
                        f.seek(offset, 2)       # read # offset chars from eof(represent by number '2')
                        lines = f.readlines()   # read from fp to eof
                        if len(lines) >= 2:     # if contains at least 2 lines
                            return bytes.decode(lines[index])    # then last line is totally included
                        else:
                            offset *= 2         # enlarge offset
                    f.seek(0)
                    lines = f.readlines()
                    return bytes.decode(lines[index])
    except Exception as err:
        traceback.print_exc()
        logger.exception('err: %s. path=%s', err, path)


def mk_or_bak(path, _mkdir=False):
    """创建文件夹，存在时先备份"""
    if path:
        new_path = path
        if os.path.exists(path):
            dir_path, file_suffix = os.path.splitext(path)
            new_path = '%s_bak_%s%s' % (dir_path, time_utils.format_time(_format="%Y%m%d-%H%M%S"), file_suffix)
            shutil.move(path, new_path)
            logger.info('{} existing, renamed to {}'.format(path, new_path))
        if _mkdir or not os.path.splitext(path)[1].startswith('.'):
            os.makedirs(path)
        return new_path


def mk_if_not_exists(path):
    """创建文件夹，如果不存在"""
    if path:
        if os.path.exists(path):
            logger.info('{} existing.'.format(path))
        else:
            os.makedirs(path)
            logger.info('make dirs: {}'.format(path))
    return path


@log(log_args=True)
def group_files(file_path, group_dirname):
    """根据文件名分组"""
    if os.path.isfile(file_path):
        src_dir, file_name = os.path.split(file_path)

        group_dir = os.path.join(src_dir, group_dirname)
        mk_if_not_exists(group_dir)

        new_file_path = os.path.join(group_dir, file_name)
        if os.path.isfile(new_file_path):
            mk_or_bak(new_file_path)

        shutil.move(file_path, new_file_path)
        logger.info('group file success. {} ==> {}'.format(file_path, new_file_path))
        return new_file_path
    else:
        logger.warn('file not exit. {}'.format(file_path))


@log(log_args=True)
def split_file(file_path, chunk_size, index=False):
    """切割文件"""
    output_file_paths = []
    if os.path.isfile(file_path):
        rows = pandas.read_csv(file_path, chunksize=chunk_size)

        output_dir, file_type = os.path.splitext(file_path)
        output_root_dir, file_name = os.path.split(output_dir)
        mk_if_not_exists(output_dir)

        for i, chuck in enumerate(rows):
            chuck_file_path = os.path.join(output_dir, '{}_000{}{}'.format(file_name, i, file_type))
            chuck.to_csv(chuck_file_path, index=index)
            output_file_paths.append(chuck_file_path)
            logger.info(chuck_file_path)
    return output_file_paths


@log(log_args=True)
def deep_extract_all(input_path, output_path, delete_rar_file=False):
    """解压目录下所有压缩文件输出到指定目录下"""
    for dir_path, dirs, files in os.walk(input_path):
        for f in files:
            is_rar = f.endswith('.rar')
            is_zip = f.endswith('.zip')
            is_tgz = f.endswith('.tgz')
            if is_rar or is_zip or is_tgz:
                file_path = os.path.join(dir_path, f)
                extract_path = os.path.join(output_path, os.path.splitext(f)[0])
                logger.info('file_path = {} \n extract_path = {}'.format(file_path, extract_path))

                namelist = []
                if is_rar:
                    namelist = un_rar(file_path, extract_path)
                elif is_zip:
                    namelist = un_zip(file_path, extract_path)
                elif is_tgz:
                    namelist = un_tgz(file_path, extract_path)

                # 删除原文件
                if delete_rar_file:
                    os.remove(file_path)

                # 递归解压文件
                need_deep_extract = False
                for f1 in namelist:
                    if f1.endswith('.rar') or f1.endswith('.zip'):
                        need_deep_extract = True
                        break
                if need_deep_extract:
                    deep_extract_all(extract_path, extract_path, True)


def un_zip(file_path, extract_path):
    f = zipfile.ZipFile(file_path)
    f.extractall(extract_path)
    return f.namelist()


def un_rar(file_path, extract_path):
    from unrar import rarfile
    f = rarfile.RarFile(file_path)
    f.extractall(extract_path)
    return f.namelist()


def un_tgz(file_path, extract_path):
    f = tarfile.open(file_path)
    f.extractall(extract_path)
    return f.namelist()


def zip_files(file_paths, zip_file_path):
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as f:
        for file_path in file_paths:
            f.write(file_path, os.path.split(file_path)[1])
    return zip_file_path


def walk_sorted(func, path, failed_paths, kwargs):
    """遍历所有文件夹以及处理文件"""
    if failed_paths is None:
        failed_paths = []

    listdir = os.listdir(path)
    listdir.sort()
    logger.info('{}, listdir = {}'.format(path, listdir))

    for dirname in listdir:
        dir_path = os.path.join(path, dirname)
        if os.path.isfile(dir_path):
            try:
                func(dir_path, kwargs)
            except Exception as err:
                failed_paths.append(dir_path)
                logger.exception('func occur error. %s err: %s', dir_path, err)
        else:
            walk_sorted(func, dir_path, failed_paths, kwargs)
