# -*- coding:utf-8 -*-
########################################################################################################################
# 数据预处理
########################################################################################################################

import time
import datetime
from pandas.tseries import offsets
from data_query import *
from data_transform import *
from config.global_config import *
from data_model.nlp import *
from data_ide_base.check_func import CheckDataForJD


class ProcessDataForHoneybee(object):

    def __init__(self, cal_data):
        # 18168724419  18677827374 15625867469 15831842620 18382035538 18847790755 18329468073
        self.raw_data = cal_data
        # self.raw_data = QueryData.query_data_from_mongodb('127.0.0.1', 27017, 'elephant', 'honey_bee',
        #                                                   ['report_data', 'mobile'], 'mobile', '18382035538')
        # self.raw_data = QueryData.query_data_from_mongodb('47.96.38.60', 3717, 'analysis', 'MobileVerifyDataCol',
        #                                                   ['report_data', 'mobile'], 'mobile', '18329468073')
        self.contact_list = TransformData.data_transform_from_dict(self.raw_data['report_data'], 'contact_list')
        self.contact_region = TransformData.data_transform_from_dict(self.raw_data['report_data'], 'contact_region')
        self.main_service = self.reshape_data_for_main_service()
        self.trip_info = TransformData.data_transform_from_dict(self.raw_data['report_data'], 'trip_info')
        self.calculate_time_diff_func()
        self.cell_behavior = TransformData.data_transform_from_dict(self.raw_data['report_data']['cell_behavior'][0],
                                                                    'behavior')
        self.application_check_list = self.raw_data['report_data']['application_check']
        self.behavior_check = TransformData.data_transform_from_dict(self.raw_data['report_data'], 'behavior_check')
        self.user_info = self.raw_data['report_data']['user_info_check']
        self.report_time = self.raw_data['report_data']['report'].get('update_time')[0:10]
        self.check_data_for_region()
        self.home_loc = self.calculate_home_loc_func()

    @property
    def get_report_time(self):

        return self.raw_data['report_data']['report'].get('update_time')[0:10]

    @property
    def get_user_cellphone_registration_location(self):

        return self.cell_behavior['cell_loc'].values[0]

    @property
    def get_user_birthplace_province(self):

        return self.application_check_list[1].get('check_points').get('province')

    def reshape_data_for_main_service(self):
        result_list = []
        for _i in self.raw_data['report_data']['main_service']:
            t_df = TransformData.data_transform_from_dict(_i, 'service_details')
            t_df['total_service_cnt'] = _i.get('total_service_cnt')
            t_df['company_type'] = _i.get('company_type')
            t_df['company_name'] = _i.get('company_name')
            result_list.append(t_df)
        result_df = pd.concat(result_list)
        return result_df

    def calculate_times_for_service(self, pre_months):

        return str((datetime.datetime.strptime(self.report_time, "%Y-%m-%d") -
                    pd.tseries.offsets.DateOffset(months=pre_months)))[0:7]

    @classmethod
    def check_mobile_func(cls, x):

        if x[0] != 0 and len(x) == 11:
            return 1
        else:
            return 0

    @classmethod
    def check_abroad_func(cls, x):

        if x in PROVINCE_LIST:
            return 1
        else:
            return 0

    @classmethod
    def check_unknown_func(cls, x):

        if x == u'未知':
            return 1
        else:
            return 0

    @classmethod
    def check_high_risk_func(cls, x):

        if x in CC_HIGH_RISK_PROVINCES:
            return 1
        else:
            return 0

    @classmethod
    def check_deadbeat_province_func(cls, x):
        if x in DEADBEAT_PROVINCES_TOP10:
            return 1
        else:
            return 0

    @classmethod
    def check_country_func(cls, x):
        if x in DEVELOPED_COUNTRY:
            return 1
        else:
            return 0

    @classmethod
    def check_province_economy_degree(cls, x):
        if x in ECONOMICALLY_DEVELOPED_PROVINCES:
            return 1
        else:
            return 0

    @classmethod
    def calculate_time_func_n(cls, x):
        return datetime.datetime.strptime(str(x), "%Y-%m-%d")

    @classmethod
    def calculate_diff_days(cls, x):
        return x.days + 1

    def calculate_time_diff_func(self):
        # 节假日 双休日 工作日
        if not self.trip_info.empty:
            self.trip_info['trip_end_time_n'] = self.trip_info['trip_end_time'].apply(self.calculate_time_func_n)
            self.trip_info['trip_start_time_n'] = self.trip_info['trip_start_time'].apply(self.calculate_time_func_n)
            self.trip_info['trip_diff_days'] = (self.trip_info['trip_end_time_n'] -
                                                self.trip_info['trip_start_time_n']).apply(self.calculate_diff_days)
            self.trip_info['trip_loc_combine'] = self.trip_info['trip_dest'] + self.trip_info['trip_leave']

    def calculate_home_loc_func(self):
        ubp_raw = self.get_user_birthplace_province
        if len(ubp_raw) < 3:
            _ubp = ubp_raw
        elif len(ubp_raw) == 3 or 4:
            _ubp = ubp_raw[:-1]
        elif len(ubp_raw) == 5 or 6:
            _ubp = ubp_raw[:-3]
        elif len(ubp_raw) == 7:
            _ubp = ubp_raw[:-5]
        else:
            _ubp = ubp_raw[:-6]
        return _ubp

    def check_data_for_region(self):
        # 就现这么写吧 不用循环了
        if not self.contact_region.empty:
            self.contact_region['china_loc'] = self.contact_region['region_loc'].map(PROVINCE_MAP_DICT)
            self.contact_region['if_china'] = self.contact_region['region_loc'].apply(self.check_abroad_func)
            self.contact_region['if_edp'] = self.contact_region['region_loc'].apply(self.check_province_economy_degree)
            self.contact_region['if_ddc'] = self.contact_region['region_loc'].apply(self.check_country_func)
            self.contact_region['if_dpt'] = self.contact_region['region_loc'].apply(self.check_deadbeat_province_func)
            self.contact_region['if_risk'] = self.contact_region['region_loc'].apply(self.check_high_risk_func)
            self.contact_region['if_unknown'] = self.contact_region['region_loc'].apply(self.check_unknown_func)


