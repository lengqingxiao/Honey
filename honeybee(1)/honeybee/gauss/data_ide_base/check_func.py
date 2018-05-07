# -*- coding: utf-8 -*-
########################################################################################################################
# binning 函数定义 （用于连续属性分箱）
########################################################################################################################


def binning_zm_score(x):

    if x < -100:
        zm_grade = x
    elif -100 <= x < 0:
        zm_grade = -1
    elif 0 <= x < 600:
        zm_grade = 0
    elif 600 <= x < 650:
        zm_grade = 1
    elif 650 <= x < 700:
        zm_grade = 2
    elif 700 <= x < 750:
        zm_grade = 3
    else:
        zm_grade = 4

    return zm_grade


def binning_hua_bei(x):
    if x < 0:
        return x
    elif 0 <= x < 5000:
        return 0
    elif 5000 <= x < 10000:
        return 1
    elif 10000 <= x < 15000:
        return 2
    elif 15000 <= x < 20000:
        return 3
    else:
        return 4


def binning_jd_xb_score(x):
    if x < 0:
        return x
    elif 0 <= x < 80:
        return 0
    elif 80 <= x < 85:
        return 1
    elif 85 <= x < 90:
        return 2
    elif 90 <= x < 95:
        return 3
    elif 95 <= x < 100:
        return 4
    else:
        return 5


def binning_jd_bt(x):
    if x < 0:
        return x
    elif 0 <= x < 5000:
        return 0
    elif 5000 <= x < 10000:
        return 1
    elif 10000 <= x < 15000:
        return 2
    elif 15000 <= x < 20000:
        return 3
    else:
        return 4


def binning_age(x):
    if x < 0:
        return x
    elif 0 <= x < 18:
        return 0
    elif 18 <= x < 25:
        return 1
    elif 25 <= x < 30:
        return 2
    elif 30 <= x < 35:
        return 3
    elif 35 <= x < 40:
        return 4
    elif 40 <= x < 50:
        return 5
    else:
        return 6


def binning_order_amount(x):
    # 分为单位
    if x < 0:
        return x
    elif 0 <= x <= 20000:
        return 0
    elif 20000 < x <= 50000:
        return 1
    elif 50000 < x <= 100000:
        return 2
    elif 100000 < x <= 300000:
        return 3
    elif 300000 < x <= 500000:
        return 4
    else:
        return 5
