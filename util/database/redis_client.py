# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   仿照mysql handler，应用单例模式和redis连接池的redis handler
   Design: wubo
-------------------------------------------------
"""
import redis

from config.redis_settings import PARSER_COUNT_REDIS
from utils.logger import log
from utils.db_conn.singleton import singleton


@singleton
class RedisPoolFactory(object):
    """Redis Connection Pool"""
    def __init__(self):
        """_pools  key: host:port value: redis pool instance"""
        self._pools = dict()

    def get_pool(self, host, port, db=0, password=None):
        """
        根据参数，判断是否存在相同参数的pool，
        如果有，则返回
        如果没有，创建一个新的pool，然后返回
        """
        if isinstance(port, str):
            port = int(port)
        if isinstance(db, str):
            db = int(db)
        key = '{}:{}:{}'.format(host, port, db)
        if key in self._pools:
            return redis.Redis(connection_pool=self._pools[key])
        else:
            try:
                new_pool = redis.ConnectionPool(host=host, port=port, db=db, password=password,
                                                decode_responses=True, max_connections=5)
                self._pools[key] = new_pool
                return redis.Redis(connection_pool=self._pools[key])
            except Exception as e:
                log.exception(e)
                raise Exception(e)


class RedisClient(object):
    """
    Redis client
    """
    def __init__(self, host, port, db=0, password=None):
        """
        init
        :param name: hash name
        :param host: host
        :param port: port
        :return:
        """
        rpf = RedisPoolFactory()
        self._conn = rpf.get_pool(host, port, db, password)

    @classmethod
    def from_setting(cls, settings):
        """从设定中创建实例"""
        if 'REDIS_HOST' in settings and 'REDIS_PORT' in settings:
            return cls(settings.get('REDIS_HOST'),
                       settings.get('REDIS_PORT'),
                       settings.get('REDIS_DB', 0),
                       settings.get('REDIS_PASSWORD', None),
                       )

    def get(self, key):
        return self._conn.get(key)

    def set(self, key, value):
        return self._conn.set(key, value)

    def setex(self, key, value, time):
        return self._conn.setex(key, value, time)

    def sadd(self, key, value):
        return self._conn.sadd(key, value)

    def delete(self, key):
        return self._conn.delete(key)

    def getbit(self, key, loc):
        return self._conn.getbit(key, loc)

    def setbit(self, key, loc, value):
        return self._conn.setbit(key, loc, value)

    def exists(self, key):
        return self._conn.exists(key)

    def hget(self, hkey, key):
        return self._conn.hget(hkey, key)

    def hset(self, hkey, key, value):
        return self._conn.hset(hkey, key, value)

    def hincrby(self, hkey, key):
        return self._conn.hincrby(hkey, key, 1)

    def hdel(self, hkey, key):
        return self._conn.hdel(hkey, key)

    def hgetall(self, hkey):
        return self._conn.hgetall(hkey)

    def keys(self, pattern):
        return self._conn.keys(pattern)

# 获取全局句柄
redis_handler = RedisClient.from_setting(PARSER_COUNT_REDIS)