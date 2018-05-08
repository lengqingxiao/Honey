# -*- coding:utf-8 -*-

# import pandas as pd
from collections import Counter
from data_transfer.data_process import *
from check_func import *


class CalculateTagsForHoneybee(ProcessDataForHoneybee):

    def __init__(self, cal_data):
        super(CalculateTagsForHoneybee, self).__init__(cal_data)
        self.honeybee_info_result = pd.DataFrame()
        self.honeybee_info_result_dict = dict()
        self.honeybee_info_result['rpt_time'] = pd.Series(self.get_report_time)
        self.calculate_user_basic_info()
        # self.calculate_contacts_list_info()
        self.calculate_main_service_info()
        self.calculate_call_list_info_n()
        self.calculate_trip_info()
        self.calculate_cell_behavior_info()
        self.calculate_maximum_call_list_info()
        self.calculate_region_info()
        self.calculate_region_info_func()
        self.calculate_call_list_cm_func()
        self.calculate_behavior()

    def calculate_user_basic_info(self):
        # 加空参模板 -999 ‘-999’ 可以用字典保存结果
        self.honeybee_info_result['rpt_time'] = pd.Series(self.get_report_time)
        user_black_info = self.user_info.get('check_black_info')
        _col_name = list(user_black_info.keys())
        _check_num = len(_col_name)
        for m in range(_check_num):
            self.honeybee_info_result[_col_name[m]] = pd.Series(user_black_info[_col_name[m]])
        user_search_info = self.user_info.get('check_search_info')
        # print user_search_info
        self.honeybee_info_result['arised_open_web_cnt'] = pd.Series(len(user_search_info.get('arised_open_web')))
        self.honeybee_info_result['phone_with_other_idcards_cnt'] = pd.Series(len(user_search_info.get('phone_with_other_idcards')))
        self.honeybee_info_result['idcard_with_other_phones_cnt'] = pd.Series(len(user_search_info.get('idcard_with_other_phones')))
        self.honeybee_info_result['idcard_with_other_names_cnt'] = pd.Series(len(user_search_info.get('idcard_with_other_names')))
        self.honeybee_info_result['searched_org_type_cnt'] = pd.Series(len(user_search_info.get('searched_org_type')))
        self.honeybee_info_result['register_org_type_cnt'] = pd.Series(len(user_search_info.get('register_org_type')))
        self.honeybee_info_result['phone_with_other_names_cnt'] = pd.Series(len(user_search_info.get('phone_with_other_names')))
        self.honeybee_info_result['register_org_cnt'] = pd.Series(user_search_info.get('register_org_cnt'))
        self.honeybee_info_result['searched_org_cnt'] = pd.Series(user_search_info.get('searched_org_cnt'))
        if self.honeybee_info_result['phone_with_other_idcards_cnt'].values[0] > 0:
            self.honeybee_info_result['if_phone_woi'] = pd.Series(1)
        else:
            self.honeybee_info_result['if_phone_woi'] = pd.Series(0)

        self.honeybee_info_result['user_mobile_loc'] = pd.Series(self.cell_behavior['cell_loc'].values[0])
        self.honeybee_info_result['user_name'] = self.application_check_list[0].get('check_points').get('key_values')
        self.honeybee_info_result['user_province'] = self.application_check_list[1].get('check_points').get('province')
        self.honeybee_info_result['user_city'] = self.application_check_list[1].get('check_points').get('city')
        self.honeybee_info_result['user_id_number'] = self.application_check_list[1].get('check_points').get('key_value')
        self.honeybee_info_result['user_gender'] = self.application_check_list[1].get('check_points').get('gender')
        self.honeybee_info_result['user_age'] = self.application_check_list[1].get('check_points').get('age')
        self.honeybee_info_result['user_if_ibl_fin'] = int(self.application_check_list[1].get('check_points').get('financial_blacklist').get('arised'))
        self.honeybee_info_result['user_if_ibl_court'] = int(self.application_check_list[1].get('check_points').get(
            'court_blacklist').get('arised'))
        self.honeybee_info_result['user_region'] = self.application_check_list[1].get('check_points').get('region')
        self.honeybee_info_result['user_mobile_website'] = self.application_check_list[2].get('check_points').get('website')
        self.honeybee_info_result['user_mobile_reg_time'] = self.application_check_list[2].get('check_points').get('reg_time')
        self.honeybee_info_result['user_mobile_rn_status'] = self.application_check_list[2].get('check_points').get(
            'reliability')

    # 可用dict保存结果 也可小数据框保存

    def calculate_contacts_list_info(self):
        # _result_df = pd.DataFrame()
        self.honeybee_info_result['cp_pct'] = pd.Series(self.contact_list.shape[0])
        self.honeybee_info_result['cp_mobile_loc_cnt'] = pd.Series(self.contact_list['phone_num_loc'].drop_duplicates().count())
        self.honeybee_info_result['cp_total_call_time'] = pd.Series(self.contact_list['call_len'].sum())
        self.honeybee_info_result['cp_total_call_in_time'] = pd.Series(self.contact_list['call_in_len'].sum())
        self.honeybee_info_result['cp_total_call_out_time'] = pd.Series(self.contact_list['call_out_len'].sum())
        if self.honeybee_info_result['cp_total_call_time'].values[0] > 0:
            call_in_times_ratio = float(self.honeybee_info_result['cp_total_call_in_time'].values[0]) / \
                                  self.honeybee_info_result['cp_total_call_time'].values[0]
            call_out_times_ratio = float(self.honeybee_info_result['cp_total_call_out_time'].values[0]) / \
                self.honeybee_info_result['cp_total_call_time'].values[0]
        else:
            call_in_times_ratio = 0
            call_out_times_ratio = 0
        self.honeybee_info_result['cp_total_call_in_time_ratio'] = pd.Series(call_in_times_ratio)
        self.honeybee_info_result['cp_total_call_out_time_ratio'] = pd.Series(call_out_times_ratio)
        self.honeybee_info_result['cp_total_call_cnt'] = pd.Series(self.contact_list['call_cnt'].sum())
        self.honeybee_info_result['cp_total_call_in_cnt'] = pd.Series(self.contact_list['call_in_cnt'].sum())
        self.honeybee_info_result['cp_total_call_out_cnt'] = pd.Series(self.contact_list['call_out_cnt'].sum())
        if self.honeybee_info_result['cp_total_call_cnt'].values[0] > 0:
            call_in_cnt_ratio = float(self.honeybee_info_result['cp_total_call_in_cnt'].values[0]) / \
                                  self.honeybee_info_result['cp_total_call_cnt'].values[0]
            call_out_cnt_ratio = float(self.honeybee_info_result['cp_total_call_out_cnt'].values[0]) / \
                self.honeybee_info_result['cp_total_call_cnt'].values[0]
        else:
            call_in_cnt_ratio = 0
            call_out_cnt_ratio = 0
        self.honeybee_info_result['cp_total_call_in_cnt_ratio'] = pd.Series(call_in_cnt_ratio)
        self.honeybee_info_result['cp_total_call_out_cnt_ratio'] = pd.Series(call_out_cnt_ratio)
        # 注意加异常
        # self.honeybee_info_result['cpc_avg_cnt_call_times'] = pd.Series()

    def calculate_main_service_info(self):
        self.honeybee_info_result['cpc_total_ser_cnt'] = \
            self.main_service.drop_duplicates('company_name')['total_service_cnt'].sum()
        self.honeybee_info_result['cpc_total_ser_org_cnt'] = len(self.raw_data['report_data']['main_service'])
        self.honeybee_info_result['cpc_total_ser_org_type_cnt'] = self.main_service['company_type'].drop_duplicates().count()
        org_check_list = [u'租车', u'招聘', u'房地产', u'电商', u'银行', u'运营商', u'支付', u'投资理财', u'贷款', u'汽车',
                          u'个人', u'健身', u'互联网', u'投资担保', u'贷款/融资', u'保险', u'短号', u'基金', u'旅游出行',
                          u'快递', u'APP软件', u'政府机构', u'婚庆'
                          ]
        org_check_result = ['crt', 'rec', 'res', 'eb', 'bank', 'opt', 'pay', 'iaf', 'loan', 'car', 'ps',
                            'gym', 'net', 'ig', 'lof', 'ins', 'sn', 'fund', 'trv', 'exp', 'app', 'gov', 'wed']
        for i in range(len(org_check_result)):
            _col_sec_name = org_check_result[i]
            _col_check_name = org_check_list[i]
            self.honeybee_info_result['cpc_ser_%s_cnt' % _col_sec_name] = \
                self.calculate_org_func(self.main_service, _col_check_name)
            self.honeybee_info_result['cpc_ser_%s_org_cnt' % _col_sec_name] = \
                self.calculate_org_func(self.main_service, _col_check_name, 'name_cnt')
        self.main_service['interact_mth'] = pd.to_datetime(self.main_service['interact_mth'])
        data_main = self.main_service.set_index('interact_mth')
        data_p1m = data_main[self.calculate_times_for_service(1)]
        data_p2m = data_main[self.calculate_times_for_service(2):self.calculate_times_for_service(1)]
        data_p3m = data_main[self.calculate_times_for_service(3):self.calculate_times_for_service(1)]
        # print data_p3m, data_main, data_p2m, data_p1m
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
                self.honeybee_info_result['cpc_ser_%s_cnt_ratio_%s' % (m, n)] = \
                    self.honeybee_info_result['cpc_ser_%s_cnt_%s' % (m, n)] / \
                    self.honeybee_info_result['cpc_total_ser_cnt_%s' % n]

    def calculate_main_service_func(self, data, time_tags):

        self.honeybee_info_result['cpc_total_ser_cnt_%s' % time_tags] = data['interact_cnt'].sum()
        self.honeybee_info_result['cpc_total_ser_org_cnt_%s' % time_tags] = data[
            'company_name'].drop_duplicates().count()
        self.honeybee_info_result['cpc_total_ser_org_type_cnt_%s' % time_tags] = data[
            'company_type'].drop_duplicates().count()
        org_check_list = [u'租车', u'招聘', u'房地产', u'电商', u'银行', u'运营商', u'支付', u'投资理财', u'贷款', u'汽车',
                          u'个人', u'健身', u'互联网', u'投资担保', u'贷款/融资', u'保险', u'短号', u'基金', u'旅游出行',
                          u'快递', u'APP软件', u'政府机构', u'婚庆'
                          ]
        org_check_result = ['crt', 'rec', 'res', 'eb', 'bank', 'opt', 'pay', 'iaf', 'loan', 'car', 'ps',
                            'gym', 'net', 'ig', 'lof', 'ins', 'sn', 'fund', 'trv', 'exp', 'app', 'gov', 'wed']
        for i in range(len(org_check_result)):
            _col_sec_name = org_check_result[i]
            _col_check_name = org_check_list[i]
            self.honeybee_info_result['cpc_ser_%s_cnt_%s' % (_col_sec_name, time_tags)] = \
                self.calculate_org_service_cnt_func(data, _col_check_name)
            self.honeybee_info_result['cpc_ser_%s_org_cnt_%s' % (_col_sec_name, time_tags)] = \
                self.calculate_org_cnt_func(data, _col_check_name)

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

    def calculate_call_list_info_n(self):

        # data_col = ['call_cnt', 'call_in_cnt', 'call_in_len', 'call_len',
        #             'call_out_cnt', 'call_out_len', 'contact_1m', 'contact_1w',
        #             'contact_3m', 'contact_3m_plus', 'contact_afternoon',
        #             'contact_early_morning', 'contact_holiday',
        #             'contact_morning', 'contact_night', 'contact_noon',
        #             'contact_weekday', 'contact_weekend', 'phone_num_loc']
        cnt_list = ['call_cnt', 'call_in_cnt', 'call_out_cnt',  'contact_1m', 'contact_1w',
                    'contact_3m', 'contact_3m_plus', 'contact_afternoon',
                    'contact_early_morning', 'contact_holiday',
                    'contact_morning', 'contact_night', 'contact_noon',
                    'contact_weekday', 'contact_weekend']
        cnt_result_list = ['call', 'call_in', 'call_out', 'contact_p1m', 'contact_p1w',
                           'contact_p3m', 'contact_po3m', 'contact_afternoon',
                           'contact_early_morning', 'contact_holiday',
                           'contact_morning', 'contact_night', 'contact_noon',
                           'contact_weekday', 'contact_weekend'
                           ]
        # cal_call_in_out_cnt = cnt_list[3:]
        # 次数 注意改名 列名重命名
        for i in range(len(cnt_list)):
            self.honeybee_info_result['cpc_total_%s_cnt' % cnt_result_list[i]] = \
                self.contact_list[cnt_list[i]].sum()
        for i in range(len(cnt_list[3:])):
            self.honeybee_info_result['cpc_total_%s_%s_cnt' % ('in', cnt_result_list[3:][i])] = \
                self.contact_list[self.contact_list['call_in_cnt'] > 0][cnt_list[3:][i]].sum()
            self.honeybee_info_result['cpc_total_%s_%s_cnt' % ('out', cnt_result_list[3:][i])] = \
                self.contact_list[self.contact_list['call_out_cnt'] > 0][cnt_list[3:][i]].sum()
        _time_tags = ['p1m', 'p1w', 'p3m', 'po3m']
        # _query_list = ['contact_1m', 'contact_1w', 'contact_3m', 'contact_3m_plus']
        # for i in range(len(_time_tags)):
        #     for m in range(len(cnt_list[7:])):
        #         self.honeybee_info_result['cpc_%s_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
        #             self.contact_list[self.contact_list[cnt_list[3:7][i]] > 0][cnt_list[7:][m]].sum()
        #         self.honeybee_info_result['cpc_%s_in_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
        #             self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
        #                               (self.contact_list['call_in_cnt'] > 0)][cnt_list[7:][m]].sum()
        #         self.honeybee_info_result['cpc_%s_out_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
        #             self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
        #                               (self.contact_list['call_out_cnt'] > 0)][cnt_list[7:][m]].sum()

        # for m in range(len(cnt_list[7:])):
        #     self.honeybee_info_result['cpc_%s_cnt_p1w' % cnt_result_list[7:][m]] = \
        #         self.contact_list[self.contact_list['contact_1w'] > 0][cnt_list[7:][m]].sum()

        # 人数
        self.honeybee_info_result['cpc_total_call_pct'] = self.contact_list.shape[0]
        for i in range(len(cnt_list[1:])):
            self.honeybee_info_result['cpc_total_%s_pct' % cnt_result_list[1:][i]] = \
                self.contact_list[self.contact_list[cnt_list[1:][i]] > 0].shape[0]
        self.honeybee_info_result['cpc_call_in_only_pct'] = \
            self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                              (self.contact_list['call_out_cnt'] == 0)].shape[0]
        self.honeybee_info_result['cpc_call_out_only_pct'] = \
            self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                              (self.contact_list['call_in_cnt'] == 0)].shape[0]
        self.honeybee_info_result['cpc_call_both_pct'] = \
            self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                              (self.contact_list['call_in_cnt'] > 0)].shape[0]
        for i in range(len(cnt_list[3:])):
            self.honeybee_info_result['cpc_total_%s_%s_pct' % ('in', cnt_result_list[3:][i])] = \
                self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                  (self.contact_list[cnt_list[3:][i]] > 0)].shape[0]
            self.honeybee_info_result['cpc_total_%s_%s_pct' % ('out', cnt_result_list[3:][i])] = \
                self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                  (self.contact_list[cnt_list[3:][i]] > 0)].shape[0]

        for i in range(len(_time_tags)):
            for m in range(len(cnt_list[7:])):
                self.honeybee_info_result['cpc_%s_pct_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
                    self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                      (self.contact_list[cnt_list[7:][m]] > 0)].shape[0]

                self.honeybee_info_result['cpc_%s_in_pct_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
                    self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                      (self.contact_list['call_in_cnt'] > 0) &
                                      (self.contact_list[cnt_list[7:][m]] > 0)].shape[0]
                self.honeybee_info_result['cpc_%s_out_pct_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
                    self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                      (self.contact_list['call_out_cnt'] > 0) &
                                      (self.contact_list[cnt_list[7:][m]] > 0)].shape[0]
        # 全天联系人数
        self.honeybee_info_result['cpc_contact_all_day_pct'] = self.contact_list[
            self.contact_list['contact_all_day'] == 1].shape[0]
        # 时长
        self.honeybee_info_result['cpc_call_lot'] = self.contact_list['call_len'].sum()
        self.honeybee_info_result['cpc_call_in_lot'] = self.contact_list['call_in_len'].sum()
        self.honeybee_info_result['cpc_call_out_lot'] = self.contact_list['call_out_len'].sum()
        # 异常机制 全天联系人 归属地数量
        if not self.contact_list[self.contact_list['contact_all_day'] == 1].empty:

            self.honeybee_info_result['cpc_contact_all_day_loc_cnt'] = self.contact_list[
                self.contact_list['contact_all_day'] == 1]['phone_num_loc'].drop_duplicates().count()
        else:
            self.honeybee_info_result['cpc_contact_all_day_loc_cnt'] = 0
        # 归属地数量
        self.honeybee_info_result['cpc_loc_cnt'] = self.contact_list['phone_num_loc'].drop_duplicates().count()
        # 注意异常 切片
        for i in range(len(cnt_list[1:])):
            if not self.contact_list[self.contact_list[cnt_list[1:][i]] > 0].empty:
                self.honeybee_info_result['cpc_%s_loc_cnt' % cnt_result_list[1:][i]] = \
                    self.contact_list[self.contact_list[cnt_list[1:][i]] > 0]['phone_num_loc'].drop_duplicates().count()
            else:
                self.honeybee_info_result['cpc_%s_loc_cnt' % cnt_result_list[1:][i]] = 0
        if not self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                  (self.contact_list['call_out_cnt'] == 0)].empty:
            self.honeybee_info_result['cpc_call_in_only_loc_cnt'] = \
                self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                  (self.contact_list['call_out_cnt'] == 0)]['phone_num_loc'].drop_duplicates().count()
        else:
            self.honeybee_info_result['cpc_call_in_only_loc_cnt'] = 0
        if not self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                 (self.contact_list['call_in_cnt'] == 0)].empty:
            self.honeybee_info_result['cpc_call_out_only_loc_cnt'] = \
                self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                  (self.contact_list['call_in_cnt'] == 0)]['phone_num_loc'].drop_duplicates().count()
        else:
            self.honeybee_info_result['cpc_call_out_only_loc_cnt'] = 0
        if not self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                 (self.contact_list['call_in_cnt'] > 0)].empty:
            self.honeybee_info_result['cpc_call_both_loc_cnt'] = \
                self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                  (self.contact_list['call_in_cnt'] > 0)]['phone_num_loc'].drop_duplicates().count()
        else:
            self.honeybee_info_result['cpc_call_both_loc_cnt'] = 0

        for i in range(len(cnt_list[3:])):
            if not self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                  (self.contact_list[cnt_list[3:][i]] > 0)].empty:
                self.honeybee_info_result['cpc_total_%s_%s_loc_cnt' % ('in', cnt_result_list[3:][i])] = \
                    self.contact_list[(self.contact_list['call_in_cnt'] > 0) &
                                      (self.contact_list[cnt_list[3:][i]] > 0)]['phone_num_loc'].drop_duplicates().count()
            else:
                self.honeybee_info_result['cpc_total_%s_%s_loc_cnt' % ('in', cnt_result_list[3:][i])] = 0

            if not self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                  (self.contact_list[cnt_list[3:][i]] > 0)].empty:
                self.honeybee_info_result['cpc_total_%s_%s_loc_cnt' % ('out', cnt_result_list[3:][i])] = \
                    self.contact_list[(self.contact_list['call_out_cnt'] > 0) &
                                      (self.contact_list[cnt_list[3:][i]] > 0)]['phone_num_loc'].drop_duplicates().count()
            else:
                self.honeybee_info_result['cpc_total_%s_%s_loc_cnt' % ('out', cnt_result_list[3:][i])] = 0

        for i in range(len(_time_tags)):
            for m in range(len(cnt_list[7:])):
                if not self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                         (self.contact_list[cnt_list[7:][m]] > 0)].empty:

                    self.honeybee_info_result['cpc_%s_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
                        self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                          (self.contact_list[cnt_list[7:][m]] > 0)]['phone_num_loc'].drop_duplicates().count()
                else:
                    self.honeybee_info_result['cpc_%s_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = 0
                if not self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                      (self.contact_list['call_in_cnt'] > 0) &
                                      (self.contact_list[cnt_list[7:][m]] > 0)].empty:
                    self.honeybee_info_result['cpc_%s_in_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
                        self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                          (self.contact_list['call_in_cnt'] > 0) &
                                          (self.contact_list[cnt_list[7:][m]] > 0)]['phone_num_loc'].drop_duplicates().count()
                else:
                    self.honeybee_info_result['cpc_%s_in_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = 0
                if not self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                      (self.contact_list['call_out_cnt'] > 0) &
                                      (self.contact_list[cnt_list[7:][m]] > 0)].empty:
                    self.honeybee_info_result['cpc_%s_out_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = \
                        self.contact_list[(self.contact_list[cnt_list[3:7][i]] > 0) &
                                          (self.contact_list['call_out_cnt'] > 0) &
                                          (self.contact_list[cnt_list[7:][m]] > 0)]['phone_num_loc'].drop_duplicates().count()
                else:
                    self.honeybee_info_result['cpc_%s_out_loc_cnt_%s' % (cnt_result_list[7:][m], _time_tags[i])] = 0

        # 计算 次数平均
        # cnt_result_list = ['call', 'call_in', 'call_out', 'contact_p1m', 'contact_p1w',
        #                    'contact_p3m', 'contact_po3m', 'contact_afternoon',
        #                    'contact_early_morning', 'contact_holiday',
        #                    'contact_morning', 'contact_night', 'contact_noon',
        #                    'contact_weekday', 'contact_weekend'
        #                    ]
        cal_avg_list = ['cpc_%s_%s_%s' % ('%s', i, '%s') for i in cnt_result_list]
                       # ['cpc_%s_in_%s_%s' % ('%s', i, '%s') for i in cnt_result_list[3:]] + \
                       # ['cpc_%s_out_%s_%s' % ('%s', i, '%s') for i in cnt_result_list[3:]]
        for s in cal_avg_list:
            if self.honeybee_info_result[s % ('total', 'pct')].values[0] != 0:
                self.honeybee_info_result[s % ('avg', 'cnt')] = \
                    self.honeybee_info_result[s % ('total', 'cnt')] / self.honeybee_info_result[s % ('total', 'pct')]
            else:
                self.honeybee_info_result[s % ('avg', 'cnt')] = 0

        # 占比 人数占比 次数占比 时长占比
        # 时长占比
        self.honeybee_info_result['cpc_total_call_in_lot_ratio'] = \
            self.honeybee_info_result['cpc_call_in_lot'] / self.honeybee_info_result['cpc_call_lot']
        self.honeybee_info_result['cpc_total_call_out_lot_ratio'] = \
            self.honeybee_info_result['cpc_call_out_lot'] / self.honeybee_info_result['cpc_call_lot']
        # 人数占比 细分人群占比 后续在做
        cal_pct_ratio = ['cpc_total_%s_%s' % (i, 'pct') for i in cnt_result_list[1:]]
        cal_pct_ratio_r = ['cpc_%s_%s_ratio' % (i, 'pct') for i in cnt_result_list[1:]]
        for i in range(len(cal_pct_ratio)):
            if self.honeybee_info_result['cpc_total_call_pct'].values[0] != 0:
                self.honeybee_info_result[cal_pct_ratio_r[i]] = \
                    self.honeybee_info_result[cal_pct_ratio[i]] / self.honeybee_info_result['cpc_total_call_pct']
            else:
                self.honeybee_info_result[cal_pct_ratio_r[i]] = 0
        self.honeybee_info_result['cpc_call_in_only_ratio'] = \
            self.honeybee_info_result['cpc_call_in_only_pct'] / self.honeybee_info_result['cpc_total_call_pct']
        self.honeybee_info_result['cpc_call_out_only_ratio'] = \
            self.honeybee_info_result['cpc_call_out_only_pct'] / self.honeybee_info_result['cpc_total_call_pct']
        self.honeybee_info_result['cpc_call_both_ratio'] = \
            self.honeybee_info_result['cpc_call_both_pct'] / self.honeybee_info_result['cpc_total_call_pct']

        # 条件人群占比 呼入 呼出
        cal_pct_ratio_c = ['cpc_%s_pct_%s_ratio' % (i, '%s') for i in cnt_result_list[3:]]
        _call_in = ['cpc_total_in_%s_%s' % (i, '%s') for i in cnt_result_list[3:]]
        _call_out = ['cpc_total_out_%s_%s' % (i, '%s') for i in cnt_result_list[3:]]
        for i in range(len(_call_in)):
            self.honeybee_info_result[cal_pct_ratio_c[i] % 'in'] = \
                self.honeybee_info_result[_call_in[i] % 'pct'] / self.honeybee_info_result['cpc_total_call_in_pct']
            self.honeybee_info_result[cal_pct_ratio_c[i] % 'out'] = \
                self.honeybee_info_result[_call_out[i] % 'pct'] / self.honeybee_info_result['cpc_total_call_out_pct']
            self.honeybee_info_result[cal_pct_ratio_c[i] % 'total'] = \
                self.honeybee_info_result[_call_in[i] % 'pct'] / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result[cal_pct_ratio_c[i] % 'total'] = \
                self.honeybee_info_result[_call_out[i] % 'pct'] / self.honeybee_info_result['cpc_total_call_pct']
        # 条件人群占比
        # 省略
        # 次数占比 总数占比
        cal_cnt_ratio = ['cpc_total_%s_%s' % (i, 'cnt') for i in cnt_result_list[1:]]
        cal_cnt_ratio_r = ['cpc_%s_%s_ratio' % (i, 'cnt') for i in cnt_result_list[1:]]
        # 注意异常 分母 0
        for i in range(len(cal_cnt_ratio)):
            if self.honeybee_info_result['cpc_total_call_cnt'].values[0] != 0:
                self.honeybee_info_result[cal_cnt_ratio_r[i]] = \
                    self.honeybee_info_result[cal_cnt_ratio[i]] / self.honeybee_info_result['cpc_total_call_cnt']
            else:
                self.honeybee_info_result[cal_cnt_ratio_r[i]] = 0

                # cal_cnt_ratio_c = ['cpc_%s_cnt_%s_ratio' % (i, '%s') for i in cnt_result_list[3:]]
        # _call_in = ['cpc_total_in_%s_%s' % (i, '%s') for i in cnt_result_list[3:]]
        # _call_out = ['cpc_total_out_%s_%s' % (i, '%s') for i in cnt_result_list[3:]]
        # for i in range(len(_call_in)):
        #     self.honeybee_info_result[cal_cnt_ratio_c[i] % 'in'] = \
        #         self.honeybee_info_result[_call_in[i] % 'cnt'] / self.honeybee_info_result['cpc_total_call_in_cnt']
        #     self.honeybee_info_result[cal_cnt_ratio_c[i] % 'out'] = \
        #         self.honeybee_info_result[_call_out[i] % 'cnt'] / self.honeybee_info_result['cpc_total_call_out_cnt']

    def calculate_call_list_func(self):
        pass

    def calculate_trip_info(self):
        # self.trip_info_n
        #
        # print self.trip_info_n
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
            _cal_pattern_result = {k: v for k, v in _cal_dict.items() if v > 1}
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
            for i in range(len(_loop_list_r)):

                self.honeybee_info_result['cpc_trip_%s_total_pct' % _loop_list_r[i]] = \
                    self.trip_info[self.trip_info['trip_type'] == _loop_list_a[i]].shape[0]
                self.honeybee_info_result['cpc_trip_%s_total_pct_ratio' % _loop_list_r[i]] = \
                    self.honeybee_info_result['cpc_trip_%s_total_pct' % _loop_list_r[i]] / \
                    self.honeybee_info_result['cpc_trip_his_cnt']

                self.honeybee_info_result['cpc_trip_%s_days_cnt' % _loop_list_r[i]] = \
                    self.trip_info[self.trip_info['trip_type'] == _loop_list_a[i]]['trip_diff_days'].sum()
                self.honeybee_info_result['cpc_trip_%s_avg_days' % _loop_list_r[i]] = \
                    self.honeybee_info_result['cpc_trip_%s_days_cnt' % _loop_list_r[i]] / \
                    self.honeybee_info_result['cpc_trip_%s_total_pct' % _loop_list_r[i]]
                self.honeybee_info_result['cpc_trip_%s_days_cnt_ratio' % _loop_list_r[i]] = \
                    self.honeybee_info_result['cpc_trip_%s_days_cnt' % _loop_list_r[i]] / \
                    self.honeybee_info_result['cpc_trip_his_total_days']

            if len(self.get_user_birthplace_province) < 3:
                _ubp = self.get_user_birthplace_province
            elif len(self.get_user_birthplace_province) == 3 or 4:
                _ubp = self.get_user_birthplace_province[:-1]
            elif len(self.get_user_birthplace_province) == 5 or 6:
                _ubp = self.get_user_birthplace_province[:-3]
            elif len(self.get_user_birthplace_province) == 7:
                _ubp = self.get_user_birthplace_province[:-5]
            else:
                _ubp = self.get_user_birthplace_province[:-6]
            self.honeybee_info_result['cpc_trip_tll_esb_pct'] = self.trip_info[self.trip_info['trip_leave'] == _ubp].shape[0]
            self.honeybee_info_result['cpc_trip_tll_esb_total_days'] = \
                self.trip_info[self.trip_info['trip_leave'] == _ubp]['trip_diff_days'].sum()
            self.honeybee_info_result['cpc_trip_tdl_esb_pct'] = self.trip_info[self.trip_info['trip_dest'] == _ubp].shape[0]
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
            loop_list_trip_r = [
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
                u'cpc_trip_tdl_esm_pct_ratio', u'cpc_trip_tdl_esm_total_days_ratio']
            for i in loop_list_trip_r:
                self.honeybee_info_result[i] = pd.Series(-999)

    def calculate_cell_behavior_info(self):
        if not self.cell_behavior.empty:
            if self.cell_behavior.shape[0] > 6:
                _cell_behavior = self.cell_behavior.iloc[0:7, :]
            else:
                _cell_behavior = self.cell_behavior
            _cal_cell_behavior = ['call_cnt', 'call_in_cnt', 'call_out_cnt', 'call_in_time', 'call_out_time',
                                  'net_flow', 'sms_cnt']
            for i in _cal_cell_behavior:
                self.honeybee_info_result['cpc_%s_p6m' % i] = _cell_behavior[i].sum()
                self.honeybee_info_result['cpc_avg_%s_p6m' % i] = self.honeybee_info_result['cpc_%s_p6m' % i] / 6
            self.honeybee_info_result['user_cell_operator'] = self.cell_behavior['cell_operator_zh'].values[0]

            if self.cell_behavior.shape[0] > 3:
                _cell_behavior_3 = self.cell_behavior.iloc[0:4, :]
            else:
                _cell_behavior_3 = self.cell_behavior
            for i in _cal_cell_behavior:
                self.honeybee_info_result['cpc_%s_p3m' % i] = _cell_behavior_3[i].sum()
                self.honeybee_info_result['cpc_avg_%s_p3m' % i] = self.honeybee_info_result['cpc_%s_p3m' % i] / 3

            if self.cell_behavior.shape[0] > 2:
                _cell_behavior_2 = self.cell_behavior.iloc[0:3, :]
            else:
                _cell_behavior_2 = self.cell_behavior
            for i in _cal_cell_behavior:
                self.honeybee_info_result['cpc_%s_p2m' % i] = _cell_behavior_2[i].sum()
                self.honeybee_info_result['cpc_avg_%s_p2m' % i] = self.honeybee_info_result['cpc_%s_p3m' % i] / 2

            for i in _cal_cell_behavior:
                self.honeybee_info_result['cpc_%s_p1m' % i] = self.cell_behavior.iloc[0][i]
        else:
            loop_list_cell_behavior = [
                u'cpc_call_cnt_p6m', u'cpc_avg_call_cnt_p6m',
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
                u'cpc_sms_cnt_p1m']
            self.honeybee_info_result['user_cell_operator'] = pd.Series('-999')
            for i in loop_list_cell_behavior:
                self.honeybee_info_result[i] = pd.Series(-999)

    def calculate_maximum_call_list_info(self):
        _cnt_list = ['call_cnt', 'call_in_cnt', 'call_out_cnt', 'contact_1m', 'contact_1w',
                    'contact_3m', 'contact_3m_plus', 'contact_afternoon',
                    'contact_early_morning', 'contact_holiday',
                    'contact_morning', 'contact_night', 'contact_noon',
                    'contact_weekday', 'contact_weekend']
        _cnt_result_list = ['call', 'call_in', 'call_out', 'contact_p1m', 'contact_p1w',
                           'contact_p3m', 'contact_po3m', 'contact_afternoon',
                           'contact_early_morning', 'contact_holiday',
                           'contact_morning', 'contact_night', 'contact_noon',
                           'contact_weekday', 'contact_weekend'
                           ]
        if not self.contact_list.empty:
            for i in range(len(_cnt_list[1:])):
                self.honeybee_info_result['cpc_sgn_max_%s_data' % _cnt_result_list[1:][i]] = \
                    self.contact_list[_cnt_list[i]].max()
        else:
            self.honeybee_info_result['cpc_sgn_max_%s_data' % _cnt_result_list[1:][i]] = \
                pd.Series(-999)

    def calculate_region_info(self):

        _col_name = [u'region_avg_call_in_time', u'region_avg_call_out_time', u'region_call_in_cnt',
                     u'region_call_in_cnt_pct', u'region_call_in_time', u'region_call_in_time_pct',
                     u'region_call_out_cnt', u'region_call_out_cnt_pct', u'region_call_out_time',
                     u'region_call_out_time_pct', u'region_uniq_num_cnt']

        _col_name_r = [i[7:] for i in _col_name]
        _cal_data_u = self.contact_region[self.contact_region['region_loc'] == u'未知']
        # _cal_data_ab = self.contact_region[self.contact_region['if_china'] == 0]
        for i in range(len(_col_name)):

            if not _cal_data_u.empty:
                self.honeybee_info_result['cpc_unknown_%s' % _col_name_r[i]] = \
                    _cal_data_u[_col_name[i]]
            else:
                self.honeybee_info_result['cpc_unknown_%s' % _col_name_r[i]] = pd.Series(-999)

        for i in range(len(_col_name)):

            if not self.contact_region.empty:
                self.honeybee_info_result['cpc_%s_top1_region' % _col_name_r[i]] = \
                    self.contact_region[self.contact_region[_col_name[i]] ==
                                        self.contact_region[_col_name[i]].max()]['region_loc'].values[0]
            else:
                self.honeybee_info_result['cpc_%s_top1_region' % _col_name_r[i]] = pd.Series('-999')
        # _cal_tags_list = ['china', 'edp', 'ddc', 'dpt', 'risk']
        _cal_col_list = ['if_china', 'if_edp', 'if_ddc', 'if_dpt', 'if_risk']
        _cal_col_r_list = [i[3:] for i in _cal_col_list]
        for i in range(len(_cal_col_list)):
            _cal_data = self.contact_region[self.contact_region[_cal_col_list[i]] == 1]
            # 命中的位置数量
            self.honeybee_info_result['cpc_%s_region_loc_cnt' % _cal_col_r_list[i]] = _cal_data.shape[0]
            self.honeybee_info_result['cpc_%s_region_loc_cnt_ratio' % _cal_col_r_list[i]] = \
                _cal_data.shape[0] / self.honeybee_info_result['cpc_loc_cnt']
            #
            self.honeybee_info_result['cpc_%s_pct' % _cal_col_r_list[i]] = _cal_data['region_uniq_num_cnt'].sum()
            self.honeybee_info_result['cpc_%s_pct_ratio' % _cal_col_r_list[i]] = \
                _cal_data['region_uniq_num_cnt'].sum() / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result['cpc_%s_call_in_cnt' % _cal_col_r_list[i]] = _cal_data['region_call_in_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_out_cnt' % _cal_col_r_list[i]] = _cal_data['region_call_out_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_cnt' % _cal_col_r_list[i]] = \
                self.honeybee_info_result['cpc_%s_call_in_cnt' % _cal_col_r_list[i]] + \
                self.honeybee_info_result['cpc_%s_call_out_cnt' % _cal_col_r_list[i]]

            self.honeybee_info_result['cpc_%s_call_in_cnt_ratio' % _cal_col_r_list[i]] = \
                _cal_data['region_call_in_cnt'].sum() / self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_out_cnt_ratio' % _cal_col_r_list[i]] = \
                _cal_data['region_call_out_cnt'].sum() / self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_cnt_ratio' % _cal_col_r_list[i]] = \
                self.honeybee_info_result['cpc_%s_call_cnt' % _cal_col_r_list[i]] / \
                self.honeybee_info_result['cpc_total_call_cnt']

            self.honeybee_info_result['cpc_%s_call_in_time' % _cal_col_r_list[i]] = _cal_data['region_call_in_time'].sum()
            self.honeybee_info_result['cpc_%s_call_out_time' % _cal_col_r_list[i]] = _cal_data['region_call_out_time'].sum()
            self.honeybee_info_result['cpc_%s_call_time' % _cal_col_r_list[i]] = \
                self.honeybee_info_result['cpc_%s_call_in_time' % _cal_col_r_list[i]] + \
                self.honeybee_info_result['cpc_%s_call_out_time' % _cal_col_r_list[i]]

            self.honeybee_info_result['cpc_%s_call_in_time_ratio' % _cal_col_r_list[i]] = \
                _cal_data['region_call_in_time'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_%s_call_out_time_ratio' % _cal_col_r_list[i]] = \
                _cal_data['region_call_out_time'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_%s_call_time_ratio' % _cal_col_r_list[i]] = \
                self.honeybee_info_result['cpc_%s_call_time' % _cal_col_r_list[i]] / \
                self.honeybee_info_result['cpc_call_lot']
            # 国外 身份证 归属地 见下方

    def calculate_region_info_func(self):

        # _cal_data_ab = self.contact_region[self.contact_region['if_china'] == 0]
        result_col = ['abr', 'esm', 'esb']
        query_col = ['if_china', 'region_loc', 'region_loc']
        query_values = [0, self.get_user_cellphone_registration_location, self.home_loc]
        for i in range(len(result_col)):
            _cal_data_r = self.contact_region[self.contact_region[query_col[i]] == query_values[i]]
            self.honeybee_info_result['cpc_%s_region_loc_cnt' % result_col[i]] = _cal_data_r.shape[0]
            self.honeybee_info_result['cpc_%s_region_loc_cnt_ratio' % result_col[i]] = \
                _cal_data_r.shape[0] / self.honeybee_info_result['cpc_loc_cnt']
            self.honeybee_info_result['cpc_%s_pct' % result_col[i]] = _cal_data_r['region_uniq_num_cnt'].sum()
            self.honeybee_info_result['cpc_%s_pct_ratio' % result_col[i]] = \
                _cal_data_r['region_uniq_num_cnt'].sum() / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result['cpc_%s_call_in_cnt' % result_col[i]] = _cal_data_r['region_call_in_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_in_cnt_ratio' % result_col[i]] = \
                _cal_data_r['region_call_in_cnt'].sum() / self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_out_cnt' % result_col[i]] = _cal_data_r['region_call_out_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_out_cnt_ratio' % result_col[i]] = \
                _cal_data_r['region_call_out_cnt'].sum() / self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_cnt' % result_col[i]] = \
                self.honeybee_info_result['cpc_%s_call_in_cnt' % result_col[i]] + \
                self.honeybee_info_result['cpc_%s_call_out_cnt' % result_col[i]]
            self.honeybee_info_result['cpc_%s_call_cnt_ratio' % result_col[i]] = \
                self.honeybee_info_result['cpc_%s_call_cnt' % result_col[i]] / \
                self.honeybee_info_result['cpc_total_call_cnt']
            self.honeybee_info_result['cpc_%s_call_in_time' % result_col[i]] = _cal_data_r['region_call_in_time'].sum()
            self.honeybee_info_result['cpc_%s_call_in_time_ratio' % result_col[i]] = \
                _cal_data_r['region_call_in_time'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_%s_call_out_time' % result_col[i]] = _cal_data_r['region_call_out_time'].sum()
            self.honeybee_info_result['cpc_%s_call_out_time_ratio' % result_col[i]] = \
                _cal_data_r['region_call_out_time'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_%s_call_time' % result_col[i]] = \
                self.honeybee_info_result['cpc_%s_call_in_time' % result_col[i]] + \
                self.honeybee_info_result['cpc_%s_call_out_time' % result_col[i]]
            self.honeybee_info_result['cpc_%s_call_time_ratio' % result_col[i]] = \
                self.honeybee_info_result['cpc_%s_call_time' % result_col[i]] / self.honeybee_info_result['cpc_call_lot']

        china_loc_list = ['HD', 'HN', 'HZ', 'HB', 'XB', 'XN', 'DB', 'GAT']
        for i in range(8):

            _cal_data_l = self.contact_region[self.contact_region['china_loc'] == i+1]
            self.honeybee_info_result['cpc_%s_region_loc_cnt' % china_loc_list[i]] = _cal_data_l.shape[0]
            self.honeybee_info_result['cpc_%s_region_loc_cnt_ratio' % china_loc_list[i]] = \
                _cal_data_l.shape[0] / self.honeybee_info_result['cpc_loc_cnt']
            self.honeybee_info_result['cpc_%s_pct' % china_loc_list[i]] = _cal_data_l['region_uniq_num_cnt'].sum()
            self.honeybee_info_result['cpc_%s_pct_ratio' % china_loc_list[i]] = \
                _cal_data_l['region_uniq_num_cnt'].sum() / self.honeybee_info_result['cpc_total_call_pct']
            self.honeybee_info_result['cpc_%s_call_in_cnt' % china_loc_list[i]] = _cal_data_l['region_call_in_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_out_cnt' % china_loc_list[i]] = _cal_data_l['region_call_out_cnt'].sum()
            self.honeybee_info_result['cpc_%s_call_cnt' % china_loc_list[i]] = \
                self.honeybee_info_result['cpc_%s_call_in_cnt' % china_loc_list[i]] + \
                self.honeybee_info_result['cpc_%s_call_out_cnt' % china_loc_list[i]]
            self.honeybee_info_result['cpc_%s_call_cnt_ratio' % china_loc_list[i]] = \
                self.honeybee_info_result['cpc_%s_call_cnt' % china_loc_list[i]] / \
                self.honeybee_info_result['cpc_total_call_cnt']

            self.honeybee_info_result['cpc_%s_call_in_time' % china_loc_list[i]] = _cal_data_l['region_call_in_time'].sum()
            self.honeybee_info_result['cpc_%s_call_out_time' % china_loc_list[i]] = _cal_data_l[
                'region_call_out_time'].sum()
            self.honeybee_info_result['cpc_%s_call_time' % china_loc_list[i]] = \
                self.honeybee_info_result['cpc_%s_call_in_time' % china_loc_list[i]] + \
                self.honeybee_info_result['cpc_%s_call_out_time' % china_loc_list[i]]
            self.honeybee_info_result['cpc_%s_call_time_ratio' % china_loc_list[i]] = \
                self.honeybee_info_result['cpc_%s_call_time' % china_loc_list[i]] / \
                self.honeybee_info_result['cpc_call_lot']

    def calculate_call_list_cm_func(self):
        _col_list = ['call_cnt', 'call_in_cnt', 'call_out_cnt', 'contact_1m', 'contact_1w',
                     'contact_3m', 'contact_3m_plus', 'contact_afternoon',
                     'contact_early_morning', 'contact_holiday',
                     'contact_morning', 'contact_night', 'contact_noon',
                     'contact_weekday', 'contact_weekend']
        _col_result_list = ['call', 'call_in', 'call_out', 'contact_p1m', 'contact_p1w',
                            'contact_p3m', 'contact_po3m', 'contact_afternoon',
                            'contact_early_morning', 'contact_holiday',
                            'contact_morning', 'contact_night', 'contact_noon',
                            'contact_weekday', 'contact_weekend']
        if not self.contact_list.empty:
            self.contact_list['if_china_mobile'] = self.contact_list['phone_num'].apply(self.check_mobile_func)
            _contact_list = self.contact_list[self.contact_list['if_china_mobile'] == 1]
            self.honeybee_info_result['cpc_mob_call_lot'] = _contact_list['call_len'].sum()
            self.honeybee_info_result['cpc_mob_call_in_lot'] = _contact_list['call_in_len'].sum()
            self.honeybee_info_result['cpc_mob_call_out_lot'] = _contact_list['call_out_len'].sum()
            # 总时长占比 对应数据暂时省略
            self.honeybee_info_result['cpc_mob_call_lot_ratio'] = \
                _contact_list['call_len'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_mob_call_in_lot_ratio'] = \
                _contact_list['call_in_len'].sum() / self.honeybee_info_result['cpc_call_lot']
            self.honeybee_info_result['cpc_mob_call_out_lot_ratio'] = \
                _contact_list['call_out_len'].sum() / self.honeybee_info_result['cpc_call_lot']
            # 时间占比 平均
            for i in range(len(_col_list)):

                self.honeybee_info_result['cpc_mob_%s_cnt' % _col_result_list[i]] = _contact_list[_col_list[i]].sum()
                self.honeybee_info_result['cpc_mob_%s_pct' % _col_result_list[i]] = \
                    _contact_list[_contact_list[_col_list[i]] > 0].shape[0]
                self.honeybee_info_result['cpc_mob_sgn_max_%s_data' % _col_result_list[i]] = \
                    _contact_list[_col_list[i]].max()
                # 与总人数占比
                self.honeybee_info_result['cpc_mob_%s_cnt_ratio' % _col_result_list[i]] = \
                    _contact_list[_col_list[i]].sum() / self.honeybee_info_result['cpc_total_call_cnt']
                self.honeybee_info_result['cpc_mob_%s_pct_ratio' % _col_result_list[i]] = \
                    _contact_list[_contact_list[_col_list[i]] > 0].shape[0] / \
                    self.honeybee_info_result['cpc_total_call_pct']
                self.honeybee_info_result['cpc_avg_mob_%s_cnt' % _col_result_list[i]] = \
                    self.honeybee_info_result['cpc_mob_%s_cnt' % _col_result_list[i]] / \
                    self.honeybee_info_result['cpc_mob_%s_pct' % _col_result_list[i]]
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
        # score 为2 个数 1 个数 0 个数  占比
        if not self.behavior_check.empty:

            try:
                _use_month = re.sub("\D", "", self.behavior_check['evidence'].values[1])[11:]
            except:
                _use_month = -999
            self.honeybee_info_result['user_mobile_use_time'] = int(_use_month)
            _cal_data_2 = self.behavior_check.iloc[2, :]
            if _cal_data_2['score'] == 2:
                _no_call_days = re.findall(r'\d+', _cal_data_2['result'])[1]
                _three_day_no_call_record = re.sub("\D", "", _cal_data_2['evidence'].split(':')[0])
                _long = _cal_data_2['evidence'].split(':')[1].split('/')
                _long_time_silent = [i.split(',')[1] for i in _long]
                _long_r = [int(re.sub("\D", "", i)) for i in _long_time_silent]
                _max_lr = max(_long_r)
                _sum_lr = sum(_long_r)
            elif _cal_data_2['score'] == 1:
                _three_day_no_call_record = 0
                try:
                    _no_call_days = re.findall(r'\d+', _cal_data_2['result'])[1]
                except:
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
            for i in range(5):
                self.honeybee_info_result['user_%s' % _check_col_list[i]] = \
                    int(self.behavior_check['score'].values[_loc_values[i]] == 2)
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
            self.honeybee_info_result['user_address_change_fre'] = check_address(self.behavior_check['result'].values[18])


if __name__ == '__main__':

    r_data = QueryData.query_data_from_mongodb('127.0.0.1', 27017, 'elephant', 'honey_bee',
                                               ['report_data', 'mobile'], 'mobile', '18382035538')
    C = CalculateTagsForHoneybee(r_data)
    data = C.honeybee_info_result
    print data

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
# data.to_csv('D:/result_05_08.csv')
# print data
# print data.columns
# print data[['cpc_contact_weekday_out_cnt_po3m', 'cpc_total_out_contact_po3m_cnt', 'cpc_contact_weekday_out_cnt_p3m']]
# print data[['cpc_total_ser_cnt_p1m', 'cpc_total_ser_cnt_p2m', 'cpc_total_ser_cnt_p3m', 'cpc_total_ser_cnt']]
# # print data['cpc_ser_bank_cnt']
