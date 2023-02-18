# -- coding: utf-8 --
# @Time : 2023/2/18 10:00
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : error_msg.py
# @Software: PyCharm
from xmlrpc.client import SERVER_ERROR


class ErrorMessage:
    SERVER_INTERNAL_ERROR = '系统繁忙，请稍后再试'
    USER_NOT_EXISTS = '用户不存在'
    USER_NOT_LOGIN = 'User not logged in,Permission denied'


