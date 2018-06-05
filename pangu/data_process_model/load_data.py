# -*- coding:gbk -*-

import pandas as pd
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
data = pd.read_csv('D:/jd_luxury.csv')
# data['goods_names'] = data['goods_names'].astype(unicode)
print(data)
a = data['goods_names'].values[0]
print(type(data['goods_names'].values[0]))


# def str2uni(x):
#     if type(x) == str:
#         return x.decode('gb2312')
# #
# #
# data['goods_names'] = data['goods_names'].apply(str2uni)
# print data
