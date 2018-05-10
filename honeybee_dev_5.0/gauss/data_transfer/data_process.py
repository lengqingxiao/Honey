# -*- coding:utf-8 -*-

import datetime
from pandas.tseries import offsets
from data_query import *
from data_transform import *
from config.global_config import *


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
        if not self.contact_region.empty:
            self.contact_region['china_loc'] = self.contact_region['region_loc'].map(PROVINCE_MAP_DICT)
            self.contact_region['if_china'] = self.contact_region['region_loc'].apply(self.check_abroad_func)
            self.contact_region['if_edp'] = self.contact_region['region_loc'].apply(self.check_province_economy_degree)
            self.contact_region['if_ddc'] = self.contact_region['region_loc'].apply(self.check_country_func)
            self.contact_region['if_dpt'] = self.contact_region['region_loc'].apply(self.check_deadbeat_province_func)
            self.contact_region['if_risk'] = self.contact_region['region_loc'].apply(self.check_high_risk_func)
            self.contact_region['if_unknown'] = self.contact_region['region_loc'].apply(self.check_unknown_func)
