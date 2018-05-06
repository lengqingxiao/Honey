# -*- coding: utf-8 -*-
# # import jieba
# import re
#
# raw_str = "根据运营商详单数据，连续三天以上无通话记录3次: 2016-05-18 - 2016-07-07, 51天 / 2016-07-09 - " \
#           "2016-08-07, 30天 / 2016-08-13 - 2016-08-23, 11天"
#
#
# a = raw_str.split(':')[1]
# b = a.split('/')
#
#
# k = raw_str.split()[1]
#
# e = re.sub("\D","", c.split(',')[1])

# import pymongo
# client = pymongo.MongoClient('47.96.38.60', 3717)
# db = client['analysis']
# db.authenticate("analysisUser", "AnalysisUser123")
# collection = db['MobileVerifyDataCol']
# collection_a = collection.find({'mobile': '18677827374'})
# list_a = list(collection_a)[0]
# print len(list_a)
# print list_a

import pymongo
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['elephant']
# db.authenticate("analysisUser", "AnalysisUser123")
collection = db['honey_bee']
collection_a = collection.find({'mobile': '18677827374'})
list_a = list(collection_a)[0]
print len(list_a)
print list_a
