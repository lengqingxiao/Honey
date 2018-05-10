# -*- coding:utf-8 -*-
########################################################################################################################
# 全局配置清单
########################################################################################################################

"""
 全局清单配置

"""

"""
国内省份列表

"""
# 省份元组
PROVINCE_LIST = (u'山东', u'江苏', u'上海', u'浙江', u'安徽', u'福建', u'江西', u'广东', u'广西', u'海南', u'河南',
                 u'湖南', u'湖北', u'北京', u'天津', u'河北', u'山西', u'内蒙古', u'宁夏', u'青海', u'陕西', u'甘肃',
                 u'新疆', u'四川', u'贵州', u'云南', u'重庆', u'西藏', u'辽宁', u'吉林', u'黑龙江', u'香港', u'澳门',
                 u'台湾', u'全国', u'运营商')
"""
中国省份区域划分
1 ====> 华东地区（包括山东、江苏、上海、浙江、安徽、福建、江西）HD
2 ====> 华南地区（包括广东、广西、海南）HN
3 ====> 华中地区（包括河南、湖南、湖北）HZ
4 ====> 华北地区（包括北京、天津、河北、山西、内蒙古）HB
5 ====> 西北地区（包括宁夏、青海、陕西、甘肃、新疆）XB
6 ====> 西南地区（包括四川、贵州、云南、重庆、西藏）XN
7 ====> 东北地区（包括辽宁、吉林、黑龙江）DB
8 ====> 港澳台地区（包括香港、澳门、台湾）GAT

"""
PROVINCE_MAP_DICT = {u'山东': 1, u'江苏': 1, u'上海': 1, u'浙江': 1, u'安徽': 1, u'福建': 1, u'江西': 1,
                     u'广东': 2, u'广西': 2, u'海南': 2,
                     u'河南': 3, u'湖南': 3, u'湖北': 3,
                     u'北京': 4, u'天津': 4, u'河北': 4, u'山西': 4, u'内蒙古': 4,
                     u'宁夏': 5, u'青海': 5, u'陕西': 5, u'甘肃': 5, u'新疆': 5,
                     u'四川': 6, u'贵州': 6, u'云南': 6, u'重庆': 6, u'西藏': 6,
                     u'辽宁': 7, u'吉林': 7, u'黑龙江': 7,
                     u'香港': 8, u'澳门': 8, u'台湾': 8,
                     u'全国': 9, u'运营商': 9, u'未知': 9}

# 经济较发达省份 edp
ECONOMICALLY_DEVELOPED_PROVINCES = [u'广东', u'江苏', u'山东', u'浙江', u'四川', u'北京', u'上海']
# 老赖top 10 省份 dpt
DEADBEAT_PROVINCES_TOP10 = [u'江苏', u'山东', u'浙江', u'河南', u'广东', u'安徽', u'福建', u'重庆', u'黑龙江', u'四川']

"""
发达国家列表 世界公认18个发达国家  ddc

"""
DEVELOPED_COUNTRY = [u'美国', u'加拿大', u'日本', u'英国', u'法国', u'德国', u'意大利', u'荷兰', u'比利时', u'卢森堡',
                     u'瑞士', u'奥地利', u'挪威', u'瑞典', u'丹麦', u'芬兰', u'澳大利亚', u'新西兰']

"""
信用卡逾期高发省份 cc_hrp

1 天津 2 江西 3 重庆 4 四川 5 黑龙江 6 福建

"""
CC_HIGH_RISK_PROVINCES = [u'天津', u'福建', u'江西', u'重庆', u'四川', u'黑龙江']

"""
用户行为检查特征结果列表 用于结果检查 behavior_check_result_list

"""

BEHAVIOR_CHECK_TUPLE = ('user_mobile_use_time', 'cpc_user_no_call_days', 'cpc_user_3days_no_call_cnt',
                        'cpc_user_max_silent_days', 'cpc_user_silent_days', 'cpc_user_high_risk_cnt',
                        'cpc_user_high_risk_cnt_ratio', 'user_if_contact_am', 'user_if_contact_110',
                        'user_if_contact_120', 'user_if_contact_lawyer', 'user_if_contact_court',
                        'user_call_night_fre', 'user_call_loan_fre', 'user_call_bank_fre', 'user_call_cc_fre',
                        'user_address_use_in_eb_fre', 'user_eb_use_fre', 'user_eb_self_use_fre', 'user_vg_buy_fre',
                        'user_lt_buy_fre', 'user_address_change_fre')
