# -*- coding: utf-8 -*-
########################################################################################################################
# 数据迁移----数据库连接
########################################################################################################################

import pymongo
import pymysql


class ConnectMongodb(object):

    def __init__(self):
        pass

    @staticmethod
    def mongodb_connection(db_path, port):

        client = pymongo.MongoClient(db_path, port)
        return client


class ConnectMysql(object):

    def __init__(self):
        pass

    @staticmethod
    def mysql_connection(db_path, port, user_name, pass_wd, db_name):
        """
        demo：  k = ConnectMysql.mysql_connection('127.0.0.1', 3306, 'root', '12345678', 'sys')
                sql = "select age, name from risk_data"
                d = pd.read_sql(sql, con=k)
                k.close()
        """
        con = pymysql.Connect(host=db_path, port=port, user=user_name, passwd=pass_wd, db=db_name, charset='utf8')
        return con
