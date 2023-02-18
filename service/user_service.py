# -- coding: utf-8 --
# @Time : 2023/2/18 10:07
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : user_service.py
# @Software: PyCharm
from models.user.user_model import UserModel


class UserService:

    def __init__(self, account):
        self.account = account

    def get_user_info(self):
        user_info: UserModel = UserModel.query.filter(UserModel.account == self.account).first()
        if user_info is not None:
            account = user_info.get_account()
            username = user_info.get_username()
            userinfo = {
                "account": account,
                "username": username,
            }
            return userinfo
        return None
