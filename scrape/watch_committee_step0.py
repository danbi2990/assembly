from datetime import datetime
import pandas as pd

from db.mongo_connection import MyMongo
from scrape.common import get_soup_from_url

url_committee = 'http://watch.peoplepower21.org/Committee'
soup = get_soup_from_url(url_committee)
select = soup.find('select', id='sangim')
options = select.find_all('option')
df_body = [o['value'] for o in options if o['value']]
new_com = pd.DataFrame(columns=['committee_id'], data=df_body)
new_com['committeename'] = new_com['committee_id'].str.replace(' ', '') + '위원회'
new_com['update_on'] = datetime.now()
# print(new_com)

with MyMongo() as db:
    prev_com = db.get_df_from_table('assembly', 'watch_committee')
    db.archive_complement_and_dump_new(prev_com, new_com, 'committee_id',
                                       'assembly', 'watch_committee',
                                       'watch_committee_archive')
