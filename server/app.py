import logging

from eve import Eve
import requests
from flask_jwt_extended import(
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask import jsonify, make_response
from server import utils


logger = logging.getLogger('app')

app = Eve()
jwt = JWTManager(app)


def register_blueprints(application):
    from server import endpoints
    application.register_blueprint(endpoints.login, url_prefix='/api/did/login')
    application.register_blueprint(endpoints.checkin, url_prefix='/api/did/checkin')

@app.route("/api/session",methods=['GET', 'POST'])
@jwt_required
def session():
    did = get_jwt_identity()
    res = requests.get(url=utils.server_url(f'/user/{did}'))
    if res.status_code == 200:
        data=res.json()
        return jsonify(user={
            'email':data.get('email'),
            'mobile': data.get('mobile',''),
            'did':data.get('did'),
            'name': data.get('name'),
        })
    else:
        return '{}'


if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0')
