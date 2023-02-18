from flask import Flask, request, make_response, jsonify

from flask_cors import CORS
from app.user.user_views import user
from exts import db
from models.error_msg import ErrorMessage
from models.response import MyResponse
from models.ret_code import RetCode

app = Flask(__name__)
CORS(app, resource=r'/*')
CORS(app, supports_credentials=True)

app.register_blueprint(user)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.after_request
def after_request(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control'] = 'no-cache'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT'
    res.headers[
        'Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-Requested-With,Origin,Content-Length.User-Agent'
    res.headers['Content-Type'] = 'application/json;charset=utf-8'
    res.headers['Authorization'] = 'accessToken'
    return res


@app.before_request
def before_request():
    ip = request.remote_addr
    url = request.url
    method = request.method
    # if request.method == 'OPTIONS':
    #     print(ip, url, method)
    # if request.method == 'POST' or request.method == 'GET':
    #     print(ip, url, method)


@app.errorhandler(RetCode.UNAUTHORIZED)
def handle_401(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():

        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(RetCode.UNAUTHORIZED)
            if hander is not None:
                return hander(e)
    response = MyResponse(error_code=RetCode.UNAUTHORIZED, error_msg=ErrorMessage.UNAUTHORIZED)

    return response.to_dict()


@app.errorhandler(RetCode.NOT_FOUND)
def handle_404(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():

        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(RetCode.NOT_FOUND)
            if hander is not None:
                return hander(e)
    response = MyResponse(error_code=RetCode.NOT_FOUND, error_msg=ErrorMessage.URL_NOT_FOUND)

    return response.to_dict()


@app.errorhandler(RetCode.INTERNAL_SERVER_ERROR)
def handle_500(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():
        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(RetCode.INTERNAL_SERVER_ERROR)
            if hander is not None:
                return hander(e)
    response = MyResponse(error_code=RetCode.INTERNAL_SERVER_ERROR, error_msg=ErrorMessage.SERVER_INTERNAL_ERROR)
    return response.to_dict()


@app.errorhandler(RetCode.BAD_REQUEST)
def handle_400(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():
        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(RetCode.BAD_REQUEST)
            if hander:
                return hander(e)
    response = MyResponse(error_code=RetCode.BAD_REQUEST, error_msg=ErrorMessage.BAD_REQUEST)
    return response.to_dict()


@app.errorhandler(RetCode.FORBIDDEN)
def handle_403(e):
    path = request.path
    for bp_name, bp in app.blueprints.items():
        if path.startswith(bp.url_prefix):
            hander = app.error_handler_spec.get(bp_name, {}).get(RetCode.FORBIDDEN)
            if hander is not None:
                return hander(e)
    response = {"error_code": RetCode.FORBIDDEN, "error_msg": "Forbidden,You are not allowed to access this"}
    return response


if __name__ == '__main__':
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    app.before_request(before_request)
    app.after_request(after_request)
    app.run(host='0.0.0.0', port=8888)
