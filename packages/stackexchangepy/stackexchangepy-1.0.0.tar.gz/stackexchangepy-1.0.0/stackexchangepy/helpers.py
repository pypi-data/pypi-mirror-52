import arrow
import datetime as dt

from stackexchangepy.request import get, post
from stackexchangepy.model import create_class


def format_ids(ids):
    delim = ';'

    if ids.find(' ') != -1:
        delim = ' '
    elif ids.find(',') != -1:
        delim = ','
    elif ids.find('-') != -1:
        delim = '-'
    elif ids.find(';') != -1:
        delim = ';'

    ids = ';'.join(ids.split(delim))
    return ids

def convert_date(date):
  return arrow.get(date).timestamp

def format_date(params):
    if 'fromdate' in params:
        params['fromdate'] = convert_date(params['fromdate'])

    if 'todate' in params:
        todate['todate'] = convert_date(params['todate'])

    if 'min' in params and type(params['min']) is dt.datetime:
        params['min'] = convert_date(params['min'])

    if 'max' in params and type(params['max']) is dt.datetime:
        params['max'] = convert_date(params['max'])

    if 'since' in params:
        params['since'] = convert_date(params['since'])

def format_result(url, name, headers=None, params=None, site=None, method_type='get'):
    if not params:
        params = {}

    if site:
        params['site'] = site

    format_date(params)

    if method_type == 'get':
        response = get(url, headers=headers, params=params)
    else:
        response = post(url, headers=headers, data=params)

    to_json = response.json()

    if method_type == 'get':
        result = [create_class(name, item) for item in to_json['items']]
    else:
        result = create_class(name, to_json['items'])

    to_json.pop('items')
    remaining = create_class('StackExchangeRemaining', to_json)

    return (result, remaining)
