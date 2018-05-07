# -*- coding: utf-8 -*-
########################################################################################################################
# 计算模块
########################################################################################################################

import datetime
import pandas as pd
from functools import partial
from config.global_config import *
from config.log_config import *
from config.route_config import *
from data_transfer.data_query import QueryData
import warnings
warnings.filterwarnings("ignore")


class DataProcess(object):

    def __init__(self):
        # self.data = pd.read_csv('D:/elephant_data_all_0413.csv')
        self.time_query_seq = DataProcess.batch_calculate_times()
        self.data = QueryData.query_data_from_mysql_mc(MYSQL_DB_CONFIG[0], MYSQL_DB_CONFIG[1], MYSQL_DB_CONFIG[2],
                                                       MYSQL_DB_CONFIG[3], MYSQL_DB_CONFIG[4],
                                                       QUERY_SQL_ALL % (self.time_query_seq[2], self.time_query_seq[0]))
        self.data_pre_1 = pd.DataFrame()
        self.data_pre_7 = pd.DataFrame()
        self.data_pre_15 = pd.DataFrame()
        self.data_pre_30 = pd.DataFrame()
        self.data_process()

    def data_process(self):
        self.data['order_time'] = self.data['order_time'].apply(DataProcess.check_order_time)
        str_order_code_list = [_i[0:2] for _i in list(self.data['order_code'])]
        str_order_time_list = [_i[0:10] for _i in list(self.data['order_time'])]
        self.data['order_type_new'] = pd.Series(str_order_code_list)
        self.data['order_time_new'] = pd.Series(str_order_time_list)
        self.data['type_new'] = self.data['order_type_new'].map(ORDER_TYPE_MAP)
        self.data['order_time'] = pd.to_datetime(self.data['order_time'])
        self.data = self.data.set_index('order_time')
        logging.info('数据映射完毕')
        try:
            self.data_pre_1 = self.data[self.time_query_seq[0]]
            self.data_pre_7 = self.data[self.time_query_seq[1]:self.time_query_seq[0]]
            self.data_pre_15 = self.data[self.time_query_seq[2]:self.time_query_seq[0]]
            self.data_pre_30 = self.data[self.time_query_seq[3]:self.time_query_seq[0]]
        except IndexError:
            print '当前数据异常，请检查，切片数据全为空'

    @staticmethod
    def check_order_time(x):
        if type(x) == str:
            return x
        else:
            return str(x)[0:21]

    @staticmethod
    def batch_calculate_times(query_list=(1, 7, 15, 31)):
        query_time_bins = []
        for _dq in query_list:
            query_time_bins.append(DataProcess.calculate_times(_dq))
        logging.info('批量计算时间完毕')
        return query_time_bins

    @staticmethod
    def calculate_times(pre_days):

        return (datetime.datetime.now() + datetime.timedelta(days=-pre_days)).strftime('%Y-%m-%d')


