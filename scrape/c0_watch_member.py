# if __name__ == "__main__" and __package__ is None:
#     import os
#     import sys
#     cur_dir = os.path.split(os.getcwd())[0]
#     if cur_dir not in sys.path:
#         sys.path.append(cur_dir)

import re
from pprint import pprint
from datetime import datetime
from collections import OrderedDict

import pandas as pd
from pymongo import UpdateOne, DeleteMany, InsertOne

from db.mongo_connection import MyMongo
from scrape.common import get_soup_from_url, print_bulk_result

# Get Total From Web
url_total = 'http://watch.peoplepower21.org/?act=&mid=AssemblyMembers&vid=&mode=search&name=&party=&region=&sangim=&gender=&age=&elect_num=&singlebutton='
soup = get_soup_from_url(url_total)
text = soup.get_text()
re_obj = re.search(r'총\s(\d+)명', text)
count_total_from_web = int(re_obj.group(1).replace(',', ''))
# print(count_total_from_web)

if not count_total_from_web:
    raise ValueError('count_total_from_web = 0')

# Get Total from db
with MyMongo() as db:
    print('Get row count from db.')
    member_table = db.get_df_from_table('assembly', 'watch_member')
    # count_total_from_db = member_table.count()

    try:
        seq_list_from_db = set(member_table['seq'].tolist())
        print(seq_list_from_db)
    except KeyError:
        print('No Member Found from assembly/watch_member')

# Get page count
count_num_of_records = 30
count_total_page = count_total_from_web // count_num_of_records + 1

url_seq_list = 'http://watch.peoplepower21.org/'
params_seq_list = {
    'mid': 'AssemblyMembers',
    'mode': 'search',
}

for i in range(count_total_page, 0, -1):
    params_seq_list['page'] = i
    soup_seq_list = get_soup_from_url(url_seq_list, params_seq_list)
    a_seq_list = soup_seq_list.find_all('a')
    seq_list = set(re.search(r'member_seq=(\d+)', a['href']).group(1) for a in a_seq_list if a['href'].find('member_seq') != -1)
    seq_list = seq_list - seq_list_from_db  # Remove existing seq
    if not seq_list:
        print(f'page {i}: No seq Found.')
        continue

    queries = []
    for seq in seq_list:
        url_member = f"http://watch.peoplepower21.org/"
        params_member = {
            'mid': 'Member',
            'member_seq': -1,
        }
        # 983: 김병관
        # seq = 983
        params_member['member_seq'] = seq
        soup = get_soup_from_url(url_member, params_member)
        body = soup.find("div", class_="panel-body")

        names = body.h1.get_text().strip().split(" ")
        name_kr = names[0].strip()
        name_hj = names[2].strip()
        table = body.find("table", class_="table-user-information")
        trs = table.find_all("tr")
        # print(trs)

        member_dict = {'seq': seq, 'empNm': name_kr, 'hjNm': name_hj}
        for tr in trs:
            tds = tr.find_all("td")
            key = tds[0].get_text().strip()
            value = tds[1].get_text().strip()

            if key == "정당":
                value = value.replace("● ", "")
            if key == "학력" or key == "주요경력":
                value = value.replace("\n", " | ")
            if key == "소속위원회":
                value = ' | '.join(list(filter(lambda x: x != '', value.split('위원회'))))

            member_dict[key] = value
            # print(key, value)

        queries.append(UpdateOne({'seq': seq}, {'$set': member_dict}, upsert=True))

    with MyMongo() as db:
        table_watch_member = db.get_table_obj('assembly', 'watch_member')
        result = table_watch_member.bulk_write(queries)
        print_bulk_result(result)
