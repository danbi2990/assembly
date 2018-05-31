if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    current_path = os.path.dirname(__file__)
    project_path = os.path.abspath(os.path.join(current_path, '..'))
    sys.path.append(project_path)

from pprint import pprint
from datetime import datetime
import pandas as pd

from api.common import get_df_from_url, get_df_as_per_total, get_refined_dict_from_url
from db.mongo_connection import MyMongo

class_name = {
    '1': '국회본회의',
    '7': '전원위원회',
    '2': '상임위원회',
    '4': '예산결산특별위원회',
    '3': '특별위원회',
    '9': '인사청문회',
    '8': '소위원회',
    '5': '국정감사',
    '6': '국정조사',
    '10': '공청회',
    '11': '청문회',
    '12': '연석회의',
}

url_conf = 'http://apis.data.go.kr/9710000/ProceedingInfoService/getAllConInfo\
List'
params_conf = {
    'dae_num': 20,
    'numOfRows': 10,
    'pageNo': 1,
}
class_code = '2'
params_conf['class_code'] = class_code

new_conf = get_df_as_per_total(url_conf, params_conf)
# new_conf = get_df_from_url(url_conf, params_conf)
new_conf['class_code'] = class_code
new_conf['class_name'] = class_name[class_code]
# print(new_conf)

with MyMongo() as db:
    conf = db.get_table_obj('assembly', 'conference')
    conf.delete_many({})
    print('Old Data Revmoed.')
    conf.insert_many(new_conf.to_dict(orient='records'))
    print('New Data Saved.')

'''
회의종류코드
1.국회본회의 1
2.전원위원회 7
3.상임위원회 2
4.예산결산특별위원회 4
5.특별위원회 3
6.인사청문회 9
7.소위원회 8
8.국정감사 5
9.국정조사 6
10.공청회 10
11.청문회 11
12.연석회의 12
'''
