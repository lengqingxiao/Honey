# -*- coding:utf-8 -*-
"""
蜜蜂报告特征计算模块

"""
import re
from collections import Counter
from data_transfer.data_process import *
from check_func import *


class CalculateTagsForHoneybee(ProcessDataForHoneybee):

    def __init__(self, cal_data):
        super(CalculateTagsForHoneybee, self).__init__(cal_data)
        self.honeybee_info_result = pd.DataFrame()
        self.honeybee_info_result['rpt_time'] = pd.Series(self.get_report_time)
        self.calculate_summary()

    def calculate_user_basic_info(self):
        # 不进行数据为空检查也无妨 这些数据一定有
        self.honeybee_info_result['rpt_time'] = pd.Series(self.get_report_time)
        user_black_info = self.user_info.get('check_black_info')
        _col_name = list(user_black_info.keys())
        _check_num = len(_col_name)
        for m in range(_check_num):
            self.honeybee_info_result[_col_name[m]] = pd.Series(user_black_info[_col_name[m]])
            self.honeybee_info_result = self.honeybee_info_result.fillna(-999)
        user_search_info = self.user_info.get('check_search_info')
        _check_col = ['arised_open_web_cnt', 'phone_with_other_idcards_cnt', 'idcard_with_other_phones_cnt',
                      'idcard_with_other_names_cnt', 'searched_org_type_cnt', 'register_org_type_cnt',
                      'phone_with_other_names_cnt']
        _check_values = ['arised_open_web', 'phone_with_other_idcards', 'idcard_with_other_phones',
                         'idcard_with_other_names', 'searched_org_type', 'register_org_type', 'phone_with_other_names']
        for _i in range(7):
            self.honeybee_info_result[_check_col[_i]] = pd.Series(len(user_search_info.get(_check_values[_i], [])))
        self.honeybee_info_result['user_reg_org_cnt'] = \
            pd.Series(user_search_info.get('register_org_cnt'))
        self.honeybee_info_result['user_src_org_cnt'] = pd.Series(user_search_info.get('searched_org_cnt'))
        if self.honeybee_info_result['phone_with_other_idcards_cnt'].values[0] > 0:
            self.honeybee_info_result['if_phone_woi'] = pd.Series(1)
        else:
            self.honeybee_info_result['if_phone_woi'] = pd.Series(0)
        self.honeybee_info_result['user_mobile_loc'] = pd.Series(self.cell_behavior['cell_loc'].values[0])
        self.honeybee_info_result['user_name'] = self.application_check_list[0].get('check_points').get('key_values')
        self.honeybee_info_result['user_province'] = self.application_check_list[1].get('check_points').get('province')
        self.honeybee_info_result['user_city'] = self.application_check_list[1].get('check_points').get('city')
        self.honeybee_info_result['user_id_number'] = \
            self.application_check_list[1].get('check_points').get('key_value')
        self.honeybee_info_result['user_gender'] = self.application_check_list[1].get('check_points').get('gender')
        self.honeybee_info_result['user_age'] = self.application_check_list[1].get('check_points').get('age')
        self.honeybee_info_result['user_if_ibl_fin'] = \
            int(self.application_check_list[1].get('check_points').get('financial_blacklist').get('arised'))
        self.honeybee_info_result['user_if_ibl_court'] = int(self.application_check_list[1].get('check_points').get(
            'court_blacklist').get('arised'))
        self.honeybee_info_result['user_region'] = self.application_check_list[1].get('check_points').get('region')
        self.honeybee_info_result['user_mobile_website'] = \
            self.application_check_list[2].get('check_points').get('website')
        self.honeybee_info_result['user_mobile_reg_time'] = \
            self.application_check_list[2].get('check_points').get('reg_time')
        self.honeybee_info_result['user_mobile_rn_status'] = self.application_check_list[2].get('check_points').get(
            'reliability')
        self.honeybee_info_result['user_cell_phone_num'] = self.application_check_list[2].get('check_points').get(
            'key_value')
        _rename_dict = {'contacts_class1_blacklist_cnt': 'cpc_dc_ibl_pct', 'contacts_router_ratio': 'cpc_rut_ratio',
                        'contacts_class2_blacklist_cnt': 'cpc_idc_ibl_pct', 'contacts_router_cnt': 'cpc_rut_pct',
                        'contacts_class1_cnt': 'cpc_dc_pct', 'phone_gray_score': 'user_gray_score',
                        'arised_open_web_cnt': 'user_phone_in_web_cnt',
                        'phone_with_other_idcards_cnt': 'user_phone_woi_cnt',
                        'idcard_with_other_phones_cnt': 'user_id_wop_cnt',
                        'idcard_with_other_names_cnt': 'user_id_won_cnt',
                        'searched_org_type_cnt': 'src_org_type_cnt', 'register_org_type_cnt': 'reg_org_type_cnt',
                        'phone_with_other_names_cnt': 'user_phone_won_cnt'}
        self.honeybee_info_result.rename(columns=_rename_dict, inplace=True)

    def calculate_main_service_info(self):

        if not self.main_service.empty:
            self.honeybee_info_result['if_main_service'] = 1
            self.honeybee_info_result['cpc_total_ser_cnt'] = \
                self.main_service.drop_duplicates('company_name')['total_service_cnt'].sum()
            self.honeybee_info_result['cpc_total_ser_org_cnt'] = len(self.raw_data['report_data']['main_service'])
            self.honeybee_info_result['cpc_total_ser_org_type_cnt'] = \
                self.main_service['company_type'].drop_duplicates().count()
            org_check_list = ORG_TYPE
            org_check_result = ORG_RESULT
            for _i in range(len(org_check_result)):
                _col_sec_name = org_check_result[_i]
                _col_check_name = org_check_list[_i]
                self.honeybee_info_result['cpc_ser_%s_cnt' % _col_sec_name] = \
                    self.calculate_org_func(self.main_service, _col_check_name)
                self.honeybee_info_result['cpc_ser_%s_org_cnt' % _col_sec_name] = \
                    self.calculate_org_func(self.main_service, _col_check_name, 'name_cnt')
            self.main_service['interact_mth'] = pd.to_datetime(self.main_service['interact_mth'])
            data_main = self.main_service.set_index('interact_mth')
            try:
                data_p1m = data_main[self.calculate_times_for_service(1)]
            except KeyError:
                data_p1m = pd.DataFrame(columns=['interact_mth', 'interact_cnt', 'total_service_cnt', 'company_type',
                                                 'company_name'])
                data_p1m['interact_mth'] = pd.to_datetime(data_p1m['interact_mth'])
                data_p1m = data_p1m.set_index('interact_mth')
            data_p2m = data_main[self.calculate_times_for_service(2):self.calculate_times_for_service(1)]
            data_p3m = data_main[self.calculate_times_for_service(3):self.calculate_times_for_service(1)]
            data_loop_list = [data_p1m, data_p2m, data_p3m]
            tags_loop_list = ['p1m', 'p2m', 'p3m']
            for m in range(3):
                self.calculate_main_service_func(data_loop_list[m], tags_loop_list[m])
            for m in org_check_result:
                self.honeybee_info_result['cpc_avg_ser_%s_cnt_p3m' % m] = \
                    self.honeybee_info_result['cpc_ser_%s_cnt_p3m' % m] / 3
                # 注意异常 分母为0的情况
                self.honeybee_info_result['cpc_ser_%s_cnt_ratio' % m] = \
                    self.honeybee_info_result['cpc_ser_%s_cnt' % m] / self.honeybee_info_result['cpc_total_ser_cnt']
                for n in tags_loop_list:
                    if self.honeybee_info_result['cpc_total_ser_cnt_%s' % n].values[0] != 0:
                        self.honeybee_info_result['cpc_ser_%s_cnt_ratio_%s' % (m, n)] = \
                            self.honeybee_info_result['cpc_ser_%s_cnt_%s' % (m, n)] / \
                            self.honeybee_info_result['cpc_total_ser_cnt_%s' % n]
                    else:
                        self.honeybee_info_result['cpc_ser_%s_cnt_ratio_%s' % (m, n)] = pd.Series(-999)
        else:
            self.honeybee_info_result['if_main_service'] = 0
            for _i in SERVICE_RESULT:
                self.honeybee_info_result[_i] = -999

    def calculate_main_service_func(self, sec_data, time_tags):

        _data = sec_data
        self.honeybee_info_result['cpc_total_ser_cnt_%s' % time_tags] = _data['interact_cnt'].sum()
        self.honeybee_info_result['cpc_total_ser_org_cnt_%s' % time_tags] = _data[
            'company_name'].drop_duplicates().count()
        self.honeybee_info_result['cpc_total_ser_org_type_cnt_%s' % time_tags] = _data[
            'company_type'].drop_duplicates().count()
        org_check_list = ORG_TYPE
        org_check_result = ORG_RESULT
        for _i in range(len(org_check_result)):
            _col_sec_name = org_check_result[_i]
            _col_check_name = org_check_list[_i]
            self.honeybee_info_result['cpc_ser_%s_cnt_%s' % (_col_sec_name, time_tags)] = \
                self.calculate_org_service_cnt_func(_data, _col_check_name)
            self.honeybee_info_result['cpc_ser_%s_org_cnt_%s' % (_col_sec_name, time_tags)] = \
                self.calculate_org_cnt_func(_data, _col_check_name)

    @classmethod
    def calculate_org_func(cls, sec_data, org_type, cal_choose='sum'):
        cal_data = sec_data[sec_data['company_type'] == org_type].drop_duplicates('company_name')
        if cal_choose == 'name_cnt':
            return cal_data.shape[0]
        else:
            return cal_data['total_service_cnt'].sum()

    @classmethod
    def calculate_org_cnt_func(cls, sec_data, org_type):
        cal_data = sec_data[sec_data['company_type'] == org_type].drop_duplicates('company_name')
        return cal_data.shape[0]

    @classmethod
    def calculate_org_service_cnt_func(cls, sec_data, org_type):
        cal_data = sec_data[sec_data['company_type'] == org_type]
        return cal_data['interact_cnt'].sum()

    @classmethod
    def calculate_call_list_cnt_func(cls, sec_data):
        if not sec_data.empty:
            _cnt = sec_data['phone_num_loc'].drop_duplicates().count()
        else:
            _cnt = 0
        return _cnt

    def calculate_call_list_info(self):

        cnt_list = USER_CONTACT_COLUMNS
        cnt_result_list = USER_CONTACT_RESULT
        if not self.contact_list.empty:
            # 次数
            for _i in range(len(cnt_list)):
                self.honeybee_info_result['cpc_total_%s_cnt' % cnt_result_list[_i]] = \
                    self.contact_list[cnt_list[_i]].sum()
            for _i in range(len(cnt_list[3:])):
                self.honeybee_info_result['cpc_total_%s_%s_cnt' % ('in', cnt_result_list[3:][_i])] = \
                    self.contact_list[self.contact_list['call_in_cnt'] > 0][cnt_list[3:][_i]].sum()
                self.honeybee_info_result['cpc_total_%s_%s_cnt' % ('out', cnt_result_list[3:][_i])] = \
                    self.contact_list[self.contact_list['call_out_cnt'] > 0][cnt_list[3:][_i]].sum()
            _time_tags = ['p1m', 'p1w', 'p3m', 'po3m']

            # 人数
            self.honeybee_info_result['cpc_total_call_pct'] = self.contact_list.shape[0]
            for _i in range(len(cnt_list[1:])):
                self.honeybee_info_result['cpc_total_%s_pct' % cnt_result_list[1:][_i]] = \
                    self.contact_list[self.contact_list[cnt_list[1:][_i]] > 0].shape[0]
            self.honeybee_info_result['cpc_call_in_only_pct'] = \
                self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                  (self.contact_list['call_out_cnt'] == 0)].shape[0]
            self.honeybee_info_result['cpc_call_out_only_pct'] = \
                self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                  (self.contact_list['call_in_cnt'] == 0)].shape[0]
            self.honeybee_info_result['cpc_call_both_pct'] = \
                self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                  (self.contact_list['call_in_cnt'] > 0)].shape[0]
            for _i in range(len(cnt_list[3:])):
                self.honeybee_info_result['cpc_total_%s_%s_pct' % ('in', cnt_result_list[3:][_i])] = \
                    self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                      (self.contact_list[cnt_list[3:][_i]] > 0)].shape[0]
                self.honeybee_info_result['cpc_total_%s_%s_pct' % ('out', cnt_result_list[3:][_i])] = \
                    self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                      (self.contact_list[cnt_list[3:][_i]] > 0)].shape[0]

            for _i in range(len(_time_tags)):
                for m in range(len(cnt_list[7:])):
                    self.honeybee_info_result['cpc_%s_pct_%s' % (cnt_result_list[7:][m], _time_tags[_i])] = \
                        self.contact_list[(self.contact_list[cnt_list[3:7][_i]] > 0) &
                                          (self.contact_list[cnt_list[7:][m]] > 0)].shape[0]

                    self.honeybee_info_result['cpc_%s_in_pct_%s' % (cnt_result_list[7:][m], _time_tags[_i])] = \
                        self.contact_list[(self.contact_list[cnt_list[3:7][_i]] > 0) &
                                          (self.contact_list['call_in_cnt'] > 0) &
                                          (self.contact_list[cnt_list[7:][m]] > 0)].shape[0]
                    self.honeybee_info_result['cpc_%s_out_pct_%s' % (cnt_result_list[7:][m], _time_tags[_i])] = \
                        self.contact_list[(self.contact_list[cnt_list[3:7][_i]] > 0) &
                                          (self.contact_list['call_out_cnt'] > 0) &
                                          (self.contact_list[cnt_list[7:][m]] > 0)].shape[0]
            # 全天联系人数
            self.honeybee_info_result['cpc_contact_all_day_pct'] = self.contact_list[
                self.contact_list['contact_all_day'] == 1].shape[0]
            # 时长
            self.honeybee_info_result['cpc_call_lot'] = self.contact_list['call_len'].sum()
            self.honeybee_info_result['cpc_call_in_lot'] = self.contact_list['call_in_len'].sum()
            self.honeybee_info_result['cpc_call_out_lot'] = self.contact_list['call_out_len'].sum()
            # 异常机制
            if not self.contact_list[self.contact_list['contact_all_day'] == 1].empty:

                self.honeybee_info_result['cpc_contact_all_day_loc_cnt'] = self.contact_list[
                    self.contact_list['contact_all_day'] == 1]['phone_num_loc'].drop_duplicates().count()
            else:
                self.honeybee_info_result['cpc_contact_all_day_loc_cnt'] = 0
            # 归属地数量
            self.honeybee_info_result['cpc_loc_cnt'] = self.contact_list['phone_num_loc'].drop_duplicates().count()
            # 注意异常 切片
            for _i in range(len(cnt_list[1:])):
                _cal_data_cl = self.contact_list[self.contact_list[cnt_list[1:][_i]] > 0]
                self.honeybee_info_result['cpc_%s_loc_cnt' % cnt_result_list[1:][_i]] = \
                    self.calculate_call_list_cnt_func(_cal_data_cl)
            _cal_data_in_only = self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                                  (self.contact_list['call_out_cnt'] == 0)]
            self.honeybee_info_result['cpc_call_in_only_loc_cnt'] = self.calculate_call_list_cnt_func(_cal_data_in_only)
            _cal_data_out_only = self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                                   (self.contact_list['call_in_cnt'] == 0)]
            self.honeybee_info_result['cpc_call_out_only_loc_cnt'] = \
                self.calculate_call_list_cnt_func(_cal_data_out_only)
            _cal_data_both = self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                               (self.contact_list['call_in_cnt'] > 0)]
            self.honeybee_info_result['cpc_call_both_loc_cnt'] = self.calculate_call_list_cnt_func(_cal_data_both)

            for _i in range(len(cnt_list[3:])):
                _sec_data_p = self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                                (self.contact_list[cnt_list[3:][_i]] > 0)]
                self.honeybee_info_result['cpc_total_%s_%s_loc_cnt' % ('in', cnt_result_list[3:][_i])] = \
                    self.calculate_call_list_cnt_func(_sec_data_p)
                _sec_data_q = self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                                (self.contact_list[cnt_list[3:][_i]] > 0)]
                self.honeybee_info_result['cpc_total_%s_%s_loc_cnt' % ('out', cnt_result_list[3:][_i])] = \
                    self.calculate_call_list_cnt_func(_sec_data_q)

            for _i in range(len(_time_tags)):
                for m in range(len(cnt_list[7:])):
                    _s_data_t1 = self.contact_list[(self.contact_list[cnt_list[3:7][_i]] > 0) &
                                                   (self.contact_list[cnt_list[7:][m]] > 0)]
                    self.honeybee_info_result['cpc_%s_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[_i])] = \
                        self.calculate_call_list_cnt_func(_s_data_t1)
                    _s_data_t2 = self.contact_list[(self.contact_list[cnt_list[3:7][_i]] > 0) &
                                                   (self.contact_list['call_in_cnt'] > 0) &
                                                   (self.contact_list[cnt_list[7:][m]] > 0)]
                    self.honeybee_info_result['cpc_%s_in_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[_i])] = \
                        self.calculate_call_list_cnt_func(_s_data_t2)
                    _s_data_t3 = self.contact_list[(self.contact_list[cnt_list[3:7][_i]] > 0) &
                                                   (self.contact_list['call_out_cnt'] > 0) &
                                                   (self.contact_list[cnt_list[7:][m]] > 0)]
                    self.honeybee_info_result['cpc_%s_out_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[_i])] = \
                        self.calculate_call_list_cnt_func(_s_data_t3)
            cal_avg_list = ['cpc_%s_%s_%s' % ('%s', _i, '%s') for _i in cnt_result_list]
            for s in cal_avg_list:
                if self.honeybee_info_result[s % ('total', 'pct')].values[0] != 0:
                    self.honeybee_info_result[s % ('avg', 'cnt')] = \
                        self.honeybee_info_result[s % ('total', 'cnt')] / \
                        self.honeybee_info_result[s % ('total', 'pct')]
                else:
                    self.honeybee_info_result[s % ('avg', 'cnt')] = 0

            # 占比 人数占比 次数占比 时长占比
            # 时长占比
            self.honeybee_info_result['cpc_total_call_in_lot_ratio'] = \
                self.honeybee_info_result['cpc_call_in_lot'] / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_total_call_out_lot_ratio'] = \
                self.honeybee_info_result['cpc_call_out_lot'] / self.honeybee_info_result['cpc_call_lot']
            # 人数占比
            cal_pct_ratio = ['cpc_total_%s_%s' % (_i, 'pct') for _i in cnt_result_list[1:]]
            cal_pct_ratio_r = ['cpc_%s_%s_ratio' % (_i, 'pct') for _i in cnt_result_list[1:]]
            for _i in range(len(cal_pct_ratio)):
                if self.honeybee_info_result['cpc_total_call_pct'].values[0] != 0:
                    self.honeybee_info_result[cal_pct_ratio_r[_i]] = \
                        self.honeybee_info_result[cal_pct_ratio[_i]] / self.honeybee_info_result['cpc_total_call_pct']
                else:
                    self.honeybee_info_result[cal_pct_ratio_r[_i]] = 0
            self.honeybee_info_result['cpc_call_in_only_ratio'] = \
                self.honeybee_info_result['cpc_call_in_only_pct'] / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result['cpc_call_out_only_ratio'] = \
                self.honeybee_info_result['cpc_call_out_only_pct'] / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result['cpc_call_both_ratio'] = \
                self.honeybee_info_result['cpc_call_both_pct'] / self.honeybee_info_result['cpc_total_call_pct']

            # 条件人群占比 呼入 呼出
            cal_pct_ratio_c = ['cpc_%s_pct_%s_ratio' % (_i, '%s') for _i in cnt_result_list[3:]]
            _call_in = ['cpc_total_in_%s_%s' % (_i, '%s') for _i in cnt_result_list[3:]]
            _call_out = ['cpc_total_out_%s_%s' % (_i, '%s') for _i in cnt_result_list[3:]]
            for _i in range(len(_call_in)):
                self.honeybee_info_result[cal_pct_ratio_c[_i] % 'in'] = \
                    self.honeybee_info_result[_call_in[_i] % 'pct'] / self.honeybee_info_result['cpc_total_call_in_pct']
                self.honeybee_info_result[cal_pct_ratio_c[_i] % 'out'] = \
                    self.honeybee_info_result[_call_out[_i] % 'pct'] / \
                    self.honeybee_info_result['cpc_total_call_out_pct']
                self.honeybee_info_result[cal_pct_ratio_c[_i] % 'total'] = \
                    self.honeybee_info_result[_call_in[_i] % 'pct'] / self.honeybee_info_result['cpc_total_call_pct']
                self.honeybee_info_result[cal_pct_ratio_c[_i] % 'total'] = \
                    self.honeybee_info_result[_call_out[_i] % 'pct'] / self.honeybee_info_result['cpc_total_call_pct']
            # 条件人群占比
            # 次数占比 总数占比
            cal_cnt_ratio = ['cpc_total_%s_%s' % (_i, 'cnt') for _i in cnt_result_list[1:]]
            cal_cnt_ratio_r = ['cpc_%s_%s_ratio' % (_i, 'cnt') for _i in cnt_result_list[1:]]
            for _i in range(len(cal_cnt_ratio)):
                if self.honeybee_info_result['cpc_total_call_cnt'].values[0] != 0:
                    self.honeybee_info_result[cal_cnt_ratio_r[_i]] = \
                        self.honeybee_info_result[cal_cnt_ratio[_i]] / self.honeybee_info_result['cpc_total_call_cnt']
                else:
                    self.honeybee_info_result[cal_cnt_ratio_r[_i]] = 0

    def calculate_trip_info(self):

        if not self.trip_info.empty:
            self.honeybee_info_result['if_trip_info'] = 1
            self.honeybee_info_result['cpc_trip_long_tsp'] = self.trip_info['trip_diff_days'].max()
            self.honeybee_info_result['cpc_trip_his_cnt'] = self.trip_info.shape[0]
            self.honeybee_info_result['cpc_trip_his_total_days'] = self.trip_info['trip_diff_days'].sum()
            self.honeybee_info_result['cpc_trip_his_avg_days'] = \
                self.honeybee_info_result['cpc_trip_his_total_days'] / self.honeybee_info_result['cpc_trip_his_cnt']
            self.honeybee_info_result['cpc_trip_his_tll_cnt'] = self.trip_info['trip_leave'].drop_duplicates().count()
            self.honeybee_info_result['cpc_trip_his_tdl_cnt'] = self.trip_info['trip_dest'].drop_duplicates().count()
            _cal_fre_pattern = list(self.trip_info['trip_loc_combine'])
            _cal_dict = dict(Counter(_cal_fre_pattern))
            _cal_pattern_result = {_k: _v for _k, _v in _cal_dict.items() if v > 1}
            self.honeybee_info_result['cpc_trip_his_fp_pct'] = len(_cal_pattern_result)
            self.honeybee_info_result['cpc_trip_his_fp_total_cnt'] = sum(_cal_pattern_result.values())
            self.honeybee_info_result['cpc_trip_his_fp_total_cnt_ratio'] = \
                self.honeybee_info_result['cpc_trip_his_fp_total_cnt'] / self.honeybee_info_result['cpc_trip_his_cnt']
            _end_time_f = self.calculate_time_func_n(self.trip_info['trip_end_time'].values[0])
            _end_time_e = self.calculate_time_func_n(self.trip_info['trip_end_time'].values[-1])
            _now_time = self.calculate_time_func_n(self.report_time)
            # first end time last
            self.honeybee_info_result['cpc_trip_his_fet_tsp'] = (_now_time - _end_time_f).days
            self.honeybee_info_result['cpc_trip_his_let_tsp'] = (_now_time - _end_time_e).days
            _loop_list_a = [u'节假日', u'双休日', u'工作日']
            _loop_list_r = ['holiday', 'weekend', 'workday']
            for _i in range(len(_loop_list_r)):

                self.honeybee_info_result['cpc_trip_%s_total_pct' % _loop_list_r[_i]] = \
                    self.trip_info[self.trip_info['trip_type'] == _loop_list_a[_i]].shape[0]
                self.honeybee_info_result['cpc_trip_%s_total_pct_ratio' % _loop_list_r[_i]] = \
                    self.honeybee_info_result['cpc_trip_%s_total_pct' % _loop_list_r[_i]] / \
                    self.honeybee_info_result['cpc_trip_his_cnt']

                self.honeybee_info_result['cpc_trip_%s_days_cnt' % _loop_list_r[_i]] = \
                    self.trip_info[self.trip_info['trip_type'] == _loop_list_a[_i]]['trip_diff_days'].sum()
                self.honeybee_info_result['cpc_trip_%s_avg_days' % _loop_list_r[_i]] = \
                    self.honeybee_info_result['cpc_trip_%s_days_cnt' % _loop_list_r[_i]] / \
                    self.honeybee_info_result['cpc_trip_%s_total_pct' % _loop_list_r[_i]]
                self.honeybee_info_result['cpc_trip_%s_days_cnt_ratio' % _loop_list_r[_i]] = \
                    self.honeybee_info_result['cpc_trip_%s_days_cnt' % _loop_list_r[_i]] / \
                    self.honeybee_info_result['cpc_trip_his_total_days']
            _ubp = self.calculate_home_loc_func()

            self.honeybee_info_result['cpc_trip_tll_esb_pct'] = \
                self.trip_info[self.trip_info['trip_leave'] == _ubp].shape[0]
            self.honeybee_info_result['cpc_trip_tll_esb_total_days'] = \
                self.trip_info[self.trip_info['trip_leave'] == _ubp]['trip_diff_days'].sum()
            self.honeybee_info_result['cpc_trip_tdl_esb_pct'] = \
                self.trip_info[self.trip_info['trip_dest'] == _ubp].shape[0]
            self.honeybee_info_result['cpc_trip_tdl_esb_total_days'] = \
                self.trip_info[self.trip_info['trip_dest'] == _ubp]['trip_diff_days'].sum()
            self.honeybee_info_result['cpc_trip_tll_esm_pct'] = \
                self.trip_info[self.trip_info['trip_leave'] == self.get_user_cellphone_registration_location].shape[0]
            self.honeybee_info_result['cpc_trip_tll_esm_total_days'] = \
                self.trip_info[self.trip_info['trip_leave'] ==
                               self.get_user_cellphone_registration_location]['trip_diff_days'].sum()
            self.honeybee_info_result['cpc_trip_tdl_esm_pct'] = \
                self.trip_info[self.trip_info['trip_dest'] == self.get_user_cellphone_registration_location].shape[0]
            self.honeybee_info_result['cpc_trip_tdl_esm_total_days'] = \
                self.trip_info[self.trip_info['trip_dest'] ==
                               self.get_user_cellphone_registration_location]['trip_diff_days'].sum()

            self.honeybee_info_result['cpc_trip_tll_esb_pct_ratio'] = \
                self.honeybee_info_result['cpc_trip_tll_esb_pct'] / self.honeybee_info_result['cpc_trip_his_cnt']
            self.honeybee_info_result['cpc_trip_tll_esb_total_days_ratio'] = \
                self.honeybee_info_result['cpc_trip_tll_esb_total_days'] / \
                self.honeybee_info_result['cpc_trip_his_total_days']
            self.honeybee_info_result['cpc_trip_tdl_esb_pct_ratio'] = \
                self.honeybee_info_result['cpc_trip_tdl_esb_pct'] / \
                self.honeybee_info_result['cpc_trip_his_cnt']
            self.honeybee_info_result['cpc_trip_tdl_esb_total_days_ratio'] = \
                self.honeybee_info_result['cpc_trip_tdl_esb_total_days'] / \
                self.honeybee_info_result['cpc_trip_his_total_days']
            self.honeybee_info_result['cpc_trip_tll_esm_pct_ratio'] = \
                self.honeybee_info_result['cpc_trip_tll_esm_pct'] / self.honeybee_info_result['cpc_trip_his_cnt']
            self.honeybee_info_result['cpc_trip_tll_esm_total_days_ratio'] = \
                self.honeybee_info_result['cpc_trip_tll_esm_total_days'] / \
                self.honeybee_info_result['cpc_trip_his_total_days']
            self.honeybee_info_result['cpc_trip_tdl_esm_pct_ratio'] = \
                self.honeybee_info_result['cpc_trip_tdl_esm_pct'] / self.honeybee_info_result['cpc_trip_his_cnt']
            self.honeybee_info_result['cpc_trip_tdl_esm_total_days_ratio'] = \
                self.honeybee_info_result['cpc_trip_tdl_esm_total_days'] / \
                self.honeybee_info_result['cpc_trip_his_total_days']

        else:
            self.honeybee_info_result['if_trip_info'] = 0
            loop_list_trip_r = TRIP_INFO_RESULT
            for _i in loop_list_trip_r:
                self.honeybee_info_result[_i] = pd.Series(-999)

    def calculate_cell_behavior_info(self):
        if not self.cell_behavior.empty:
            _cal_cell_behavior = ['call_cnt', 'call_in_cnt', 'call_out_cnt', 'call_in_time', 'call_out_time',
                                  'net_flow', 'sms_cnt']
            self.honeybee_info_result['user_cell_operator'] = self.cell_behavior['cell_operator_zh'].values[0]
            _loop_cal_seq = [6, 3, 2]
            for _i in _loop_cal_seq:
                self.calculate_cell_behavior_func(_i)
            for _i in _cal_cell_behavior:
                self.honeybee_info_result['cpc_%s_p1m' % _i] = self.cell_behavior.iloc[0][_i]
        else:
            loop_list_cell_behavior = CELL_BEHAVIOR
            self.honeybee_info_result['user_cell_operator'] = pd.Series('-999')
            for _i in loop_list_cell_behavior:
                self.honeybee_info_result[_i] = pd.Series(-999)

    def calculate_cell_behavior_func(self, tags_num):
        # 6 3 2
        _cal_cell_behavior = ['call_cnt', 'call_in_cnt', 'call_out_cnt', 'call_in_time', 'call_out_time',
                              'net_flow', 'sms_cnt']
        if self.cell_behavior.shape[0] > tags_num:
            _cell_behavior = self.cell_behavior.iloc[0:tags_num+1, :]
        else:
            _cell_behavior = self.cell_behavior
        for _i in _cal_cell_behavior:
            self.honeybee_info_result['cpc_%s_p%sm' % (_i, str(tags_num))] = _cell_behavior[_i].sum()
            self.honeybee_info_result['cpc_avg_%s_p%sm' % (_i, str(tags_num))] = \
                self.honeybee_info_result['cpc_%s_p6m' % _i] / tags_num

    def calculate_maximum_call_list_info(self):
        _cnt_list = USER_CONTACT_COLUMNS
        _cnt_result_list = USER_CONTACT_RESULT
        if not self.contact_list.empty:
            for _i in range(len(_cnt_list[1:])):
                self.honeybee_info_result['cpc_sgn_max_%s_data' % _cnt_result_list[1:][_i]] = \
                    self.contact_list[_cnt_list[_i]].max()
        else:
            for _i in range(len(_cnt_list[1:])):
                self.honeybee_info_result['cpc_sgn_max_%s_data' % _cnt_result_list[1:][_i]] = \
                    pd.Series(-999)

    def calculate_region_info(self):

        _col_name = CONTACT_REGION
        # 结果占比 pct换成ratio
        _col_name_r = [_i[7:] for _i in _col_name]
        _cal_data_u = self.contact_region[self.contact_region['region_loc'] == u'未知']
        for _i in range(len(_col_name)):
            if not _cal_data_u.empty:
                self.honeybee_info_result['cpc_unknown_%s' % _col_name_r[_i]] = \
                    _cal_data_u[_col_name[_i]]
            else:
                self.honeybee_info_result['cpc_unknown_%s' % _col_name_r[_i]] = pd.Series(-999)
        _unknown_dict = {'cpc_unknown_call_in_cnt_pct': 'cpc_unknown_call_in_cnt_ratio',
                         'cpc_unknown_call_in_time_pct': 'cpc_unknown_call_in_time_ratio',
                         'cpc_unknown_call_out_time_pct': 'cpc_unknown_call_out_time_ratio',
                         'cpc_unknown_call_out_cnt_pct': 'cpc_unknown_call_out_cnt_ratio'}
        self.honeybee_info_result.rename(columns=_unknown_dict, inplace=True)
        for _i in range(len(_col_name)):
            if not self.contact_region.empty:
                self.honeybee_info_result['cpc_%s_top1_region' % _col_name_r[_i]] = \
                    self.contact_region[self.contact_region[_col_name[_i]] ==
                                        self.contact_region[_col_name[_i]].max()]['region_loc'].values[0]
            else:
                self.honeybee_info_result['cpc_%s_top1_region' % _col_name_r[_i]] = pd.Series('-999')
        _cal_col_list = ['if_china', 'if_edp', 'if_ddc', 'if_dpt', 'if_risk']
        _cal_col_r_list = [_i[3:] for _i in _cal_col_list]
        for _i in range(len(_cal_col_list)):
            _cal_data = self.contact_region[self.contact_region[_cal_col_list[_i]] == 1]
            # 命中的位置数量
            self.honeybee_info_result['cpc_%s_region_loc_cnt' % _cal_col_r_list[_i]] = _cal_data.shape[0]
            self.honeybee_info_result['cpc_%s_region_loc_cnt_ratio' % _cal_col_r_list[_i]] = \
                _cal_data.shape[0] / self.honeybee_info_result['cpc_loc_cnt']
            self.honeybee_info_result['cpc_%s_pct' % _cal_col_r_list[_i]] = _cal_data['region_uniq_num_cnt'].sum()
            self.honeybee_info_result['cpc_%s_pct_ratio' % _cal_col_r_list[_i]] = \
                _cal_data['region_uniq_num_cnt'].sum() / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result['cpc_%s_call_in_cnt' % _cal_col_r_list[_i]] = \
                _cal_data['region_call_in_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_out_cnt' % _cal_col_r_list[_i]] = \
                _cal_data['region_call_out_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_cnt' % _cal_col_r_list[_i]] = \
                self.honeybee_info_result['cpc_%s_call_in_cnt' % _cal_col_r_list[_i]] + \
                self.honeybee_info_result['cpc_%s_call_out_cnt' % _cal_col_r_list[_i]]

            self.honeybee_info_result['cpc_%s_call_in_cnt_ratio' % _cal_col_r_list[_i]] = \
                _cal_data['region_call_in_cnt'].sum() / self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_out_cnt_ratio' % _cal_col_r_list[_i]] = \
                _cal_data['region_call_out_cnt'].sum() / self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_cnt_ratio' % _cal_col_r_list[_i]] = \
                self.honeybee_info_result['cpc_%s_call_cnt' % _cal_col_r_list[_i]] / \
                self.honeybee_info_result['cpc_total_call_cnt']

            self.honeybee_info_result['cpc_%s_call_in_time' % _cal_col_r_list[_i]] = \
                _cal_data['region_call_in_time'].sum()
            self.honeybee_info_result['cpc_%s_call_out_time' % _cal_col_r_list[_i]] = \
                _cal_data['region_call_out_time'].sum()
            self.honeybee_info_result['cpc_%s_call_time' % _cal_col_r_list[_i]] = \
                self.honeybee_info_result['cpc_%s_call_in_time' % _cal_col_r_list[_i]] + \
                self.honeybee_info_result['cpc_%s_call_out_time' % _cal_col_r_list[_i]]

            self.honeybee_info_result['cpc_%s_call_in_time_ratio' % _cal_col_r_list[_i]] = \
                _cal_data['region_call_in_time'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_%s_call_out_time_ratio' % _cal_col_r_list[_i]] = \
                _cal_data['region_call_out_time'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_%s_call_time_ratio' % _cal_col_r_list[_i]] = \
                self.honeybee_info_result['cpc_%s_call_time' % _cal_col_r_list[_i]] / \
                self.honeybee_info_result['cpc_call_lot']

    def calculate_region_info_func(self):

        result_col = ['abr', 'esm', 'esb']
        query_col = ['if_china', 'region_loc', 'region_loc']
        query_values = [0, self.get_user_cellphone_registration_location, self.home_loc]
        for _i in range(len(result_col)):
            _cal_data_r = self.contact_region[self.contact_region[query_col[_i]] == query_values[_i]]
            self.honeybee_info_result['cpc_%s_region_loc_cnt' % result_col[_i]] = _cal_data_r.shape[0]
            self.honeybee_info_result['cpc_%s_region_loc_cnt_ratio' % result_col[_i]] = \
                _cal_data_r.shape[0] / self.honeybee_info_result['cpc_loc_cnt']
            self.honeybee_info_result['cpc_%s_pct' % result_col[_i]] = _cal_data_r['region_uniq_num_cnt'].sum()
            self.honeybee_info_result['cpc_%s_pct_ratio' % result_col[_i]] = \
                _cal_data_r['region_uniq_num_cnt'].sum() / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result['cpc_%s_call_in_cnt' % result_col[_i]] = _cal_data_r['region_call_in_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_in_cnt_ratio' % result_col[_i]] = \
                _cal_data_r['region_call_in_cnt'].sum() / self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_out_cnt' % result_col[_i]] = _cal_data_r['region_call_out_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_out_cnt_ratio' % result_col[_i]] = \
                _cal_data_r['region_call_out_cnt'].sum() / self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_cnt' % result_col[_i]] = \
                self.honeybee_info_result['cpc_%s_call_in_cnt' % result_col[_i]] + \
                self.honeybee_info_result['cpc_%s_call_out_cnt' % result_col[_i]]
            self.honeybee_info_result['cpc_%s_call_cnt_ratio' % result_col[_i]] = \
                self.honeybee_info_result['cpc_%s_call_cnt' % result_col[_i]] / \
                self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_in_time' % result_col[_i]] = _cal_data_r['region_call_in_time'].sum()
            self.honeybee_info_result['cpc_%s_call_in_time_ratio' % result_col[_i]] = \
                _cal_data_r['region_call_in_time'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_%s_call_out_time' % result_col[_i]] = \
                _cal_data_r['region_call_out_time'].sum()
            self.honeybee_info_result['cpc_%s_call_out_time_ratio' % result_col[_i]] = \
                _cal_data_r['region_call_out_time'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_%s_call_time' % result_col[_i]] = \
                self.honeybee_info_result['cpc_%s_call_in_time' % result_col[_i]] + \
                self.honeybee_info_result['cpc_%s_call_out_time' % result_col[_i]]
            self.honeybee_info_result['cpc_%s_call_time_ratio' % result_col[_i]] = \
                self.honeybee_info_result['cpc_%s_call_time' % result_col[_i]] / \
                self.honeybee_info_result['cpc_call_lot']

        china_loc_list = CHINA_LOC
        for _m in range(8):

            _cal_data_l = self.contact_region[self.contact_region['china_loc'] == _m+1]
            self.honeybee_info_result['cpc_%s_region_loc_cnt' % china_loc_list[_m]] = _cal_data_l.shape[0]
            self.honeybee_info_result['cpc_%s_region_loc_cnt_ratio' % china_loc_list[_m]] = \
                _cal_data_l.shape[0] / self.honeybee_info_result['cpc_loc_cnt']
            self.honeybee_info_result['cpc_%s_pct' % china_loc_list[_m]] = _cal_data_l['region_uniq_num_cnt'].sum()
            self.honeybee_info_result['cpc_%s_pct_ratio' % china_loc_list[_m]] = \
                _cal_data_l['region_uniq_num_cnt'].sum() / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result['cpc_%s_call_in_cnt' % china_loc_list[_m]] = \
                _cal_data_l['region_call_in_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_out_cnt' % china_loc_list[_m]] = \
                _cal_data_l['region_call_out_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_cnt' % china_loc_list[_m]] = \
                self.honeybee_info_result['cpc_%s_call_in_cnt' % china_loc_list[_m]] + \
                self.honeybee_info_result['cpc_%s_call_out_cnt' % china_loc_list[_m]]
            self.honeybee_info_result['cpc_%s_call_cnt_ratio' % china_loc_list[_m]] = \
                self.honeybee_info_result['cpc_%s_call_cnt' % china_loc_list[_m]] / \
                self.honeybee_info_result['cpc_total_call_cnt']

            self.honeybee_info_result['cpc_%s_call_in_time' % china_loc_list[_m]] = \
                _cal_data_l['region_call_in_time'].sum()
            self.honeybee_info_result['cpc_%s_call_out_time' % china_loc_list[_m]] = _cal_data_l[
                'region_call_out_time'].sum()
            self.honeybee_info_result['cpc_%s_call_time' % china_loc_list[_m]] = \
                self.honeybee_info_result['cpc_%s_call_in_time' % china_loc_list[_m]] + \
                self.honeybee_info_result['cpc_%s_call_out_time' % china_loc_list[_m]]
            self.honeybee_info_result['cpc_%s_call_time_ratio' % china_loc_list[_m]] = \
                self.honeybee_info_result['cpc_%s_call_time' % china_loc_list[_m]] / \
                self.honeybee_info_result['cpc_call_lot']

    def calculate_call_list_cm_func(self):
        _col_list = USER_CONTACT_COLUMNS
        _col_result_list = USER_CONTACT_RESULT
        if not self.contact_list.empty:
            self.contact_list['if_china_mobile'] = self.contact_list['phone_num'].apply(self.check_mobile_func)
            _contact_list = self.contact_list[self.contact_list['if_china_mobile'] == 1]
            self.honeybee_info_result['cpc_mob_call_lot'] = _contact_list['call_len'].sum()
            self.honeybee_info_result['cpc_mob_call_in_lot'] = _contact_list['call_in_len'].sum()
            self.honeybee_info_result['cpc_mob_call_out_lot'] = _contact_list['call_out_len'].sum()
            # 总时长占比
            self.honeybee_info_result['cpc_mob_call_lot_ratio'] = \
                _contact_list['call_len'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_mob_call_in_lot_ratio'] = \
                _contact_list['call_in_len'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_mob_call_out_lot_ratio'] = \
                _contact_list['call_out_len'].sum() / self.honeybee_info_result['cpc_call_lot']
            # 时间占比 平均
            for _i in range(len(_col_list)):

                self.honeybee_info_result['cpc_mob_%s_cnt' % _col_result_list[_i]] = _contact_list[_col_list[_i]].sum()
                self.honeybee_info_result['cpc_mob_%s_pct' % _col_result_list[_i]] = \
                    _contact_list[_contact_list[_col_list[_i]] > 0].shape[0]
                self.honeybee_info_result['cpc_mob_sgn_max_%s_data' % _col_result_list[_i]] = \
                    _contact_list[_col_list[_i]].max()
                # 与总人数占比
                self.honeybee_info_result['cpc_mob_%s_cnt_ratio' % _col_result_list[_i]] = \
                    _contact_list[_col_list[_i]].sum() / self.honeybee_info_result['cpc_total_call_cnt']
                self.honeybee_info_result['cpc_mob_%s_pct_ratio' % _col_result_list[_i]] = \
                    _contact_list[_contact_list[_col_list[_i]] > 0].shape[0] / \
                    self.honeybee_info_result['cpc_total_call_pct']
                self.honeybee_info_result['cpc_avg_mob_%s_cnt' % _col_result_list[_i]] = \
                    self.honeybee_info_result['cpc_mob_%s_cnt' % _col_result_list[_i]] / \
                    self.honeybee_info_result['cpc_mob_%s_pct' % _col_result_list[_i]]
            self.honeybee_info_result['cpc_mob_call_in_only_pct'] = \
                _contact_list[(_contact_list['call_in_cnt'] > 0) & (_contact_list['call_out_cnt'] == 0)].shape[0]
            self.honeybee_info_result['cpc_mob_call_out_only_pct'] = \
                _contact_list[(_contact_list['call_out_cnt'] > 0) & (_contact_list['call_in_cnt'] == 0)].shape[0]
            self.honeybee_info_result['cpc_mob_call_both_pct'] = \
                _contact_list[(_contact_list['call_out_cnt'] > 0) & (_contact_list['call_in_cnt'] > 0)].shape[0]

            self.honeybee_info_result['cpc_avg_mob_call_lot'] = \
                _contact_list['call_len'].sum() / self.honeybee_info_result['cpc_mob_call_cnt']
            self.honeybee_info_result['cpc_avg_mob_call_in_lot'] = \
                _contact_list['call_in_len'].sum() / self.honeybee_info_result['cpc_mob_call_in_cnt']
            self.honeybee_info_result['cpc_avg_mob_call_out_lot'] = \
                _contact_list['call_out_len'].sum() / self.honeybee_info_result['cpc_mob_call_out_cnt']

    def calculate_behavior(self):

        if not self.behavior_check.empty:

            try:
                _use_month = re.sub("\D", "", self.behavior_check['evidence'].values[1])[11:]
            except Exception, e:
                print Exception, e
                _use_month = -999
            self.honeybee_info_result['user_mobile_use_time'] = int(_use_month)
            _cal_data_2 = self.behavior_check.iloc[2, :]
            if _cal_data_2['score'] == 2:
                _no_call_days = re.findall(r'\d+', _cal_data_2['result'])[1]
                _three_day_no_call_record = re.sub("\D", "", _cal_data_2['evidence'].split(':')[0])
                _long = _cal_data_2['evidence'].split(':')[1].split('/')
                _long_time_silent = [_i.split(',')[1] for _i in _long]
                _long_r = [int(re.sub("\D", "", _i)) for _i in _long_time_silent]
                _max_lr = max(_long_r)
                _sum_lr = sum(_long_r)
            elif _cal_data_2['score'] == 1:
                _three_day_no_call_record = 0
                try:
                    _no_call_days = re.findall(r'\d+', _cal_data_2['result'])[1]
                except Exception, e:
                    print Exception, e
                    _no_call_days = 0
                _max_lr = -999
                _sum_lr = -999
            else:

                _sum_lr = -999
                _three_day_no_call_record = -999
                _no_call_days = -999
                _max_lr = -999
            self.honeybee_info_result['cpc_user_no_call_days'] = int(_no_call_days)
            self.honeybee_info_result['cpc_user_3days_no_call_cnt'] = int(_three_day_no_call_record)
            self.honeybee_info_result['cpc_user_max_silent_days'] = int(_max_lr)
            self.honeybee_info_result['cpc_user_silent_days'] = int(_sum_lr)
            self.honeybee_info_result['cpc_user_high_risk_cnt'] = \
                self.behavior_check[self.behavior_check['score'] == 2].shape[0]
            self.honeybee_info_result['cpc_user_high_risk_cnt_ratio'] = \
                self.honeybee_info_result['cpc_user_high_risk_cnt'] / 19
            _check_col_list = ['if_contact_am', 'if_contact_110', 'if_contact_120', 'if_contact_lawyer',
                               'if_contact_court']
            _loc_values = [4, 5, 6, 7, 8]
            for _i in range(5):
                self.honeybee_info_result['user_%s' % _check_col_list[_i]] = \
                    int(self.behavior_check['score'].values[_loc_values[_i]] == 2)
            self.honeybee_info_result['user_call_night_fre'] = check_night_fre(self.behavior_check['result'].values[9])
            self.honeybee_info_result['user_call_loan_fre'] = check_number_fre(self.behavior_check['result'].values[10])
            self.honeybee_info_result['user_call_bank_fre'] = check_number_fre(self.behavior_check['result'].values[11])
            self.honeybee_info_result['user_call_cc_fre'] = check_number_fre(self.behavior_check['result'].values[12])
            self.honeybee_info_result['user_address_use_in_eb_fre'] = \
                check_loc_fre(self.behavior_check['result'].values[13])
            self.honeybee_info_result['user_eb_use_fre'] = check_eb_use_fre(self.behavior_check['result'].values[14])
            self.honeybee_info_result['user_eb_self_use_fre'] = \
                check_eb_use_fre(self.behavior_check['result'].values[15])
            self.honeybee_info_result['user_vg_buy_fre'] = check_buy_fre(self.behavior_check['result'].values[16])
            self.honeybee_info_result['user_lt_buy_fre'] = check_buy_fre(self.behavior_check['result'].values[17])
            self.honeybee_info_result['user_address_change_fre'] = \
                check_address(self.behavior_check['result'].values[18])
        else:
            for _i in BEHAVIOR_CHECK_TUPLE:
                self.honeybee_info_result[_i] = -999

    def calculate_summary(self):
        self.calculate_user_basic_info()
        self.calculate_main_service_info()
        self.calculate_call_list_info()
        self.calculate_trip_info()
        self.calculate_cell_behavior_info()
        self.calculate_maximum_call_list_info()
        self.calculate_region_info()
        self.calculate_region_info_func()
        self.calculate_call_list_cm_func()
        self.calculate_behavior()


# if __name__ == '__main__':
#
#     from config.log_config import *
#
#     logging.info('System Begin')
#     result = []
#     for i in ['15625867469', '18168724419', '18677827374', '15831842620', '18382035538', '18329468073', '18734594770',
#               '18536575736', '18909678383', '18789575931']:
#         # r_data = QueryData.query_data_from_mongodb_func('127.0.0.1', 27017, 'elephant', 'honey_bee',
#         #                                                 ['report_data', 'mobile'], 'mobile', i)
#         r_data = QueryData.query_data_from_mongodb_func('47.96.38.60', 3717, 'analysis', 'MobileVerifyDataCol',
#                                                         ['report_data', 'mobile'], 'mobile', i)
#         logging.info('数据[%s]拉取完成，开始计算' % i)
#         data_shape = len(r_data)
#         if data_shape == 0:
#             print '数据为空'
#         elif data_shape == 1:
#             cal_data_r = pd.DataFrame(r_data[0])
#             C = CalculateTagsForHoneybee(cal_data_r)
#             data = C.honeybee_info_result
#             result.append(data)
#             # data['mob_num'] = pd.Series(i)
#             print data
#             logging.info('蜜蜂报告特征计算完毕')
#         else:
#             for d in r_data:
#                 cal_data_r = pd.DataFrame(d)
#                 C = CalculateTagsForHoneybee(cal_data_r)
#                 data = C.honeybee_info_result
#                 result.append(data)
#                 # data['mob_num'] = pd.Series(i)
#                 print data
#         # C = CalculateTagsForHoneybee(r_data)
#         # data = C.honeybee_info_result
#                 logging.info('蜜蜂报告特征计算完毕')
#
#     logging.info('System End')
#     result_df_n = pd.concat(result)
#     print result_df_n
