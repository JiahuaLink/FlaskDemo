# -- coding: utf-8 --
# @Time : 2023/2/18 10:00
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : error_msg.py
# @Software: PyCharm
from xmlrpc.client import SERVER_ERROR


class ErrorMessage:
    SUCCESS = 'SUCCESS'
    SERVER_INTERNAL_ERROR = 'SERVER INTERNAL ERROR'
    USER_NOT_EXISTS = 'USER NOT EXISTS'
    USER_NOT_LOGIN = 'User Not Login,Permission Denied'
    URL_NOT_FOUND = 'URL NOT FOUND'
    UNAUTHORIZED = 'User is not authorized'
    BAD_REQUEST = 'BAD REQUEST'
    PARAM_INCORRECT = 'The username or password is incorrect'
