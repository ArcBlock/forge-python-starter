import logging

import requests
from flask import jsonify
from flask_jwt_extended import (
    create_access_token
)
from forge_sdk import did as forge_did

from server import utils
from server.endpoints.lib import auth_component

logger = logging.getLogger('did-login')


def get_handler(args):
    params = {
        'workflow': 'get-profile'
    }
    return forge_did.require_profile(**args.did_params, **params)


def post_handler(args):
    wallet_res = args.wallet_res
    did = wallet_res.get_did()
    res = requests.post(url=utils.server_url('/user'),
                        data={'did': did,
                              'name': wallet_res.requested_claim.get(
                                      'fullName'),
                              'email': wallet_res.requested_claim.get(
                                      'email')})

    session_token = create_access_token(identity=did)

    utils.mark_token_status(args.token, 'succeed', session_token)

    return jsonify(status=0)


login = auth_component.create('login',
                              get_handler,
                              post_handler)
