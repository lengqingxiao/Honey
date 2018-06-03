# -*- coding: utf-8 -*-
"""
此模块为nlp 命名实体识别/词性标注/词法分析模块
base model : JieBa, HanLp ,StanfordNLP ......

"""
# from pyhanlp import *
import jieba


class ProvinceRecognize(object):

    """
     此类用于京东地址信息中地址名称识别

    """

    def __init__(self):
        pass

    # @staticmethod
    # def province_recognize_func(rec_str):
    #     """
    #      感知机分析 用于省份，地区分词提取
    #      Usage: analyzer.analyze(data_test) ; type(data_test) : str
    #
    #     """
    #     nlp_pla = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')
    #     analyzer = nlp_pla()
    #     nlp_result = analyzer.analyze(rec_str)
    #     return nlp_result

    @staticmethod
    def get_address_province(rec_str):
        """
         结巴分词提取， 用于省份，地区分词提取
         Usage:  type(data_test) : str ; return : province_name_str

        """
        return jieba.cut(rec_str).next()
