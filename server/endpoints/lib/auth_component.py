from flask import Blueprint
from flask import request
from forge_sdk import did as forge_did

from server import env
from server import utils
from server.endpoints.auth import common


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
            }
            return get_handler(AuthHandlerArgs(token=token,
                                                    user_did=user_did,
                                                    user_pk=user_pk,
                                                    did_params=params))

        if request.method == 'POST':
            wallet_res = forge_did.WalletResponse(request.get_json())
            return post_handler(AuthHandlerArgs(token=token,
                                                     wallet_res=wallet_res))

    @bp.route('/token', methods=['GET'])
    def get_token():
        return common.token(operation)

    @bp.route('/status', methods=['GET'])
    def get_status():
        return common.status()

    @bp.route('/timeout', methods=['GET'])
    def timeout():
        return common.timeout()

    return bp


class AuthHandlerArgs:
    def __init__(self, **kwargs):
        self.token = kwargs.get('token')
        self.user_did = kwargs.get('user_did')
        self.user_pk = kwargs.get('user_pk')
        self.wallet_res = kwargs.get('wallet_res')
        self.did_params = kwargs.get('did_params')