class ProcessDataForJD(object):
    # 15755158185 13032343344
    def __init__(self):
        # self.raw_data = QueryData.query_data_from_mongodb_func('47.96.38.60', 3717, 'analysis', 'JdCol',
        #                                                   ['mobile', 'level', 'securityLevel', 'yue', 'eCard',
        #                                                    'xiaojinku', 'baitiao', 'baitiaoDebt', 'xiaobai',
        #                                                    'addrs', 'orders', 'submitTime'], 'mobile', '13048090404')
        self.raw_data = QueryData.query_data_from_mongodb_func('127.0.0.1', 27017, 'elephant', 'jd',
                                                          ['mobile', 'level', 'securityLevel', 'yue', 'eCard',
                                                           'xiaojinku', 'baitiao', 'baitiaoDebt', 'xiaobai',
                                                           'addrs', 'orders', 'submitTime'], 'mobile', '18862323143')
        # self.raw_data = QueryData.query_data_from_mongodb('127.0.0.1', 27017, 'elephant', 'honey_bee',
        #                                                   ['report_data', 'mobile'], 'mobile', '18382035538')
        self.jd_order_info = TransformData.data_transform_from_dict(self.raw_data[0], 'orders')
        self.jd_delivery_address = TransformData.data_transform_from_dict(self.raw_data[0], 'addrs')
        self.jd_delivery_address_df = self.process_address_data()
        self.process_order_data()
        self.jd_data_time = self.calculate_time_for_jd()

    def process_address_data(self):
        _r_f = self.jd_delivery_address[0].apply(lambda x: pd.Series([i for i in x.split()]))
        _rf = _r_f[[0, 2, 4, 6, 8]].rename(columns={0: 'name', 2: 'loc_sec', 4: 'detail_address', 6: 'phone_num', 8: 'num_line'})
        _pvc_list = [ProvinceRecognize.get_address_province(_i) for _i in _rf['loc_sec'].values]
        _rf['user_province'] = pd.Series(_pvc_list)
        return _rf

    @classmethod
    def cal_num_func(cls, sec_data):
        return sec_data['user_province'].drop_duplicates().count()

    @classmethod
    def cal_num_func_a(cls, x):
        return x['detail_address'].drop_duplicates().count()

    @classmethod
    def cal_num_func_b(cls, x):
        return x['name'].drop_duplicates().count()

    @classmethod
    def check_num_func(cls, x):
        if x > 1:
            return 1
        else:
            return 0

    def process_order_data(self):
        self.jd_order_info['order_status'] = self.jd_order_info['status'].apply(CheckDataForJD.check_order_status)
        self.jd_order_info['pay_channel'] = self.jd_order_info['payType'].apply(CheckDataForJD.check_order_pay_type)
        self.jd_order_info['amount_f'] = self.jd_order_info['amount'].apply(CheckDataForJD.check_order_amount_type)
        self.jd_order_info['year_month'] = self.jd_order_info['time'].apply(CheckDataForJD.get_order_time_year_mouth)
        self.jd_order_info['year_month_day'] = \
            self.jd_order_info['time'].apply(CheckDataForJD.get_order_time_year_mouth_days)
        self.jd_order_info['month'] = self.jd_order_info['time'].apply(CheckDataForJD.get_order_time_mouth)
        self.jd_order_info['quarter_tags'] = self.jd_order_info['month'].apply(CheckDataForJD.map_mouth_to_quarter)
        self.jd_order_info['year_quarter'] = \
            self.jd_order_info.apply(lambda x: x['year_month'][0:5] + str(x['quarter_tags']), axis=1)
        _amount_check_list = [100, 200, 500, 1000, 3000, 5000, 10000]
        for _i in _amount_check_list:
            self.jd_order_info['if_order_amt_over_%s' % str(_i)] = \
                self.jd_order_info['amount_f'].apply(CheckDataForJD.check_order_amount_config(_i))
        self.jd_order_info['hour'] = self.jd_order_info['time'].apply(CheckDataForJD.get_order_time_hour)
        self.jd_order_info['order_trade_time'] = self.jd_order_info['hour'].apply(CheckDataForJD.map_order_time)
        for _i in CATEGORY_TAGS:
            self.jd_order_info['if_order_buy_%s' % _i] = \
                self.jd_order_info['title'].apply(CheckDataForJD.check_order_goods_type_config(USE_FOR_CHECK_PERSONAL_CARE))

    def calculate_time_for_jd(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.raw_data[0].get('submitTime')/1000))

    @classmethod
    def calculate_market_type_for_jd(cls):
        pass

    @classmethod
    def calculate_time_func_n(cls, x):
        _cal_times = str(x)[0:10]
        return datetime.datetime.strptime(_cal_times, "%Y-%m-%d")

    def calculate_times_for_service(self, pre_months):

        return str((datetime.datetime.strptime(self.jd_data_time[0:10], "%Y-%m-%d") -
                    pd.tseries.offsets.DateOffset(months=pre_months)))[0:7]

    # @classmethod
    # def calculate_diff_days(cls, x):
    #     return x.days + 1
