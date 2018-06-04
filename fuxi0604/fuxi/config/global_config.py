# -*- coding:utf-8 -*-
########################################################################################################################
# 全局配置清单
########################################################################################################################

"""
 全局清单配置

"""

"""
国内省份列表

"""
# 省份元组
PROVINCE_LIST = (u'山东', u'江苏', u'上海', u'浙江', u'安徽', u'福建', u'江西', u'广东', u'广西', u'海南', u'河南',
                 u'湖南', u'湖北', u'北京', u'天津', u'河北', u'山西', u'内蒙古', u'宁夏', u'青海', u'陕西', u'甘肃',
                 u'新疆', u'四川', u'贵州', u'云南', u'重庆', u'西藏', u'辽宁', u'吉林', u'黑龙江', u'香港', u'澳门',
                 u'台湾', u'全国', u'运营商')
"""
中国省份区域划分
1 ====> 华东地区（包括山东、江苏、上海、浙江、安徽、福建、江西）HD
2 ====> 华南地区（包括广东、广西、海南）HN
3 ====> 华中地区（包括河南、湖南、湖北）HZ
4 ====> 华北地区（包括北京、天津、河北、山西、内蒙古）HB
5 ====> 西北地区（包括宁夏、青海、陕西、甘肃、新疆）XB
6 ====> 西南地区（包括四川、贵州、云南、重庆、西藏）XN
7 ====> 东北地区（包括辽宁、吉林、黑龙江）DB
8 ====> 港澳台地区（包括香港、澳门、台湾）GAT

"""
PROVINCE_MAP_DICT = {u'山东': 1, u'江苏': 1, u'上海': 1, u'浙江': 1, u'安徽': 1, u'福建': 1, u'江西': 1,
                     u'广东': 2, u'广西': 2, u'海南': 2,
                     u'河南': 3, u'湖南': 3, u'湖北': 3,
                     u'北京': 4, u'天津': 4, u'河北': 4, u'山西': 4, u'内蒙古': 4,
                     u'宁夏': 5, u'青海': 5, u'陕西': 5, u'甘肃': 5, u'新疆': 5,
                     u'四川': 6, u'贵州': 6, u'云南': 6, u'重庆': 6, u'西藏': 6,
                     u'辽宁': 7, u'吉林': 7, u'黑龙江': 7,
                     u'香港': 8, u'澳门': 8, u'台湾': 8,
                     u'全国': 9, u'运营商': 9, u'未知': 9}

# 经济较发达省份 edp
ECONOMICALLY_DEVELOPED_PROVINCES = [u'广东', u'江苏', u'山东', u'浙江', u'四川', u'北京', u'上海']
# 老赖top 10 省份 dpt
DEADBEAT_PROVINCES_TOP10 = [u'江苏', u'山东', u'浙江', u'河南', u'广东', u'安徽', u'福建', u'重庆', u'黑龙江', u'四川']

"""
发达国家列表 世界公认18个发达国家  ddc

"""
DEVELOPED_COUNTRY = [u'美国', u'加拿大', u'日本', u'英国', u'法国', u'德国', u'意大利', u'荷兰', u'比利时', u'卢森堡',
                     u'瑞士', u'奥地利', u'挪威', u'瑞典', u'丹麦', u'芬兰', u'澳大利亚', u'新西兰']

"""
信用卡逾期高发省份 cc_hrp

1 天津 2 江西 3 重庆 4 四川 5 黑龙江 6 福建

"""
CC_HIGH_RISK_PROVINCES = [u'天津', u'福建', u'江西', u'重庆', u'四川', u'黑龙江']

"""
用户行为检查特征结果列表 用于结果检查 behavior_check_result_list

"""

BEHAVIOR_CHECK_TUPLE = ('user_mobile_use_time', 'cpc_user_no_call_days', 'cpc_user_3days_no_call_cnt',
                        'cpc_user_max_silent_days', 'cpc_user_silent_days', 'cpc_user_high_risk_cnt',
                        'cpc_user_high_risk_cnt_ratio', 'user_if_contact_am', 'user_if_contact_110',
                        'user_if_contact_120', 'user_if_contact_lawyer', 'user_if_contact_court',
                        'user_call_night_fre', 'user_call_loan_fre', 'user_call_bank_fre', 'user_call_cc_fre',
                        'user_address_use_in_eb_fre', 'user_eb_use_fre', 'user_eb_self_use_fre', 'user_vg_buy_fre',
                        'user_lt_buy_fre', 'user_address_change_fre')
"""
通话信息字段表

"""
USER_CONTACT_COLUMNS = ('call_cnt', 'call_in_cnt', 'call_out_cnt', 'contact_1m', 'contact_1w', 'contact_3m',
                        'contact_3m_plus', 'contact_afternoon', 'contact_early_morning', 'contact_holiday',
                        'contact_morning', 'contact_night', 'contact_noon', 'contact_weekday', 'contact_weekend')

USER_CONTACT_RESULT = ('call', 'call_in', 'call_out', 'contact_p1m', 'contact_p1w', 'contact_p3m', 'contact_po3m',
                       'contact_afternoon', 'contact_early_morning', 'contact_holiday', 'contact_morning',
                       'contact_night', 'contact_noon', 'contact_weekday', 'contact_weekend')


CHINA_LOC = ('HD', 'HN', 'HZ', 'HB', 'XB', 'XN', 'DB', 'GAT')

CONTACT_REGION = (u'region_avg_call_in_time', u'region_avg_call_out_time', u'region_call_in_cnt',
                  u'region_call_in_cnt_pct', u'region_call_in_time', u'region_call_in_time_pct',
                  u'region_call_out_cnt', u'region_call_out_cnt_pct', u'region_call_out_time',
                  u'region_call_out_time_pct', u'region_uniq_num_cnt')

