if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    cur_dir = os.path.split(os.getcwd())[0]
    if cur_dir not in sys.path:
        sys.path.append(cur_dir)

from datetime import datetime
import re
import pandas as pd

from db.mongo_connection import MyMongo
from scrape.common import get_soup_from_url, print_bulk_result

from pymongo import UpdateOne

url_total = 'http://watch.peoplepower21.org/RollBook'
soup = get_soup_from_url(url_total)
text = soup.get_text()
re_obj = re.search(r'전체\s(.+)\s건', text)
count_total_from_web = int(re_obj.group(1).replace(',', ''))

if not count_total_from_web:
    raise ValueError('count_total_from_web = 0')

with MyMongo() as db:
    print('Get row count from db.')
    confer = db.get_table_obj('assembly', 'watch_conference')
    count_total_from_db = confer.count()

# print(count_total_from_web, count_total_from_db)

# example: 255
# 1 ~ 13
count_new = count_total_from_web - count_total_from_db
count_num_of_records = 20
count_total_page = count_new // count_num_of_records + 1
count_total_page_with_spare = count_total_page + 1

queries = []
for page in range(count_total_page_with_spare, 0, -1):
    url_confer = 'http://watch.peoplepower21.org/index.php'
    params_committee = {
        'mid': 'RollBook',
        'page': page,
    }
    try:
        soup_com = get_soup_from_url(url_confer, params_committee)
    except ConnectionError:
        print(f'Connection Error: Page {page} Not Found.')
        continue
    content = soup_com.find('div', id='content')
    tbody = content.tbody
    trs = tbody.find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')
        confer = {
            'confer_date': tds[0].string,
            'committee_id': tds[1].string,
            'committeename': tds[1].string.replace(' ', ''),
            'committee_round': tds[2].string,
            'confer_id': tds[3].button['data-whatever'],
            'rollbook_fetched': False,
        }
        queries.append(UpdateOne({'confer_id': confer['confer_id']},
                                 {'$set': confer}, upsert=True))

with MyMongo() as db:
    print('Run upsert operation.')
    confer_table = db.get_table_obj('assembly', 'watch_conference')
    result = confer_table.bulk_write(queries)

print()
print(f'Rows from web: {count_total_from_web}')
print(f'Rows from db: {count_total_from_db}')
print(f'Rows to update: {count_new}')
print_bulk_result(result)
