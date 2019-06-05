import json
import json
import logging
import os
import secrets

import requests
from dotenv import load_dotenv
from eve import Eve
from flask import request
from forge_sdk import did as forge_did, utils as forge_utils

from server.config import APP_ADDR, APP_PK, APP_SK
logger = logging.getLogger('app')

app = Eve()
load_dotenv(dotenv_path="../.env")

SERVER_HOST = os.getenv('SERVER_HOST')
CHAIN_HOST = os.getenv('REACT_APP_CHAIN_HOST')
# APP_PK = base64.b16decode(os.getenv('REACT_APP_APP_PK'))
# APP_SK = base64.b16decode(os.getenv('REACT_APP_APP_SK'))
APP_ADDR = os.getenv('REACT_APP_APP_ID')


def server_url(endpoint):
    return SERVER_HOST + endpoint


# routes for login


@app.route('/api/session')
def session():
    return "{}"

# NO.1 generate action token


@app.route('/api/did/login/token', methods=['GET'])
def get_token():
    token = secrets.token_urlsafe(8)
    response = requests.post(url='http://localhost:5000/token/',
                             data={'token': token,
                                   'status': 'created'})

    url = forge_utils.did_url(
        url=server_url(f'/api/did/login/auth?_t_={token}'),
        action='requestAuth',
        app_pk=forge_utils.multibase_b58encode(APP_PK),
        app_addr=APP_ADDR)
    if response.status_code == 201:
        return json.dumps({'token': token, 'url': url})
    else:
        return json.dumps({'error': "wrong"})

# NO.3 check status of action token


@app.route('/api/did/login/status', methods=['GET'])
def get_status():
    token = request.args.get('_t_')
    response = requests.get(url=server_url(f'/token/{token}'))
    data = response.json()
    if response.status_code == 200:
        return json.dumps(
                {'token': data.get('token'), 'status': data.get('status')})
    else:
        return json.dumps({'error': 'error'})
# NO.4 and NO.5


@app.route('/api/did/login/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        token = request.args.get('_t_')
        endpoint = '/token/' + token
        get_res = requests.get(url=server_url(endpoint)).json()
        patch_res = requests.patch(url=server_url(
                f"/token/{get_res.get('_id')}"),
                data={'status': 'scanned'},
                headers={'If-Match': get_res.get('_etag')})
        params = {
            'url': server_url('/api/did/login/auth'),
            'action': 'responseAuth',
            'workflow': 'get-profile',
            'chain_host': CHAIN_HOST,
            'app_addr': APP_ADDR,
            'app_pk': APP_PK,
            'app_sk': APP_SK,
        }
        return forge_did.require_profile(**params)

        # NO.6 mark the token as expired
    if request.method =='POST':
        return json.dumps({'status':0})


@app.route('/api/did/login/timeout')
def timeout():
    token = request.args.get('_t_')
    response = requests.delete(
            url=f'http://localhost:5000/token', data={"token": token})
    if response.status_code == 204:
        return json.dumps({"message": f"token {token} deleted."})
    else:
        return json.dumps({'error': 'error'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
