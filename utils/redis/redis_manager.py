# -- coding: utf-8 --
# @Time : 2023/2/18 10:31
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : redis_manager.py
# @Software: PyCharm
import json
import traceback

import redis
from flask import current_app

from utils.log.log_manager import logger


class RedisManager(object):
    @staticmethod
    def _get_r():
        host = current_app.config.get('REDIS_HOST')
        port = current_app.config.get('REDIS_PORT')
        pwd = current_app.config.get('REDIS_PWD')
        db = current_app.config.get('REDIS_DB')
        r = redis.StrictRedis(host=host, port=port, db=db, password=pwd)
        return r

    @staticmethod
    def read_cache(redis_key, redis_enable=False):
        if redis_enable:
            return RedisManager.read(redis_key)
        return None

    @staticmethod
    def read_keys_chache(redis_key, redis_enable=False):
        if redis_enable:
            return RedisManager.read_keys(redis_key, redis_enable)
        return []

    @classmethod
    def read(cls, key):
        r = cls._get_r()
        try:
            value: bytes = r.get(key)
        except Exception as e:
            logger.error(f'Exception,read key {key} error,{traceback.format_exc()}')
            return
        return value.decode('utf-8') if value else value

    @classmethod
    def read_keys(cls, key, redis_enable=False):
        r = cls._get_r()
        tmp = []
        try:
            value_list = r.keys(f'{key}')
            value_list = [i.decode('utf-8') for i in value_list]
            if value_list:
                for key in value_list:
                    data_string = RedisManager.read_cache(key, redis_enable)
                    if data_string:
                        data = json.loads(data_string)
                        tmp.append(data)

        except Exception as e:
            logger.error(f'Exception,{traceback.format_exc()}')
            return
        return tmp

    @classmethod
    def delete(cls, *names):
        r = cls._get_r()
        r.delete(*names)

    @classmethod
    def expire(cls, key, expires=None):
        """
        ??????????????????
        :param key:
        :param expires: ?????????
        :return:
        """
        if expires:
            exppire_in_secconds = expires
        else:
            exppire_in_secconds = current_app.config['REDIS_EXPIRE']
        r = cls._get_r()
        r.expire(key, expires)
