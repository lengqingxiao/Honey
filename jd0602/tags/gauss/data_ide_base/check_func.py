# -*- coding: utf-8 -*-
########################################################################################################################
# 部分计算函数定义
########################################################################################################################
from config.global_config import *


def check_night_fre(data):

    if u'频繁' in data:
        return 3
    elif u'偶尔' in data:
        return 2
    elif u'很少' in data:
        return 1
    else:
        return -999


def check_number_fre(data):

    if u'经常' in data:
        return 4
    elif u'偶尔' in data:
        return 3
    elif u'很少' in data:
        return 2
    elif u'无该类号码记录':
        return 1
    else:
        return -999


def check_loc_fre(data):
    if u'未超过' in data:
        return 1
    elif u'至少' in data:
        return 2
    else:
        return -999


def check_eb_use_fre(data):
    if u'经常' in data:
        return 4
    elif u'偶尔' in data:
        return 3
    elif u'很少' in data:
        return 2
    elif u'基本' in data:
        return 1
    else:
        return -999


def check_buy_fre(data):
    if u'大量' in data:
        return 4
    elif u'经常' in data:
        return 3
    elif u'基本' in data:
        return 2
    elif u'从未购买' in data:
        return 1
    else:
        return -999


def check_address(data):
    if u'经常' in data:
        return 4
    elif u'偶尔' in data:
        return 3
    elif u'少量' in data:
        return 2
    elif u'无使用记录' in data:
        return 1
    else:
        return -999


class CheckDataForJD(object):

    def __init__(self):
        pass

    @staticmethod
    def check_order_status(x):
        """
        order status check :  已完成/充值成功 ========> 1
                              已取消 ========> 2
                              等待收货 ========> 3
                              等待付款 ========>4
                              失败 ========>5
                              其他 ========>6
        """
        if x in [u'已完成', u'充值成功']:
            return 1
        elif x == u'已取消':
            return 2
        elif x == u'等待收货':
            return 3
        elif x in [u'待付款', u'等待付款']:
            return 4
        else:
            if u'失败' in x:
                return 5
            else:
                return 6

    @staticmethod
    def check_order_pay_type(x):
        """
        order pay channel check : 在线支付 =====> 1
                                  在线支付/白条 =====> 2
                                  混合支付 =====> 3
                                  货到付款 =====> 4
                                  公司转账 =====> 5

        """
        if x == u'在线支付':
            return 1
        elif x == u'在线支付/白条':
            return 2
        elif x == u'混合支付':
            return 3
        elif x == u'货到付款':
            return 4
        elif x == u'公司转账':
            return 5
        else:
            return 6

    @staticmethod
    def check_order_amount_type(x):
        if type(x) == str or unicode:
            return float(x)
        else:
            return x

    @staticmethod
    def get_order_time_year_mouth(x):
        return str(x)[0:7]

    @staticmethod
    def get_order_time_year_mouth_days(x):
        return str(x)[0:10]

    @staticmethod
    def get_order_time_mouth(x):
        return str(x)[5:7]

    @staticmethod
    def get_order_time_hour(x):
        return str(x)[10:13]

    @staticmethod
    def map_mouth_to_quarter(x):
        _m = int(x)
        if _m < 4:
            return 1
        elif 4 <= _m < 7:
            return 2
        elif 7 <= _m < 10:
            return 3
        else:
            return 4

    @staticmethod
    def check_order_amount_config(values):
        def check_order_amount(x):
            if x > values:
                return 1
            else:
                return 0
        return check_order_amount

    @staticmethod
    def check_order_goods_type_config(check_list):
        def check_order_goods_type(x):
            _res = []
            for _i in check_list:
                if _i in x:
                    _res.append(1)
                else:
                    _res.append(0)
            if sum(_res) > 0:
                return 1
            else:
                return 0
        return check_order_goods_type

    @staticmethod
    def map_order_time(x):
        x = int(x)
        if 0 <= x < 6:
            return 1
        elif 6 <= x < 9:
            return 2
        elif 9 <= x < 12:
            return 3
        elif 12 <= x < 15:
            return 4
        elif 15 <= x < 19:
            return 5
        else:
            return 6


    # @staticmethod
    # def map_year_month(x):
    #     return x['year_month'].values[0][0:6] + str(x['quarter_tags'].values[0])
    @staticmethod
    def check_order_goods_type_1(x):
        _res = []
        for _i in USER_FOR_CHECK_HOUSEHOLD:
            if _i in x:
                _res.append(1)
            else:
                _res.append(0)
        if sum(_res) > 0:
            return 1
        else:
            return 0