"""
通话信息字段表

"""
USER_CONTACT_COLUMNS = ('call_cnt', 'call_in_cnt', 'call_out_cnt', 'contact_1m', 'contact_1w', 'contact_3m',
                        'contact_3m_plus', 'contact_afternoon', 'contact_early_morning', 'contact_holiday',
                        'contact_morning', 'contact_night', 'contact_noon', 'contact_weekday', 'contact_weekend')

USER_CONTACT_RESULT = ('call', 'call_in', 'call_out', 'contact_p1m', 'contact_p1w', 'contact_p3m', 'contact_po3m',
                       'contact_afternoon', 'contact_early_morning', 'contact_holiday', 'contact_morning',
                       'contact_night', 'contact_noon', 'contact_weekday', 'contact_weekend')


CHINA_LOC = ('HD', 'HN', 'HZ', 'HB', 'XB', 'XN', 'DB', 'GAT')

CONTACT_REGION = (u'region_avg_call_in_time', u'region_avg_call_out_time', u'region_call_in_cnt',
                  u'region_call_in_cnt_pct', u'region_call_in_time', u'region_call_in_time_pct',
                  u'region_call_out_cnt', u'region_call_out_cnt_pct', u'region_call_out_time',
                  u'region_call_out_time_pct', u'region_uniq_num_cnt')

CELL_BEHAVIOR = (u'cpc_call_cnt_p6m', u'cpc_avg_call_cnt_p6m',
                 u'cpc_call_in_cnt_p6m', u'cpc_avg_call_in_cnt_p6m',
                 u'cpc_call_out_cnt_p6m', u'cpc_avg_call_out_cnt_p6m',
                 u'cpc_call_in_time_p6m', u'cpc_avg_call_in_time_p6m',
                 u'cpc_call_out_time_p6m', u'cpc_avg_call_out_time_p6m',
                 u'cpc_net_flow_p6m', u'cpc_avg_net_flow_p6m', u'cpc_sms_cnt_p6m',
                 u'cpc_avg_sms_cnt_p6m', u'cpc_call_cnt_p3m',
                 u'cpc_avg_call_cnt_p3m', u'cpc_call_in_cnt_p3m',
                 u'cpc_avg_call_in_cnt_p3m', u'cpc_call_out_cnt_p3m',
                 u'cpc_avg_call_out_cnt_p3m', u'cpc_call_in_time_p3m',
                 u'cpc_avg_call_in_time_p3m', u'cpc_call_out_time_p3m',
                 u'cpc_avg_call_out_time_p3m', u'cpc_net_flow_p3m',
                 u'cpc_avg_net_flow_p3m', u'cpc_sms_cnt_p3m', u'cpc_avg_sms_cnt_p3m',
                 u'cpc_call_cnt_p2m', u'cpc_avg_call_cnt_p2m', u'cpc_call_in_cnt_p2m',
                 u'cpc_avg_call_in_cnt_p2m', u'cpc_call_out_cnt_p2m',
                 u'cpc_avg_call_out_cnt_p2m', u'cpc_call_in_time_p2m',
                 u'cpc_avg_call_in_time_p2m', u'cpc_call_out_time_p2m',
                 u'cpc_avg_call_out_time_p2m', u'cpc_net_flow_p2m',
                 u'cpc_avg_net_flow_p2m', u'cpc_sms_cnt_p2m', u'cpc_avg_sms_cnt_p2m',
                 u'cpc_call_cnt_p1m', u'cpc_call_in_cnt_p1m', u'cpc_call_out_cnt_p1m',
                 u'cpc_call_in_time_p1m', u'cpc_call_out_time_p1m', u'cpc_net_flow_p1m',
                 u'cpc_sms_cnt_p1m')

