if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    current_path = os.path.dirname(__file__)
    project_path = os.path.abspath(os.path.join(current_path, '..'))
    sys.path.append(project_path)

import pandas as pd
from db.mongo_connection import MyMongo

asset = pd.read_csv('asset.tsv', sep='\t')
asset.loc[asset['name']=='황희', 'pos'] = '국회의원'
asset.loc[(asset['num']==-1)&(asset['name']=='박준영'), 'num'] = -2
asset['netInc'] = asset['incAmt'] - asset['decAmt']
asset['incRate'] = asset['netInc'] / abs(asset['prvPrice']) * 100; asset
asset['num'] = asset['num'].astype(str)

with MyMongo() as db:
    tbl = db.get_table_obj('assembly', 'asset')
    tbl.delete_many({})
    tbl.insert_many(asset.to_dict(orient='records'))
    print('Asset saved.')
