# -- coding: utf-8 --
# @Time : 2023/2/18 10:31
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : redis_manager.py
# @Software: PyCharm
import redis
from flask import current_app


class RedisManager:
    @staticmethod
    def _get_r():
        host = current_app.config.get('REDIS_HOST')
        port = current_app.config.get('REDIS_PORT')
        pwd = current_app.config.get('REDIS_PWD')
        db = current_app.config.get('REDIS_DB')
        r = redis.StrictRedis(host=host, port=port,password=pwd)