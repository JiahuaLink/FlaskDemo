from flask import Flask, request, make_response, jsonify

from flask_cors import CORS
from app.user.user_views import user
from exts import db
from models.response import MyResponse
from models.stutus_code import StatusCode

app = Flask(__name__)
CORS(app, resource=r'/*')
CORS(app, supports_credentials=True)

app.register_blueprint(user)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.after_request
def after_request(resp):
    res = make_response(resp)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control'] = 'no-cache'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT'
    res.headers[
        'Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-Requested-With,Origin,Content-Length.User-Agent'
    res.headers['Content-Type'] = 'application/json;charset=utf-8'
    return res


@app.before_request
def before_request():
    ip = request.remote_addr
    url = request.url
    method = request.method
    if request.method == 'OPTIONS':
        print(ip, url, method)
    if request.method == 'POST' or request.method == 'GET':
        print(ip, url, method)


@app.errorhandler(StatusCode.UNAUTHORIZED)
def handle_401(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():

        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(StatusCode.UNAUTHORIZED)
            if hander is not None:
                return hander(e)
    response = {"error_code": StatusCode.UNAUTHORIZED, "error_msg": "url not found"}
    return response


@app.errorhandler(StatusCode.NOT_FOUND)
def handle_404(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():

        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(StatusCode.NOT_FOUND)
            if hander is not None:
                return hander(e)
    response = {"error_code": StatusCode.NOT_FOUND, "error_msg": "url not found"}
    return response


@app.errorhandler(StatusCode.INTERNAL_SERVER_ERROR)
def handle_500(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():
        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(StatusCode.INTERNAL_SERVER_ERROR)
            if hander is not None:
                return hander(e)
    response = {"error_code": StatusCode.INTERNAL_SERVER_ERROR, "error_msg": "INTERNAL ERROR"}
    return response


@app.errorhandler(StatusCode.BAD_REQUEST)
def handle_400(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():
        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(StatusCode.BAD_REQUEST)
            if hander is not None:
                return hander(e)
    response = {"error_code": StatusCode.BAD_REQUEST, "error_msg": "BAD REQUEST"}
    return response


@app.errorhandler(StatusCode.FORBIDDEN)
def handle_403(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():
        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(StatusCode.FORBIDDEN)
            if hander is not None:
                return hander(e)
    response = {"error_code": StatusCode.FORBIDDEN, "error_msg": "Forbidden,You are not allowed to access this"}
    return response


if __name__ == '__main__':
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    app.before_request(before_request)
    app.after_request(after_request)
    app.run(host='0.0.0.0', port=8888)
