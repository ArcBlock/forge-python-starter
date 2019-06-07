import logging

import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token
)
from forge_sdk import did as forge_did

from server import env
from server import utils
from server.endpoints import common

login = Blueprint('did-login', __name__)

logger = logging.getLogger('did-login')


def auth_get(token):
    utils.mark_token_status(token, 'scanned')
    params = {
        'url': utils.server_url(f'/api/did/login/auth?_t_={token}'),
        'action': 'responseAuth',
        'workflow': 'get-profile',
        'chain_host': env.CHAIN_HOST,
        'app_addr': env.APP_ADDR,
        'app_pk': env.APP_PK,
        'app_sk': env.APP_SK,
    }
    return forge_did.require_profile(**params)


def auth_post(token, request):
    # TODO: check signature
    wallet_res = forge_did.WalletResponse(request.get_json())

    did = wallet_res.get_did()

    res = requests.post(url=utils.server_url('/user'),
                  data={'did': did,
                        'name': wallet_res.requested_claim.get('fullName'),
                        'email': wallet_res.requested_claim.get('email')})

    session_token = create_access_token(identity=did)

    utils.mark_token_status(token, 'succeed', session_token)

    return jsonify(status=0)


@login.route('/auth', methods=['GET', 'POST'])
def auth():
    token = request.args.get('_t_')
    if request.method == 'GET':
        return auth_get(token)

    if request.method == 'POST':
        return auth_post(token, request)

@login.route('/token', methods=['GET'])
def get_token():
    return common.token("login")
#
# @login.route('/status', methods=['GET'])
# def get_status():
#     return common.status()
#
# @login.route('/timeout', methods=['GET'])
# def get_timeout():
#     return common.timeout()
