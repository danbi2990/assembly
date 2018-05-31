if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    cur_dir = os.path.split(os.getcwd())[0]
    if cur_dir not in sys.path:
        sys.path.append(cur_dir)

import re
from pprint import pprint
from datetime import datetime

from pymongo import UpdateOne, DeleteMany, InsertOne

from db.mongo_connection import MyMongo
from scrape.common import post_soup_from_url, print_bulk_result


url_rollbook = 'http://watch.peoplepower21.org/opages/_comm_rollbook.php'

with MyMongo() as db:
    print('Fetch confer_id_list from mongo.')
    confer_df = db.get_df_from_table('assembly', 'watch_conference', {'rollbook_fetched': False})

confer_id_list = confer_df['confer_id'].tolist()


for confer_id in confer_id_list:
    query_on_watch_conference = []
    query_on_watch_rollbook = []

    query_on_watch_conference.append(UpdateOne({'confer_id': confer_id}, {'$set': {'rollbook_fetched': True}}))
    query_on_watch_rollbook.append(DeleteMany({'confer_id': confer_id}))
    data_rollbook = {'meeting_seq': confer_id}
    soup = post_soup_from_url(url_rollbook, data_rollbook)
    tables = soup.find_all('table', class_='table-striped')
    data = []

    for table in tables:
        re_obj = re.search(r'\n(\D+)\d+명', table.thead.get_text())
        try:
            attended = re_obj.group(1)
        except AttributeError:
            print(f'confer_id: {confer_id} has blank table.')
            continue
        trs = table.table.find_all('tr')

        for tr in trs:
            tds = tr.find_all('td')
            party = tds[0].string.split()[0]

            member_a = tds[1].find_all('a')
            for a in member_a:
                seq = re.search(r'member_seq=(\d+)', a['href']).group(1)
                empNm = a.string
                rollbook_dict = {
                    'confer_id': confer_id,
                    'attended': attended,
                    'party': party,
                    'seq': seq,
                    'empNm': empNm,
                }
                query_on_watch_rollbook.append(InsertOne(rollbook_dict))

    with MyMongo() as db:
        table_watch_conference = db.get_table_obj('assembly',
                                                  'watch_conference')
        result_watch_conference = table_watch_conference.bulk_write(query_on_watch_conference)
        table_watch_rollbook = db.get_table_obj('assembly', 'watch_rollbook')
        result_watch_rollbook = table_watch_rollbook.bulk_write(query_on_watch_rollbook)

        print_bulk_result(result_watch_conference)
        print_bulk_result(result_watch_rollbook)
