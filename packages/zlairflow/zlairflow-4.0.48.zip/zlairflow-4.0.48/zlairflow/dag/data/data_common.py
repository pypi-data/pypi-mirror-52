from collections import defaultdict
from pprint import pprint

from zlsrc.data import quyu_dict

para_dict={

 'fujian_nanan_ggzy':'minutes=360',
 'guangdong_guangdongsheng_1_zfcg':'minutes=480',
 'guangdong_zhanjiang_zfcg':'minutes=300',
 'zhejiang_hangzhou_gcjs':'minutes=480',
 'hebei_hebeisheng_ggzy':'minutes=480',
 'hebei_hebeisheng_zfcg':'minutes=420',
 'qycg_b2b_10086_cn':'minutes=480',
 'chongqing_chongqingshi_ggzy':'minutes=480',

}



"""
DB_A=['anhui','beijing','chongqing','fujian','gansu','guangdong','guangxi','guizhou','hainan','hebei','heilongjiang']
DB_B=['henan','hubei','hunan','jiangsu','jiangxi','jilin','liaoning']
DB_C=['neimenggu','ningxia','qinghai','shandong','shanghai','shanxi','shanxi1','sichuan','tianjin','xinjiang','xizang','yunnan','zhejiang']
DB_D=['zlcommon']
"""

def get_para(db_type):
    para=[]
    for sheng in db_type:
        quyu_list=quyu_dict.get(sheng)
        for quyu in quyu_list:
            timeout=para_dict.get(quyu)
            if timeout:
                quyu_cfg=[quyu,timeout]
            else:
                quyu_cfg=[quyu,"minutes=240"]
            para.append(quyu_cfg)

    return para



