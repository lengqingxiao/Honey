# # coding=gbk
# v1 = [21, 34, 45]
# v2 = [55, 25, 77]
# #v = v2 - v1 # Error: TypeError: unsupported operand type(s) for -: 'list' and 'list'
# v = list(map(lambda x: x[0]-x[1], zip(v2, v1)))
# print v
# print("%sn%sn%s" %(v1, v2, v))
# d = {'a':1,'b':4,'c':2}
# print d.values()
# f = zip(d.values(),d.keys())
# h = sorted(f)
# print h

d = {1: 1, 2: 0, 3: 2}
f = zip(d.values(), d.keys())
h = sorted(f)
print h

# cc = min(d, key=d.get)
# print cc
# cc1 = max(d, key=d.get)
# print cc1
#
# dd = {1: 1, 2: 0, 3: 2}
# max(dd, key=dd.get)
