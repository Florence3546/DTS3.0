# coding=UTF-8
'''
日期、时间处理工具类
Created on 2011-09-07
@author: zhangyu
'''

import datetime
import time


def generate_timestamp():
    '''根据当前时间获取时间戳，返回整数'''
    return int(time.time())


def date_2datetime(dt):
    """
    date_2datetime(datetime.date(2013,7,13))
    >>> datetime.datetime(2013,7,13,0,0)
    """
    return datetime.datetime(dt.year, dt.month, dt.day)

def format_datetime(dt):
    """将mongodb保存的时间转格式，去除毫秒精度"""
    if not dt:
        return None
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def datetime_2string(dt = None, fmt = '%Y-%m-%d-%H-%M'):
    '''将datetime类型转换为字符串'''
    if not dt:
        dt = datetime.datetime.now()
    return datetime.datetime.strftime(dt, fmt)

def string_2datetime(dt_str, fmt = '%Y-%m-%d %H:%M:%S'):
    '''将字符串转换为datetime类型
    >>> string_2datetime("2011-09-07 12:30:09")
    datetime.datetime(2011, 9, 7, 12, 30, 9)
    '''
    return datetime.datetime.strptime(dt_str, fmt)

def string_2datetime2(dt_str, fmt = '%Y-%m-%d'):
    return string_2datetime(dt_str[:10], fmt)

def string_2date(dt_str):
    '''将字符串转换为datet类型'''
    return datetime.datetime.strptime(dt_str, '%Y-%m-%d').date()

def get_start_datetime(dt = None):
    '''根据日期、或时间取得当日00:00:00的时间；参数可以是date或datetime类型'''
    start = None
    if not dt:
        dt = datetime.date.today()
    if isinstance(dt, datetime.date):
        dt_str = dt.strftime("%Y-%m-%d") + " 00:00:00"
        start = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return start

def get_end_datetime(dt = None):
    '''根据日期、或时间取得当日23:59:59的时间；参数可以是date或datetime类型'''
    end = None
    if not dt:
        dt = datetime.date.today()
    if isinstance(dt, datetime.date):
        dt_str = dt.strftime("%Y-%m-%d") + " 23:59:59"
        end = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return end

def get_time_delta(begin_dt, end_dt, time_fmt = None):
    '''获取时间差，根据time_fmt返回数据，如果time_fmt=None，则返回days,hours,minutes,seconds'''
    days, hours, minutes, seconds = None, None, None, None
    if isinstance(begin_dt, datetime.date) and isinstance(end_dt, datetime.date):
        days = (end_dt - begin_dt).days
        left_seconds = (end_dt - datetime.timedelta(days = days) - begin_dt).seconds
        hours = left_seconds / 3600
        tmp_seconds = left_seconds - hours * 3600
        minutes = tmp_seconds / 60
        seconds = tmp_seconds - minutes * 60

    if time_fmt == "DAYS":
        return days
    elif time_fmt == "HOURS":
        return days * 24 + hours
    elif time_fmt == "MINUTES":
        return (days * 24 + hours) * 60 + minutes
    elif time_fmt == "SECONDS":
        return (days * 24 * 3600) + left_seconds
    else:
        return days, hours, minutes, seconds

def time_is_someday(dt, days = 0):
    '''判断datetime或date是否是哪一天，默认是今天'''
    if not dt:
        return False
    someday = datetime.date.today() - datetime.timedelta(days = days)
    if isinstance(dt, datetime.datetime):
        return dt.date() == someday
    elif isinstance(dt, datetime.date):
        return dt == someday
    return False

def time_is_ndays_interval(dt, ndays):
    '''计算datetime或date与今天是否相差n天，ndays为正数表示相差过去n天，为负数表示相差今后n天'''
    if not dt:
        return False
    before_ndays = datetime.date.today() - datetime.timedelta(days = ndays)
    if isinstance(dt, datetime.datetime):
        return dt.date() <= before_ndays
    elif isinstance(dt, datetime.date):
        return dt <= before_ndays
    return False

def time_is_recent(dt, **kwargs):
    """这个函数其实跟上面的类似，只不过能够支持对hour、second进行判断"""
    if dt and isinstance(dt, datetime.datetime) and kwargs and (not set(kwargs.keys()) - set(['days', 'hours', 'minutes', 'seconds'])):
        last_time = datetime.datetime.now() - datetime.timedelta(**kwargs)
        return dt >= last_time
    else:
        return False

def time_humanize(dt):
    '''将时间转换为"n天前"，使其更人性化，增加可读性'''
    result = ""
    if dt:
        time = ""
        if isinstance(dt, datetime.datetime):
            time = dt.strftime('%H:%M')
            dt = dt.date()
        days = (datetime.date.today() - dt).days
        if days == 0:
            result = "今天 %s" % time
        elif days == 1:
            result = "昨天 %s" % time
        elif days == 2:
            result = "前天 %s" % time
        elif days > 2:
            result = "%s天前" % days
        return result
    return dt

def days_diff_interval(ed):
    """ 获取日期与当前日期相差的天数"""
    if not ed:
        return -1
    bd = datetime.date.today()
    oneday=datetime.timedelta(days=1)
    count=0
    if ed>bd:
        while bd!=ed:
            ed=ed-oneday
            count+=1
        return count
    elif ed==bd:
        return 0
    else:
        while bd!=ed:
            ed=ed+oneday
            count-=1
        return count

