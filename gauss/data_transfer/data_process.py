# -*- coding:utf-8 -*-
# import pandas as pd
import datetime
from data_query import *
from data_transform import *


class ProcessDataForHoneybee(object):

    def __init__(self):
        # 18168724419  18677827374 15625867469 15831842620
        self.raw_data = QueryData.query_data_from_mongodb('127.0.0.1', 27017, 'elephant', 'honey_bee',
                                                          ['report_data', 'mobile'], 'mobile', '18382035538')
        # self.raw_data = QueryData.query_data_from_mongodb('47.96.38.60', 3717, 'analysis', 'MobileVerifyDataCol',
        #                                                   ['report_data', 'mobile'], 'mobile', '18168724419')
        self.contact_list = TransformData.data_transform_from_dict(self.raw_data['report_data'], 'contact_list')
        self.contact_region = TransformData.data_transform_from_dict(self.raw_data['report_data'], 'contact_region')
        self.main_service = self.reshape_data_for_main_service()
        self.trip_info = TransformData.data_transform_from_dict(self.raw_data['report_data'], 'trip_info')
        self.cell_behavior = TransformData.data_transform_from_dict(self.raw_data['report_data']['cell_behavior'][0],
                                                                    'behavior')
        self.application_check_list = self.raw_data['report_data']['application_check']
        self.behavior_check = TransformData.data_transform_from_dict(self.raw_data['report_data'], 'behavior_check')
        self.user_info = self.raw_data['report_data']['user_info_check']
        self.report_time = self.raw_data['report_data']['report'].get('update_time')[0:10]
        # self.data_mapping()

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
        for i in self.raw_data['report_data']['main_service']:
            t_df = TransformData.data_transform_from_dict(i, 'service_details')
            t_df['total_service_cnt'] = i.get('total_service_cnt')
            t_df['company_type'] = i.get('company_type')
            t_df['company_name'] = i.get('company_name')
            result_list.append(t_df)
        result_df = pd.concat(result_list)
        return result_df

    def calculate_times_for_service(self, pre_months):

        return str((datetime.datetime.strptime(self.report_time, "%Y-%m-%d") - pd.tseries.offsets.DateOffset(months=pre_months)))[0:7]


# H = ProcessDataForHoneybee()
# data = H.contact_list
# # # t = H.calculate_times_for_service(1)
# # # print t
# print data
# print data[data['contact_all_day'] == 1].shape[0]
#
# a = map(lambda x: x.encode('gb18030'), list(data['company_type']))
# data['company_type_str'] = pd.Series(a)
# print type(data['company_type_str'].values[0])
# print data[]
# w1 = H.get_report_time
# print w1
# w2 = H.get_user_birthplace_province
# w3 = H.get_user_cellphone_registration_location
# w4 = w2.find(w3) >= 0
# print w1, w2, w3, w4
# d = []
# for i in data:

#     df = TransformData.data_transform_from_dict(i, 'service_details')
#     df['total_service_cnt'] = i.get('total_service_cnt')
#     df['company_type'] = i.get('company_type')
#     df['company_name'] = i.get('company_name')
#     d.append(df)
# result = pd.concat(d)
# print result
# # data = H.application_check_list[1]   #.get('check_point')   #.get('financial_blacklist')    #.get('arised')
# # print data
# data2 = H.contact_list
# print data2

# data = H.raw_data['report_data']['application_check']
# # print type(data)
# # print data[1]
# # dd = H.be
# # print dd
# time = H.get_report_time
# # dt = H.contact_list
# print data
# print time
# print type(time)
# # print dt
# int(self.application_check_list[1].get('check_point').get('financial_blacklist').get('arised'))