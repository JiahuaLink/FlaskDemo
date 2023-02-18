# -- coding: utf-8 --
# @Time : 2023/2/18 09:38
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : object_to_map.py
# @Software: PyCharm
import json


def dict_to_obj(dictObject: dict, obj):
    for k,v in dictObject.items():
        obj.__dict__[k] = v
    return obj
def dict_to_str(dict_object: dict, ensure_ascii=False):
    return json.dumps(dict_object, ensure_ascii=ensure_ascii)

def str_to_dict(str_object: str):
    dic = json.loads(str_object)
    return dic

def object_to_json_string(self, ensure_ascii=False):
    return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=ensure_ascii)

