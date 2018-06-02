# -*- coding:utf-8 -*-
########################################################################################################################
# 用于结果保存到mysql的辅助函数
########################################################################################################################
from data_transfer.data_connect import ConnectMysql
from config.log_config import *


class SaveTagsToMysql(object):

    def __init__(self):
        pass

    @staticmethod
    def save_result_mysql(path, port, user_name, pass_wd, db_name, table_name, result_df):

        try:
            connection = ConnectMysql.mysql_connection(path, port, user_name, pass_wd, db_name)
            result_df.to_sql(table_name, connection, flavor='mysql', if_exists='append', index=False)
            print '结果写入Mysql成功'
            logging.info('结果写入mysql成功')
        except Exception, ex:
            logging.info(str(Exception) + ':' + str(ex))
            print '写入出错，请检查权限，连接等问题'
