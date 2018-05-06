# -*- coding:utf-8 -*-
########################################################################################################################
# 数据迁移----数据库查询( Mongodb Mysql)
########################################################################################################################
# from pandas import * as pd
import pandas as pd
from data_connect import ConnectMongodb, ConnectMysql


class QueryData(object):

    def __init__(self):

        pass

    @staticmethod
    def query_data_from_mongodb(db_path, port, db_name, table_name, check_list, unique_id_col, unique_id_value):
        """
        mongodb conditional query
        return : result DataFrame

        """
        _client = ConnectMongodb.mongodb_connection(db_path, port)
        _db = _client['%s' % db_name]
        # _db.authenticate("analysisUser", "AnalysisUser123")
        _raw_data = _db[table_name]
        list_values = []
        h = 1
        for i in range(len(check_list)):
            list_values.append(h)
        _query_dict = dict(zip(check_list, list_values))
        # query_dict = dict(map(lambda x, y: [x, y], check_list, list_values))  # python 3
        try:
            _query_data = _raw_data.find({unique_id_col: unique_id_value}, _query_dict)
            query_result = list(_query_data)[0]
            _client.close()
            query_raw_data = pd.DataFrame(query_result)
            # print query_raw_data
        except KeyError:
            print '查询用户%s数据失败' % unique_id_col
            query_raw_data = pd.DataFrame()

        return query_raw_data

    @staticmethod
    def query_data_from_mysql(db_path, port, db_name, user_name, pass_wd, table_name,
                              check_list, unique_id_col, unique_id_value):
        """
        mysql conditional query
        return : result DataFrame
        catch all exceptions

        """
        _query_col = ",".join(check_list)
        try:
            _con = ConnectMysql.mysql_connection(db_path, port, user_name, pass_wd, db_name)
            _query_sql = "select %s from %s where %s = %s" % (_query_col, table_name, unique_id_col, unique_id_value)
            data_from_mysql = pd.read_sql(_query_sql, con=_con)
            _con.close()
        except Exception, ex:
            print Exception, ":", ex
            data_from_mysql = pd.DataFrame()

        return data_from_mysql

    @staticmethod
    def query_data_from_mysql_mc(db_path, port, db_name, user_name, pass_wd, query_sql):
        """
        mysql conditional query    (query by SQL)
        return : result DataFrame
        catch all exceptions
        usage: pass

        """
        # _query_col = ",".join(check_list)
        try:
            _con = ConnectMysql.mysql_connection(db_path, port, user_name, pass_wd, db_name)
            _query_sql = query_sql
            _data_from_mysql = pd.read_sql(_query_sql, con=_con)
            _con.close()
        except Exception, ex:
            print Exception, ":", ex
            _data_from_mysql = pd.DataFrame()

        return _data_from_mysql

    @staticmethod
    def query_data_from_mysql_mq(db_path, port, db_name, user_name, pass_wd, table_name, check_list, unique_id_col,
                                 value_list):
        """
        mysql conditional query    use in (multi conditional subquery)
        return : result DataFrame
        catch all exceptions
        usage: pass

        """
        _query_col = ",".join(check_list)
        value_tuple = str(tuple(value_list))
        try:
            _con = ConnectMysql.mysql_connection(db_path, port, user_name, pass_wd, db_name)
            _query_sql = "select %s from %s where %s in %s" % (_query_col, table_name, unique_id_col, value_tuple)
            data_from_mysql = pd.read_sql(_query_sql, con=_con)
            _con.close()
        except Exception, ex:
            print Exception, ":", ex
            data_from_mysql = pd.DataFrame()

        return data_from_mysql
