from eve import Eve
from forge_sdk import utils as forge_utils, did as forge_did
import secrets
from flask import request
import requests
import json
import logging
import os
import base64
from dotenv import load_dotenv


logger = logging.getLogger('app')

app = Eve()
load_dotenv()

SERVER_HOST = os.getenv('SERVER_HOST')
APP_PK = base64.b16decode(os.getenv('APP_PK'))
APP_SK = base64.b16decode(os.getenv('APP_SK'))
APP_ADDR = os.getenv('APP_ADDR')


def server_url(endpoint):
    return SERVER_HOST + endpoint

# routes for login


@app.route('/api/session')
def session():
    return "{}"

# NO.1 generate action token


@app.route('/api/did/login/token', methods=['GET'])
def token():
    token = secrets.token_urlsafe(8)
    response = requests.post(url='http://localhost:5000/token/', data={'token': token,
                                                                       'status': 'created'})

    url = forge_utils.did_url(url=server_url('/api/did/login/auth'),
                              action='requestAuth',
                              app_pk=os.getenv('APP_PK'),
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
        return json.dumps({'token': data.get('token'), 'status': data.get('status')})
    else:
        return json.dumps({'error': 'error'})

# NO.4 and NO.5


@app.route('/api/did/login/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        token = request.args.get('_t_')
        params = {
            'url': server_url('/api/did/login/auth'),
            'action': 'ResponseAuth',
            'workflow': 'get-profile',
            'APP_ADDR': APP_ADDR,
            'APP_PK': APP_PK,
            'APP_SK': APP_SK,
        }
        res = requests.get(url=server_url(f'/token/{_t_}'))
        requests.patch(url=server_url(
            f"/token/{res.json().get('_id')}"), data={'status': 'scanned'})

        return forge_did.require_profile(**params)

        # NO.6 mark the token as expired


@app.route('/api/did/login/timeout')
def timeout():
    token = request.args.get('_t_')
    response = requests.delete(
        url=f'http://localhost:5000/token', data={"token": token})
    if response.status_code == 204:
        return json.dumps({"message": f"token {token} deleted."})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
