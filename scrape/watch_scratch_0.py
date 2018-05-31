if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    cur_dir = os.path.split(os.getcwd())[0]
    if cur_dir not in sys.path:
        sys.path.append(cur_dir)

from scrape.common import get_soup_from_url

url_confer = 'http://watch.peoplepower21.org/index.php'
params_committee = {
    'mid': 'RollBook',
    'page': 65,
}

soup_com = get_soup_from_url(url_confer, params_committee)
content = soup_com.find('div', id='content')
tbody = content.tbody
trs = tbody.find_all('tr')

for tr in trs:
    tds = tr.find_all('td')
    confer_date = tds[0].string
    committee_id = tds[1].string
    committeename = committee_id.replace(' ', '')
    committee_round = tds[2].string
    confer_id = tds[3].button['data-whatever']
    # print(confer_date, committee_id, committeename, committee_round, confer_id)
