from __future__ import division

import pandas
import time
import calendar
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta


TIMESTAMP_SEC = 1e9
DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PRECISE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def format_time(_time=None, _format=DEFAULT_TIME_FORMAT):
    """时间格式化"""
    if not _time:
        return datetime.now().strftime(_format)
    return time.strftime(_format, _time)


def parse_nano_to_timetuple(timestamp):
    """时间戳转为timetuple类型"""
    return time.localtime(timestamp / (TIMESTAMP_SEC * 1.))


def parse_nano(timestamp, _format=DEFAULT_TIME_FORMAT):
    """时间戳转为时间字符串"""
    return format_time(parse_nano_to_timetuple(timestamp), _format)


def get_day_end_time(daytime=None):
    """获取一天的最大时间"""
    daytime = pandas.to_datetime(str(daytime)) if daytime else datetime.now()
    return dt.datetime.combine(daytime, dt.time.max)


def get_nano(_datetime=None, millisec=0):
    """
    字符串时间转换成时间戳.
    :param _datetime: 时间
    :param millisec: 毫秒数
    :return: 时间戳
    """
    _datetime = pandas.to_datetime(str(_datetime)) if _datetime else datetime.now()
    return (int(time.mktime(pandas.to_datetime(_datetime).timetuple())) + float(millisec) / 1000.) * TIMESTAMP_SEC


def delta_time(_datetime=None, months=0, days=0, hours=0, minutes=0, seconds=0):
    _datetime = pandas.to_datetime(datetime.now() if _datetime is None else str(_datetime))
    _datetime += relativedelta(months=months, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return _datetime


def delta_and_format_time(_datetime=None, minutes=0, days=0, months=0, seconds=0, _format=DEFAULT_TIME_FORMAT):
    return format_time(delta_time(_datetime, minutes=minutes, days=days, months=months, seconds=seconds).timetuple(),
                       _format=_format)


def get_month_days(year=None, month=None):
    """获取月份的天数"""
    m_years = 0
    if month is not None:
        m_years = int(month / 12)
        month = month % 12
        if month == 0:
            month = 12

    if year is None or month is None:
        now_timetuple = datetime.now().timetuple()
        if year is None:
            year = now_timetuple.tm_year
        if month is None:
            month = now_timetuple.tm_mon

    year += m_years
    mdays = calendar.monthrange(year, month)[1]
    return mdays


def cal_time_diff(time1, time2, auto_across_day=False):
    start_time = pandas.to_datetime(time1)
    end_time = pandas.to_datetime(time2)
    if auto_across_day and start_time > end_time:  # 跨天
        end_time += relativedelta(days=1)
    return end_time - pandas.to_datetime(start_time)


def cal_time_diff_seconds(time1, time2, auto_across_day=False):
    return cal_time_diff(time1, time2, auto_across_day).total_seconds()


def cal_time_diff_minutes(time1, time2, auto_across_day=False):
    return cal_time_diff_seconds(time1, time2, auto_across_day) / 60.


def is_including_time_period(_time, time_s, time_e):
    """判断时间是否在指定时间段中"""
    hm = pandas.to_datetime(_time)
    for i in range(0, len(time_s), 1):
        if time_s[i] != time_e[i]:
            start_time = pandas.to_datetime(time_s[i])
            end_time = pandas.to_datetime(time_e[i])
            condition1 = hm >= start_time
            condition2 = hm <= end_time
            condition0 = (condition1 and condition2) if (start_time < end_time) else (condition1 or condition2)
            if condition0:
                return i
    return -1


def is_work_day_time(daytime, holiday_time_arr, weekend_workday_time_arr):
    """是否是工作日"""
    daytime = pandas.to_datetime(str(daytime))
    # 周六周日
    if daytime.timetuple().tm_wday >= 5:
        if weekend_workday_time_arr:
            for t in weekend_workday_time_arr:
                st, et = [pandas.to_datetime(s) for s in t.split(' - ')]
                if st <= daytime <= et:
                    return True
        return False
    # 周一至周五
    if holiday_time_arr:
        for t in holiday_time_arr:
            holiday_start_time, holiday_end_time = [pandas.to_datetime(s) for s in t.split(' - ')]
            if holiday_start_time <= daytime <= holiday_end_time:
                return False
    return True


def get_next_workday(daytime, holiday_time_arr, weekend_workday_time_arr):
    """获取下一个工作日"""
    day_dt = pandas.to_datetime(str(daytime))

    if holiday_time_arr or weekend_workday_time_arr:
        while True:
            day_dt = delta_and_format_time(day_dt, days=1, _format="%Y%m%d")
            if is_work_day_time(day_dt, holiday_time_arr, weekend_workday_time_arr):
                return int(day_dt)
    else:
        daytime_timetuple = daytime.timetuple()
        delta_day = 1 if (daytime_timetuple.tm_wday < 4) else (7 - daytime_timetuple.tm_wday)
        return int(delta_and_format_time(day_dt, days=delta_day, _format="%Y%m%d"))
