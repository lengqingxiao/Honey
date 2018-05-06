# -*- coding:utf-8 -*-
########################################################################################################################
# 全局配置清单
########################################################################################################################
# MYSQL 查询语句配置
QUERY_SQL_ALL = "SELECT e.*,u.age,u.jobType,u.sex,u.os,u.maxLevel,u.province from" \
                "(SELECT c.*, d.zmScore,d.huabeiQuota,d.JdXiaobai, d.JdBaitiaoQuota, d.mobile from" \
                "(SELECT a.*,b.lastreview_decision,b.has_borrowed from" \
                "(select * from alz_order where order_time BETWEEN '%s' and '%s') a " \
                "LEFT OUTER JOIN alz_order_review b on a.order_code = b.order_code) c " \
                "LEFT OUTER JOIN alz_order_credit d on c.order_code = d.order_code) e " \
                "LEFT OUTER JOIN alz_order_user u on e.order_code = u.order_code"
# 订单类型映射
ORDER_TYPE_MAP = {'30': 1, '31': 1, '32': 1, '34': 1, '20': 1, '21': 1, '35': 2, '37': 2, '33': 3, '43': 4, '42': 5,
                  '44': 6, '40': 7, '41': 8, '36': 9}
