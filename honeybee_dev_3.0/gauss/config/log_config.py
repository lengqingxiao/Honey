# -*- coding:utf-8 -*-
########################################################################################################################
# 日志配置
########################################################################################################################
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='D:\\ele_data\sys_e.log',
                    filemode='a+')