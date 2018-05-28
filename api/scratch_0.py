if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    current_path = os.path.dirname(__file__)
    project_path = os.path.abspath(os.path.join(current_path, '..'))
    sys.path.append(project_path)


# from pprint import pprint
from datetime import datetime
import pandas as pd

from api.common import get_url, get_refined_dict_from_url, get_df_from_url
from db.mongo_connection import MyMongo
# from common import get_data_frame, KEY


db = MyMongo()
# tmp = list(db.assembly.member.find({}))
# df = pd.DataFrame(tmp)
# print(df.columns)

col = [
    'deptCd', 'empNm', 'engNm', 'hjNm', 'jpgLink', 'num', 'origNm',
    'reeleGbnNm', 'update_on'
]
val = [
    ['test', 'test', 't', 't', 't', 't', 't', 't', datetime.now()]
]

new = pd.DataFrame(columns=col, data=val)
db.assembly.member.insert_many(new.to_dict(orient='records'))
tmp = list(db.assembly.member.find({'deptCd': 'test'}))
print(tmp[0])

db.close_connection()
