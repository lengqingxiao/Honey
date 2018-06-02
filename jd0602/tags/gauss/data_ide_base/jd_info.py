# -*- coding: utf-8 -*-
import pandas as pd
import math
import itertools
import collections
from config.global_config import *
# import time
# import numpy as np
from data_transfer.data_process import ProcessDataForJD


class CalculateTagsForJD(ProcessDataForJD):

    def __init__(self):
        super(CalculateTagsForJD, self).__init__()
        self.jd_result_info = pd.DataFrame()
        self.calculate_jd_tags()
        self.batch_calculate_jd_order_type_info()
        self.batch_calculate_jd_order_basic_func()
        self.batch_calculate_jd_order_status_func()
        self.batch_calculate_jd_order_performance_m_func()
        self.batch_calculate_jd_order_performance_q_func()
        self.batch_calculate_jd_order_performance_s_func()
        self.batch_calculate_jd_order_performance_d_func()
        self.batch_calculate_jd_order_amount_info()
        self.batch_calculate_jd_order_cancel_info()
        self.calculate_jd_order_trade_other_info()

    def select_jd_order_data(self, pre_months):
        # 为空检查
        self.jd_order_info['year_month_day'] = pd.to_datetime(self.jd_order_info['year_month_day'])
        _reset_data = self.jd_order_info.set_index('year_month_day')
        _data_pm = _reset_data[self.jd_data_time[0:7]: self.calculate_times_for_service(pre_months)]
        return _data_pm

    @property
    def jd_order_data_p1m(self):
        return self.select_jd_order_data(1)

    def calculate_jd_basic_info(self):
        self.jd_result_info['csm_jd_user_mobile'] = pd.Series(self.raw_data[0].get('mobile'))
        self.jd_result_info['csm_jd_xb_score'] = pd.Series(self.raw_data[0].get('xiaobai', -999))
        self.jd_result_info['csm_jd_user_bt_line'] = pd.Series(self.raw_data[0].get('baitiao', -999))
        self.jd_result_info['csm_jd_user_bt_used_amt'] = pd.Series(self.raw_data[0].get('baitiaoDebt', -999))

        # self.jd_result_info['csm_jd_user_bt_debt_ratio'] = pd.Series(self.raw_data[0].get('baitiaoDebt', -999))
        self.jd_result_info['csm_jd_user_acc_scl'] = pd.Series(self.raw_data[0].get('securityLevel', '-999'))
        self.jd_result_info['csm_jd_user_acc_level'] = pd.Series(self.raw_data[0].get('level'))
        _bt_line = float(self.jd_result_info['csm_jd_user_bt_line'].values[0])
        _bt_debt = float(self.jd_result_info['csm_jd_user_bt_used_amt'].values[0])
        if _bt_debt and _bt_line != -999:
            self.jd_result_info['csm_jd_user_bt_debt_ratio'] = _bt_debt / _bt_line
        else:
            self.jd_result_info['csm_jd_user_bt_debt_ratio'] = 0
        self.jd_result_info['csm_jd_user_acc_balance'] = self.raw_data[0].get('yue', -999)
        self.jd_result_info['csm_jd_user_acc_xjk'] = self.raw_data[0].get('xiaojinku', -999)
        self.jd_result_info['csm_jd_user_submit_time'] = self.raw_data[0].get('submitTime', -999)
        self.jd_result_info['csm_jd_user_submit_time_str'] = self.jd_data_time

    def calculate_jd_region_info(self):
        if not self.jd_delivery_address_df.empty:
            self.jd_result_info['csm_jd_if_address_info'] = 1
            self.jd_result_info['csm_jd_acc_ra_cnt'] = self.jd_delivery_address_df.shape[0]
            self.jd_result_info['csm_jd_acc_csg_cnt'] = self.jd_delivery_address_df['name'].drop_duplicates().count()
            self.jd_result_info['csm_jd_acc_ra_pvc_cnt'] = \
                self.jd_delivery_address_df['user_province'].drop_duplicates().count()
            if self.jd_result_info['csm_jd_acc_ra_pvc_cnt'].values[0] == 1:
                self.jd_result_info['csm_jd_acc_ra_ias'] = 1
            else:
                self.jd_result_info['csm_jd_acc_ra_ias'] = 0
            _group_df = self.jd_delivery_address_df.groupby(['name']).count().reset_index()
            self.jd_result_info['csm_jd_csg_max_ra_cnt'] = _group_df['loc_sec'].max()
            _top_k_name = _group_df.sort_values(by=['loc_sec'], ascending=False)['name'].values[0]
            self.jd_result_info['csm_jd_ra_fre_name'] = _top_k_name
            _pvc_cnt_df = self.jd_delivery_address_df.groupby(['name']).apply(self.cal_num_func).reset_index()
            _pvc_cnt_df.columns = ['name', 'pvc_cnt']
            self.jd_result_info['csm_jd_csg_max_pvc_cnt'] = _pvc_cnt_df['pvc_cnt'].max()
            _add_cnt_df = self.jd_delivery_address_df.groupby(['name']).apply(self.cal_num_func_a).reset_index()
            _add_cnt_df.columns = ['name', 'add_cnt']
            _add_cnt_df['tags'] = _add_cnt_df['add_cnt'].apply(self.check_num_func)
            self.jd_result_info['csm_jd_csg_mra_cnt'] = _add_cnt_df[_add_cnt_df['tags'] == 1].shape[0]
            self.jd_result_info['csm_jd_csg_sra_cnt'] = _add_cnt_df[_add_cnt_df['tags'] == 0].shape[0]
            if _add_cnt_df.shape[0] > 1 and _add_cnt_df['tags'].sum() > 0:
                self.jd_result_info['csm_jd_acc_if_mp_mra'] = 1
            else:
                self.jd_result_info['csm_jd_acc_if_mp_mra'] = 0
            _add_edt_df = \
                self.jd_delivery_address_df.groupby(['detail_address']).apply(self.cal_num_func_b).reset_index()
            _add_edt_df.columns = ['detail_address', 'people_cnt']
            _add_edt_df['check_tags'] = _add_edt_df['people_cnt'].apply(self.check_num_func)
            if _add_edt_df['check_tags'].sum() == 0:
                self.jd_result_info['csm_jd_acc_if_mp_sra'] = 0
            else:
                self.jd_result_info['csm_jd_acc_if_mp_sra'] = 1

        else:
            self.jd_result_info['csm_jd_if_address_info'] = 0

    def calculate_jd_order_info(self):
        self.calculate_jd_order_basic_func()
        self.calculate_jd_order_status_func()
        self.calculate_jd_order_performance_m_func()
        self.calculate_jd_order_performance_q_func()
        self.calculate_jd_order_performance_s_func()
        self.calculate_jd_order_performance_d_func()
        self.calculate_jd_order_amount_info()
        self.calculate_jd_order_cancel_info()
        self.calculate_jd_order_type_info()
        self.calculate_jd_order_trade_time_info()

    def calculate_jd_tags(self):
        self.calculate_jd_basic_info()
        self.calculate_jd_region_info()
        self.calculate_jd_order_info()

    def calculate_jd_order_basic_func(self):
        # 后续重构
        if not self.jd_order_info.empty:
            self.jd_result_info['csm_jd_if_order_info'] = 1
            self.jd_result_info['csm_jd_cpd_order_cnt'] = \
                self.jd_order_info[self.jd_order_info['order_status'] == 1].shape[0]
            self.jd_result_info['csm_jd_cnc_order_cnt'] = \
                self.jd_order_info[self.jd_order_info['order_status'] == 2].shape[0]
            # print self.jd_result_info[self.jd_order_info['order_status'] == 1]
            self.jd_result_info['csm_jd_cpd_order_amt'] = \
                self.jd_order_info[self.jd_order_info['order_status'] == 1]['amount_f'].sum()
            self.jd_result_info['csm_jd_cnc_order_amt'] = \
                self.jd_order_info[self.jd_order_info['order_status'] == 2]['amount_f'].sum()
            self.jd_result_info['csm_jd_order_cnt'] = self.jd_order_info.shape[0]
            self.jd_result_info['csm_jd_order_amt'] = self.jd_order_info['amount_f'].sum()
            self.jd_result_info['csm_jd_cpd_order_cnt_ratio'] = \
                self.jd_result_info['csm_jd_cpd_order_cnt'] / self.jd_result_info['csm_jd_order_cnt']
            self.jd_result_info['csm_jd_cnc_order_cnt_ratio'] = \
                self.jd_result_info['csm_jd_cnc_order_cnt'] / self.jd_result_info['csm_jd_order_cnt']
            self.jd_result_info['csm_jd_cpd_order_amt_ratio'] = \
                self.jd_result_info['csm_jd_cpd_order_amt'] / self.jd_result_info['csm_jd_order_amt']
            self.jd_result_info['csm_jd_cnc_order_amt_ratio'] = \
                self.jd_result_info['csm_jd_cnc_order_amt'] / self.jd_result_info['csm_jd_order_amt']
            self.jd_result_info['csm_jd_order_avg_amt'] = \
                self.jd_result_info['csm_jd_order_amt'] / self.jd_result_info['csm_jd_order_cnt']
            self.jd_result_info['csm_jd_cpd_order_avg_amt'] = \
                self.jd_result_info['csm_jd_cpd_order_amt'] / self.jd_result_info['csm_jd_cpd_order_cnt']
            self.jd_result_info['csm_jd_cnc_order_avg_amt'] = \
                self.jd_result_info['csm_jd_cnc_order_amt'] / self.jd_result_info['csm_jd_cnc_order_cnt']

        else:
            self.jd_result_info['csm_jd_if_order_info'] = 0

    def batch_calculate_jd_order_basic_func(self):
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))
        # _cal_loop_dict = {'p1m': data_p1m, 'p2m': data_p2m, 'p3m': data_p3m, 'p6m': data_p6m}
        for _k, _v in _cal_loop_dict.items():

            self.jd_result_info['csm_jd_cpd_order_cnt_%s' % _k] = \
                _v[_v['order_status'] == 1].shape[0]
            self.jd_result_info['csm_jd_cnc_order_cnt_%s' % _k] = \
                _v[_v['order_status'] == 2].shape[0]
            # print self.jd_result_info[self.jd_order_info['order_status'] == 1]
            self.jd_result_info['csm_jd_cpd_order_amt_%s' % _k] = \
                _v[_v['order_status'] == 1]['amount_f'].sum()
            self.jd_result_info['csm_jd_cnc_order_amt_%s' % _k] = \
                _v[_v['order_status'] == 2]['amount_f'].sum()
            self.jd_result_info['csm_jd_order_cnt_%s' % _k] = _v.shape[0]
            self.jd_result_info['csm_jd_order_amt_%s' % _k] = _v['amount_f'].sum()
            self.jd_result_info['csm_jd_cpd_order_cnt_ratio_%s' % _k] = \
                self.jd_result_info['csm_jd_cpd_order_cnt_%s' % _k] / self.jd_result_info['csm_jd_order_cnt_%s' % _k]
            self.jd_result_info['csm_jd_cnc_order_cnt_ratio_%s' % _k] = \
                self.jd_result_info['csm_jd_cnc_order_cnt_%s' % _k] / self.jd_result_info['csm_jd_order_cnt_%s' % _k]
            self.jd_result_info['csm_jd_cpd_order_amt_ratio_%s' % _k] = \
                self.jd_result_info['csm_jd_cpd_order_amt_%s' % _k] / self.jd_result_info['csm_jd_order_amt_%s' % _k]
            self.jd_result_info['csm_jd_cnc_order_amt_ratio_%s' % _k] = \
                self.jd_result_info['csm_jd_cnc_order_amt_%s' % _k] / self.jd_result_info['csm_jd_order_amt_%s' % _k]
            self.jd_result_info['csm_jd_order_avg_amt_%s' % _k] = \
                self.jd_result_info['csm_jd_order_amt_%s' % _k] / self.jd_result_info['csm_jd_order_cnt_%s' % _k]
            self.jd_result_info['csm_jd_cpd_order_avg_amt_%s' % _k] = \
                self.jd_result_info['csm_jd_cpd_order_amt_%s' % _k] / self.jd_result_info['csm_jd_cpd_order_cnt_%s' % _k]
            self.jd_result_info['csm_jd_cnc_order_avg_amt_%s' % _k] = \
                self.jd_result_info['csm_jd_cnc_order_amt_%s' % _k] / self.jd_result_info['csm_jd_cnc_order_cnt_%s' % _k]

    def calculate_jd_order_status_func(self):
        # 后续重构
        _cal_query_tags_dict = {'bt': 2, 'ubt': 1, 'cod': 4, 'pbc': 5}
        _cal_loop_tags = ['cnt', 'amt']
        _cal_order_status = {'cnc': 2, 'cpd': 1}
        for _k, _v in _cal_query_tags_dict.items():

            self.jd_result_info['csm_jd_%s_order_cnt' % _k] = \
                self.jd_order_info[self.jd_order_info['pay_channel'] == _v].shape[0]
            self.jd_result_info['csm_jd_%s_order_amt' % _k] = \
                self.jd_order_info[self.jd_order_info['pay_channel'] == _v]['amount_f'].sum()
            if self.jd_result_info['csm_jd_%s_order_cnt' % _k].values[0] != 0:

                self.jd_result_info['csm_jd_%s_order_avg_amt' % _k] = \
                    self.jd_result_info['csm_jd_%s_order_amt' % _k] / self.jd_result_info['csm_jd_%s_order_cnt' % _k]
            else:
                self.jd_result_info['csm_jd_%s_order_avg_amt' % _k] = 0
            for _i in _cal_loop_tags:
                self.jd_result_info['csm_jd_%s_order_%s_ratio' % (_k, _i)] = \
                    self.jd_result_info['csm_jd_%s_order_%s' % (_k, _i)] / self.jd_result_info['csm_jd_order_%s' % _i]
            for _m, _n in _cal_order_status.items():
                self.jd_result_info['csm_jd_%s_%s_order_cnt' % (_k, _m)] = \
                    self.jd_order_info[(self.jd_order_info['pay_channel'] == _v) &
                                       (self.jd_order_info['order_status'] == _n)].shape[0]
                self.jd_result_info['csm_jd_%s_%s_order_amt' % (_k, _m)] = \
                    self.jd_order_info[(self.jd_order_info['pay_channel'] == _v) &
                                       (self.jd_order_info['order_status'] == _n)]['amount_f'].sum()
                if self.jd_result_info['csm_jd_%s_%s_order_cnt' % (_k, _m)].values[0] != 0:
                    self.jd_result_info['csm_jd_%s_%s_order_avg_amt' % (_k, _m)] = \
                        self.jd_result_info['csm_jd_%s_%s_order_amt' % (_k, _m)] / \
                        self.jd_result_info['csm_jd_%s_%s_order_cnt' % (_k, _m)]
                else:
                    self.jd_result_info['csm_jd_%s_%s_order_avg_amt' % (_k, _m)] = 0
                for _i in _cal_loop_tags:
                    if self.jd_result_info['csm_jd_%s_order_%s' % (_m, _i)].values[0] != 0:
                        self.jd_result_info['csm_jd_%s_order_%s_%s_%s_ratio' % (_k, _m, _i, _m)] = \
                            self.jd_result_info['csm_jd_%s_%s_order_%s' % (_k, _m, _i)] / self.jd_result_info[
                                'csm_jd_%s_order_%s' % (_m, _i)]
                    else:
                        self.jd_result_info['csm_jd_%s_order_%s_%s_%s_ratio' % (_k, _m, _i, _m)] = 0
                    self.jd_result_info['csm_jd_%s_order_%s_%s_total_ratio' % (_k, _m, _i)] = \
                        self.jd_result_info['csm_jd_%s_%s_order_%s' % (_k, _m, _i)] / self.jd_result_info[
                            'csm_jd_order_%s' % _i]

    def batch_calculate_jd_order_status_func(self):
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))

        _cal_query_tags_dict = {'bt': 2, 'ubt': 1, 'cod': 4, 'pbc': 5}
        _cal_loop_tags = ['cnt', 'amt']
        _cal_order_status = {'cnc': 2, 'cpd': 1}

        for _p, _q in _cal_loop_dict.items():
            for _k, _v in _cal_query_tags_dict.items():
                self.jd_result_info['csm_jd_%s_order_cnt_%s' % (_k, _p)] = \
                    _q[_q['pay_channel'] == _v].shape[0]
                self.jd_result_info['csm_jd_%s_order_amt_%s' % (_k, _p)] = \
                    _q[_q['pay_channel'] == _v]['amount_f'].sum()
                if self.jd_result_info['csm_jd_%s_order_cnt_%s' % (_k, _p)].values[0] != 0:

                    self.jd_result_info['csm_jd_%s_order_avg_amt_%s' % (_k, _p)] = \
                        self.jd_result_info['csm_jd_%s_order_amt_%s' % (_k, _p)] / \
                        self.jd_result_info['csm_jd_%s_order_cnt_%s' % (_k, _p)]
                else:
                    self.jd_result_info['csm_jd_%s_order_avg_amt_%s' % (_k, _p)] = 0
                for _i in _cal_loop_tags:
                    self.jd_result_info['csm_jd_%s_order_%s_ratio_%s' % (_k, _i, _p)] = \
                        self.jd_result_info['csm_jd_%s_order_%s_%s' % (_k, _i, _p)] / \
                        self.jd_result_info['csm_jd_order_%s_%s' % (_i, _p)]
                for _m, _n in _cal_order_status.items():
                    self.jd_result_info['csm_jd_%s_%s_order_cnt_%s' % (_k, _m, _p)] = \
                        _q[(_q['pay_channel'] == _v) & (_q['order_status'] == _n)].shape[0]
                    self.jd_result_info['csm_jd_%s_%s_order_amt_%s' % (_k, _m, _p)] = \
                        _q[(_q['pay_channel'] == _v) & (_q['order_status'] == _n)]['amount_f'].sum()
                    if self.jd_result_info['csm_jd_%s_%s_order_cnt_%s' % (_k, _m, _p)].values[0] != 0:
                        self.jd_result_info['csm_jd_%s_%s_order_avg_amt_%s' % (_k, _m, _p)] = \
                            self.jd_result_info['csm_jd_%s_%s_order_amt_%s' % (_k, _m, _p)] / \
                            self.jd_result_info['csm_jd_%s_%s_order_cnt_%s' % (_k, _m, _p)]
                    else:
                        self.jd_result_info['csm_jd_%s_%s_order_avg_amt_%s' % (_k, _m, _p)] = 0
                    for _i in _cal_loop_tags:
                        if self.jd_result_info['csm_jd_%s_order_%s_%s' % (_m, _i, _p)].values[0] != 0:
                            self.jd_result_info['csm_jd_%s_order_%s_%s_%s_ratio_%s' % (_k, _m, _i, _m, _p)] = \
                                self.jd_result_info['csm_jd_%s_%s_order_%s_%s' % (_k, _m, _i, _p)] / \
                                self.jd_result_info['csm_jd_%s_order_%s_%s' % (_m, _i, _p)]
                        else:
                            self.jd_result_info['csm_jd_%s_order_%s_%s_%s_ratio_%s' % (_k, _m, _i, _m, _p)] = 0
                        self.jd_result_info['csm_jd_%s_order_%s_%s_total_ratio_%s' % (_k, _m, _i, _p)] = \
                            self.jd_result_info['csm_jd_%s_%s_order_%s_%s' % (_k, _m, _i, _p)] / \
                            self.jd_result_info['csm_jd_order_%s_%s' % (_i, _p)]

    def calculate_jd_order_performance_m_func(self):
        # 空参模板后续加 函数更换
        if not self.jd_order_info.empty:
            _smf_data = self.jd_order_info[self.jd_order_info['order_status'] == 1]
            _smf_count_data = _smf_data.groupby('year_month').count().reset_index()
            _smf_sort_data = _smf_count_data.sort_values(by=['amount_f', 'year_month'], ascending=False)
            _smf_amt = _smf_data.groupby(by=['year_month']).agg({'amount_f': 'sum'}).reset_index()
            _smf_amt_sort = _smf_amt.sort_values(by=['amount_f', 'year_month'], ascending=False)
            self.jd_result_info['csm_jd_smf_order_max_cnt'] = _smf_count_data['amount'].max()
            self.jd_result_info['csm_jd_smf_order_max_cnt_rt'] = _smf_sort_data['year_month'].values[0]
            self.jd_result_info['csm_jd_smf_order_max_amt'] = _smf_amt_sort['amount_f'].values[0]
            self.jd_result_info['csm_jd_smf_order_max_amt_rt'] = _smf_amt_sort['year_month'].values[0]
            self.jd_result_info['csm_jd_smf_order_max_cnt_mt'] = \
                self.jd_result_info['csm_jd_smf_order_max_cnt_rt'].values[0][5:7]
            self.jd_result_info['csm_jd_smf_order_max_amt_mt'] = \
                self.jd_result_info['csm_jd_smf_order_max_amt_rt'].values[0][5:7]

            _cal_status_tags_dict = {'bt': 2, 'ubt': 1, 'cod': 4}
            for _k, _v in _cal_status_tags_dict.items():
                _smf_data_sec = _smf_data[_smf_data['pay_channel'] == _v]
                if not _smf_data_sec.empty:

                    _smf_count_data_sec = _smf_data_sec.groupby('year_month').count().reset_index()
                    _smf_sort_data_sec = _smf_count_data_sec.sort_values(by=['amount_f', 'year_month'], ascending=False)
                    _smf_amt_sec = _smf_data_sec.groupby(by=['year_month']).agg({'amount_f': 'sum'}).reset_index()
                    _smf_amt_sort_sec = _smf_amt_sec.sort_values(by=['amount_f', 'year_month'], ascending=False)
                    self.jd_result_info['csm_jd_%s_smf_order_max_cnt' % _k] = _smf_count_data_sec['amount'].max()
                    self.jd_result_info['csm_jd_%s_smf_order_max_cnt_rt' % _k] = _smf_sort_data_sec['year_month'].values[0]
                    self.jd_result_info['csm_jd_%s_smf_order_max_amt' % _k] = _smf_amt_sort_sec['amount_f'].values[0]
                    self.jd_result_info['csm_jd_%s_smf_order_max_amt_rt' % _k] = _smf_amt_sort_sec['year_month'].values[0]
                    self.jd_result_info['csm_jd_%s_smf_order_max_cnt_mt' % _k] = \
                        self.jd_result_info['csm_jd_%s_smf_order_max_cnt_rt' % _k].values[0][5:7]
                    self.jd_result_info['csm_jd_%s_smf_order_max_amt_mt' % _k] = \
                        self.jd_result_info['csm_jd_%s_smf_order_max_amt_rt' % _k].values[0][5:7]
                else:
                    self.jd_result_info['csm_jd_%s_smf_order_max_cnt' % _k] = 0
                    self.jd_result_info['csm_jd_%s_smf_order_max_cnt_rt' % _k] = '-999'
                    self.jd_result_info['csm_jd_%s_smf_order_max_amt' % _k] = 0
                    self.jd_result_info['csm_jd_%s_smf_order_max_amt_rt' % _k] = '-999'
                    self.jd_result_info['csm_jd_%s_smf_order_max_cnt_mt' % _k] = '-999'
                    self.jd_result_info['csm_jd_%s_smf_order_max_amt_mt' % _k] = '-999'

            _smf_data_2 = self.jd_order_info[self.jd_order_info['order_status'] == 2]
            _smf_count_data_2 = _smf_data_2.groupby('year_month').count().reset_index()
            _smf_sort_data_2 = _smf_count_data_2.sort_values(by=['amount_f', 'year_month'], ascending=False)
            _smf_amt_2 = _smf_data_2.groupby(by=['year_month']).agg({'amount_f': 'sum'}).reset_index()
            _smf_amt_sort_2 = _smf_amt_2.sort_values(by=['amount_f', 'year_month'], ascending=False)
            self.jd_result_info['csm_jd_smc_order_max_cnt'] = _smf_count_data_2['amount'].max()
            self.jd_result_info['csm_jd_smc_order_max_cnt_rt'] = _smf_sort_data_2['year_month'].values[0]
            self.jd_result_info['csm_jd_smc_order_max_amt'] = _smf_amt_sort_2['amount_f'].values[0]
            self.jd_result_info['csm_jd_smc_order_max_amt_rt'] = _smf_amt_sort_2['year_month'].values[0]
            self.jd_result_info['csm_jd_smc_order_max_cnt_mt'] = \
                self.jd_result_info['csm_jd_smc_order_max_cnt_rt'].values[0][5:7]
            self.jd_result_info['csm_jd_smc_order_max_amt_mt'] = \
                self.jd_result_info['csm_jd_smc_order_max_amt_rt'].values[0][5:7]

    def batch_calculate_jd_order_performance_m_func(self):
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))
        for _kx, _vx in _cal_loop_dict.items():
            if not _vx.empty:
                _smf_data = _vx[_vx['order_status'] == 1]
                _smf_count_data = _smf_data.groupby('year_month').count().reset_index()
                _smf_sort_data = _smf_count_data.sort_values(by=['amount_f', 'year_month'], ascending=False)
                # print _smf_sort_data
                _smf_amt = _smf_data.groupby(by=['year_month']).agg({'amount_f': 'sum'}).reset_index()
                _smf_amt_sort = _smf_amt.sort_values(by=['amount_f', 'year_month'], ascending=False)
                # print _smf_amt_sort
                self.jd_result_info['csm_jd_smf_order_max_cnt_%s' % _kx] = _smf_count_data['amount'].max()
                self.jd_result_info['csm_jd_smf_order_max_cnt_rt_%s' % _kx] = _smf_sort_data['year_month'].values[0]
                self.jd_result_info['csm_jd_smf_order_max_amt_%s' % _kx] = _smf_amt_sort['amount_f'].values[0]
                self.jd_result_info['csm_jd_smf_order_max_amt_rt_%s' % _kx] = _smf_amt_sort['year_month'].values[0]
                self.jd_result_info['csm_jd_smf_order_max_cnt_mt_%s' % _kx] = \
                    self.jd_result_info['csm_jd_smf_order_max_cnt_rt_%s' % _kx].values[0][5:7]
                self.jd_result_info['csm_jd_smf_order_max_amt_mt_%s' % _kx] = \
                    self.jd_result_info['csm_jd_smf_order_max_amt_rt_%s' % _kx].values[0][5:7]

                _cal_status_tags_dict = {'bt': 2, 'ubt': 1, 'cod': 4}
                for _k, _v in _cal_status_tags_dict.items():
                    _smf_data_sec = _smf_data[_smf_data['pay_channel'] == _v]
                    if not _smf_data_sec.empty:

                        _smf_count_data_sec = _smf_data_sec.groupby('year_month').count().reset_index()
                        _smf_sort_data_sec = _smf_count_data_sec.sort_values(by=['amount_f', 'year_month'], ascending=False)
                        _smf_amt_sec = _smf_data_sec.groupby(by=['year_month']).agg({'amount_f': 'sum'}).reset_index()
                        _smf_amt_sort_sec = _smf_amt_sec.sort_values(by=['amount_f', 'year_month'], ascending=False)
                        self.jd_result_info['csm_jd_%s_smf_order_max_cnt_%s' % (_k, _kx)] = _smf_count_data_sec['amount'].max()
                        self.jd_result_info['csm_jd_%s_smf_order_max_cnt_rt_%s' % (_k, _kx)] = _smf_sort_data_sec['year_month'].values[0]
                        self.jd_result_info['csm_jd_%s_smf_order_max_amt_%s' % (_k, _kx)] = _smf_amt_sort_sec['amount_f'].values[0]
                        self.jd_result_info['csm_jd_%s_smf_order_max_amt_rt_%s' % (_k, _kx)] = _smf_amt_sort_sec['year_month'].values[0]
                        self.jd_result_info['csm_jd_%s_smf_order_max_cnt_mt_%s' % (_k, _kx)] = \
                            self.jd_result_info['csm_jd_%s_smf_order_max_cnt_rt_%s' % (_k, _kx)].values[0][5:7]
                        self.jd_result_info['csm_jd_%s_smf_order_max_amt_mt_%s' % (_k, _kx)] = \
                            self.jd_result_info['csm_jd_%s_smf_order_max_amt_rt_%s' % (_k, _kx)].values[0][5:7]
                    else:
                        self.jd_result_info['csm_jd_%s_smf_order_max_cnt_%s' % (_k, _kx)] = 0
                        self.jd_result_info['csm_jd_%s_smf_order_max_cnt_rt_%s' % (_k, _kx)] = '-999'
                        self.jd_result_info['csm_jd_%s_smf_order_max_amt_%s' % (_k, _kx)] = 0
                        self.jd_result_info['csm_jd_%s_smf_order_max_amt_rt_%s' % (_k, _kx)] = '-999'
                        self.jd_result_info['csm_jd_%s_smf_order_max_cnt_mt_%s' % (_k, _kx)] = '-999'
                        self.jd_result_info['csm_jd_%s_smf_order_max_amt_mt_%s' % (_k, _kx)] = '-999'

                _smf_data_2 = _vx[_vx['order_status'] == 2]
                _smf_count_data_2 = _smf_data_2.groupby('year_month').count().reset_index()
                _smf_sort_data_2 = _smf_count_data_2.sort_values(by=['amount_f', 'year_month'], ascending=False)
                # print _smf_sort_data_2
                _smf_amt_2 = _smf_data_2.groupby(by=['year_month']).agg({'amount_f': 'sum'}).reset_index()
                _smf_amt_sort_2 = _smf_amt_2.sort_values(by=['amount_f', 'year_month'], ascending=False)
                # print _smf_amt_sort_2
                if not _smf_count_data_2.empty:
                    self.jd_result_info['csm_jd_smc_order_max_cnt_%s' % _kx] = _smf_count_data_2['amount_f'].max()
                if not _smf_sort_data_2.empty:
                    self.jd_result_info['csm_jd_smc_order_max_cnt_rt_%s' % _kx] = _smf_sort_data_2['year_month'].values[0]
                if not _smf_amt_sort_2.empty:
                    self.jd_result_info['csm_jd_smc_order_max_amt_%s' % _kx] = _smf_amt_sort_2['amount_f'].values[0]
                    self.jd_result_info['csm_jd_smc_order_max_amt_rt_%s' % _kx] = _smf_amt_sort_2['year_month'].values[0]
                    self.jd_result_info['csm_jd_smc_order_max_cnt_mt_%s' % _kx] = \
                        self.jd_result_info['csm_jd_smc_order_max_cnt_rt_%s' % _kx].values[0][5:7]
                    self.jd_result_info['csm_jd_smc_order_max_amt_mt_%s' % _kx] = \
                        self.jd_result_info['csm_jd_smc_order_max_amt_rt_%s' % _kx].values[0][5:7]

    def calculate_jd_order_performance_q_func(self):
        # 空参模板后续加 函数更换
        if not self.jd_order_info.empty:
            _smf_data = self.jd_order_info[self.jd_order_info['order_status'] == 1]
            _smf_count_data = _smf_data.groupby('year_quarter').count().reset_index()
            _smf_sort_data = _smf_count_data.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
            _smf_amt = _smf_data.groupby(by=['year_quarter']).agg({'amount_f': 'sum'}).reset_index()
            _smf_amt_sort = _smf_amt.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
            self.jd_result_info['csm_jd_sqf_order_max_cnt'] = _smf_count_data['amount'].max()
            self.jd_result_info['csm_jd_sqf_order_max_cnt_rt'] = _smf_sort_data['year_quarter'].values[0]
            self.jd_result_info['csm_jd_sqf_order_max_amt'] = _smf_amt_sort['amount_f'].values[0]
            self.jd_result_info['csm_jd_sqf_order_max_amt_rt'] = _smf_amt_sort['year_quarter'].values[0]
            self.jd_result_info['csm_jd_sqf_order_max_cnt_mt'] = \
                self.jd_result_info['csm_jd_sqf_order_max_cnt_rt'].values[0][5:7]
            self.jd_result_info['csm_jd_sqf_order_max_amt_mt'] = \
                self.jd_result_info['csm_jd_sqf_order_max_amt_rt'].values[0][5:7]

            _cal_status_tags_dict = {'bt': 2, 'ubt': 1, 'cod': 4}
            for _k, _v in _cal_status_tags_dict.items():
                _smf_data_sec = _smf_data[_smf_data['pay_channel'] == _v]
                if not _smf_data_sec.empty:

                    _smf_count_data_sec = _smf_data_sec.groupby('year_quarter').count().reset_index()
                    _smf_sort_data_sec = _smf_count_data_sec.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
                    _smf_amt_sec = _smf_data_sec.groupby(by=['year_quarter']).agg({'amount_f': 'sum'}).reset_index()
                    _smf_amt_sort_sec = _smf_amt_sec.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
                    self.jd_result_info['csm_jd_%s_sqf_order_max_cnt' % _k] = _smf_count_data_sec['amount'].max()
                    self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_rt' % _k] = _smf_sort_data_sec['year_quarter'].values[0]
                    self.jd_result_info['csm_jd_%s_sqf_order_max_amt' % _k] = _smf_amt_sort_sec['amount_f'].values[0]
                    self.jd_result_info['csm_jd_%s_sqf_order_max_amt_rt' % _k] = _smf_amt_sort_sec['year_quarter'].values[0]
                    self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_mt' % _k] = \
                        self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_rt' % _k].values[0][5:7]
                    self.jd_result_info['csm_jd_%s_sqf_order_max_amt_mt' % _k] = \
                        self.jd_result_info['csm_jd_%s_sqf_order_max_amt_rt' % _k].values[0][5:7]
                else:
                    self.jd_result_info['csm_jd_%s_sqf_order_max_cnt' % _k] = 0
                    self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_rt' % _k] = '-999'
                    self.jd_result_info['csm_jd_%s_sqf_order_max_amt' % _k] = 0
                    self.jd_result_info['csm_jd_%s_sqf_order_max_amt_rt' % _k] = '-999'
                    self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_mt' % _k] = '-999'
                    self.jd_result_info['csm_jd_%s_sqf_order_max_amt_mt' % _k] = '-999'
            # if not 判断
            _smf_data_2 = self.jd_order_info[self.jd_order_info['order_status'] == 2]
            _smf_count_data_2 = _smf_data_2.groupby('year_quarter').count().reset_index()
            _smf_sort_data_2 = _smf_count_data_2.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
            _smf_amt_2 = _smf_data_2.groupby(by=['year_quarter']).agg({'amount_f': 'sum'}).reset_index()
            _smf_amt_sort_2 = _smf_amt_2.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
            self.jd_result_info['csm_jd_sqc_order_max_cnt'] = _smf_count_data_2['amount'].max()
            self.jd_result_info['csm_jd_sqc_order_max_cnt_rt'] = _smf_sort_data_2['year_quarter'].values[0]
            self.jd_result_info['csm_jd_sqc_order_max_amt'] = _smf_amt_sort_2['amount_f'].values[0]
            self.jd_result_info['csm_jd_sqc_order_max_amt_rt'] = _smf_amt_sort_2['year_quarter'].values[0]
            self.jd_result_info['csm_jd_sqc_order_max_cnt_mt'] = \
                self.jd_result_info['csm_jd_sqc_order_max_cnt_rt'].values[0][5:7]
            self.jd_result_info['csm_jd_sqc_order_max_amt_mt'] = \
                self.jd_result_info['csm_jd_sqc_order_max_amt_rt'].values[0][5:7]

    def batch_calculate_jd_order_performance_q_func(self):
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))
        for _kx, _vx in _cal_loop_dict.items():
            if not _vx.empty:
                _smf_data = _vx[_vx['order_status'] == 1]
                _smf_count_data = _smf_data.groupby('year_quarter').count().reset_index()
                _smf_sort_data = _smf_count_data.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
                _smf_amt = _smf_data.groupby(by=['year_quarter']).agg({'amount_f': 'sum'}).reset_index()
                _smf_amt_sort = _smf_amt.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
                self.jd_result_info['csm_jd_sqf_order_max_cnt_%s' % _kx] = _smf_count_data['amount'].max()
                self.jd_result_info['csm_jd_sqf_order_max_cnt_rt_%s' % _kx] = _smf_sort_data['year_quarter'].values[0]
                self.jd_result_info['csm_jd_sqf_order_max_amt_%s' % _kx] = _smf_amt_sort['amount_f'].values[0]
                self.jd_result_info['csm_jd_sqf_order_max_amt_rt_%s' % _kx] = _smf_amt_sort['year_quarter'].values[0]
                self.jd_result_info['csm_jd_sqf_order_max_cnt_mt_%s' % _kx] = \
                    self.jd_result_info['csm_jd_sqf_order_max_cnt_rt_%s' % _kx].values[0][5:7]
                self.jd_result_info['csm_jd_sqf_order_max_amt_mt_%s' % _kx] = \
                    self.jd_result_info['csm_jd_sqf_order_max_amt_rt_%s' % _kx].values[0][5:7]

                _cal_status_tags_dict = {'bt': 2, 'ubt': 1, 'cod': 4}
                for _k, _v in _cal_status_tags_dict.items():
                    _smf_data_sec = _smf_data[_smf_data['pay_channel'] == _v]
                    if not _smf_data_sec.empty:

                        _smf_count_data_sec = _smf_data_sec.groupby('year_quarter').count().reset_index()
                        _smf_sort_data_sec = _smf_count_data_sec.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
                        _smf_amt_sec = _smf_data_sec.groupby(by=['year_quarter']).agg({'amount_f': 'sum'}).reset_index()
                        _smf_amt_sort_sec = _smf_amt_sec.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
                        self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_%s' % (_k, _kx)] = _smf_count_data_sec['amount'].max()
                        self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_rt_%s' % (_k, _kx)] = _smf_sort_data_sec['year_quarter'].values[0]
                        self.jd_result_info['csm_jd_%s_sqf_order_max_amt_%s' % (_k, _kx)] = _smf_amt_sort_sec['amount_f'].values[0]
                        self.jd_result_info['csm_jd_%s_sqf_order_max_amt_rt_%s' % (_k, _kx)] = _smf_amt_sort_sec['year_quarter'].values[0]
                        self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_mt_%s' % (_k, _kx)] = \
                            self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_rt_%s' % (_k, _kx)].values[0][5:7]
                        self.jd_result_info['csm_jd_%s_sqf_order_max_amt_mt_%s' % (_k, _kx)] = \
                            self.jd_result_info['csm_jd_%s_sqf_order_max_amt_rt_%s' % (_k, _kx)].values[0][5:7]
                    else:
                        self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_%s' % (_k, _kx)] = 0
                        self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_rt_%s' % (_k, _kx)] = '-999'
                        self.jd_result_info['csm_jd_%s_sqf_order_max_amt_%s' % (_k, _kx)] = 0
                        self.jd_result_info['csm_jd_%s_sqf_order_max_amt_rt_%s' % (_k, _kx)] = '-999'
                        self.jd_result_info['csm_jd_%s_sqf_order_max_cnt_mt_%s' % (_k, _kx)] = '-999'
                        self.jd_result_info['csm_jd_%s_sqf_order_max_amt_mt_%s' % (_k, _kx)] = '-999'
                # if not 判断
                _smf_data_2 = _vx[_vx['order_status'] == 2]
                _smf_count_data_2 = _smf_data_2.groupby('year_quarter').count().reset_index()
                _smf_sort_data_2 = _smf_count_data_2.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
                _smf_amt_2 = _smf_data_2.groupby(by=['year_quarter']).agg({'amount_f': 'sum'}).reset_index()
                _smf_amt_sort_2 = _smf_amt_2.sort_values(by=['amount_f', 'year_quarter'], ascending=False)
                self.jd_result_info['csm_jd_sqc_order_max_cnt_%s' % _kx] = _smf_count_data_2['amount'].max()
                if not _smf_sort_data_2.empty:
                    self.jd_result_info['csm_jd_sqc_order_max_cnt_rt_%s' % _kx] = _smf_sort_data_2['year_quarter'].values[0]
                if not _smf_amt_sort_2.empty:
                    self.jd_result_info['csm_jd_sqc_order_max_amt_%s' % _kx] = _smf_amt_sort_2['amount_f'].values[0]
                    self.jd_result_info['csm_jd_sqc_order_max_amt_rt_%s' % _kx] = _smf_amt_sort_2['year_quarter'].values[0]
                    self.jd_result_info['csm_jd_sqc_order_max_cnt_mt_%s' % _kx] = \
                        self.jd_result_info['csm_jd_sqc_order_max_cnt_rt_%s' % _kx].values[0][5:7]
                    self.jd_result_info['csm_jd_sqc_order_max_amt_mt_%s' % _kx] = \
                        self.jd_result_info['csm_jd_sqc_order_max_amt_rt_%s' % _kx].values[0][5:7]

    def calculate_jd_order_performance_s_func(self):
        _check_loop_list = ['bt', 'ubt', 'cod', 'pbc']
        _check_values = [self.jd_result_info['csm_jd_%s_order_cnt' % _i].values[0] for _i in _check_loop_list]
        # print _check_values
        _pay_tags = _check_loop_list[_check_values.index(max(_check_values))]
        self.jd_result_info['csm_jd_order_top_mop'] = _pay_tags
        self.jd_result_info['csm_jd_so_max_amt'] = self.jd_order_info['amount_f'].max()
        self.jd_result_info['csm_jd_bt_so_max_amt'] = \
            self.jd_order_info[self.jd_order_info['pay_channel'] == 1]['amount_f'].max()
        self.jd_result_info['csm_jd_ubt_so_max_amt'] = \
            self.jd_order_info[self.jd_order_info['pay_channel'] == 2]['amount_f'].max()
        self.jd_result_info['csm_jd_cod_so_max_amt'] = \
            self.jd_order_info[self.jd_order_info['pay_channel'] == 4]['amount_f'].max()
        self.jd_result_info['csm_jd_sfo_max_amt'] = \
            self.jd_order_info[self.jd_order_info['order_status'] == 1]['amount_f'].max()
        self.jd_result_info['csm_jd_bt_sfo_max_amt'] = \
            self.jd_order_info[(self.jd_order_info['pay_channel'] == 1) &
                               (self.jd_order_info['order_status'] == 1)]['amount_f'].max()
        self.jd_result_info['csm_jd_ubt_sfo_max_amt'] = \
            self.jd_order_info[(self.jd_order_info['pay_channel'] == 2) &
                               (self.jd_order_info['order_status'] == 1)]['amount_f'].max()
        self.jd_result_info['csm_jd_cod_sfo_max_amt'] = \
            self.jd_order_info[(self.jd_order_info['pay_channel'] == 4) &
                               (self.jd_order_info['order_status'] == 1)]['amount_f'].max()
        # self.jd_result_info['csm_jd_cod_sfo_max_amt'] = -999
        # print type(self.jd_result_info['csm_jd_cod_sfo_max_amt'].values[0])
        _check_list = ['csm_jd_so_max_amt', 'csm_jd_bt_so_max_amt', 'csm_jd_ubt_so_max_amt', 'csm_jd_cod_so_max_amt',
                       'csm_jd_sfo_max_amt', 'csm_jd_bt_sfo_max_amt', 'csm_jd_ubt_sfo_max_amt', 'csm_jd_cod_sfo_max_amt'
                       ]
        for _i in _check_list:
            if math.isnan(self.jd_result_info[_i].values[0]):
                # print 1
                self.jd_result_info[_i] = self.jd_result_info[_i].fillna(-999)
            else:
                pass
        # 结果校验 不能为nan

    def batch_calculate_jd_order_performance_s_func(self):
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))

        _check_loop_list = ['bt', 'ubt', 'cod', 'pbc']
        for _kx, _vx in _cal_loop_dict.items():

            _check_values = \
                [self.jd_result_info['csm_jd_%s_order_cnt_%s' % (_i, _kx)].values[0] for _i in _check_loop_list]
            # print _check_values
            _pay_tags = _check_loop_list[_check_values.index(max(_check_values))]
            self.jd_result_info['csm_jd_order_top_mop_%s' % _kx] = _pay_tags
            self.jd_result_info['csm_jd_so_max_amt_%s' % _kx] = _vx['amount_f'].max()
            self.jd_result_info['csm_jd_bt_so_max_amt_%s' % _kx] = \
                _vx[_vx['pay_channel'] == 1]['amount_f'].max()
            self.jd_result_info['csm_jd_ubt_so_max_amt_%s' % _kx] = \
                _vx[_vx['pay_channel'] == 2]['amount_f'].max()
            self.jd_result_info['csm_jd_cod_so_max_amt_%s' % _kx] = \
                _vx[_vx['pay_channel'] == 4]['amount_f'].max()
            self.jd_result_info['csm_jd_sfo_max_amt_%s' % _kx] = \
                _vx[_vx['order_status'] == 1]['amount_f'].max()
            self.jd_result_info['csm_jd_bt_sfo_max_amt_%s' % _kx] = \
                _vx[(_vx['pay_channel'] == 1) & (_vx['order_status'] == 1)]['amount_f'].max()
            self.jd_result_info['csm_jd_ubt_sfo_max_amt_%s' % _kx] = \
                _vx[(_vx['pay_channel'] == 2) & (_vx['order_status'] == 1)]['amount_f'].max()
            self.jd_result_info['csm_jd_cod_sfo_max_amt_%s' % _kx] = \
                _vx[(_vx['pay_channel'] == 4) & (_vx['order_status'] == 1)]['amount_f'].max()
            # self.jd_result_info['csm_jd_cod_sfo_max_amt'] = -999
            # print type(self.jd_result_info['csm_jd_cod_sfo_max_amt'].values[0])
            _check_list = ['csm_jd_so_max_amt_%s', 'csm_jd_bt_so_max_amt_%s', 'csm_jd_ubt_so_max_amt_%s',
                           'csm_jd_cod_so_max_amt_%s', 'csm_jd_sfo_max_amt_%s', 'csm_jd_bt_sfo_max_amt_%s',
                           'csm_jd_ubt_sfo_max_amt_%s', 'csm_jd_cod_sfo_max_amt_%s'
                           ]
            for _i in _check_list:
                if math.isnan(self.jd_result_info[_i % _kx].values[0]):
                    # print 1
                    self.jd_result_info[_i % _kx] = self.jd_result_info[_i % _kx].fillna(-999)
                else:
                    pass

    def calculate_jd_order_performance_d_func(self):
        _cal_dict = {'f': 1, 'c': 2}
        if not self.jd_order_info.empty:
            for _k, _v in _cal_dict.items():
                _smf_data = self.jd_order_info[self.jd_order_info['order_status'] == _v]
                if not _smf_data.empty:

                    _smf_count_data = _smf_data.groupby('year_month_day').count().reset_index()
                    _smf_sort_data = _smf_count_data.sort_values(by=['amount_f', 'year_month_day'], ascending=False)
                    _smf_amt = _smf_data.groupby(by=['year_month_day']).agg({'amount_f': 'sum'}).reset_index()
                    _smf_amt_sort = _smf_amt.sort_values(by=['amount_f', 'year_month_day'], ascending=False)
                    self.jd_result_info['csm_jd_sd%s_order_max_cnt' % _k] = _smf_count_data['amount'].max()
                    self.jd_result_info['csm_jd_sd%s_order_max_cnt_rt' % _k] = _smf_sort_data['year_month_day'].values[0]
                    self.jd_result_info['csm_jd_sd%s_order_max_amt' % _k] = _smf_amt_sort['amount_f'].values[0]
                    self.jd_result_info['csm_jd_sd%s_order_max_amt_rt' % _k] = _smf_amt_sort['year_month_day'].values[0]
                else:
                    self.jd_result_info['csm_jd_sd%s_order_max_cnt' % _k] = -999
                    self.jd_result_info['csm_jd_sd%s_order_max_cnt_rt' % _k] = '-999'
                    self.jd_result_info['csm_jd_sd%s_order_max_amt' % _k] = -999
                    self.jd_result_info['csm_jd_sd%s_order_max_amt_rt' % _k] = '-999'
            # print self.jd_result_info['csm_jd_sdf_order_max_cnt_rt'].values[0]
            _cal_days_list = ['csm_jd_sdf_order_max_cnt_rt', 'csm_jd_sdc_order_max_cnt_rt',
                              'csm_jd_sdf_order_max_amt_rt', 'csm_jd_sdc_order_max_amt_rt']
            for _i in _cal_days_list:

                if self.jd_result_info[_i].values[0] != '-999':

                    _n_time = self.calculate_time_func_n(self.jd_data_time)
                    _c_time = self.calculate_time_func_n(self.jd_result_info['csm_jd_sdf_order_max_cnt_rt'].values[0])
                    self.jd_result_info[_i + 's'] = (_n_time - _c_time).days + 1
                else:
                    self.jd_result_info[_i + 's'] = -999

    def batch_calculate_jd_order_performance_d_func(self):
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))

        _cal_dict = {'f': 1, 'c': 2}
        for _kx, _vx in _cal_loop_dict.items():

            if not _vx.empty:
                for _k, _v in _cal_dict.items():
                    _smf_data = _vx[_vx['order_status'] == _v]
                    if not _smf_data.empty:
                        # print _smf_data
                        _smf_count_data = _smf_data.groupby('year_month_day').count().reset_index()
                        _smf_sort_data = _smf_count_data.sort_values(by=['amount_f', 'year_month_day'], ascending=False)
                        # print _smf_sort_data
                        if _smf_data.shape[0] == 1:
                            _smf_amt_sort = _smf_data.reset_index()
                        else:
                            _smf_amt = _smf_data.groupby(by=['year_month_day']).agg({'amount_f': 'sum'}).reset_index()
                            _smf_amt_sort = _smf_amt.sort_values(by=['amount_f', 'year_month_day'], ascending=False)
                        self.jd_result_info['csm_jd_sd%s_order_max_cnt_%s' % (_k, _kx)] = _smf_count_data['amount_f'].max()
                        self.jd_result_info['csm_jd_sd%s_order_max_cnt_%s_rt' % (_k, _kx)] = \
                            _smf_sort_data['year_month_day'].values[0]
                        self.jd_result_info['csm_jd_sd%s_order_max_amt_%s' % (_k, _kx)] = \
                            _smf_amt_sort['amount_f'].values[0]
                        self.jd_result_info['csm_jd_sd%s_order_max_amt_%s_rt' % (_k, _kx)] = \
                            _smf_amt_sort['year_month_day'].values[0]
                    else:
                        self.jd_result_info['csm_jd_sd%s_order_max_cnt_%s' % (_k, _kx)] = -999
                        self.jd_result_info['csm_jd_sd%s_order_max_cnt_%s_rt' % (_k, _kx)] = '-999'
                        self.jd_result_info['csm_jd_sd%s_order_max_amt_%s' % (_k, _kx)] = -999
                        self.jd_result_info['csm_jd_sd%s_order_max_amt_%s_rt' % (_k, _kx)] = '-999'
                # print self.jd_result_info['csm_jd_sdf_order_max_cnt_rt'].values[0]
                _cal_days_list = ['csm_jd_sdf_order_max_cnt_%s_rt', 'csm_jd_sdc_order_max_cnt_%s_rt',
                                  'csm_jd_sdf_order_max_amt_%s_rt', 'csm_jd_sdc_order_max_amt_%s_rt']
                for _i in _cal_days_list:

                    if self.jd_result_info[_i % _kx].values[0] != '-999':

                        _n_time = self.calculate_time_func_n(self.jd_data_time)
                        _c_time = self.calculate_time_func_n(self.jd_result_info[_i % _kx].values[0])
                        self.jd_result_info[_i % _kx + 's'] = (_n_time - _c_time).days + 1
                    else:
                        self.jd_result_info[_i % _kx + 's'] = -999

    def calculate_jd_order_amount_info(self):
        _amount_check_list = [100, 200, 500, 1000, 3000, 5000, 10000]
        if not self.jd_order_info.empty:

            for _i in _amount_check_list:
                self.jd_result_info['csm_jd_order_amt_over_%s_cnt' % str(_i)] = \
                    self.jd_order_info[self.jd_order_info['if_order_amt_over_%s' % str(_i)] == 1].shape[0]
                self.jd_result_info['csm_jd_order_amt_over_%s_cnt_ratio' % str(_i)] = \
                    float(self.jd_order_info[self.jd_order_info['if_order_amt_over_%s' % str(_i)] == 1].shape[0]) / \
                    self.jd_result_info['csm_jd_order_cnt'].values[0]
            _success_data = self.jd_order_info[self.jd_order_info['order_status'] == 1]
            if not _success_data.empty:
                for _i in _amount_check_list:
                    self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt' % str(_i)] = \
                        _success_data[_success_data['if_order_amt_over_%s' % str(_i)] == 1].shape[0]
                    self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt_ratio' % str(_i)] = \
                        float(_success_data[_success_data['if_order_amt_over_%s' % str(_i)] == 1].shape[0]) / \
                        self.jd_result_info['csm_jd_cpd_order_cnt'].values[0]
            else:
                for _i in _amount_check_list:
                    self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt' % str(_i)] = 0
                    self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt_ratio' % str(_i)] = 0

        else:
            for _i in _amount_check_list:
                self.jd_result_info['csm_jd_order_amt_over_%s_cnt' % str(_i)] = 0
                self.jd_result_info['csm_jd_order_amt_over_%s_cnt_ratio' % str(_i)] = 0
                self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt' % str(_i)] = 0
                self.jd_result_info['csm_jd_order_amt_over_%s_cnt_ratio' % str(_i)] = 0

    def batch_calculate_jd_order_amount_info(self):
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))
        _amount_check_list = [100, 200, 500, 1000, 3000, 5000, 10000]
        for _kx, _vx in _cal_loop_dict.items():
            if not _vx.empty:

                for _i in _amount_check_list:
                    self.jd_result_info['csm_jd_order_amt_over_%s_cnt_%s' % (str(_i), _kx)] = \
                        _vx[_vx['if_order_amt_over_%s' % str(_i)] == 1].shape[0]
                    self.jd_result_info['csm_jd_order_amt_over_%s_cnt_ratio_%s' % (str(_i), _kx)] = \
                        self.jd_result_info['csm_jd_order_amt_over_%s_cnt_%s' % (str(_i), _kx)] / \
                        self.jd_result_info['csm_jd_order_cnt_%s' % _kx]
                _success_data = _vx[_vx['order_status'] == 1]
                if not _success_data.empty:
                    for _i in _amount_check_list:
                        self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt_%s' % (str(_i), _kx)] = \
                            _success_data[_success_data['if_order_amt_over_%s' % str(_i)] == 1].shape[0]
                        self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt_ratio_%s' % (str(_i), _kx)] = \
                            float(_success_data[_success_data['if_order_amt_over_%s' % str(_i)] == 1].shape[0]) / \
                            self.jd_result_info['csm_jd_cpd_order_cnt_%s' % _kx].values[0]
                else:
                    for _i in _amount_check_list:
                        self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt_%s' % (str(_i), _kx)] = 0
                        self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt_ratio_%s' % (str(_i), _kx)] = 0

            else:
                for _i in _amount_check_list:
                    self.jd_result_info['csm_jd_order_amt_over_%s_cnt_%s' % (str(_i), _kx)] = 0
                    self.jd_result_info['csm_jd_order_amt_over_%s_cnt_ratio_%s' % (str(_i), _kx)] = 0
                    self.jd_result_info['csm_jd_cpd_order_amt_over_%s_cnt_%s' % (str(_i), _kx)] = 0
                    self.jd_result_info['csm_jd_order_amt_over_%s_cnt_ratio_%s' % (str(_i), _kx)] = 0

    def calculate_jd_order_cancel_info(self):
        if not self.jd_order_info.empty:
            _check_col = list(self.jd_order_info['order_status'])
            _num_times = [(k, len(list(v))) for k, v in itertools.groupby(_check_col)]
            _cancel_times = [_m for _m in _num_times if _m[0] == 2]
            _seq_cancel_times = [_n for _n in _cancel_times if _n[1] > 1]
            if len(_cancel_times) > 0:
                _max_cancel_times = max(_cancel_times)[1]
            else:
                _max_cancel_times = 0
            self.jd_result_info['csm_jd_order_csc_cnc_cnt'] = len(_seq_cancel_times)
            self.jd_result_info['csm_jd_order_csc_cnc_max_oct'] = _max_cancel_times
        else:
            self.jd_result_info['csm_jd_order_csc_cnc_cnt'] = 0
            self.jd_result_info['csm_jd_order_csc_cnc_max_oct'] = 0

    def batch_calculate_jd_order_cancel_info(self):
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))
        for _kx, _vx in _cal_loop_dict.items():

            if not _vx.empty:
                _check_col = list(_vx['order_status'])
                _num_times = [(_k, len(list(_v))) for _k, _v in itertools.groupby(_check_col)]
                _cancel_times = [_m for _m in _num_times if _m[0] == 2]
                _seq_cancel_times = [_n for _n in _cancel_times if _n[1] > 1]
                if len(_cancel_times) > 0:
                    _max_cancel_times = max(_cancel_times)[1]
                else:
                    _max_cancel_times = 0
                self.jd_result_info['csm_jd_order_csc_cnc_cnt_%s' % _kx] = len(_seq_cancel_times)
                self.jd_result_info['csm_jd_order_csc_cnc_max_oct_%s' % _kx] = _max_cancel_times
            else:
                self.jd_result_info['csm_jd_order_csc_cnc_cnt_%s' % _kx] = 0
                self.jd_result_info['csm_jd_order_csc_cnc_max_oct_%s' % _kx] = 0

    def calculate_jd_order_type_info(self):
        """
        总数据计算 不包含数据时间切片
        :return:
        """
        # _cal_tags = ['hea']
        # _hea_amt = [200, 500, 1000, 3000, 5000, 10000]

        _cal_dict = CATEGORY_DICT
        # _cal_amt_check_1 = [1000, 2000, 3000, 5000, 10000, 30000, 50000]
        _cal_status_tags = ['cpd', 'cnc']
        _cal_agg_tags = ['cnt', 'amt']
        if not self.jd_order_info.empty:
            for _k, _v in _cal_dict.items():
                _cal_data = self.jd_order_info[self.jd_order_info['if_order_buy_%s' % _k] == 1]
                self.jd_result_info['csm_jd_order_%s_cnt' % _k] = _cal_data.shape[0]
                self.jd_result_info['csm_jd_order_%s_amt' % _k] = _cal_data['amount_f'].sum()
                self.jd_result_info['csm_jd_order_%s_cnt_ratio' % _k] = \
                    self.jd_result_info['csm_jd_order_%s_cnt' % _k] / self.jd_result_info['csm_jd_order_cnt']
                self.jd_result_info['csm_jd_order_%s_amt_ratio' % _k] = \
                    self.jd_result_info['csm_jd_order_%s_amt' % _k] / self.jd_result_info['csm_jd_order_amt']

                _cal_data_s = _cal_data[_cal_data['order_status'] == 1]
                _cal_data_c = _cal_data[_cal_data['order_status'] == 2]
                self.jd_result_info['csm_jd_order_%s_cpd_cnt' % _k] = _cal_data_s.shape[0]
                self.jd_result_info['csm_jd_order_%s_cnc_cnt' % _k] = _cal_data_c.shape[0]
                self.jd_result_info['csm_jd_%s_so_cpd_max_amt' % _k] = _cal_data_s['amount_f'].max()
                self.jd_result_info['csm_jd_%s_so_cnc_max_amt' % _k] = _cal_data_c['amount_f'].max()
                self.jd_result_info['csm_jd_order_%s_cpd_amt' % _k] = _cal_data_s['amount_f'].sum()
                self.jd_result_info['csm_jd_order_%s_cnc_amt' % _k] = _cal_data_c['amount_f'].sum()

                for _p in _cal_agg_tags:
                    for _q in _cal_status_tags:
                        self.jd_result_info['csm_jd_order_%s_%s_%s_%s_ratio' % (_k, _q, _p, _k)] = \
                            self.jd_result_info['csm_jd_order_%s_%s_%s' % (_k, _q, _p)] / self.jd_result_info[
                                'csm_jd_order_%s_%s' % (_k, _p)]
                        self.jd_result_info['csm_jd_order_%s_%s_%s_%s_ratio' % (_k, _q, _p, _q)] = \
                            self.jd_result_info['csm_jd_order_%s_%s_%s' % (_k, _q, _p)] / self.jd_result_info[
                                'csm_jd_%s_order_%s' % (_q, _p)]
                        self.jd_result_info['csm_jd_order_%s_%s_%s_total_ratio' % (_k, _q, _p)] = \
                            self.jd_result_info['csm_jd_order_%s_%s_%s' % (_k, _q, _p)] / self.jd_result_info[
                                'csm_jd_order_%s' % _p]
                # self.jd_result_info['csm_jd_order_%s_cpd_cnt_%s_ratio' % _k] = \
                #     self.jd_result_info['csm_jd_order_%s_cpd_cnt' % _k] / self.jd_result_info['csm_jd_order_%s_cnt' % _k]
                # self.jd_result_info['csm_jd_order_%s_cpd_cnt_cpd_ratio' % _k] = \
                #     self.jd_result_info['csm_jd_order_%s_cpd_cnt' % _k] / self.jd_result_info['csm_jd_cpd_order_cnt']
                # self.jd_result_info['csm_jd_order_%s_cpd_cnt_total_ratio' % _k] = \
                #     self.jd_result_info['csm_jd_order_%s_cpd_cnt' % _k] / self.jd_result_info['csm_jd_order_cnt']

                if not _cal_data_s.empty:
                    if len(_v) > 0:
                        for _n in _v:
                            self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt' % (_k, str(_n))] = \
                                _cal_data_s[_cal_data_s['amount_f'] > _n].shape[0]
                            # 占总完成
                            self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_cpd_ratio' % (_k, str(_n))] = \
                                self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt' % (_k, str(_n))] / \
                                self.jd_result_info['csm_jd_cpd_order_cnt']
                            # 占当前类别已完成数量
                            self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_%s_ratio' % (_k, str(_n), _k)] = \
                                self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt' % (_k, str(_n))] / self.jd_result_info['csm_jd_order_%s_cpd_cnt' % _k]

    def batch_calculate_jd_order_type_info(self):

        _cal_status_tags = ['cpd', 'cnc']
        _cal_agg_tags = ['cnt', 'amt']
        _cal_dict = CATEGORY_DICT
        self.jd_order_info['year_month_day'] = pd.to_datetime(self.jd_order_info['year_month_day'])
        # print self.jd_order_info
        _reset_data = self.jd_order_info.set_index('year_month_day')
        # print _reset_data
        # print self.jd_data_time[0:7]
        # print self.calculate_times_for_service(1)
        # print self.calculate_times_for_service(6)
        # print _reset_data['2016-12': '2017-01']
        # print _reset_data['2016-12': '2016-10']
        data_p1m = _reset_data[self.jd_data_time[0:7]: self.calculate_times_for_service(1)]
        data_p2m = _reset_data[self.jd_data_time[0:7]: self.calculate_times_for_service(2)]
        data_p3m = _reset_data[self.jd_data_time[0:7]: self.calculate_times_for_service(3)]
        data_p6m = _reset_data[self.jd_data_time[0:7]: self.calculate_times_for_service(6)]
        # print data_p6m
        _cal_loop_dict = {'p1m': data_p1m, 'p2m': data_p2m, 'p3m': data_p3m, 'p6m': data_p6m}
        for _m, _nb in _cal_loop_dict.items():
            _sec_data = _nb[_nb['order_status'] == 1]
            if not _sec_data.empty:
                for _k, _v in _cal_dict.items():
                    # 加时间标记
                    _cal_data = _sec_data[_sec_data['if_order_buy_%s' % _k] == 1]
                    self.jd_result_info['csm_jd_order_%s_cnt_%s' % (_k, _m)] = _cal_data.shape[0]
                    self.jd_result_info['csm_jd_order_%s_amt_%s' % (_k, _m)] = _cal_data['amount_f'].sum()
                    self.jd_result_info['csm_jd_order_%s_avg_amt_%s' % (_k, _m)] = \
                        self.jd_result_info['csm_jd_order_%s_amt_%s' % (_k, _m)] / \
                        self.jd_result_info['csm_jd_order_%s_cnt_%s' % (_k, _m)]
                    self.jd_result_info['csm_jd_order_%s_cnt_ratio_%s' % (_k, _m)] = \
                        self.jd_result_info['csm_jd_order_%s_cnt_%s' % (_k, _m)] / \
                        self.jd_result_info['csm_jd_cpd_order_cnt']
                    self.jd_result_info['csm_jd_order_%s_amt_ratio_%s' % (_k, _m)] = \
                        self.jd_result_info['csm_jd_order_%s_amt_%s' % (_k, _m)] / \
                        self.jd_result_info['csm_jd_cpd_order_amt']

                    if not _sec_data.empty:
                        if len(_v) > 0:
                            for _n in _v:
                                self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_%s' % (_k, str(_n), _m)] = \
                                    _sec_data[_sec_data['amount_f'] > _n].shape[0]
                                # 占总完成
                                self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_cpd_ratio_%s' % (_k, str(_n), _m)] = \
                                    self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_%s' % (_k, str(_n), _m)] / \
                                    self.jd_result_info['csm_jd_cpd_order_cnt']
                                # 占当前类别已完成数量
                                self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_%s_ratio_%s' % (_k, str(_n), _k, _m)] = \
                                    self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_%s' % (_k, str(_n), _m)] / \
                                    self.jd_result_info['csm_jd_order_%s_cpd_cnt' % _k]
                    # _cal_data = _sec_data[_sec_data['if_order_buy_%s' % _k] == 1]
                    # self.jd_result_info['csm_jd_order_%s_cnt' % _m] = _cal_data.shape[0]
                    # self.jd_result_info['csm_jd_order_%s_amt' % _m] = _cal_data['amount_f'].sum()
                    # self.jd_result_info['csm_jd_order_%s_cnt_ratio' % _m] = \
                    #     self.jd_result_info['csm_jd_order_%s_cnt' % _m] / self.jd_result_info['csm_jd_order_cnt']
                    # self.jd_result_info['csm_jd_order_%s_amt_ratio' % _m] = \
                    #     self.jd_result_info['csm_jd_order_%s_amt' % _m] / self.jd_result_info['csm_jd_order_amt']
                    # _cal_data_s = _cal_data[_cal_data['order_status'] == 1]
                    # if not _cal_data_s.empty:
                    #     self.jd_result_info['csm_jd_order_%s_cpd_cnt'] = _cal_data_s.shape[0]
                    #     for _n in _v:
                    #         self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt' % (_k, str(_n))] = \
                    #             _cal_data_s[_cal_data_s['amount_f'] > _n].shape[0]
                    #         # 占总完成
                    #         self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_cpd_ratio' % (_k, str(_n))] = \
                    #             self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt' % (_k, str(_n))] / \
                    #             self.jd_result_info['csm_jd_cpd_order_cnt']
                    #         # 占当前类别已完成数量
                    #         self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt_%s_ratio' % (_k, str(_n), _k)] = \
                    #             self.jd_result_info['csm_jd_order_%s_amt_over_%s_cnt' % (_k, str(_n))] / \
                    #             self.jd_result_info['csm_jd_order_%s_cpd_cnt']

    def calculate_jd_order_trade_time_info(self):
        # _cal_category = ['hea', 'laj', 'mdg', 'cof', 'hfs', 'sct', 'pwh', 'pet', 'ods', 'car', 'mab', 'food', 'nhc',
        #                  'book', 'fin', 'trv', 'ltr', 'other']
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))
        _status_dict = {'cpd': 1, 'cnc': 2}
        _cal_trade_time = {'early_morning': 1, 'morning': 2, 'forenoon': 3, 'noon': 4, 'afternoon': 5, 'night': 6}
        if not self.jd_order_info.empty:
            for _k, _v in _cal_trade_time.items():
                _cal_data_time_sec = self.jd_order_info[self.jd_order_info['order_trade_time'] == _v]
                self.jd_result_info['csm_jd_%s_order_cnt' % _k] = _cal_data_time_sec.shape[0]
                self.jd_result_info['csm_jd_%s_order_amt' % _k] = _cal_data_time_sec['amount_f'].sum()
                self.jd_result_info['csm_jd_%s_order_avg_amt' % _k] = \
                    self.jd_result_info['csm_jd_%s_order_amt' % _k] / self.jd_result_info['csm_jd_%s_order_cnt' % _k]
                for _km, _vm in _cal_loop_dict.items():
                    _cal_t_data = _vm[_vm['order_trade_time'] == _v]
                    self.jd_result_info['csm_jd_%s_order_cnt_%s' % (_k, _km)] = _cal_t_data.shape[0]
                    self.jd_result_info['csm_jd_%s_order_amt_%s' % (_k, _km)] = _cal_t_data['amount_f'].sum()
                    self.jd_result_info['csm_jd_%s_order_avg_amt_%s' % (_k, _km)] = \
                        self.jd_result_info['csm_jd_%s_order_amt_%s' % (_k, _km)] / \
                        self.jd_result_info['csm_jd_%s_order_cnt_%s' % (_k, _km)]

                for _m, _n in _status_dict.items():
                    _cal_data_df = _cal_data_time_sec[_cal_data_time_sec['order_status'] == _n]
                    self.jd_result_info['csm_jd_%s_%s_order_cnt' % (_k, _m)] = _cal_data_df.shape[0]
                    self.jd_result_info['csm_jd_%s_%s_order_amt' % (_k, _m)] = _cal_data_df['amount_f'].sum()
                    self.jd_result_info['csm_jd_%s_%s_order_avg_amt' % (_k, _m)] = \
                        self.jd_result_info['csm_jd_%s_%s_order_amt' % (_k, _m)] / \
                        self.jd_result_info['csm_jd_%s_%s_order_cnt' % (_k, _m)]
                    self.jd_result_info['csm_jd_%s_%s_order_cnt_ratio' % (_k, _m)] = \
                        self.jd_result_info['csm_jd_%s_%s_order_cnt' % (_k, _m)] / \
                        self.jd_result_info['csm_jd_%s_order_cnt' % _m]
                    self.jd_result_info['csm_jd_%s_%s_order_amt_ratio' % (_k, _m)] = \
                        self.jd_result_info['csm_jd_%s_%s_order_amt' % (_k, _m)] / \
                        self.jd_result_info['csm_jd_%s_order_amt' % _m]
                for _i in CATEGORY_TAGS:
                    _cal_data_c = _cal_data_time_sec[_cal_data_time_sec['if_order_buy_%s' % _i] == 1]
                    _cal_data_cs = _cal_data_c[_cal_data_c['order_status'] == 1]
                    self.jd_result_info['csm_jd_%s_%s_order_cnt' % (_k, _i)] = _cal_data_cs.shape[0]
                    self.jd_result_info['csm_jd_%s_%s_order_amt' % (_k, _i)] = _cal_data_cs['amount_f'].sum()
                    self.jd_result_info['csm_jd_%s_%s_order_cnt_ratio' % (_k, _i)] = \
                        self.jd_result_info['csm_jd_%s_%s_order_cnt' % (_k, _i)] / \
                        self.jd_result_info['csm_jd_%s_cpd_order_cnt' % _k]
                    self.jd_result_info['csm_jd_%s_%s_order_amt_ratio' % (_k, _i)] = \
                        self.jd_result_info['csm_jd_%s_%s_order_amt' % (_k, _i)] / \
                        self.jd_result_info['csm_jd_%s_cpd_order_amt' % _k]
        _time_check_list = [_i for _i in _cal_trade_time.keys()]
        _time_result = [self.jd_result_info['csm_jd_%s_order_cnt' % _i].values[0] for _i in _time_check_list]
        _trade_time_fre = sorted(zip(_time_result, _time_check_list))
        for _i in range(3):
            self.jd_result_info['csm_jd_user_trade_time_top_%s' % str(_i+1)] = _trade_time_fre[-1-_i][1]
        for _u in _cal_time_tags:
            _time_sec_result = \
                [self.jd_result_info['csm_jd_%s_order_cnt_%s' % (_i, _u)].values[0] for _i in _time_check_list]
            _trade_time_sec_fre = sorted(zip(_time_sec_result, _time_check_list))
            for _r in range(3):
                self.jd_result_info['csm_jd_user_trade_time_top_%s_%s' % (str(_r + 1), _u)] = _trade_time_sec_fre[-1-_r][1]

    def calculate_jd_order_trade_other_info(self):
        _cal_category = ['hea', 'laj', 'mdg', 'cof', 'hfs', 'sct', 'pwh', 'pet', 'ods', 'car', 'mab', 'food', 'nhc',
                         'book', 'fin', 'trv', 'ltr']
        _cal_data_list = [self.select_jd_order_data(_i) for _i in (1, 2, 3, 6)]
        _cal_time_tags = ['p1m', 'p2m', 'p3m', 'p6m']
        _cal_loop_dict = dict(zip(_cal_time_tags, _cal_data_list))
        if not self.jd_order_info.empty:
            _smf_data = self.jd_order_info[self.jd_order_info['order_status'] == 1]
            _smf_count_data = _smf_data.groupby('time').count().reset_index()
            self.jd_result_info['csm_jd_order_max_cnt_stp'] = _smf_count_data['amount_f'].max()

            for _i in _cal_category:
                _cal_category_data = self.jd_order_info[self.jd_order_info['if_order_buy_%s' % _i] == 1]
                _cal_category_fre = list(_cal_category_data['order_trade_time'])
                _cal_category_fre_dict = dict(collections.Counter(_cal_category_fre))
                _cal_main_time = max(_cal_category_fre_dict, key=_cal_category_fre_dict.get)
                self.jd_result_info['csm_jd_%s_trade_main_time' % _i] = _cal_main_time
            _cal_category_cnt = [self.jd_order_info['if_order_buy_%s' % _i].sum() for _i in _cal_category]
            _trade_category_fre = sorted(zip(_cal_category_cnt, _cal_category))
            for _j in range(3):
                self.jd_result_info['csm_jd_order_main_type_%s' % str(_j + 1)] = \
                    _trade_category_fre[-1 - _j][1]

        for _k, _v in _cal_loop_dict.items():
            _pmf_data = _v[_v['order_status'] == 1]
            _pmf_count_data = _pmf_data.groupby('time').count().reset_index()
            self.jd_result_info['csm_jd_order_max_cnt_stp_%s' % _k] = _pmf_count_data['amount_f'].drop_duplicates().max()

            _cal_category_cnt_b = [_v['if_order_buy_%s' % _i].sum() for _i in _cal_category]
            _trade_category_fre_b = sorted(zip(_cal_category_cnt_b, _cal_category))
            for _j in range(3):
                self.jd_result_info['csm_jd_order_main_type_%s_%s' % (str(_j + 1), _k)] = \
                    _trade_category_fre_b[-1 - _j][1]



if __name__ == '__main__':

    fc = CalculateTagsForJD()
    da = fc.jd_result_info
    print da
    print da[['csm_jd_user_trade_time_top_1', 'csm_jd_user_trade_time_top_2', 'csm_jd_user_trade_time_top_3']]
    print da[['csm_jd_user_trade_time_top_1_p1m', 'csm_jd_user_trade_time_top_2_p1m', 'csm_jd_user_trade_time_top_3_p1m']]
    print da[
        ['csm_jd_user_trade_time_top_1_p6m', 'csm_jd_user_trade_time_top_2_p6m', 'csm_jd_user_trade_time_top_3_p6m']]
    # for i in da.columns:
    #     print da[i]
    # print da['csm_jd_bt_order_cpd_cnt_cpd_ratio']