TRIP_INFO_RESULT = (
                u'cpc_trip_long_tsp', u'cpc_trip_his_cnt',
                u'cpc_trip_his_total_days', u'cpc_trip_his_avg_days',
                u'cpc_trip_his_tll_cnt', u'cpc_trip_his_tdl_cnt',
                u'cpc_trip_his_fp_pct', u'cpc_trip_his_fp_total_cnt',
                u'cpc_trip_his_fp_total_cnt_ratio', u'cpc_trip_his_fet_tsp',
                u'cpc_trip_his_let_tsp', u'cpc_trip_holiday_total_pct',
                u'cpc_trip_holiday_total_pct_ratio', u'cpc_trip_holiday_days_cnt',
                u'cpc_trip_holiday_avg_days', u'cpc_trip_holiday_days_cnt_ratio',
                u'cpc_trip_weekend_total_pct', u'cpc_trip_weekend_total_pct_ratio',
                u'cpc_trip_weekend_days_cnt', u'cpc_trip_weekend_avg_days',
                u'cpc_trip_weekend_days_cnt_ratio', u'cpc_trip_workday_total_pct',
                u'cpc_trip_workday_total_pct_ratio', u'cpc_trip_workday_days_cnt',
                u'cpc_trip_workday_avg_days', u'cpc_trip_workday_days_cnt_ratio',
                u'cpc_trip_tll_esb_pct', u'cpc_trip_tll_esb_total_days',
                u'cpc_trip_tdl_esb_pct', u'cpc_trip_tdl_esb_total_days',
                u'cpc_trip_tll_esm_pct', u'cpc_trip_tll_esm_total_days',
                u'cpc_trip_tdl_esm_pct', u'cpc_trip_tdl_esm_total_days',
                u'cpc_trip_tll_esb_pct_ratio', u'cpc_trip_tll_esb_total_days_ratio',
                u'cpc_trip_tdl_esb_pct_ratio', u'cpc_trip_tdl_esb_total_days_ratio',
                u'cpc_trip_tll_esm_pct_ratio', u'cpc_trip_tll_esm_total_days_ratio',
                u'cpc_trip_tdl_esm_pct_ratio', u'cpc_trip_tdl_esm_total_days_ratio')

ORG_TYPE = (
    u'租车', u'招聘', u'房地产', u'电商', u'银行', u'运营商', u'支付', u'投资理财', u'贷款', u'汽车', u'个人',
    u'健身', u'互联网', u'投资担保', u'贷款/融资', u'保险', u'短号', u'基金', u'旅游出行', u'快递', u'APP软件',
    u'政府机构', u'婚庆'
)

ORG_RESULT = ('crt', 'rec', 'res', 'eb', 'bank', 'opt', 'pay', 'iaf', 'loan', 'car', 'ps',
              'gym', 'net', 'ig', 'lof', 'ins', 'sn', 'fund', 'trv', 'exp', 'app', 'gov', 'wed')

SERVICE_TIME_TAGS = ('p1m', 'p2m', 'p3m')

SR_0 = ['cpc_ser_%s_cnt' % i for i in ORG_RESULT]
SR_1 = ['cpc_ser_%s_org_cnt' % i for i in ORG_RESULT]
SR_2 = ['cpc_ser_%s_cnt_%s' % (k, v) for k in ORG_RESULT for v in SERVICE_TIME_TAGS]
SR_3 = ['cpc_ser_%s_org_cnt_%s' % (k, v) for k in ORG_RESULT for v in SERVICE_TIME_TAGS]
SR_4 = ['cpc_ser_%s_cnt_ratio_%s' % (k, v) for k in ORG_RESULT for v in SERVICE_TIME_TAGS]
SR_5 = ['cpc_ser_%s_cnt_ratio' % i for i in ORG_RESULT]
SR_6 = ['cpc_avg_ser_%s_cnt_p3m' % i for i in ORG_RESULT]
SR_B = ['cpc_total_ser_cnt_%s', 'cpc_total_ser_org_cnt_%s', 'cpc_total_ser_org_type_cnt_%s']
SR_7 = [k % v for k in SR_B for v in SERVICE_TIME_TAGS]
S = ('cpc_total_ser_cnt', 'cpc_total_ser_org_cnt', 'cpc_total_ser_org_type_cnt')
SERVICE_RESULT = S + tuple(SR_0) + tuple(SR_1) + tuple(SR_2) + tuple(SR_3) + tuple(SR_4) + tuple(SR_5) + tuple(SR_6) + \
                 tuple(SR_7)

# cpc_total_ser_cnt_p1m
# cpc_total_ser_org_cnt_p1m
# cpc_total_ser_org_type_cnt_p1m
#
# cpc_total_ser_cnt_p2m
# cpc_total_ser_org_cnt_p2m
# cpc_total_ser_org_type_cnt_p2m
#
# cpc_total_ser_cnt_p3m
# cpc_total_ser_org_cnt_p3m
# cpc_total_ser_org_type_cnt_p3m



