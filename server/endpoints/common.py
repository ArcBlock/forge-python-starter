import json
import secrets

from flask import jsonify, request
from forge_sdk import utils as forge_utils

from server import env
from server import utils


def token():
    # TODO: change token name
    token = secrets.token_urlsafe(8)
    response = utils.mark_token_status(token, 'created')

    url = forge_utils.did_url(
            url=utils.server_url(f'/api/did/login/auth?_t_={token}'),
            action='requestAuth',
            app_pk=forge_utils.multibase_b58encode(env.APP_PK),
            app_addr=env.APP_ADDR)
    if response.status_code == 201:
        return jsonify(token=token, url=url)
    else:
        return jsonify(error="error in getting token")


def status():
    token = request.args.get('_t_')
    response = utils.mark_token_status(token)
    data = response.json()
    if response.status_code == 200:
        return jsonify(token=data.get('token'),
                       status=data.get('status'))
    else:
        return jsonify(error="error in getting status")


def timeout():
    token = request.args.get('_t_')
    utils.mark_token_status(token, 'expired')
    return json.dumps({'error': 'error'})
