# -- coding: utf-8 --
# @Time : 2023/2/18 10:19
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : user_dao.py
# @Software: PyCharm
from models.user.user_model import UserModel


class UserDao:
    @staticmethod
    def query_userinfo(account='', username=''):
        user_info_paginate = UserModel.query.filter(
            UserModel.account == account,
            UserModel.username.like(f'%{username}%')
        ).first()
        return user_info_paginate
