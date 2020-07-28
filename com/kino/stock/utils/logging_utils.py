"""
日志工具封装
"""

import sys
import logging
import inspect
from logging import handlers
from datetime import datetime


class LoggingUtil(object):
    logging_format = '%(asctime)s %(levelname)s %(process)s %(filename)s.%(funcName)s %(lineno)d - %(message)s'

    root_logging_level = logging.WARN
    root_logger = logging.getLogger()
    if len(root_logger.handlers) == 0:
        root_logger.setLevel(root_logging_level)
        root_logging_handler = logging.StreamHandler(sys.stdout)
        root_logging_handler.setLevel(root_logging_level)
        root_logging_handler.setFormatter(logging.Formatter(logging_format))
        root_logger.addHandler(root_logging_handler)

    default_logging_name = 'default'
    default_logging_level = logging.INFO
    default_logging_propagate = False
    default_logging_handler = logging.StreamHandler(sys.stdout)
    default_logging_handler.setLevel(default_logging_level)
    default_logging_handler.setFormatter(logging.Formatter(logging_format))

    @classmethod
    def get_logger(cls, name, handler=None, logging_level=default_logging_level, propagate=default_logging_propagate,
                   fmt=logging_format, override=False):
        logger = logging.getLogger(name)

        if not logger.handlers or override:
            logger.setLevel(logging_level)
            logger.propagate = propagate

            if handler:
                if logger.handlers:
                    for hd in logger.handlers:
                        logger.removeHandler(hd)
                        print('removeHandler: {}'.format(hd))

                handler.setLevel(logging_level)
                handler.setFormatter(logging.Formatter(fmt))
                logger.addHandler(handler)

            print('[{}] logger configuration. level={}, propagate={}, handlers={}'.format(
                logger.name, logger.level, logger.propagate, logger.handlers))
        return logger

    @classmethod
    def get_rotating_file_logger(cls, log_file_path, name=default_logging_name, logging_level=default_logging_level,
                                 propagate=default_logging_propagate, fmt=logging_format, override=False,
                                 backup_count=30, max_bytes=1024 * 1024 * 500):
        """根据日志文件大小存储日志"""
        handler = handlers.RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count)
        logger = cls.get_logger(name=name, handler=handler, logging_level=logging_level, fmt=fmt, propagate=propagate,
                                override=override)
        return logger

    @classmethod
    def get_timed_rotating_file_logger(cls, log_file_path, name=default_logging_name,
                                       logging_level=default_logging_level, propagate=default_logging_propagate,
                                       fmt=logging_format, override=False, backup_count=30, when='MIDNIGHT',
                                       interval=1, delay=False):
        """根据日期存储日志"""
        handler = handlers.TimedRotatingFileHandler(
            log_file_path, when=when, interval=interval, backupCount=backup_count, delay=delay)
        logger = cls.get_logger(name=name, handler=handler, logging_level=logging_level, fmt=fmt, propagate=propagate,
                                override=override)
        return logger

    @classmethod
    def get_console_logger(cls, name=default_logging_name, logging_level=default_logging_level,
                           propagate=default_logging_propagate, fmt=logging_format, override=False):
        """不存储日志文件，输出到控制台"""
        handler = logging.StreamHandler(sys.stdout)
        logger = cls.get_logger(name=name, handler=handler, logging_level=logging_level, fmt=fmt, propagate=propagate,
                                override=override)
        return logger

    @classmethod
    def get_default_logger(cls):
        logger = logging.getLogger(cls.default_logging_name)
        if not logger.handlers:
            logger.addHandler(cls.default_logging_handler)
            logger.setLevel(cls.default_logging_level)
            logger.propagate = cls.default_logging_propagate
            print('[{}] logger configuration. level={}, propagate={}, handlers={}'.format(
                logger.name, logger.level, logger.propagate, logger.handlers))
        return logger


def log(log_args=False, log_result=False):
    """
    运行消耗时间日志注解
    :param log_args:    是否打印入参值
    :param log_result:  是否打印返回值
    """

    def decorator(func):
        def wrapper(*args, **kw):
            logger = LoggingUtil.get_default_logger()
            start = datetime.now()

            func_name = "[{}.{}]".format(func.__module__, func.__name__)
            args_log = ""
            if log_args:
                args_log = "{} {}".format(args, kw) if args or kw else inspect.signature(func)
                args_log = "\n>> {}".format(args_log) if args_log else ""
            logger.info('{} start...{}'.format(func_name, args_log))

            result = func(*args, **kw)

            result_log = "\n=> {}".format(result) if log_result else ""
            logger.info('{} end. \t ts: {} {}'.format(func_name, str(datetime.now() - start), result_log))
            return result
        return wrapper
    return decorator