CELL_BEHAVIOR = (u'cpc_call_cnt_p6m', u'cpc_avg_call_cnt_p6m',
                 u'cpc_call_in_cnt_p6m', u'cpc_avg_call_in_cnt_p6m',
                 u'cpc_call_out_cnt_p6m', u'cpc_avg_call_out_cnt_p6m',
                 u'cpc_call_in_time_p6m', u'cpc_avg_call_in_time_p6m',
                 u'cpc_call_out_time_p6m', u'cpc_avg_call_out_time_p6m',
                 u'cpc_net_flow_p6m', u'cpc_avg_net_flow_p6m', u'cpc_sms_cnt_p6m',
                 u'cpc_avg_sms_cnt_p6m', u'cpc_call_cnt_p3m',
                 u'cpc_avg_call_cnt_p3m', u'cpc_call_in_cnt_p3m',
                 u'cpc_avg_call_in_cnt_p3m', u'cpc_call_out_cnt_p3m',
                 u'cpc_avg_call_out_cnt_p3m', u'cpc_call_in_time_p3m',
                 u'cpc_avg_call_in_time_p3m', u'cpc_call_out_time_p3m',
                 u'cpc_avg_call_out_time_p3m', u'cpc_net_flow_p3m',
                 u'cpc_avg_net_flow_p3m', u'cpc_sms_cnt_p3m', u'cpc_avg_sms_cnt_p3m',
                 u'cpc_call_cnt_p2m', u'cpc_avg_call_cnt_p2m', u'cpc_call_in_cnt_p2m',
                 u'cpc_avg_call_in_cnt_p2m', u'cpc_call_out_cnt_p2m',
                 u'cpc_avg_call_out_cnt_p2m', u'cpc_call_in_time_p2m',
                 u'cpc_avg_call_in_time_p2m', u'cpc_call_out_time_p2m',
                 u'cpc_avg_call_out_time_p2m', u'cpc_net_flow_p2m',
                 u'cpc_avg_net_flow_p2m', u'cpc_sms_cnt_p2m', u'cpc_avg_sms_cnt_p2m',
                 u'cpc_call_cnt_p1m', u'cpc_call_in_cnt_p1m', u'cpc_call_out_cnt_p1m',
                 u'cpc_call_in_time_p1m', u'cpc_call_out_time_p1m', u'cpc_net_flow_p1m',
                 u'cpc_sms_cnt_p1m')

TRIP_INFO_RESULT = (
                u'cpc_trip_long_tsp', u'cpc_trip_his_cnt',
                u'cpc_trip_his_total_days', u'cpc_trip_his_avg_days',
                u'cpc_trip_his_tll_cnt', u'cpc_trip_his_tdl_cnt',
                u'cpc_trip_his_fp_pct', u'cpc_trip_his_fp_total_cnt',
                u'cpc_trip_his_fp_total_cnt_ratio', u'cpc_trip_his_fet_tsp',
                u'cpc_trip_his_let_tsp', u'cpc_trip_holiday_total_pct',
                u'cpc_trip_holiday_total_pct_ratio', u'cpc_trip_holiday_days_cnt',
                u'cpc_trip_holiday_avg_days', u'cpc_trip_holiday_days_cnt_ratio',
                u'cpc_trip_weekend_total_pct', u'cpc_trip_weekend_total_pct_ratio',
                u'cpc_trip_weekend_days_cnt', u'cpc_trip_weekend_avg_days',
                u'cpc_trip_weekend_days_cnt_ratio', u'cpc_trip_workday_total_pct',
                u'cpc_trip_workday_total_pct_ratio', u'cpc_trip_workday_days_cnt',
                u'cpc_trip_workday_avg_days', u'cpc_trip_workday_days_cnt_ratio',
                u'cpc_trip_tll_esb_pct', u'cpc_trip_tll_esb_total_days',
                u'cpc_trip_tdl_esb_pct', u'cpc_trip_tdl_esb_total_days',
                u'cpc_trip_tll_esm_pct', u'cpc_trip_tll_esm_total_days',
                u'cpc_trip_tdl_esm_pct', u'cpc_trip_tdl_esm_total_days',
                u'cpc_trip_tll_esb_pct_ratio', u'cpc_trip_tll_esb_total_days_ratio',
                u'cpc_trip_tdl_esb_pct_ratio', u'cpc_trip_tdl_esb_total_days_ratio',
                u'cpc_trip_tll_esm_pct_ratio', u'cpc_trip_tll_esm_total_days_ratio',
                u'cpc_trip_tdl_esm_pct_ratio', u'cpc_trip_tdl_esm_total_days_ratio')

ORG_TYPE = (
    u'租车', u'招聘', u'房地产', u'电商', u'银行', u'运营商', u'支付', u'投资理财', u'贷款', u'汽车', u'个人',
    u'健身', u'互联网', u'投资担保', u'贷款/融资', u'保险', u'短号', u'基金', u'旅游出行', u'快递', u'APP软件',
    u'政府机构', u'婚庆'
)

ORG_RESULT = ('crt', 'rec', 'res', 'eb', 'bank', 'opt', 'pay', 'iaf', 'loan', 'car', 'ps',
              'gym', 'net', 'ig', 'lof', 'ins', 'sn', 'fund', 'trv', 'exp', 'app', 'gov', 'wed')

SERVICE_TIME_TAGS = ('p1m', 'p2m', 'p3m')

SR_0 = ['cpc_ser_%s_cnt' % i for i in ORG_RESULT]
SR_1 = ['cpc_ser_%s_org_cnt' % i for i in ORG_RESULT]
SR_2 = ['cpc_ser_%s_cnt_%s' % (k, v) for k in ORG_RESULT for v in SERVICE_TIME_TAGS]
SR_3 = ['cpc_ser_%s_org_cnt_%s' % (k, v) for k in ORG_RESULT for v in SERVICE_TIME_TAGS]
SR_4 = ['cpc_ser_%s_cnt_ratio_%s' % (k, v) for k in ORG_RESULT for v in SERVICE_TIME_TAGS]
SR_5 = ['cpc_ser_%s_cnt_ratio' % i for i in ORG_RESULT]
SR_6 = ['cpc_avg_ser_%s_cnt_p3m' % i for i in ORG_RESULT]
SR_B = ['cpc_total_ser_cnt_%s', 'cpc_total_ser_org_cnt_%s', 'cpc_total_ser_org_type_cnt_%s']
SR_7 = [k % v for k in SR_B for v in SERVICE_TIME_TAGS]
S = ('cpc_total_ser_cnt', 'cpc_total_ser_org_cnt', 'cpc_total_ser_org_type_cnt')
SERVICE_RESULT = S + tuple(SR_0) + tuple(SR_1) + tuple(SR_2) + tuple(SR_3) + tuple(SR_4) + tuple(SR_5) + tuple(SR_6) + \
                 tuple(SR_7)


# 18 type

"""
字段映射配置

"""

"""
奢饰品 (各类别奢饰品）
"""
USE_FOR_CHECK_LUXURY = (
    '香奈儿', 'CHANEL', '路易.威登', 'LV', '迪奥', 'Dior', '范思哲', 'Versace', '古琦欧.古琦',  'Gucci', '阿玛尼',
    'Armani', '瓦伦蒂诺', 'Valentino', '普拉达', 'prada', '巴宝莉', 'Burberry', '杰尼亚', 'Zeqna', '雅诗兰黛', '兰蔻',
    '倩碧', '迪奥', '香奈儿', 'Berj Al-Arab', '伯瓷', 'Fendi', '芬迪', 'Piaget','伯爵', 'Patek Philippe','百达翡丽',
    'Riva' ,'丽娃', 'Azimut','阿兹慕', 'Bvlgari','宝格丽', 'MontBlance','万宝龙', '杜嘉班纳', 'Boucheron','宝诗龙',
    'GiorgioArmani', '阿玛尼', 'ElizabethArden', '雅顿', 'Loewe', '罗意威', 'LANCOME', '兰蔻', 'Dunhill', '登喜路',
    '路易威登', '爱马仕', 'Hermes', '茅台', '五粮液', '古驰', '劳力士', 'Rolex', '卡地亚', 'Cartier', '轩尼诗',
    'Hennessy', '蒂芙尼', 'Tiffany', '酩悦', 'MOET&CHANDON', '华伦天奴', 'Valentino', '波士', 'Hugoboss', '纪梵希',
    'Givenchy', '百加得', 'Bacardi', '梵克雅宝', 'VanCleef', '伊夫圣罗兰', '绝对伏特加', 'Absolut', '尊尼获加',
    'JohnnieWailer'


)


