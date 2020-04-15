import hashlib

import time

import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor

from bspider.utils import singleton
from bspider.utils.database.mysql.session import DBSession


@singleton
class MysqlPoolFactory(object):
    MYSQL_DEFAULT_CHARSET = 'utf8'

    def __init__(self):
        self.__pools = dict()

    def __del__(self):
        for key, pool in self.__pools.items():
            pool.close()

    def prepare_params(self, *args, **kwargs):
        mysql_params = {
            'host': None,
            'port': None,
            'user': None,
            'password': None,
            'db': None,
            'charset': self.MYSQL_DEFAULT_CHARSET,
        }
        if args or kwargs:
            for k, v in dict(*args, **kwargs).items():
                if k in mysql_params:
                    mysql_params[k] = v
        return mysql_params

    @staticmethod
    def __make_hash(mysql_config):
        hashstr = ','.join([f'{k}:{v}' for k, v in mysql_config.items()])
        hashcode = hashlib.md5(hashstr.encode('utf8')).hexdigest()
        return hashcode

    def get_pool(self, creator=pymysql, mincached=0, maxcached=20,
                 maxshared=20, maxconnections=20,
                 *args, **kwargs):
        mysql_params = self.prepare_params(*args, **kwargs)
        hashcode = self.__make_hash(mysql_params)

        if hashcode in self.__pools:
            return self.__pools[hashcode]
        else:
            pool = PooledDB(creator=creator,
                            mincached=mincached, maxcached=maxcached,
                            maxshared=maxshared, maxconnections=maxconnections,
                            *args, **kwargs)
            self.__pools[hashcode] = pool
            return pool


class MysqlClient(object):
    """封装了常用操作的mysql句柄，重试默认3次, 线程安全"""

    def __init__(self, mysql_config):
        self.__pool = MysqlPoolFactory().get_pool(
            host=mysql_config['host'],
            port=mysql_config['port'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            db=mysql_config['db'],
            charset=mysql_config['charset'],
            cursorclass=DictCursor
        )

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    @staticmethod
    def _do_query(func, sql: str, values: tuple = None, retry_times: int = 0,
                  retry_interval: int = 1, lastrowid: bool = False):
        loop_times = retry_times if retry_times > 0 else 3
        while loop_times > 0:
            try:
                if lastrowid:
                    return func(sql, values, lastrowid=lastrowid)
                else:
                    return func(sql, values)
            except pymysql.Error as e:
                errid, errmsg = e.args
                if errid != 2014:
                    raise e
            time.sleep(retry_interval)
        raise pymysql.MySQLError('mysql connection error')

    def select(self, sql: str, values: tuple = None,
               retry_times: int = 0, retry_interval: int = 1) -> list:
        """
        提供重试的查询方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: 查询结果
        """
        return self._do_query(self._select, sql,
                              values=values,
                              retry_times=retry_times,
                              retry_interval=retry_interval)

    def insert(self, sql: str, values: tuple = None, retry_times: int = 0,
               retry_interval: int = 1, lastrowid: bool = False) -> int:
        """
        提供重试的插入方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :param lastrowid: 是否返回自增id
        :return: 插入结果
        """
        return self._do_query(self._insert, sql,
                              values=values,
                              retry_times=retry_times,
                              retry_interval=retry_interval,
                              lastrowid=lastrowid)

    def update(self, sql: str, values: tuple = None,
               retry_times: int = 0, retry_interval: int = 1) -> int:
        """
        提供重试的更新方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: 更新结果
        """
        return self._do_query(self._update, sql, values=values,
                              retry_times=retry_times,
                              retry_interval=retry_interval)

    def delete(self, sql: str, values: tuple = None,
               retry_times: int = 0, retry_interval: int = 1) -> int:
        """
        提供重试的删除方法方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: 删除行数
        """
        return self._do_query(self._delete, sql, values=values,
                              retry_times=retry_times,
                              retry_interval=retry_interval)

    def query(self, sql: str, values: tuple = None,
              retry_times: int = 0, retry_interval: int = 1):
        """
        query
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: T
        """
        return self._do_query(self._query, sql, values=values,
                              retry_times=retry_times,
                              retry_interval=retry_interval)

    def session(self) -> DBSession:
        """返回一个session 来支持事务"""
        return DBSession(self.__pool, self.select)

    def _select(self, sql: str, values: tuple = None) -> list:
        conn = None
        cursor = None
        try:
            conn = self.__pool.dedicated_connection()
            cursor = conn.cursor()
            if values is None:
                result_count = cursor.execute(sql)
            else:
                result_count = cursor.execute(sql, values)
            if result_count > 0:
                return cursor.fetchall()
            else:
                return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _query(self, sql: str, values: tuple = None, lastrowid: bool = False):
        conn = None
        cursor = None
        try:
            conn = self.__pool.dedicated_connection()
            cursor = conn.cursor()
            if values is None:
                result = cursor.execute(sql)
            else:
                result = cursor.execute(sql, values)

            if lastrowid:
                return cursor.lastrowid
            else:
                return result
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.commit()
                conn.close()

    def _insert(self, sql: str, values: tuple = None, lastrowid: bool=False) -> int:
        return self._query(sql, values, lastrowid=lastrowid)

    def _update(self, sql: str, values: tuple = None) -> int:
        return self._query(sql, values)

    def _delete(self, sql: str, values: tuple = None) -> int:
        return self._query(sql, values)
