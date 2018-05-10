# -*- coding:utf-8 -*-

# import pandas as pd
from data_transfer.data_process import *


class CalculateTagsForHoneybee(ProcessDataForHoneybee):

    def __init__(self):
        super(CalculateTagsForHoneybee, self).__init__()
        self.honeybee_info_result = pd.DataFrame()
        self.honeybee_info_result_dict = dict()
        self.calculate_user_basic_info()
        self.calculate_contacts_list_info()
        self.calculate_main_service_info()
        self.calculate_call_list_info_n()

    def calculate_user_basic_info_n(self):
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
        cal_avg_list = ['cpc_%s_%s_%s' % ('%s', i, '%s') for i in cnt_result_list] + \
                       ['cpc_%s_in_%s_%s' % ('%s', i, '%s') for i in cnt_result_list[3:]] + \
                       ['cpc_%s_out_%s_%s' % ('%s', i, '%s') for i in cnt_result_list[3:]]
        for s in cal_avg_list:
            if self.honeybee_info_result[s % ('total', 'pct')].values[0] != 0:
                self.honeybee_info_result[s % ('avg', 'cnt')] = \
                    self.honeybee_info_result[s % ('total', 'cnt')] / self.honeybee_info_result[s % ('total', 'pct')]
            else:
                self.honeybee_info_result[s % ('avg', 'cnt')] = 0




C = CalculateTagsForHoneybee()
data = C.honeybee_info_result
# import sys  
# reload(sys)  
# sys.setdefaultencoding('utf8')
# data.to_csv('D:/001.csv')
print data
# print data[['cpc_contact_weekday_out_cnt_po3m', 'cpc_total_out_contact_po3m_cnt', 'cpc_contact_weekday_out_cnt_p3m']]
# print data[['cpc_total_ser_cnt_p1m', 'cpc_total_ser_cnt_p2m', 'cpc_total_ser_cnt_p3m', 'cpc_total_ser_cnt']]
# # print data['cpc_ser_bank_cnt']
