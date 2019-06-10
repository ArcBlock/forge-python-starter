from flask import jsonify
from forge_sdk import did as forge_did, rpc as forge_rpc, utils as forge_utils

from server import env
from server import utils
from server.endpoints.lib import auth_component


def get_handler(args):
    tx = forge_rpc.build_transfer_tx(to=env.APP_ADDR,
                                     value=2,
                                     address=args.user_did.lstrip(
                                         forge_did.PREFIX),
                                     pk=forge_utils.multibase_b58decode(
                                             args.user_pk))

    params = {
        'workflow': 'payment',
        'tx': tx,
        'description': 'Pay 2 TBA',
    }
    return forge_did.require_sig(**args.did_params, **params)


def post_handler(args):
    wallet_res = args.wallet_res
    tx = wallet_res.get_origin_tx()
    tx.signature = wallet_res.get_signature()

    res = forge_rpc.send_tx(tx)
    if res.hash:
        utils.mark_token_status(args.token, 'succeed')
        return jsonify(status=0, hash=res.hash,
                       tx=forge_utils.multibase_b58encode(
                               tx.SerializeToString()))
    else:
        utils.mark_token_status(args.token, 'error')
        return jsonify(error=f"Oops, error code: {res.code}")


payment = auth_component.create('payment',
                                get_handler,
                                post_handler)
