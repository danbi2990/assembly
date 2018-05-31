if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    current_path = os.path.dirname(__file__)
    project_path = os.path.abspath(os.path.join(current_path, '..'))
    sys.path.append(project_path)

# from pprint import pprint
from datetime import datetime
from api.common import get_df_as_per_total
from db.mongo_connection import MyMongo

url = 'http://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemb\
erCurrStateList'
params = {
    'numOfRows': 10,
    'pageNo': 1,
}

new_mem = get_df_as_per_total(url, params)
time_stamp = datetime.now()
new_mem['update_on'] = time_stamp

with MyMongo() as db:
    prev_mem = db.get_df_from_table('assembly', 'member')
    db.archive_complement_and_dump_new(prev_mem, new_mem, 'num', 'assembly',
                                       'member', 'member_archive')
