# -*- coding: utf-8 -*-
########################################################################################################################
# 用于csv文件读取和结果保存的辅助函数
########################################################################################################################
from config.log_config import *
import pandas as pd


class OperateData(object):

    def __init__(self):
        pass

    @staticmethod
    def save_result(data, output_file, output_file_p):

        try:
            logging.info("写入csv...")
            data.to_csv(output_file)
            print '计算结果保存csv成功'
            logging.info("计算结果写入csv成功...")
        except IOError:
            logging.info("写入csv文件出错...")
            print '写入csv文件出错'
        except UnicodeError:
            logging.info("写入csv出现编码错误...")
            print '写入csv出现编码错误'
        finally:
            logging.info("写入pickle...")
            data.to_pickle(output_file_p)
            print '计算结果写入pickle成功'
            logging.info("计算结果写入pickle成功...")

    @staticmethod
    def read_data_csv(input_file, size_number):

        logging.info("开始分块读取数据 ...")
        reader = pd.read_csv(input_file, iterator=True)
        chunks = []
        chunk_size = size_number
        loop = True
        while loop:
            try:
                chunk = reader.get_chunk(chunk_size)
                chunks.append(chunk)
                # print chunks
            except StopIteration:
                loop = False
                # print "Iteration is stopped."
        data = pd.concat(chunks, ignore_index=True)
        logging.info("分块读取数据完毕，合并数据完毕 ...")
        return data
