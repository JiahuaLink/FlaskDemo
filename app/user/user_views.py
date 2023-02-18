# -- coding: utf-8 --
# @Time : 2023/2/17 22:27
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : user_views.py
# @Software: PyCharm
from flask import Blueprint, make_response, request
from flask_cors import cross_origin

from models.error_msg import ErrorMessage
from models.response import MyResponse
from models.stutus_code import StatusCode
from service.user_service import UserService
from utils.auth.login import login_required

user = Blueprint('user', __name__, url_prefix='/api')


@login_required
@cross_origin(support_credentials=True)
@user.route('/v1/users', methods=['GET'])
def get_user_info():
    response = MyResponse(error_code=StatusCode.SUCCESS, error_msg='success', data=[])

    account = request.args.get('account')
    username = request.args.get('username')

    try:
        user_info = UserService(account=account).get_user_info()
        if user_info is None:
            response.set_error_msg(f'{username}，{ErrorMessage.USER_NOT_EXISTS}')
            response.set_error_code(StatusCode.USER_NOT_EXISTS)
            return make_response(response.to_dict()), StatusCode.FORBIDDEN
        response.set_data(user_info)
    except:
        response.set_error_msg(ErrorMessage.SERVER_INTERNAL_ERROR)
    return make_response(response.to_dict()), StatusCode.SUCCESS
