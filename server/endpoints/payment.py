from flask import Blueprint, jsonify, request
from forge_sdk import did as forge_did

from server import env
from server import utils

payment = Blueprint('did-payment', __name__)


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
    utils.mark_token_status(token, 'succeed')
    return jsonify(status=0)


@payment.route('/auth', methods=['GET', 'POST'])
def auth():
    token = request.args.get('_t_')
    if request.method == 'GET':
        return auth_get(token)

    if request.method == 'POST':
        return auth_post(token)
