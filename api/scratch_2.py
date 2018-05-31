if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    current_path = os.path.dirname(__file__)
    project_path = os.path.abspath(os.path.join(current_path, '..'))
    sys.path.append(project_path)

# from pprint import pprint
from datetime import datetime
import pandas as pd

from api.common import get_df_from_url, get_df_as_per_total
from db.mongo_connection import MyMongo

url_comm = 'http://apis.data.go.kr/9710000/BillInfoService/getCommitPeti\
tionList'
params_comm = {
    'numOfRows': 10,
    'pageNo': 1,
    'start_age_cd': 20,
    # 'gbn': 'C06',
}
new_comm = get_df_from_url(url_comm, params_comm)
time_stamp = datetime.now()
new_comm['update_on'] = time_stamp
print(new_comm)
# cur_comm_list = new_comm.loc[(new_comm['committeecode'].str[0:2] == '97'),
#                              ['committeecode', 'committeename']]
# new_comm_mem = pd.DataFrame()


'''
gbn code
1.처리의안 검색  gbn=C01
2.계류의안 검색 gbn =C02
3.본회의요청안건검색 gbn =C03
4.청원처리 검색 gbn =C04
5.청원계류 검색 gbn =C05
6.의안목록 검색 gbn=C06

bill_kind_cd
의안종류
1.헌법개정 B01
2.예산안 B02
3.결산 B03
4.법률안 B04
5.동의안 B05
6.승인안 B06
7.결의안 B07
8.건의안 B08
9.규칙안 B09
10.선출안 B10
11.중요동의 B11
12.의원징계 B12
13.의원자격심사 B13
14.윤리심사 B14
15.기타안 B15
16.기타 B16
'''
