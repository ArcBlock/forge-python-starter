import logging

import requests
from flask import jsonify
from flask_jwt_extended import (
    create_access_token
)
from forge_sdk import did as forge_did

from server import utils
from server.endpoints.lib import auth_component


def get_handler(**args):
    return {
        'request_type': 'profile',
        'workflow': 'get-profile'
    }


def post_handler(**args):
    wallet_res = args.get('wallet_res')
    did = wallet_res.get_did()
    res = requests.post(url=utils.server_url('/user'),
                        data={'did': did,
                              'name': wallet_res.requested_claim.get(
                                      'fullName'),
                              'email': wallet_res.requested_claim.get(
                                      'email')})

    session_token = create_access_token(identity=did)

    utils.mark_token_status(args.get('token'), 'succeed', session_token)

    return {'status': 0}


login = auth_component.create('login',
                              get_handler,
                              post_handler)
