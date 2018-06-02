# -*- coding: utf-8 -*-
########################################################################################################################
# 关于时间处理的辅助函数
########################################################################################################################

import datetime


def now_datetime_str():
    """
    显示当前时间
    return: 字符串格式
    """
    date_time_now = datetime.datetime.now()
    date_time_str = date_time_now.strftime('%Y-%m-%d %H:%M:%S')

    return date_time_str


def datetime_str_tran(date_time_str):
    """
    将字符串格式时间转成 datetime 格式
    param : date_time_str: 需要转换的时间
    return : datetime
    """
    try:
        date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print e
        date_time = None
    return date_time


def diff_months(datetime_a, datetime_b):
    """
    计算两个datetime 相差几个自然月
    param0: datetime_a: 格式 datetime
    param1:datetime_b: 格式 datetime
    return: int
    """
    year_a = datetime_a.year
    year_b = datetime_b.year
    month_a = datetime_a.month
    month_b = datetime_b.month

    return (year_a-year_b)*12+(month_a-month_b)