"""
家电清单
"""
USE_FOR_CHECK_HOUSEHOLD = (
    u'平板电视', u'空调', u'冰箱', u'洗衣机', u'家庭影院', u'DVD', u'迷你音响', u'冷柜/冰吧', u'冰柜', u'冰吧',
    u'酒柜', u'家电配件', u'油烟机', u'燃气灶', u'烟灶套装', u'消毒柜', u'洗碗机', u'电热水器', u'燃气热水器',
    u'嵌入式厨电', u'电饭煲', u'微波炉', u'电烤箱', u'电磁炉', u'电压力锅', u'豆浆机', u'咖啡机', u'面包机',
    u'榨汁机', u'料理机', u'电饼铛', u'养生壶/煎药壶', u'养生壶', u'煎药壶', u'酸奶机', u'煮蛋器', u'电水壶/热水瓶',
    u'电水壶', u'热水瓶', u'电炖锅', u'多用途锅', u'电烧烤炉', u'电热饭盒', u'其它厨房电器', u'电风扇', u'冷风扇',
    u'净化器', u'扫地机器人', u'吸尘器', u'加湿器', u'挂烫机/熨斗', u'挂烫机', u'熨斗', u'取暖电器', u'插座', u'电话机',
    u'净水器', u'饮水机', u'除湿机', u'干衣机', u'清洁机', u'收录/音机', u'收音机', u'录音机', u'其它生活电器',
    u'生活电器配件', u'剃须刀', u'剃/脱毛器', u'口腔护理', u'电吹风', u'美容器', u'理发器', u'卷/直发器', u'卷发器',
    u'直发器', u'按摩椅', u'按摩器', u'足浴盆', u'血压计', u'健康秤/厨房秤', u'健康秤', u'厨房秤',
    u'血糖仪', u'体温计', u'计步器/脂肪检测仪', u'计步器', u'脂肪检测仪', u'其它健康电器', u'电动工具',
    u'手动工具', u'仪器仪表', u'浴霸/排气扇', u'浴霸', u'排气扇',  u'灯具', u'LED灯', u'洁身器', u'水槽', u'龙头',
    u'淋浴花洒', u'厨卫五金', u'家具五金', u'门铃', u'电气开关', u'插座', u'电工电料', u'监控安防', u'电线/线缆',
    u'电线', u'线缆', u'剃毛器', u'脱毛器', u'大家电', u'厨卫大电', u'厨房小电', u'生活电器', u'个护健康', u'五金家装',
    u'京东商城'

)


"""
京东商城

"""
USE_FOR_CHECK_JD_SHOP = u'京东超市'
USE_FOR_CHECK_JD_SEND = [u'京东配送']


"""
手机数码清单 先过滤充值 再判断

"""
USE_FOR_CHECK_MOBILE_DIGITAL = (
    u'手机', u'对讲机', u'以旧换新', u'手机维修', u'选号中心', u'自助服务', u'合约机', u'办套餐', u'选号码', u'装宽带',
    u'中国移动', u'中国联通', u'中国电信', u'电池/移动电源', u'电池', u'移动电源', u'蓝牙耳机', u'充电器/数据线',
    u'充电器', u'数据线', u'手机耳机', u'手机支架', u'贴膜', u'存储卡', u'保护套', u'车载配件', u'iPhone配件',
    u'创意配件', u'便携/无线音箱', u'便携音箱', u'无线音箱', u'手机饰品', u'拍照配件', u'数码相机', u'单电/微单相机',
    u'单电', u'微单', u'相机', u'单反相机', u'拍立得', u'运动相机', u'摄像机', u'镜头', u'户外器材', u'影棚器材',
    u'冲印服务', u'数码相框', u'存储卡', u'读卡器', u'支架', u'滤镜', u'闪光灯/手柄', u'闪光灯', u'手柄', u'相机包',
    u'三脚架/云台', u'三脚架', u'云台', u'相机清洁/贴膜', u'相机清洁', u'贴膜', u'机身附件', u'镜头附件',
    u'电池/充电器', u'移动电源', u'耳机/耳麦', u'耳机', u'耳麦', u'音箱/音响', u'音箱', u'音响', u'收音机', u'麦克风',
    u'MP3/MP4', u'MP3', u'MP4', u'专业音频', u'苹果周边', u'智能手环', u'智能手表', u'智能眼镜', u'智能机器人',
    u'运动跟踪器', u'健康监测', u'智能配饰', u'智能家居', u'体感车', u'无人机', u'其他配件', u'学生平板', u'点读机/笔',
    u'点读机', u'点读笔', u'早教益智', u'录音笔', u'电纸书', u'电子词典', u'复读机', u'手机通讯', u'京东通信',
    u'运营商', u'手机配件', u'摄影摄像', u'数码配件', u'影音娱乐', u'智能设备', u'电子教育'

)


"""
电脑办公类 清单

"""

USE_FOR_CHECK_COMPUTER_OFFICE = (
    u'笔记本', u'超极本', u'游戏本', u'平板电脑', u'平板电脑配件', u'台式机', u'一体机', u'服务器/工作站', u'服务器',
    u'工作站', u'笔记本配件', u'CPU', u'主板', u'显卡', u'硬盘', u'SSD固态硬盘', u'内存', u'机箱', u'电源', u'显示器',
    u'刻录机/光驱', u'刻录机', u'光驱', u'声卡/扩展卡', u'声卡', u'扩展卡', u'散热器', u'装机配件', u'组装电脑',
    u'鼠标', u'键盘', u'网络仪表仪器', u'U盘', u'移动硬盘', u'鼠标垫', u'线缆', u'电玩', u'手写板', u'外置盒',
    u'电脑工具', u'电脑清洁', u'UPS', u'插座', u'游戏机', u'游戏耳机', u'手柄/方向盘', u'手柄', u'方向盘', u'游戏软件',
    u'游戏周边', u'路由器', u'网卡', u'交换机', u'网络存储', u'4G/3G上网', u'4G上网', u'3G上网', u'网络盒子',
    u'网络配件', u'投影机', u'投影配件', u'多功能一体机', u'打印机', u'传真设备', u'验钞/点钞机', u'点钞机', u'验钞机',
    u'扫描设备', u'扫描', u'复合机', u'碎纸机', u'考勤机', u'收款/POS机', u'收款机', u'POS机',  u'会议音频视频',
    u'保险柜', u'装订/封装机', u'装订机', u'封装机', u'装订', u'封装', u'安防监控', u'办公家具', u'白板', u'硒鼓/墨粉',
    u'硒鼓', u'墨粉', u'墨盒', u'色带', u'纸类', u'办公文具', u'学生文具', u'文件管理', u'本册/便签', u'本册', u'便签',
    u'计算器', u'笔类', u'画具画材', u'财会用品', u'刻录碟片/附件', u'刻录碟片', u'碟片', u'附件', u'延保服务',
    u'维修保养', u'电脑软件', u'软件', u'电脑整机', u'外设产品', u'电脑配件', u'游戏设备', u'网络产品', u'办公设备',
    u'文具耗材'

)


