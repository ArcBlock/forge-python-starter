from forge_sdk import did as forge_did, rpc as forge_rpc, utils as forge_utils

from server import utils
from server.endpoints.lib import auth_component


def get_handler(**args):
    tx = forge_rpc.build_poke_tx(
            address=args.get('user_did').lstrip(forge_did.PREFIX),
            pk=forge_utils.multibase_b58decode(args.get('user_pk')))

    return {
        'request_type': 'signature',
        'workflow': 'poke',
        'tx': tx,
        'description': 'Get 25 TBA',
    }


def post_handler(**args):
    wallet_res = args.get('wallet_res')
    token = args.get('token')

    tx = wallet_res.get_origin_tx()
    tx.signature = wallet_res.get_signature()

    res = forge_rpc.send_tx(tx)
    if res.hash:
        utils.mark_token_status(token, 'succeed')
        return {'status': 0,
                'hash': res.hash,
                'tx': forge_utils.multibase_b58encode(
                        tx.SerializeToString())}
    else:
        utils.mark_token_status(token, 'error')
        return {'error': f"Oops, error code: {res.code}"}


checkin = auth_component.create('checkin',
                                get_handler=get_handler,
                                post_handler=post_handler)
