import logging

import requests
from eve import Eve
from flask import g, jsonify, make_response
from flask_jwt_extended import (JWTManager, get_jwt_identity, jwt_required)
from forge_sdk import did as forge_did, protos as forge_protos, \
    rpc as forge_rpc

from server import env
from server import utils

logging.basicConfig(level=logging.DEBUG)

app = Eve()
jwt = JWTManager(app)


def register_blueprints(application):
    from server import endpoints as ep
    application.register_blueprint(ep.login, url_prefix='/api/did/login')
    application.register_blueprint(ep.checkin, url_prefix='/api/did/checkin')
    application.register_blueprint(ep.payment, url_prefix='/api/did/payment')



@app.before_request
def before_request():
    g.logger = logging.getLogger('app')
    g.logger.setLevel(level=logging.DEBUG)


@app.route("/api/session", methods=['GET', 'POST'])
@jwt_required
def session():
    did = get_jwt_identity()
    res = requests.get(url=utils.server_url(f'/user/{did}'))
    if res.status_code == 200:
        data = res.json()
        return jsonify(user={
            'email': data.get('email'),
            'mobile': data.get('mobile', ''),
            'did': data.get('did'),
            'name': data.get('name'),
        })
    else:
        return '{}'


@app.route("/api/payments", methods=['GET'])
@jwt_required
def list_payments():
    did = get_jwt_identity()
    res = forge_rpc.list_transactions(
            address_filter=forge_protos.AddressFilter(
                    sender=did.lstrip(forge_did.PREFIX),
                    receiver=env.APP_ADDR),
            type_filter=forge_protos.TypeFilter(types=['transfer']))
    if len(res.transactions) > 0:
        tx = next(tx for tx in res.transactions if tx.code == 0)
        if tx and tx.hash:
            return jsonify(hash=tx.hash)
    return make_response()


if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0', debug=True)