"""
家居 home furnishing
"""

USE_FOR_CHECK_HOME_FURNISHING = (
    u'厨具', u'家装建材', u'家纺', u'家具', u'灯具', u'生活日用', u'家装软饰', u'烹饪锅具', u'刀剪菜板', u'厨房配件',
    u'水具酒具', u'餐具', u'茶具/咖啡具', u'茶具', u'咖啡具', u'灯饰照明', u'厨房卫浴', u'五金工具', u'电工电料',
    u'墙地面材料', u'装饰材料', u'装修服务', u'吸顶灯', u'淋浴花洒', u'开关插座', u'油漆涂料', u'龙头', u'床品套件',
    u'被子', u'枕芯', u'蚊帐', u'凉席', u'毛巾浴巾', u'床单被罩', u'床垫/床褥', u'毯子', u'毛巾', u'浴巾', u'被罩',
    u'床单', u'床垫', u'床褥', u'抱枕靠垫', u'靠垫', u'抱枕', u'窗帘/窗纱', u'窗帘', u'窗纱', u'电热毯',
    u'布艺软饰', u'布艺', u'软饰', u'卧室家具', u'家具', u'客厅家具', u'餐厅家具', u'书房家具', u'储物家具',
    u'阳台/户外', u'阳台', u'户外', u'商业办公', u'床', u'床垫', u'沙发', u'电脑椅', u'衣柜', u'茶几', u'电视柜',
    u'餐桌', u'电脑桌', u'鞋架/衣帽架', u'鞋架', u'衣帽架', u'台灯', u'吸顶灯', u'筒灯射灯', u'筒灯', u'射灯', u'灯',
    u'LED灯', u'节能灯', u'落地灯', u'五金电器', u'五金', u'led灯', u'应急灯/手电', u'应急灯', u'手电', u'装饰灯',
    u'吊灯', u'氛围照明', u'照明', u'收纳用品', u'收纳', u'雨伞雨具', u'雨具', u'雨伞', u'净化除味', u'净化', u'除味',
    u'浴室用品', u'洗晒/熨烫', u'熨烫', u'洗晒', u'缝纫/针织用品', u'针织用品', u'缝纫', u'清洁工具', u'清洁',
    u'桌布/罩件', u'桌布', u'罩件', u'地毯地垫', u'地垫', u'地毯', u'沙发垫套/椅垫', u'沙发垫套', u'椅垫', u'装饰字画',
    u'字画', u'装饰', u'装饰摆件', u'摆件', u'手工/十字绣', u'手工', u'十字绣', u'相框/照片墙', u'相框', u'照片墙',
    u'墙贴/装饰贴', u'墙贴', u'装饰贴', u'花瓶花艺', u'花瓶', u'花艺', u'香薰蜡烛', u'香薰', u'蜡烛', u'节庆饰品',
    u'节庆', u'饰品', u'钟饰', u'帘艺隔断', u'帘艺', u'隔断', u'创意家居', u'家居', u'保暖防护', u'保暖', u'防护',
    u'厨', u'家装', u'软饰', u'生活', u'烹饪锅具', u'烹饪', u'锅具', u'锅', u'刀剪菜板', u'刀', u'剪', u'菜板',
    u'厨房配件', u'厨房', u'水具', u'酒具', u'餐具', u'灯饰', u'照明', u'卫浴', u'电工', u'电料', u'五金', u'工具',
    u'吸顶灯', u'油漆', u'龙头', u'床品', u'装饰', u'涂料', u'装修', u'淋浴', u'花洒', u'开关', u'插座', u'座便器',
    u'座便', u'家居床品', u'安全防护', u'防盗', u'家居', u'床品', u'碗盘叉勺', u'碗', u'盘', u'叉', u'勺', u'水壶/水杯',
    u'水壶', u'水杯', u'壶', u'杯', u'椅', u'三轮车', u'自行车', u'电动车'

)

"""
箱包服饰类 

"""

