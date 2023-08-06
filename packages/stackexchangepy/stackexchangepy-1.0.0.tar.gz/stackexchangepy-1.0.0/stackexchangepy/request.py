import requests

from .exception import ExchangeException


def get(url, headers=None, params=None):
  response = requests.get(url, headers=headers, params=params)
  if response.status_code != requests.codes.ok:
    response = response.json()
    raise ExchangeException(response['error_message'], response['error_name'], response['error_id'])

  return response

def post(url, headers=None, data=None):
  response = requests.post(url, headers=headers, data=data)

  if response.status_code != requests.codes.ok:
    response = response.json()
    raise ExchangeException(response['error_message'], response['error_name'], response['error_id'])

  return response