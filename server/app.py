import logging

from eve import Eve

logger = logging.getLogger('app')

app = Eve()


def register_blueprints(application):
    from server.endpoints import login
    application.register_blueprint(login, url_prefix='/api/did/login')


@app.route("/api/session",methods=['GET', 'POST'])
def session():
    return '{}'


if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0')