USE_FOR_CHECK_SUITCASE_CLOTHING = (
    u'女装', u'男装', u'内衣', u'配饰', u'连衣裙', u'裙', u'裙子', u'T恤', u'雪纺衫', u'衬衫', u'休闲裤', u'裤',
    u'裤子', u'牛仔裤', u'针织衫', u'短外套', u'外套', u'卫衣', u'衣', u'小西装', u'西装', u'风衣', u'毛呢大衣',
    u'大衣', u'毛呢', u'半身裙', u'短裤', u'吊带/背心', u'吊带', u'背心', u'打底衫', u'打底', u'打底裤', u'正装裤',
    u'马甲', u'大码女装', u'大码', u'中老年女装', u'女装', u'真皮皮衣', u'皮衣', u'皮草', u'羊毛衫', u'羊绒衫',
    u'棉服', u'羽绒服', u'仿皮皮衣', u'加绒裤', u'婚纱', u'旗袍/唐装', u'旗袍', u'唐装', u'礼服', u'设计师/潮牌',
    u'设计师', u'潮牌', u'牛仔裤', u'卫衣', u'针织衫', u'西服', u'西裤', u'POLO衫', u'羽绒服', u'西服套装', u'真皮皮衣',
    u'夹克', u'风衣', u'卫裤/运动裤', u'卫裤', u'运动裤', u'短裤', u'仿皮皮衣', u'皮衣', u'棉服', u'马甲/背心', u'马甲',
    u'背心', u'毛呢大衣', u'羊毛衫', u'羊绒衫', u'大码男装', u'中老年男装', u'工装', u'唐装/中山装', u'唐装', u'中山装',
    u'加绒裤', u'文胸', u'睡衣/家居服', u'睡衣', u'家居服', u'男式内裤', u'内裤', u'女式内裤', u'塑身美体', u'塑身',
    u'美体', u'文胸套装', u'文胸', u'情侣睡衣', u'少女文胸', u'休闲棉袜', u'棉袜', u'袜', u'袜子', u'商务男袜',
    u'连裤袜/丝袜', u'连裤袜', u'丝袜', u'美腿袜', u'打底裤袜', u'抹胸', u'内衣配件', u'内衣', u'大码内衣', u'打底衫',
    u'泳衣', u'秋衣秋裤', u'秋衣', u'秋裤', u'保暖内衣', u'情趣内衣', u'内衣', u'太阳镜', u'光学镜架/镜片', u'光学镜架',
    u'镜片', u'镜架', u'男士腰带/礼盒', u'腰带', u'防辐射眼镜', u'眼镜', u'老花镜', u'花镜', u'女士丝巾/围巾/披肩',
    u'丝巾', u'围巾', u'披肩', u'男士丝巾/围巾', u'棒球帽', u'帽', u'帽子', u'遮阳帽', u'鸭舌帽', u'贝雷帽', u'礼帽',
    u'毛线帽', u'防晒手套', u'手套', u'真皮手套', u'围巾/手套/帽子套装', u'遮阳伞/雨伞', u'遮阳伞', u'伞',
    u'女士腰带/礼盒', u'口罩', u'假领', u'毛线/布面料', u'领带/领结/领带夹', u'领带', u'领结', u'领带夹', u'耳罩/耳包',
    u'耳罩', u'耳包', u'袖扣', u'钥匙扣', u'时尚女鞋', u'鞋', u'流行男鞋', u'潮流女包', u'精品男包', u'功能箱包',
    u'鞋靴', u'靴', u'单鞋', u'休闲鞋', u'帆布鞋', u'鱼嘴鞋', u'妈妈鞋', u'凉鞋', u'拖鞋/人字拖', u'布鞋/绣花鞋',
    u'坡跟鞋', u'松糕鞋', u'防水台', u'高跟鞋', u'踝靴', u'内增高', u'女靴', u'马丁靴', u'雪地靴', u'雨鞋/雨靴',
    u'鞋配件', u'休闲鞋', u'商务休闲鞋', u'正装鞋', u'帆布鞋', u'工装鞋', u'增高鞋', u'拖鞋/人字拖', u'凉鞋/沙滩鞋',
    u'雨鞋/雨靴', u'定制鞋', u'男靴', u'传统布鞋', u'功能鞋', u'鞋配件', u'单肩包', u'手提包', u'包', u'斜挎包',
    u'双肩包', u'钱包', u'手拿包/晚宴包', u'手拿包', u'晚宴包', u'卡包/零钱包', u'钥匙包', u'商务公文包',
    u'单肩/斜挎包', u'男士手包', u'双肩包', u'钱包/卡包', u'钥匙包', u'拉杆箱/拉杆包', u'旅行包', u'电脑包',
    u'休闲运动包', u'相机包', u'腰包/胸包', u'登山包', u'旅行配件', u'书包', u'妈咪包', u'时尚饰品', u'钻石', u'饰品',
    u'翡翠玉石', u'纯金K金饰品', u'银饰', u'水晶玛瑙', u'彩宝', u'铂金', u'天然木饰', u'珍珠', u'翡翠', u'玉石',
    u'水晶', u'玛瑙', u'木饰'

)

"""
个人洗护类 映射表

"""
USE_FOR_CHECK_PERSONAL_CARE = (
    u'面部护肤', u'护肤', u'洗发护发', u'洗发', u'护发', u'身体护肤', u'口腔护理', u'护理', u'女性护理', u'香水彩妆',
    u'香水', u'彩妆', u'清洁用品', u'清洁', u'面膜', u'剃须', u'染发', u'造型', u'假发', u'沐浴', u'润肤', u'颈部',
    u'手足', u'纤体塑形', u'纤体', u'塑形', u'美胸', u'牙膏/牙粉', u'牙膏', u'牙粉', u'牙刷/牙线', u'牙刷', u'牙线',
    u'漱口水', u'卫生巾', u'卫生护垫', u'私密护理', u'脱毛膏', u'香水', u'底妆', u'腮红', u'眼部', u'唇部', u'美甲',
    u'美容工具', u'美容', u'纸品湿巾', u'纸品', u'湿巾', u'纸', u'衣物清洁', u'清洁工具', u'家庭清洁', u'一次性用品',
    u'驱虫用品', u'驱虫', u'皮具护理', u'理发器', u'洗衣液/皂', u'洗衣液', u'洗衣皂', u'洗衣粉', u'洗衣', u'洗面',
    u'润肤', u'面膜', u'面部清洁', u'驱蚊防蚊', u'驱蚊', u'防蚊', u'灭蚊', u'蚊香'
)

"""
宠物类映射表

"""
USE_FOR_CHECK_PET_CONSUMPTION = (
    u'宠物生活', u'宠物', u'水族用品', u'水族', u'宠物主粮', u'宠物零食', u'猫砂/尿布', u'猫砂', u'宠物玩具',
    u'宠物牵引', u'宠物驱虫', u'犬主粮', u'龟虾蟹类及其用品', u'猫主粮', u'宠物服装/雨衣', u'狗零食', u'猫咪',
    u'鱼类及其用品', u'猫/狗日用品', u'猫/狗医疗用品', u'宠物医疗', u'猫粮', u'狗粮'

)

