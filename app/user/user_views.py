# -- coding: utf-8 --
# @Time : 2023/2/17 22:27
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : user_views.py
# @Software: PyCharm
import traceback

from flask import Blueprint, make_response, request, current_app
from flask_cors import cross_origin

from models.error_msg import ErrorMessage
from models.response import MyResponse
from models.ret_code import RetCode
from models.user.user_model import UserModel
from service.user_service import UserService
from utils.auth.login_auth import login_required
from utils.log.log_manager import logger
from utils.redis.redis_manager import RedisManager

user = Blueprint('user', __name__, url_prefix='/api')


@cross_origin(support_credentials=True)
@user.route('/v1/login', methods=['POST'])
def login():
    try:
        account: str = request.json.get('account')
        password: str = request.json.get('password')
        verify_code = request.json.get('verifycode')
        logger.info(f' Try to login,account is {account},verify_code is {verify_code}')
    except Exception:
        logger.error(f'Exception,{traceback.format_exc()}')
    return UserService(account=account).verify_login(account, password, verify_code)


@cross_origin(support_credentials=True)
@user.route('/v1/users', methods=['GET'])
# @login_required
def get_user_info():
    response = MyResponse(error_code=RetCode.SUCCESS, error_msg=ErrorMessage.SUCCESS, data=[])
    account = request.args.get('account')
    # username = request.args.get('username')
    try:
        user_info = UserService(account=account).get_user_info()
        if user_info is None:
            response.set_error_msg(f'{account} {ErrorMessage.USER_NOT_EXISTS}')
            response.set_error_code(RetCode.USER_NOT_EXISTS)
            return make_response(response.to_dict()), RetCode.BAD_REQUEST
        response.set_data(user_info)
    except Exception:
        logger.error(f'Exception,get_user_info {traceback.format_exc()}')
        response.set_error_msg(ErrorMessage.SERVER_INTERNAL_ERROR)
    return make_response(response.to_dict()), RetCode.SUCCESS
