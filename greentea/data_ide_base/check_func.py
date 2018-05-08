# -*- coding: utf-8 -*-
########################################################################################################################
# 函数定义 （用于连续属性分箱）
########################################################################################################################


def check_night_fre(data):

    if u'频繁' in data:
        return 3
    elif u'偶尔' in data:
        return 2
    elif u'很少' in data:
        return 1
    else:
        return 0


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
        return 0


def check_loc_fre(data):
    if u'未超过' in data:
        return 1
    elif u'至少' in data:
        return 2
    else:
        return 0


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
        return 0


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
        return 0


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
        return 0