"""
运动户外类 映射表

"""
USE_FOR_CHECK_OUTDOOR_SPORTS = (
    u'运动鞋包', u'运动鞋', u'运动包', u'运动服饰', u'运动服', u'健身训练', u'骑行运动', u'体育用品', u'户外鞋服',
    u'户外装备', u'垂钓用品', u'游泳用品', u'钟表', u'跑步鞋', u'休闲鞋', u'篮球鞋', u'板鞋', u'运动包', u'足球鞋',
    u'帆布鞋', u'乒羽网鞋', u'训练鞋', u'专项运动鞋', u'拖鞋', u'运动套装', u'羽绒服', u'卫衣/套头衫', u'卫衣',
    u'套头衫', u'棉服', u'运动裤', u'夹克/风衣', u'夹克', u'风衣', u'运动配饰', u'运动背心', u'乒羽网服', u'训练服',
    u'毛衫/线衫', u'毛衫', u'线衫', u'T恤', u'跑步机', u'健身车/动感单车', u'健身车', u'动感单车', u'哑铃', u'踏步机',
    u'仰卧板/收腹机', u'甩脂机', u'运动护具', u'运动', u'瑜伽舞蹈', u'瑜伽', u'舞蹈', u'武术搏击', u'武术', u'搏击',
    u'综合训练器', u'其他大型器械', u'其他中小型器材', u'山地车/公路车', u'山地车', u'公路车', u'折叠车', u'电动车',
    u'平衡车', u'其他整车', u'骑行装备', u'骑行服', u'乒乓球', u'羽毛球', u'篮球', u'足球', u'轮滑滑板', u'轮滑',
    u'滑板', u'网球', u'高尔夫', u'台球', u'排球', u'棋牌麻将', u'棋牌', u'麻将', u'其它', u'冲锋衣裤', u'速干衣裤',
    u'滑雪服', u'羽绒服/棉服', u'羽绒服', u'棉服', u'休闲衣裤', u'抓绒衣裤', u'软壳衣裤', u'T恤', u'户外风衣',
    u'功能内衣', u'军迷服饰', u'登山鞋', u'徒步鞋', u'越野跑鞋', u'休闲鞋', u'工装鞋', u'溯溪鞋', u'沙滩/凉拖',
    u'凉拖', u'拖鞋', u'凉鞋', u'户外袜', u'背包', u'帐篷/垫子', u'帐篷', u'垫子', u'睡袋/吊床', u'睡袋', u'吊床',
    u'登山攀岩', u'登山', u'攀岩', u'户外照明', u'户外', u'野餐烧烤', u'野外', u'便携桌椅床', u'户外工具', u'户外',
    u'望远镜', u'户外仪表', u'旅游用品', u'军迷用品', u'救援装备', u'滑雪装备', u'极限户外', u'冲浪潜水', u'冲浪',
    u'潜水', u'户外配饰', u'鱼竿鱼线', u'鱼竿', u'鱼线', u'浮漂鱼饵', u'浮漂', u'鱼饵', u'钓鱼桌椅', u'钓鱼配件',
    u'钓箱鱼包', u'泳镜', u'泳帽', u'游泳包防水包', u'游泳包', u'防水包', u'男士泳衣', u'女士泳衣', u'比基尼',
    u'男表', u'女表', u'儿童表', u'智能手表', u'座钟挂钟', u'座钟', u'挂钟'

)
"""
汽车类
"""
USE_FOR_CHECK_CAR = (
    u'微型车', u'小型车', u'紧凑型车', u'中型车', u'中大型车', u'豪华车', u'MPV', u'mpv', u'SUV', u'suv', u'跑车',
    u'东风标致', u'东风风行', u'东风雪铁龙', u'天津一汽', u'陆风', u'北汽新能源', u'一汽奔腾', u'机油', u'防冻液',
    u'滤清器', u'火花塞', u'雨刷', u'车灯', u'减震器', u'轮胎', u'轮毂', u'刹车片/盘', u'刹车片', u'刹车盘', u'蓄电池',
    u'底盘装甲/护板', u'底盘装甲', u'底盘护板', u'底盘', u'汽修工具', u'汽车改装配件', u'正时皮带', u'汽车喇叭',
    u'行车记录仪', u'导航仪', u'车载电源', u'车用电器配件', u'车载电器配件', u'车载净化器', u'车用净化器', u'车载影音',
    u'车载冰箱', u'车用冰箱', u'安全预警仪', u'倒车雷达', u'车用蓝牙设备', u'车载蓝牙设备', u'倒车', u'车雷达',
    u'车蓝牙', u'智能驾驶', u'车载电台', u'车电台', u'车用电台', u'车用吸尘器', u'车吸尘器', u'车载吸尘器', u'智能车机',
    u'汽车音响', u'车载生活电器', u'车用生活电器', u'车生活电器', u'车蜡', u'镀晶镀膜', u'补漆笔', u'玻璃水',
    u'车用清洁剂', u'车清洁剂', u'洗车机', u'洗车水枪', u'洗车配件', u'毛巾掸子', u'脚垫', u'车脚垫', u'座垫', u'座套',
    u'后备箱垫', u'方向盘套', u'头枕腰靠', u'车用香水', u'车载空气净化', u'车用空气净化', u'车辆空气净化',
    u'车用功能小件', u'车载功能小件', u'车衣', u'车用挂件摆件', u'车载挂件摆件', u'车辆挂件摆件', u'车挂件摆件',
    u'车挂件', u'车摆件', u'车用挂件', u'车用摆件', u'车身装饰件', u'车装饰件', u'安全座椅', u'胎压监测', u'充气泵',
    u'防盗设备', u'车用防盗设备', u'车辆防盗设备', u'车用应急救援', u'车载应急救援', u'车辆应急救援', u'车用保温箱',
    u'车载保温箱', u'车辆保温箱', u'车保温箱', u'车储物箱', u'车用储物箱', u'车载储物箱', u'车辆储物箱', u'自驾野营',
    u'摩托车装备', u'摩托车', u'车清洗美容', u'车辆清洗美容', u'车功能升级', u'车辆功能升级', u'车辆保养维修',
    u'车保养维修', u'驾驶培训', u'ETC', u'加油卡', u'etc', u'车', u'车维修保养', u'车维修', u'车保养', u'车辆维修保养',
    u'车辆维修', u'车辆保养', u'车载电器', u'车水枪', u'车美容清洗', u'车装饰', u'车美容', u'车清洗', u'车辆美容清洗',
    u'车辆美容', u'车辆清洗', u'车辆装饰'
)

"""
母婴类
"""
USE_FOR_CHECK_MOTHER_BABY = (
    u'安全座椅', u'婴儿', u'母婴', u'儿童', u'童', u'产妇', u'孕妇', u'宝宝', u'幼儿', u'婴幼儿', u'产妇', u'产后',
    u'奶粉', u'营养辅食', u'婴儿辅食', u'尿裤湿巾', u'尿裤', u'母婴洗护用品', u'婴儿洗护用品', u'纸尿裤',
    u'喂养用品', u'童车童床', u'童车', u'童床', u'童装童鞋', u'童装', u'童鞋', u'儿童玩具乐器', u'母婴', u'婴幼奶粉',
    u'婴儿奶粉', u'奶粉', u'DHA', u'dha', u'钙铁锌/维生素', u'益生菌/初乳', u'初乳', u'清火/开胃', u'米粉/菜粉',
    u'果泥/果汁', u'宝宝零食', u'婴儿尿裤', u'尿裤', u'拉拉裤', u'成人尿裤', u'宝宝护肤', u'宝宝洗浴',
    u'奶瓶清洗', u'奶瓶', u'母婴日常护理', u'儿童日常护理', u'奶瓶奶嘴', u'奶嘴', u'吸奶器', u'牙胶安抚', u'牙胶',
    u'暖奶消毒', u'暖奶', u'辅食料理机', u'婴儿床', u'婴儿推车', u'餐椅摇椅', u'餐椅', u'摇椅', u'学步车', u'扭扭车',
    u'滑板车',  u'提篮式', u'增高垫', u'婴儿外出服', u'婴儿内衣', u'婴儿礼盒', u'婴儿鞋帽袜', u'孕妇装',
    u'防辐射服', u'妈咪包/背婴带', u'妈咪包', u'背婴带', u'产后塑身', u'孕妈美容', u'月子装', u'待产/新生', u'待产',
    u'新生', u'孕期营养', u'孕期', u'亲子装', u'益智玩具', u'益智', u'玩具', u'积木拼插', u'积木', u'动漫玩具',
    u'动漫', u'毛绒布艺', u'模型玩具', u'健身玩具', u'娃娃玩具', u'DIY玩具', u'创意减压', u'乐器'

)

