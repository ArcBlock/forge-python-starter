import logging

from eve import Eve
from flask import g, jsonify, make_response
from flask_jwt_extended import (JWTManager, get_jwt_identity, jwt_required)
from forge_sdk import did as forge_did, protos as forge_protos

from server import env

logging.basicConfig(level=logging.DEBUG)
from eve_sqlalchemy.validation import ValidatorSQL
from eve_sqlalchemy import SQL
from server.models import Base, init_db
from server.forge import forge


app = Eve(validator=ValidatorSQL, data=SQL)
jwt = JWTManager(app)
forge_rpc = forge.rpc
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base

def register_blueprints(application):
    from server import endpoints as ep
    application.register_blueprint(ep.login)
    application.register_blueprint(ep.checkin)
    application.register_blueprint(ep.payment)


@app.before_request
def before_request():
    g.logger = logging.getLogger('app')
    g.logger.setLevel(level=logging.DEBUG)


@app.route("/api/session", methods=['GET', 'POST'])
@jwt_required
def session():
    from server.models import DBUser
    did = get_jwt_identity()
    user = DBUser.query.filter_by(did=did).first()
    if user:
        return jsonify(user={
            'email': user.email,
            'mobile': user.mobile,
            'did': user.did,
            'name': user.name,
        })
    else:
        return '{}'


@app.route("/api/payments", methods=['GET'])
@jwt_required
def payments():
    did = get_jwt_identity()
    res = forge_rpc.list_transactions(
            address_filter=forge_protos.AddressFilter(
                    sender=did.lstrip(forge_did.PREFIX),
                    receiver=env.APP_ADDR),
            type_filter=forge_protos.TypeFilter(types=['transfer']))
    try:
        tx = next(tx for tx in res.transactions if tx.code == 0)
    except Exception:
        return make_response()
    return jsonify(hash=tx.hash)

sql_db = init_db(app)

if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0', debug=True, threaded=True, port=env.SERVER_PORT)
