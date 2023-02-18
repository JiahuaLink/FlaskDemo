# -- coding: utf-8 --
# @Time : 2023/2/17 22:37
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : response.py
# @Software: PyCharm
import json


class MyResponse:
    def __init__(self, error_code=200, error_msg=None, data: dict = None):
        self.error_code = error_code
        self.error_msg = error_msg
        self.data = data

    def set_error_code(self, code):
        self.error_code = code

    def set_error_msg(self, msg):
        self.error_msg = msg

    def set_data(self, data):
        self.data = data

    def to_dict(self):
        response = {"error_code": self.error_code, "error_msg": self.error_msg, "data": self.data}
        return response


if __name__ == '__main__':
    print(MyResponse(200, 'success', '123'))
