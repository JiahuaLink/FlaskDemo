# -- coding: utf-8 --
# @Time : 2023/2/18 00:10
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : login_auth.py
# @Software: PyCharm
import random
from functools import wraps

import jwt
import datetime
from datetime import timedelta

from flask import current_app, request, make_response

from models.error_msg import ErrorMessage
from models.response import MyResponse
from models.ret_code import RetCode
from utils.log.log_manager import logger


def generate_access_token(username, algorithm='HS256', exp=2):
    jwt_key = current_app.config['JWT_KEY']
    exp = current_app.config['EXPIRE_TIME']
    now = datetime.datetime.utcnow()
    exp_datetime = now + timedelta(hours=exp)
    access_payload = {
        'exp': exp_datetime,
        'flag': 0,
        'iat': now,
        'iss': 'jiahualink',
        'username': username

    }
    access_token = jwt.encode(access_payload, jwt_key, algorithm=algorithm)
    return access_token


def decode_auth_token(token):
    """
    解密token
    :param token:
    :return:
    """
    jwt_key = current_app.config['JWT_KEY']
    try:
        payload = jwt.decode(token, key=jwt_key, algorithms='HS256')
    except(jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        return ""
    else:
        return payload


def identity(auth_header):
    """
    用户鉴权
    :param auth_header:
    :return:
    """
    if auth_header:
        payload = decode_auth_token(auth_header)
        if not payload:
            return False
        if 'username' in payload and 'flag' in payload:
            return payload['username']
        else:
            return False
    return False


def login_required(f):
    """
    登录保护，验证用户是否登录
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        response = MyResponse(RetCode.SUCCESS, 'SUCCESS')
        logger.info(f'login required,function is {f}')
        token = request.headers.get('Authorization', default=None)

        if not token:
            response.set_error_code(RetCode.FORBIDDEN)
            response.set_error_msg(ErrorMessage.USER_NOT_LOGIN)
            logger.error(
                f'Login Failed,Account:{ErrorMessage.USER_NOT_LOGIN},cause by:Authorization token is not pass')
            return make_response(response.to_dict())
        username = identity(token)
        if not username:
            response.set_error_code(RetCode.FORBIDDEN)
            response.set_error_msg(ErrorMessage.USER_NOT_LOGIN)
            logger.error(
                f'Login Failed,Account:{ErrorMessage.USER_NOT_LOGIN},cause by:username is not pass')
            return make_response(response.to_dict())
        return f(*args, **kwargs)

    return wrapper


def generate_verify_code():
    password_len = 8
    for i in range(20):
        s = ''
        for j in range(password_len):
            if random.randint(0, 1) == 0:
                s += str(random.randint((0, 9)))
            else:
                s += chr(random.randint(65, 90))
        return s
