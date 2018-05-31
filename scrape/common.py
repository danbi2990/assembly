import urllib.parse

from bs4 import BeautifulSoup as bs
import requests


def print_bulk_result(result):
    print('- bulk_write result:')
    print('match, insert, modify, upsert')
    print(f'{result.matched_count} {result.inserted_count} {result.modified_count} {result.upserted_count}')


def post_soup_from_url(url, data, encoding='utf-8'):
    response = requests.post(url, data)
    if response.status_code != 200:
        raise ConnectionError(f'Status Code: {response.status_code}')
    response.encoding = encoding
    html = response.text
    soup = bs(html, 'html.parser')
    return soup


def add_params_to_base_url(url, params):
    query_params = urllib.parse.urlencode(params)
    return f'{url}?{query_params}'


def get_soup_from_url(url, params={}):
    if params:
        url = add_params_to_base_url(url, params)
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f'Status Code: {response.status_code}')
    html = response.text
    soup = bs(html, 'html.parser')
    return soup