"""
食品类
"""
USE_FOR_CHECK_FOOD = (
    u'中外名酒', u'酒', u'进口食品', u'食品', u'休闲食品', u'地方特产', u'特产', u'茗茶', u'茶', u'饮料冲调', u'饮料',
    u'冲调', u'粮油调味', u'调味', u'粮油', u'生鲜食品', u'生鲜', u'食品礼券', u'礼券', u'白酒', u'葡萄酒', u'洋酒',
    u'啤酒', u'黄酒/养生酒', u'收藏酒/陈年老酒', u'牛奶', u'饼干蛋糕', u'饼干', u'蛋糕', u'糖果/巧克力', u'糖果',
    u'巧克力', u'糖', u'休闲零食', u'零食', u'冲调饮品', u'饮品', u'坚果炒货', u'坚果', u'炒货', u'肉干肉脯', u'肉干',
    u'肉脯', u'蜜饯果干', u'蜜饯', u'果干', u'无糖食品', u'无糖', u'铁观音', u'普洱', u'龙井', u'绿茶', u'红茶',
    u'乌龙茶', u'花草茶', u'花果茶', u'黑茶', u'白茶', u'养生茶', u'其他茶', u'牛奶乳品', u'乳品', u'饮料', u'饮用水',
    u'水', u'咖啡/奶茶', u'咖啡', u'奶茶', u'蜂蜜/柚子茶', u'蜂蜜', u'柚子茶', u'冲饮谷物', u'谷物', u'成人奶粉',
    u'奶粉', u'米面杂粮', u'米', u'面', u'粮', u'杂粮', u'食用油', u'调和油', u'调味品', u'南北干货', u'干货',
    u'方便食品', u'有机食品', u'水果蔬菜', u'水果', u'蔬菜', u'海鲜水产', u'海鲜', u'水产', u'海参', u'牛排',
    u'肉禽蛋奶', u'肉', u'禽', u'蛋', u'奶', u'鸡', u'鸭', u'鱼', u'牛', u'羊', u'猪', u'熟食腊味', u'熟食', u'腊味',
    u'环球美食', u'美食', u'产地直供', u'产地', u'大闸蟹', u'蟹', u'粽子', u'月饼', u'饼干', u'糕点', u'膨化', u'小食',
    u'蜜饯', u'枣类', u'梅', u'果脯', u'肉干', u'肉脯', u'豆干', u'肉类', u'山核桃', u'坚果', u'炒货', u'鱿鱼', u'鱼干',
    u'海味即食', u'糕点', u'点心', u'糖果', u'果冻', u'布丁', u'奶酪', u'乳品', u'蜂蜜', u'蜂产品', u'有机茶', u'蔬果',
    u'蔬', u'果', u'豆', u'母婴食品', u'有机', u'有机滋补品', u'小米', u'面粉', u'玉米', u'黄豆', u'红豆', u'黑豆',
    u'绿豆', u'橄榄油', u'花生油', u'菜籽油', u'山茶油', u'更多食用油', u'玉米油', u'方便面', u'面条/挂面', u'面条',
    u'挂面', u'汤圆', u'香/腊肠', u'腊肠', u'香肠', u'腊/腌肉', u'腌肉', u'腊肉', u'即食肠类', u'成人奶粉',
    u'速溶咖啡/咖啡豆/粉', u'咖啡豆', u'咖啡', u'咖啡粉', u'乳制品', u'麦片', u'柚子茶', u'冲饮品', u'饮料', u'新鲜',
    u'天然粉粉食品', u'芒果', u'石榴', u'奇异果', u'猕猴桃', u'枣', u'山药', u'番薯', u'土豆', u'腌制', u'泡菜',
    u'火腿', u'培根', u'猪肉', u'羊肉', u'牛肉', u'青蟹', u'三文鱼', u'鸡肉', u'鸭肉', u'鸡蛋', u'鸭蛋'


)
"""
营养保健类
"""
USE_FOR_CHECK_NUTRITION_HEALTH = (
    u'调节免疫', u'免疫', u'调节三高', u'三高', u'缓解疲劳', u'疲劳', u'美体塑身', u'塑身', u'美体', u'美容养颜',
    u'养颜', u'肝肾养护', u'护肝', u'护肾', u'肠胃养护', u'肠胃', u'养胃', u'明目益智', u'明目', u'益智', u'骨骼健康',
    u'健康', u'养生', u'改善睡眠', u'抗氧化', u'耐缺氧', u'维生素/矿物质', u'维生素', u'矿物质', u'蛋白质',
    u'鱼油/磷脂', u'鱼油', u'磷脂', u'褪黑素', u'叶黄素', u'姜黄素', u'螺旋藻', u'番茄红素', u'叶酸', u'葡萄籽',
    u'左旋肉碱', u'辅酶Q10', u'辅酶', u'益生菌', u'玛咖', u'膳食纤维', u'牛初乳', u'初乳', u'胶原蛋白', u'大豆异黄酮',
    u'芦荟提取', u'酵素', u'阿胶', u'蜂蜜/蜂产品', u'蜂蜜', u'蜂产品', u'枸杞', u'燕窝', u'海参', u'冬虫夏草',
    u'人参/西洋参', u'人参', u'西洋参', u'三七', u'鹿茸', u'雪蛤', u'青钱柳', u'石斛/枫斗', u'石斛', u'枫斗',
    u'灵芝/孢子粉', u'灵芝', u'孢子粉', u'当归', u'养生茶饮', u'保健', u'药食同源', u'安全避孕', u'避孕', u'验孕测孕',
    u'验孕', u'测孕', u'人体润滑', u'男用延时', u'延时', u'男用器具', u'女用器具', u'情趣内衣', u'血压计', u'血糖仪',
    u'血氧仪', u'体温计', u'体重秤', u'胎心仪', u'呼吸制氧', u'雾化器', u'助听器', u'轮椅', u'拐杖', u'中医保健',
    u'养生器械', u'理疗仪', u'家庭护理', u'智能健康', u'隐形眼镜', u'护理液', u'口罩', u'眼罩/耳塞', u'眼罩', u'耳塞',
    u'跌打损伤', u'跌打', u'损伤', u'暖贴', u'鼻喉护理', u'眼部保健', u'美体护理', u'阿胶膏方', u'阿胶', u'燕窝',
    u'冬虫夏草', u'药食同源食品', u'鹿茸', u'灵芝', u'参类滋补品', u'功能复合型膳食营养补充剂', u'蛋白质/氨基酸',
    u'氨基酸', u'植物精华/提取物', u'植物精华', u'海洋生物类'

)