class CalculateTags(DataProcess):

    def __init__(self):

        super(CalculateTags, self).__init__()
        self.calculate_sdp_ep_info = self.calculate_pass_ep_info_config(self.calculate_someday_pass_info)
        self.calculate_edp_ep_info = self.calculate_pass_ep_info_config(self.calculate_everyday_pass_info)

    @staticmethod
    def calculate_overall_ratio_func(sec_data, distinct=False):
        if sec_data.shape[0] > 0:
            if distinct:
                return float(sec_data[sec_data['lastreview_decision'] == 1].drop_duplicates('mobile').
                             shape[0]) / sec_data.shape[0]
            else:
                return float(sec_data[sec_data['lastreview_decision'] == 1].shape[0]) / sec_data.shape[0]
        else:
            return 0

    @classmethod
    def batch_calculate_performance_ratio(cls, sec_data, if_distinct=False):
        result_list = list()
        if not sec_data.empty:
            result_list.append(cls.calculate_overall_ratio_func(sec_data, if_distinct))
            for _z in range(9):
                df = sec_data[sec_data['type_new'] == _z + 1]
                result_list.append(cls.calculate_overall_ratio_func(df, if_distinct))
        return result_list

    @classmethod
    def cal_distinct_func(cls, sec_data):
        sec_data = sec_data.drop_duplicates('mobile')
        result = sec_data['order_code'].count()
        return result

    @classmethod
    def cal_fill_func(cls, sec_data, fill_col):
        if type(sec_data[fill_col].values[0]) == str:
            sec_data.loc[:, fill_col] = sec_data[fill_col].fillna('-999')
        else:
            sec_data.loc[:, fill_col] = sec_data[fill_col].fillna(-999)
        return sec_data

    def calculate_someday_performance(self, method='order'):

        """
        计算 前1天 ，前7 天 ， 前15天，前30天
        总体 和 各个产品的 总体通过率  默认按订单
        method ： order 按订单统计 和 people 按人统计
        return : result DataFrame

        """
        result_all_list = list()
        _df = pd.DataFrame()
        logging.info('开始总体和各个产品区块时间总体通过率计算，计算方式by %s' % method)
        intro_result = ['product_type_%s' % (s + 1) for s in range(9)]
        intro_result.insert(0, 'product_all')
        if method == 'order':
            _df['summary_by_order'] = pd.Series(intro_result)
        else:
            _df['summary_by_people'] = pd.Series(intro_result)
        _check_dict = {'order': False, 'people': True}
        for m in [self.data_pre_1, self.data_pre_7, self.data_pre_15, self.data_pre_30]:
            r_df = self.batch_calculate_performance_ratio(m, _check_dict.get(method))
            result_all_list.append(r_df)
        _df_columns = ['pre_1_days', 'pre_7_days', 'pre_15_days', 'pre_30_days']
        for n in range(4):
            _df[_df_columns[n]] = pd.Series(result_all_list[n])
        logging.info('计算完毕，计算方式by %s' % method)
        return _df

    def calculate_everyday_performance(self, method='order'):
        """
        计算 前30天 每天情况
        总体 和 各个产品的 总体通过率 （现在按照前30天计算，如需计算其他数据 ，需更改此方法）
        method ： order 按订单统计 和 people 按人统计
        return : result DataFrame

        """
        _check_dict = {'order': False, 'people': True}
        logging.info('开始总体和各产品区块时间内每天总体通过率计算，计算方式by %s' % method)
        # 函数柯里化
        cal_func = partial(self.calculate_overall_ratio_func, distinct=_check_dict.get(method))
        logging.info('函数柯里化完成，进行下一步处理。。')
        _result_df = pd.DataFrame()
        if not self.data_pre_30.empty:
            _cal_data = self.data_pre_30[['order_code', 'order_time_new', 'lastreview_decision', 'type_new', 'mobile']]
            all_result_df = _cal_data.groupby('order_time_new').apply(cal_func).reset_index()
            all_result_df.columns = ['order_time', 'product_all']
            _result_df['order_time'] = all_result_df['order_time']
            _result_df['product_all'] = all_result_df['product_all']
            for _i in range(9):
                _cal_col_name = 'product_type_%s' % (_i + 1)
                _product_cal_df = _cal_data[_cal_data['type_new'] == _i + 1]
                _product_result_df = _product_cal_df.groupby('order_time_new').apply(
                    cal_func).reset_index()
                try:
                    _result_df[_cal_col_name] = pd.Series(_product_result_df.iloc[:, 1])
                except IndexError:
                    _result_df[_cal_col_name] = pd.Series(-999)
            logging.info('计算完成，计算方式by %s' % method)
        return _result_df

    @classmethod
    def calculate_everyday_pass_info(cls, cal_col, cal_data, cal_func=None, method='order'):
        """
        计算 某段时间每天通过人群 总体指标情况
        cal_col : 计算字段名称 字符串
        cal_data : 需计算数据框
        cal_func ： binning func
        method ： order 按订单统计 和 people 按人统计
        return : result DataFrame

        """
        _cal_data = cal_data
        logging.info('开始计算某段时间每天通过人群指标 %s情况，分箱函数为 %s，计算方式by %s' % (cal_col, str(cal_func),
                                                                                                method))
        if not _cal_data.empty:
            _cal_pass_data = _cal_data[_cal_data['lastreview_decision'] == 1]
            _cal_pass_col = cls.cal_fill_func(_cal_pass_data, cal_col)
            if cal_func is not None:
                _cal_col_new = '%s_bg' % cal_col
                _cal_pass_col.loc[:, _cal_col_new] = _cal_pass_col[cal_col].apply(cal_func)
                if method == 'order':
                    all_result_df = _cal_pass_col.groupby(['order_time_new', _cal_col_new])[
                        'order_code'].count().reset_index()
                else:
                    all_result_df = _cal_pass_col.groupby(['order_time_new', _cal_col_new]).apply(
                        cls.cal_distinct_func).reset_index()
                all_result_df.columns = ['order_time', _cal_col_new, '%s_pct' % _cal_col_new]
                all_people_count = all_result_df['%s_pct' % _cal_col_new].groupby(
                    all_result_df['order_time']).sum().reset_index()
                all_people_count.columns = ['order_time', 'count']
                all_result_df = all_result_df.set_index('order_time')
                all_people_count = all_people_count.set_index('order_time')
                result_all_f = all_result_df.join(all_people_count).reset_index()
                result_all_f['ratio'] = result_all_f['%s_pct' % _cal_col_new] / result_all_f['count']
            else:
                if method == 'order':
                    all_result_df = _cal_pass_col.groupby(['order_time_new', cal_col])['order_code'].count().\
                        reset_index()
                else:
                    all_result_df = _cal_pass_col.groupby(['order_time_new', cal_col]).apply(
                        cls.cal_distinct_func).reset_index()
                all_result_df.columns = ['order_time', cal_col, '%s_pct' % cal_col]
                all_people_count = all_result_df['%s_pct' % cal_col].groupby(
                    all_result_df['order_time']).sum().reset_index()
                all_people_count.columns = ['order_time', 'count']
                all_result_df = all_result_df.set_index('order_time')
                all_people_count = all_people_count.set_index('order_time')
                result_all_f = all_result_df.join(all_people_count).reset_index()
                result_all_f['ratio'] = result_all_f['%s_pct' % cal_col] / result_all_f['count']
        else:
            result_all_f = pd.DataFrame()
        logging.info('计算完毕，分箱函数为 %s，计算方式by %s' % (str(cal_func), method))
        return result_all_f

    @classmethod
    def calculate_someday_pass_info(cls, cal_col, cal_data, cal_func=None, method='order'):
        """
        计算 某段时间通过人群 总体指标情况
        cal_col : 计算字段名称 字符串
        cal_data : 计算数据框
        cal_func ： binning func
        method ： order 按订单统计 和 people 按人统计
        return : result DataFrame

        """
        logging.info('开始计算某段时间通过人群%s 情况，分箱函数为 %s，计算方式by %s' % (cal_col, str(cal_func), method))
        if not cal_data.empty:

            _cal_data_s = cal_data[cal_data['lastreview_decision'] == 1]
            if method == 'order':
                _cal_data_f = _cal_data_s
            else:
                _cal_data_f = _cal_data_s.drop_duplicates('mobile')
            _cal_data = cls.cal_fill_func(_cal_data_f, cal_col)
            if cal_func is not None:
                _cal_col_new = '%s_bg' % cal_col
                _cal_data[_cal_col_new] = _cal_data[cal_col].apply(cal_func)
                all_result_df = _cal_data.groupby(_cal_col_new)['order_code'].count().reset_index()
                all_result_df.columns = [_cal_col_new, '%s_pct' % _cal_col_new]
                all_pct = all_result_df['%s_pct' % _cal_col_new].sum()
                # all_pct_list = [all_pct for i in range(all_result_df.shape[0])]
                all_pct_list = [all_pct] * all_result_df.shape[0]
                all_result_df['count'] = pd.Series(all_pct_list)
                all_result_df['ratio'] = all_result_df['%s_pct' % _cal_col_new] / all_result_df['count']
            else:
                all_result_df = _cal_data.groupby(cal_col)['order_code'].count().reset_index()
                all_result_df.columns = [cal_col, '%s_pct' % cal_col]
                all_pct = all_result_df['%s_pct' % cal_col].sum()
                # all_pct_list = [all_pct for i in range(all_result_df.shape[0])]
                all_pct_list = [all_pct] * all_result_df.shape[0]
                all_result_df['count'] = pd.Series(all_pct_list)
                all_result_df['ratio'] = all_result_df['%s_pct' % cal_col] / all_result_df['count']
        else:
            all_result_df = pd.DataFrame()
        logging.info('计算完毕，分箱函数为 %s，计算方式by %s' % (str(cal_func), method))
        return all_result_df

    @classmethod
    def calculate_pass_ep_info_config(cls, func):
        """
                计算 某段时间每天通过人群或某段时间总体通过人群 各个产品指标情况 （分为9 类）
                （年龄，性别，省份，芝麻分，小白分 .........)
                需要分箱的变量 请使用cal_func 参数
                需调整计算方式 by people by order 请使用method参数
                计算函数定义 为 闭包生成, 订单类型请使用market_type 参数 1 ---》9

                """
        def calculate_pass_ep_info(cal_col, cal_data, market_type, cal_func=None, method='order'):
            if not cal_data.empty:
                _cal_data_type = cal_data[cal_data['type_new'] == market_type]
                logging.info('order type ====> %s' % str(market_type))
                if method == 'order':
                    if cal_func is not None:
                        _result = func(cal_col, _cal_data_type, cal_func)
                    else:
                        _result = func(cal_col, _cal_data_type)
                else:
                    if cal_func is not None:
                        _result = func(cal_col, _cal_data_type, cal_func, method='people')
                    else:
                        _result = func(cal_col, _cal_data_type, method='people')
            else:
                _result = pd.DataFrame()
            return _result
        return calculate_pass_ep_info