#
#


# jd = ProcessDataForJD()
# k = jd.jd_order_info
# print k
# k['year_month'] = pd.to_datetime(k['year_month'])
# m = k.set_index('year_month')
# # print m
# print m['2017-01': '2016-05']
# print m['2016-05': '2017-01']
# print m['2017-01']
# # k = pd.to_datetime()
# a = k['title'].values[0]
# print type(a)
# for i in USER_FOR_CHECK_HOUSEHOLD:
#     if i in a:
#         print 1
#     else:
#         print 0
# k = k[k['order_status'] == 1]
# k = k[k['pay_channel'] == 1]
# print k
# n = k.groupby('year_month').count().reset_index()
# nt = n.sort_values(by=['amount_f', 'year_month'], ascending=False)
# print nt

# m = k.groupby('year_month').agg({'amount_f': ['sum']}).reset_index()
# import numpy as np
# gb = k.groupby(by=['year_month'])['amount_f'].agg(
#     {'total_amount': np.sum, 'mean': np.mean, 'var': np.var, 'std': np.std})

# dt = k.groupby(by=['year_month']).agg({'amount_f': 'sum'}).reset_index()
# # print dt
# dtt = dt.sort_values(by=['amount_f', 'year_month'], ascending=False)
# print dtt
# print gb.reset_index()
# print m
# a = m['amount_f'].max()
# print a
# mm = m.sort_values(by=['amount_f'], ascending=False)
# print mm
# b = m[m['amount_f'].isin(a)]
# print b
# # m1 = m.sort_values('amount_f')
# print m1
# print k['amount']

