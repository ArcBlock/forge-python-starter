import secrets

from flask import Blueprint
from flask import jsonify, request
from forge_sdk import did as forge_did
from forge_sdk import utils as forge_utils

from server import env
from server import utils
from server.app import forge


def create(operation,
           get_handler,
           post_handler):
    bp = Blueprint(f'auth-component-{operation}', __name__,
                   url_prefix=f'/api/did/{operation}')

    @bp.route('/auth', methods=['GET', 'POST'])
    def auth():
        token = request.args.get('_t_')

        if request.method == 'GET':
            user_did = request.args.get('userDid')
            user_pk = request.args.get('userPk')
            utils.mark_token_status(token, 'scanned')
            params = {
                'url': utils.server_url(
                        f'/api/did/{operation}/auth?_t_={token}'),
                'action': 'responseAuth',
                'chain_host': env.CHAIN_HOST,
                'app_addr': env.APP_ADDR,
                'app_pk': env.APP_PK,
                'app_sk': env.APP_SK,
                'user_did': user_did,
                'chain_id': forge.config.chain_id,
                'chain_version': forge.rpc.get_chain_info().info.version,
                'token_symbol': forge.config.symbol,
                'decimals': forge.config.decimals,

            }
            user_params = get_handler(token=token,
                                      user_did=user_did,
                                      user_pk=user_pk,
                                      did_params=params)

            return utils.send_did_request(**params, **user_params)

        if request.method == 'POST':
            wallet_res = forge_did.WalletResponse(request.get_json())
            response_data = post_handler(token=token,
                                         wallet_res=wallet_res)
            return jsonify(response_data)

    @bp.route('/token', methods=['GET'])
    def token():
        return get_token(operation)

    @bp.route('/status', methods=['GET'])
    def status():
        return check_status()

    @bp.route('/timeout', methods=['GET'])
    def timeout():
        return token_timeout()

    return bp


def get_token(endpoint):
    token = secrets.token_hex(8)
    utils.mark_token_status(token, 'created')

    url = forge_utils.did_url(
            url=utils.server_url(f'/api/did/{endpoint}/auth?_t_={token}'),
            action='requestAuth',
            app_pk=forge_utils.multibase_b58encode(env.APP_PK),
            app_addr=env.APP_ADDR)

    return jsonify(token=token, url=url)


def check_status():
    token = utils.check_token_status(request.args.get('_t_'))
    if not token:
        return jsonify(error="Token does not exist.")
    elif token.session_token:
        return jsonify(token=token.token,
                       status=token.status,
                       sessionToken=token.session_token)
    else:
        return jsonify(token=token.token,
                       status=token.status)


def token_timeout():
    token = request.args.get('_t_')
    utils.mark_token_status(token, 'expired')
    return jsonify(msg="Token has been marked as expired.")