"""
图书
"""
USE_FOR_CHECK_BOOK = (
    u'图书', u'音像', u'电子书', u'书籍', u'少儿', u'文学', u'出版社', u'文学经典', u'国学', u'案例', u'文艺',
    u'国学经典', u'散记', u'笔记', u'文白对照', u'白话版', u'历史书籍', u'精选本', u'精装本', u'教育', u'文艺',
    u'经管励志', u'经管', u'励志', u'人文社科', u'人文', u'社科', u'生活', u'科技', u'电子书', u'数字音乐', u'音乐',
    u'影视', u'教育音像', u'游戏', u'影视/动漫周边', u'0-2岁', u'3-6岁', u'7-10岁', u'11-14岁', u'儿童文学', u'绘本',
    u'科普', u'幼儿启蒙', u'启蒙', u'幼儿', u'手工游戏', u'智力开发', u'教材', u'中小学教辅', u'教辅', u'考试',
    u'外语学习', u'字典词典', u'字典', u'词典', u'小说', u'文学', u'青春文学', u'传记', u'动漫', u'艺术', u'摄影',
    u'管理', u'金融与投资', u'金融', u'投资', u'经济', u'励志与成功', u'励志', u'成功', u'历史', u'心理学', u'心理',
    u'政治/军事', u'政治', u'军事', u'国学/古籍', u'国学', u'古籍', u'哲学/宗教', u'哲学', u'宗教', u'社会科学',
    u'社会', u'科学', u'社科', u'法律', u'文化', u'家教与育儿', u'家教', u'育儿', u'孕产', u'旅游/地图', u'旅游',
    u'地图', u'美食', u'时尚美妆', u'时尚', u'美妆', u'两性', u'体育', u'计算机与互联网', u'计算机', u'互联网',
    u'科普', u'建筑', u'工业技术', u'工业', u'技术', u'电子/通信', u'电子', u'通信', u'医学', u'科学与自然', u'科学',
    u'自然', u'农林', u'杂志/期刊', u'杂志', u'期刊', u'英文原版书', u'港台图书', u'畅读VIP', u'小说', u'励志与成功',
    u'励志', u'成功', u'经济金融', u'经济', u'金融', u'文学', u'社科', u'婚恋两性', u'外文原版', u'外文', u'通俗流行',
    u'古典音乐', u'摇滚说唱', u'摇滚', u'说唱', u'爵士蓝调', u'蓝调', u'爵士', u'乡村民谣', u'民谣', u'有声读物'

)

"""
理财
"""
USE_FOR_CHECK_FIN = (
    u'理财', u'众筹', u'东家', u'钱包', u'保险', u'京东小金库', u'小金库', u'票据理财', u'基金理财', u'定期理财',
    u'固收理财', u'妈妈理财', u'众投理财', u'公益', u'其他权益众筹', u'私募股权', u'白条联名卡', u'京东钢镚',
    u'京东金采', u'金采', u'京东钱包', u'车险', u'健康险', u'意外险', u'旅行险', u'金银投资', u'投资'

)
"""
旅行
"""
USE_FOR_CHECK_TRAVEL = (
    u'票务', u'旅行', u'国内机票', u'机票', u'车票', u'国际机票', u'火车票', u'汽车票', u'旅游度假', u'景点门票',
    u'度假', u'景点', u'门票', u'机场服务', u'国内酒店', u'酒店', u'特惠酒店', u'旅游团购', u'旅游', u'旅行保险',
    u'全球签证', u'签证', u'国内租车', u'租车'
)

"""
彩票充值
"""
USE_FOR_CHECK_LOTTERY = (
    u'彩票', u'充值', u'缴费', u'话费', u'双色球', u'福彩3D', u'七乐彩', u'新时时彩', u'快3', u'大乐透', u'排列三',
    u'七星彩', u'新11选5', u'11选5', u'竞彩足球', u'竞彩篮球', u'北单', u'足彩', u'排列五', u'手机话费充值',
    u'手机流量充值', u'QQ充值', u'游戏点卡', u'点卡', u'网页游戏', u'游戏周边', u'手机游戏', u'单机游戏', u'游戏',
    u'外卖订座', u'订座', u'生活缴费', u'健康丽人', u'电影选座', u'选座', u'演唱会', u'音乐会', u'话剧歌剧', u'话剧',
    u'歌剧', u'体育赛事', u'语言/留学', u'留学'

)

#
"""
 Category amount check config

"""
HEA_AMT = [200, 500, 1000, 3000, 5000, 10000]
LAJ_AMT = [1000, 2000, 3000, 5000, 10000, 30000, 50000]
MDG_AMT = [2000, 3000, 5000, 8000]
COF_AMT = [5000, 8000, 10000, 15000]
HFS_AMT = []
SCT_AMT = []
PWH_AMT = []
PET_AMT = []
ODS_AMT = []
CAR_AMT = []
MAB_AMT = []
FOOD_AMT = []
NHC_AMT = []
BOOK_AMT = []
FIN_AMT = [2000, 5000, 10000, 20000]
TRV_AMT = []
LTR_AMT = []

CATEGORY_TAGS = [
    'hea', 'laj', 'mdg', 'cof', 'hfs', 'sct', 'pwh', 'pet', 'ods', 'car', 'mab', 'food', 'nhc', 'book', 'fin', 'trv',
    'ltr'
]

CATEGORY_AMOUNT_TAGS = [HEA_AMT, LAJ_AMT, MDG_AMT, COF_AMT, HFS_AMT, SCT_AMT, PWH_AMT, PET_AMT, ODS_AMT, CAR_AMT,
                        MAB_AMT, FOOD_AMT, NHC_AMT, BOOK_AMT, FIN_AMT, TRV_AMT, LTR_AMT]

CATEGORY_DICT = dict(zip(CATEGORY_TAGS, CATEGORY_AMOUNT_TAGS))
CATEGORY_CHECK_TAGS = [USE_FOR_CHECK_HOUSEHOLD, USE_FOR_CHECK_LUXURY, USE_FOR_CHECK_MOBILE_DIGITAL,
                       USE_FOR_CHECK_COMPUTER_OFFICE, USE_FOR_CHECK_HOME_FURNISHING, USE_FOR_CHECK_SUITCASE_CLOTHING,
                       USE_FOR_CHECK_PERSONAL_CARE, USE_FOR_CHECK_PET_CONSUMPTION, USE_FOR_CHECK_OUTDOOR_SPORTS,
                       USE_FOR_CHECK_CAR, USE_FOR_CHECK_MOTHER_BABY, USE_FOR_CHECK_FOOD, USE_FOR_CHECK_NUTRITION_HEALTH,
                       USE_FOR_CHECK_BOOK, USE_FOR_CHECK_FIN, USE_FOR_CHECK_TRAVEL, USE_FOR_CHECK_LOTTERY]
CATEGORY_RESHAPE_DICT = dict(zip(CATEGORY_TAGS, CATEGORY_CHECK_TAGS))
