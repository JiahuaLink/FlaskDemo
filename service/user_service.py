# -- coding: utf-8 --
# @Time : 2023/2/18 10:07
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : user_service.py
# @Software: PyCharm
import json
import traceback

from flask import current_app, make_response

from dao.user.user_dao import UserDao
from models.error_msg import ErrorMessage
from models.response import MyResponse
from models.ret_code import RetCode
from models.user.user_model import UserModel
from utils.auth.login_auth import generate_access_token
from utils.log.log_manager import logger
from utils.redis.redis_manager import RedisManager


class UserService:

    def __init__(self, account):
        self.account = account

    def get_user_info(self):
        user_info: UserModel = UserDao.query_userinfo(self.account)
        if user_info is not None:
            account = user_info.get_account()
            username = user_info.get_username()
            password = user_info.get_password()
            userinfo = {
                "account": account,
                "username": username,
                "password": password
            }
            return userinfo
        return None

    def verify_login(self, account, password, verify_code):
        response = MyResponse(error_code=RetCode.SUCCESS_CODE, error_msg=ErrorMessage.SUCCESS, data=[])
        try:
            verify_mode = current_app.config['VERIFYs_CODE']
            user_info: UserModel = UserDao.query_userinfo(self.account)
            if not user_info:
                logger.error(
                    f'Login Failed,Account:{account},cause by:{RetCode.USER_NOT_EXISTS},{ErrorMessage.USER_NOT_EXISTS}')
                response.set_error_msg(f'{account} {ErrorMessage.USER_NOT_EXISTS}')
                response.set_error_code(RetCode.USER_NOT_EXISTS)
                return make_response(response.to_dict()), RetCode.BAD_REQUEST
            if user_info.get_account().lower() == account.lower() and user_info.get_password().lower() == password.lower():
                if verify_mode == 1:
                    redis_key = f'verify_mode:{account}'
                    data_string = RedisManager.read_cache(redis_key)
                    if data_string:
                        verify_code_redis = json.loads(data_string)
                        if verify_code_redis == verify_code:

                            access_token = generate_access_token(user_info.get_account())
                            response.set_error_code(RetCode.SUCCESS_CODE)
                            response.set_error_msg(ErrorMessage.SUCCESS)
                            response.set_access_token(access_token)
                            logger.error(f'Login Successful,Account {user_info.get_account()} verify code is correct')
                            return make_response(response.to_dict()), RetCode.SUCCESS
                        else:
                            logger.error(
                                f'Login Failed,Account {user_info.get_account()}cause by:{RetCode.BAD_REQUEST},{ErrorMessage.VERIFY_INCORRECT}')
                            response.set_error_msg(ErrorMessage.VERIFY_INCORRECT)
                            response.set_error_code(RetCode.BAD_REQUEST)
                            return make_response(response.to_dict()), RetCode.BAD_REQUEST

                else:

                    access_token = generate_access_token(user_info.get_account())
                    response.set_error_code(RetCode.SUCCESS_CODE)
                    response.set_error_msg(ErrorMessage.SUCCESS)
                    response.set_access_token(access_token)
                    logger.info(f'Login Successful,account is {user_info.get_account()} ')
                    return make_response(response.to_dict()), RetCode.SUCCESS
            response.set_error_msg(ErrorMessage.PARAM_INCORRECT)
            response.set_error_code(RetCode.BAD_REQUEST)
            logger.error(f'Login Failed,Account {user_info.get_account()} {ErrorMessage.PARAM_INCORRECT}')
            return make_response(response.to_dict()), RetCode.BAD_REQUEST
        except Exception:
            logger.error(f'verify login is Exception,{traceback.format_exc()}')
            response.set_error_msg(ErrorMessage.SERVER_INTERNAL_ERROR)
            response.set_error_code(RetCode.INTERNAL_SERVER_ERROR)
            return make_response(response.to_dict()), RetCode.INTERNAL_SERVER_ERROR