if __name__ == '__main__':

    from check_func import *
    logging.info('System Begin ......')
    h = CalculateTags()
    # 1---> 9 9产品线
    c_a = ['sex', 'jobType', 'maxLevel', 'os', 'pay_method', 'province']
    c_b = ['zmScore', 'huabeiQuota', 'JdXiaobai', 'JdBaitiaoQuota', 'age', 'order_amount']
    for q in c_a:
        for w in range(9):

            k = h.calculate_edp_ep_info(q, h.data_pre_30, w+1)
            print k

    for q in c_a:
        for w in range(9):
            k = h.calculate_edp_ep_info(q, h.data_pre_30, w+1, method='people')
            print k

    k2 = h.calculate_edp_ep_info('zmScore', h.data_pre_30, 1, binning_zm_score)
    k3 = h.calculate_edp_ep_info('zmScore', h.data_pre_30, 1, binning_zm_score, method='people')
    k4 = h.calculate_sdp_ep_info('sex', h.data_pre_30, 1)
    k5 = h.calculate_sdp_ep_info('sex', h.data_pre_30, 1, method='people')
    k6 = h.calculate_sdp_ep_info('zmScore', h.data_pre_30, 1, binning_zm_score)
    k7 = h.calculate_sdp_ep_info('zmScore', h.data_pre_30, 1, binning_zm_score, method='people')
    k8 = h.calculate_someday_performance()
    k9 = h.calculate_everyday_performance()
    k10 = h.calculate_someday_performance('people')
    k11 = h.calculate_everyday_performance('people')

    k12 = h.calculate_someday_pass_info('sex', h.data_pre_30)
    k13 = h.calculate_someday_pass_info('sex', h.data_pre_30, method='people')
    k14 = h.calculate_someday_pass_info('zmScore', h.data_pre_30, binning_zm_score)
    k15 = h.calculate_someday_pass_info('age', h.data_pre_30, binning_age, 'people')

    k16 = h.calculate_everyday_pass_info('age', h.data_pre_30, binning_age, 'people')
    k17 = h.calculate_everyday_pass_info('age', h.data_pre_30, binning_age)
    k18 = h.calculate_everyday_pass_info('sex', h.data_pre_30)
    k19 = h.calculate_everyday_pass_info('sex', h.data_pre_30, method='people')
    logging.info('System End ......')
    for i in [k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15, k16, k17, k18, k19]:
        print i
