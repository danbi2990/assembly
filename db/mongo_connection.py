import socket
from pymongo import MongoClient
import pandas as pd


class MyMongo:
    def __init__(self):
        con_str = self.get_connection_string()
        self.client = MongoClient(con_str)
        print('<--Mongo Connected.')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.close()
        print('Mongo Connection Closed.-->')

    def get_table_obj(self, schema, table):
        return getattr(getattr(self.client, schema), table)

    def archive_and_dump(self, prev, new, on, schema, main_table,
                         archive_table):
        if new.empty:
            raise ValueError('New Data Not Found.')

        main = self.get_table_obj(schema, main_table)
        if not prev.empty:
            intersection = pd.merge(prev, new, how='left', on=on)
            complement = prev[intersection.isnull().any(axis=1)]
            # union = pd.merge(prev, new, how='outer', on='num')
            if not complement.empty:
                arch = self.get_table_obj(schema, archive_table)
                arch.insert_many(complement.to_dict(orient='records'))
                print(f'Complement Data Archived in \'{archive_table}\'.')

            main.delete_many({})
            print(f'Old Data Removed from \'{main_table}\'.')

        main.insert_many(new.to_dict(orient='records'))
        print(f'New Data Dumped to \'{main_table}\'.')

    def get_df_from_table(self, schema, table, args={}):
        tb_obj = self.get_table_obj(schema, table)
        return pd.DataFrame(list(tb_obj.find(args)))

    def get_connection_string(self):
        hname = socket.gethostname()
        con_str = ''
        if hname == 'ideapad':
            file_path = '/home/jake/Private/local_mongo_connection.txt'
        elif hname == 'danbi-mac.local':
            file_path = '/Users/jake/Private/mongo_connection_to_ideapad.txt'

        with open(file_path) as f:
            con_str = f.read()
        return con_str
