# -*- coding:utf-8 -*-
########################################################################################################################
# 数据迁移----数据重塑
########################################################################################################################

import pandas as pd
import json


class TransformData(object):

    def __init__(self):
        pass

    @staticmethod
    def data_transform(data_raw, reshape_col):
        """
        data reshape
        raw data ===> Choose Reshape column ===> DataFrame

        """
        _check_list = list(data_raw[reshape_col])
        _reshape_df = pd.DataFrame()
        _col_name = list(_check_list[0].keys())
        _check_num = len(_col_name)
        for _check_list_member in _check_list:
            _check_df = pd.DataFrame()
            for _i in range(_check_num):
                _check_df[_col_name[_i]] = pd.Series(_check_list_member[_col_name[_i]])
            _reshape_df = _reshape_df.append(_check_df)
        # print _reshape_df
        return _reshape_df

    @staticmethod
    def data_reshape(data_raw, reshape_col):

        """
        data reshape
        raw data ===> Choose Reshape column ===> DataFrame

        """
        _reshape_df = pd.DataFrame()
        # _loop_count = data_raw[reshape_col].count()
        try:
            _loop_list = data_raw[reshape_col][0]
            # print type(_loop_list)
            if type(_loop_list) == dict:
                _col_dict = _loop_list
                _col_name = list(_col_dict.keys())
                _check_num = len(_col_name)
                _check_df = pd.DataFrame()
                for m in range(_check_num):
                    _check_df[_col_name[m]] = pd.Series(_loop_list[_col_name[m]])
                _reshape_df = _reshape_df.append(_check_df)
            else:
                _col_dict = data_raw[reshape_col][0][0]
                _col_name = list(_col_dict.keys())
                _check_num = len(_col_name)
                for _check_list_member in _loop_list:
                    _check_df = pd.DataFrame()
                    for m in range(_check_num):
                        _check_df[_col_name[m]] = pd.Series(_check_list_member[_col_name[m]])
                    _reshape_df = _reshape_df.append(_check_df)
        except KeyError:
            print '数据异常,当前用户%s 数据为空' % reshape_col
        finally:
            # print _reshape_df
            return _reshape_df

    @staticmethod
    def data_transform_from_dict(data_raw, reshape_col):

        """
        data transform (batch transform)
        Dict ===> Choose Reshape column ===> DataFrame(pandas DataFrame)

        """
        t_df = pd.DataFrame()
        try:
            _feat_list = []
            _feat_list.extend(data_raw.get(reshape_col, [{}]))
            _df = pd.DataFrame(_feat_list)
            t_df = _df
        except Exception, ex:
            print Exception, ":", ex
            # pass
        finally:
            return t_df

    @staticmethod
    def data_reshape_single_dict(single_dict):

        """
        data transform
        data ===> Json ===> Dict(single) ===> DataFrame

        """

        # data_processed = json.loads(raw_data)
        # single_dict = data_processed.get(data_name)
        _col_dict = single_dict
        _col_name = list(_col_dict.keys())
        _check_num = len(_col_name)
        _check_df = pd.DataFrame()
        for m in range(_check_num):
            _check_df[_col_name[m]] = pd.Series(_col_dict[_col_name[m]])
        return _check_df
