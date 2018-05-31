if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    current_path = os.path.dirname(__file__)
    project_path = os.path.abspath(os.path.join(current_path, '..'))
    sys.path.append(project_path)

import pandas as pd
from db.mongo_connection import MyMongo

donation = pd.read_csv('donation.tsv', sep='\t')
donation['num'] = donation['num'].fillna(-1).astype(int).astype(str)
donation['후원금 모금액'] = donation['후원금 모금액'].str.replace(',', '').astype(int)
no_dup = donation.loc[(donation['국회의원명']!='김성태')&(donation['국회의원명']!='최경환'), ['연번', '시도명', '국회의원명', '소속정당', '선거구명', '후원금 모금액']]
dup = donation.loc[(donation['국회의원명']=='김성태')|(donation['국회의원명']=='최경환')]
# print(dup)

with MyMongo() as db:
    mem = db.get_df_from_table('assembly', 'member')
    # print(mem)
    no_dup = no_dup.merge(mem[['empNm', 'num']], left_on='국회의원명', right_on='empNm', how='left')
    no_dup = no_dup[['연번', '시도명', '국회의원명', '소속정당', '선거구명', '후원금 모금액', 'num']]
    # print(no_dup)
    no_dup = no_dup.append(dup)
    tbl = db.get_table_obj('assembly', 'donation')
    tbl.delete_many({})
    tbl.insert_many(no_dup.to_dict(orient='records'))
    print('Donation saved.')
