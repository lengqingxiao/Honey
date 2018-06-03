# -*- coding:utf-8 -*-
"""
标签计算（特征计算） 调度

"""
from config.log_config import *
# from data_transfer.data_query import *
from honeybee_info import *
import numba


@numba.jit
def calculate_honeybee_tags(num):

    r_data = QueryData.query_data_from_mongodb_func('47.96.38.60', 3717, 'analysis', 'MobileVerifyDataCol',
                                                    ['report_data', 'mobile'], 'mobile', num)
    logging.info('数据[%s]拉取完成，开始计算' % num)
    data_shape = len(r_data)
    print (data_shape)
    if data_shape == 0:
        print '数据为空'
    elif data_shape == 1:
        cal_data_r = pd.DataFrame(r_data[0])
        c = CalculateTagsForHoneybee(cal_data_r)
        _data = c.honeybee_info_result
        print (_data)
        logging.info('蜜蜂报告特征计算完毕')
        return _data
    else:
        r_s = []
        for d in r_data:
            cal_data_r = pd.DataFrame(d)
            c = CalculateTagsForHoneybee(cal_data_r)
            data = c.honeybee_info_result
            print (data)
            logging.info('蜜蜂报告特征计算完毕')
            r_s.append(data)
        _data = pd.concat(r_s)
        print _data
        return _data


logging.info('System Begin')
result = []
for i in ['15625867469', '18168724419', '18677827374', '15831842620', '18382035538', '18329468073', '18734594770',
          '18536575736', '18909678383', '18789575931']:
    r = calculate_honeybee_tags(i)
    result.append(r)

logging.info('System End')
result_df_n = pd.concat(result)
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
# result_df_n.to_csv('D:/honeybee_info_tags_result_demo.csv')
print result_df_n
