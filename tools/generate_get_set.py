# -- coding: utf-8 --
# @Time : 2023/2/18 09:34
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : generate_get_set.py
# @Software: PyCharm
class UserModel:
    def __init__(self,**kwargs):
        self.username = None
        self.password = None
        self.account = None


def generate_get_set(model:object):
    print(model.__dict__)
    for k in model.__dict__:
        print("def set_" + k + "(self," + k + "):")
        print("\tself." + k, "=" + k)
        print("def get_" + k + "(self):")
        print("\treturn self." + k)
if __name__ == '__main__':
    model = UserModel()
    generate_get_set(model)

