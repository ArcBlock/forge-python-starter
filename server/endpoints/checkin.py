from flask import Blueprint, jsonify, request
from forge_sdk import did as forge_did, rpc as forge_rpc, utils as forge_utils

from server import env
from server import utils
from server.endpoints import common
import logging

logger = logging.getLogger('did-checkin')

checkin = Blueprint('did-checkin', __name__)


def auth_get(token, user_did, user_pk):
    utils.mark_token_status(token, 'scanned')
    tx = forge_rpc.build_poke_tx(address=user_did.lstrip(forge_did.PREFIX),
                                 pk=forge_utils.multibase_b58decode(user_pk))
    params = {
        'url': utils.server_url(f'/api/did/checkin/auth?_t_={token}'),
        'action': 'responseAuth',
        'workflow': 'poke',
        'chain_host': env.CHAIN_HOST,
        'app_addr': env.APP_ADDR,
        'app_pk': env.APP_PK,
        'app_sk': env.APP_SK,
        'tx': tx,
        'user_did': user_did,
        'description': 'Get 25 TBA',
    }
    return forge_did.require_sig(**params)


def auth_post(token, request):
    wallet_res = forge_did.WalletResponse(request.get_json())

    tx = wallet_res.get_origin_tx()
    tx.signature = wallet_res.get_signature()

    res = forge_rpc.send_tx(tx)
    if res.hash:
        logger.info(f'checkin hash: {res.hash}')
        utils.mark_token_status(token, 'succeed')
        return jsonify(status=0, hash=res.hash,
                       tx=forge_utils.multibase_b58encode(tx.SerializeToString()))
    else:
        logger.error(f'checkin : {res.code}')
        utils.mark_token_status(token, 'error')
        return jsonify(error=f"Oops, error code: {res.code}")


@checkin.route('/auth', methods=['GET', 'POST'])
def auth():
    token = request.args.get('_t_')
    user_did = request.args.get('userDid')
    user_pk = request.args.get('userPk')
    if request.method == 'GET':
        return auth_get(token, user_did, user_pk)

    if request.method == 'POST':
        return auth_post(token, request)


@checkin.route('/token', methods=['GET'])
def get_token():
    return common.token("checkin")