# # # # h = jd.jd_order_info
# h1 = jd.jd_delivery_address_df
# h3 = h1.groupby(['name']).count().reset_index()
#
#
# def cal_num_func(x):
#     return x['user_province'].drop_duplicates().count()
#
#
# def cal_num_func_a(x):
#     return x['detail_address'].drop_duplicates().count()
#
#
# def cal_num_func_b(x):
#     return x['name'].drop_duplicates().count()
#
#
# def check_num_func(x):
#     if x > 1:
#         return 1
#     else:
#         return 0

#
# h4 = h1.groupby(['detail_address']).apply(cal_num_func_b).reset_index()
# h4.columns = ['detail_address', 'people_cnt']
# h4['check_tags'] = h4['people_cnt'].apply(check_num_func)
# # print h4
# # h5 = h4.sort_values(by=['loc_sec'], ascending=False)['name'].values[0]
# # print h5
# print h4
# # h4 = h1.groupby(['name']).apply(cal_num_func_a).reset_index()
# # h4.columns = ['name', 'add_cnt']
# # h4['tags'] = h4['add_cnt'].apply(check_num_func)
#
# # h5 = h1.groupby(['name'])['user_province'].count().reset_index()
# # print h5
# # def cal_num_func(x):
# #     return x['user_province'].count()
#
# # print h3
# # print h4
# # h8 = h3['loc_sec'].max()
# # print h8
# # # # h2 = jd.jd_basic_data
# # # # print h2
# # print h1
# # # from data_model.nlp import *
# # import jieba
# # r_l = []
# # for i in h1['loc_sec'].values:
# #
# #     kk = ProvinceRecognize.province_recognize_func(i)
# #     k11 = ProvinceRecognize.get_address_province(i)
# #     r_l.append(k11)
# #     print kk
# #     # print k11
# #     # print type(kk)
# # # import jieba
# #
# #
# #
# # print r_l
# # # loc_test = h1['detail_address'].values[2]
# # # from pyhanlp import *
# # # PerceptronLexicalAnalyzer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')
# # # analyzer = PerceptronLexicalAnalyzer()
# # # ree = analyzer.analyze(loc_test)
# # # print ree
# # # print type(ree)
# #
# # # ppr = JClass('com.hankcs.hanlp.model.perceptron.PerceptionNERecognizer')
# # # p_1 = ppr()
# # # r_1 = p_1.recognize(ree)
# # # print r_1
# # # ner = JClass('com.hankcs.hanlp.model.perceptron.PerceptionNERecognizer')
# # # analyzer = ner()
# # # seq = analyzer.recognize(loc_test)
# # # seq1 = HanLP.segment(loc_test)
# # # print seq1
# # #
# # # # h2 = pd.DataFrame(h1)
# # # # h2 = h2.rename(['c'])
# # # aa = h1[0].apply(lambda x: pd.Series([i for i in x.split()]))
# # # rf = aa[[0, 2, 4, 6, 8]]
# # # rf.rename(columns={0: 'name', 2: 'loc_sec', 4: 'detail_address', 6: 'phone_num', 8: 'num_line'}, inplace=True)
# # #
# # # print rf
# # # loc_s = rf['loc_sec'].values[0]
# # # import sys
# # # reload(sys)
# # # sys.setdefaultencoding('utf8')
# # # import nltk
# # # # nltk.download('maxent_ne_chunker')
# # # # nltk.download('punkt')
# # # # nltk.download('words')
# # # # nltk.download('averaged_perceptron_tagger')
# # # tokens = nltk.word_tokenize(loc_s)  #分词
# # # print tokens
# # # tagged = nltk.pos_tag(tokens)  #词性标注
# # # print tagged
# # # entities = nltk.chunk.ne_chunk(tagged)
# # # for i in entities:
# # #     print i
# # # # print entities
# # # ne = nltk.chunk.ne_chunk(loc_s)
# # # print ne
# # # print h
# # #
# # # a = h1[0].split()
# # # print len(a)
# # # for i in a:
# # #     print i
# # # # print a
