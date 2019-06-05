import logging

import requests

from server import env

logger = logging.getLogger('utils')


def mark_token_status(token, status=None):
    endpoint = server_url('/token')
    if status == 'created':
        return requests.post(url=endpoint,
                             data={'token': token,
                                   'status': 'created'})
    else:
        response = requests.get(url=f'{endpoint}/{token}')
        if not status:
            return response
        else:
            info = response.json()
            return requests.patch(url=f'{endpoint}/{info.get("_id")}',
                                  data={'status': status},
                                  headers={'If-Match': info.get('_etag')})


def server_url(endpoint):
    return env.SERVER_HOST + endpoint
