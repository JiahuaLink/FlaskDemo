# -- coding: utf-8 --
# @Time : 2023/2/18 09:29
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : user_model.py
# @Software: PyCharm
from exts import db


class UserModel(db.Model):
    __tablename__ = 't_user'

    account = db.Column(db.String(collation='NOCASE'), primary_key=True, autoincrement=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def set_account(self, account):
        self.account = account

    def get_account(self) -> str:
        return self.account
