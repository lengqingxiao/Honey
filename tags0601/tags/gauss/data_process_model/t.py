# coding=gbk
v1 = [21, 34, 45]
v2 = [55, 25, 77]
#v = v2 - v1 # Error: TypeError: unsupported operand type(s) for -: 'list' and 'list'
v = list(map(lambda x: x[0]-x[1], zip(v2, v1)))
print v
print("%sn%sn%s" %(v1, v2, v))
