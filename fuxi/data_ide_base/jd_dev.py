# -*- coding: utf-8 -*-
import itertools


mylist = [1,1,0,1,1,1,0,0,0,0,1,1,1,1,0,1,0,1,1,0]
num_times = [(k, len(list(v))) for k, v in itertools.groupby(mylist)]
print num_times
aa = [m for m in num_times if m[0] ==1]
print aa
aa1 = [n for n in aa if n[1] > 1]
print aa1
bb = max(aa)
print bb

# mylist = [1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 11, 0]
#
# result = {}
# tmp = None
# for i in mylist:
#     if not result.has_key(i):
#         # 新出现的值为1
#         result[i] = {'tmpcount': 1, 'maxcount': 1}
#     else:
#         if i == tmp:
#             # 同上一次相同,tmpcount数字加一,同时更新maxcount
#             result[tmp]['tmpcount'] = result[tmp]['tmpcount'] + 1
#             if result[tmp]['maxcount'] < result[tmp]['tmpcount']:
#                 result[tmp]['maxcount'] = result[tmp]['tmpcount']
#         else:
#             # 如果不同，上次数字的tmpcount归零，这次的数字的tmpcount归一
#             result[i]['tmpcount'] = 1
#             result[tmp]['tmpcount'] = 0
#     tmp = i
#
# for j, k in result.items():
#     print '数字' + str(j) + '出现的最大连续次数为' + str(k['maxcount'])