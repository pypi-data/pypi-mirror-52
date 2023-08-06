import requests

from .exceptions.unsuccessful_response_exception import UnsuccessfulResponseException


def get(url, params=None):

    response = requests.get(url, params=params)

    if response.status_code != requests.codes.ok:
        raise UnsuccessfulResponseException(response.status_code)

    return response
