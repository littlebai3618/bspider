"""
mysql 的异步封装
"""
import asyncio
import hashlib

import aiomysql
from aiomysql import Pool, DictCursor

from bspider.utils import singleton
from bspider.utils.tools import coroutine_result


@singleton
class AioMysqlPoolFactory(object):
    """
    mysql 异步连接池的连接池 不支持事务
    """

    def __init__(self):
        self.__pools = dict()

    def __del__(self):
        for key, pool in self.__pools.items():
            pool.close()

    @staticmethod
    def __make_hash(mysql_config):
        hashstr = ','.join([f'{k}:{v}' for k, v in mysql_config.items()])
        hashcode = hashlib.md5(hashstr.encode('utf8')).hexdigest()
        return hashcode

    def get_pool(self, mysql_config) -> Pool:
        hashcode = self.__make_hash(mysql_config)
        if hashcode in self.__pools:
            return self.__pools[hashcode]
        else:
            pool = coroutine_result(aiomysql.create_pool(
                host=mysql_config['host'],
                port=mysql_config['port'],
                user=mysql_config['user'],
                password=mysql_config['password'],
                db=mysql_config['db'],
                charset=mysql_config['charset'],
                cursorclass=DictCursor
            ))
            self.__pools[hashcode] = pool
            return pool


class AioMysqlClient(object):
    """封装了常用操作的mysql句柄，重试默认3次"""

    def __init__(self, config):
        self.__pool = AioMysqlPoolFactory().get_pool(config)

    @classmethod
    def from_settings(cls, settings):
        """通过配置创建AioMysqlHandler对象"""
        return cls(settings)

    async def select(self, sql: str, values: tuple = None,
                     retry_times: int = 0, retry_interval: int = 1) -> list:
        """
        提供重试的查询方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: 查询结果
        """
        return await self._do_query(self._select, sql, values=values,
                                    retry_times=retry_times,
                                    retry_interval=retry_interval)

    async def insert(self, sql: str, values: tuple = None,
                     retry_times: int = 0, retry_interval: int = 1) -> int:
        """
        提供重试的插入方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: 插入结果
        """
        return await self._do_query(self._insert, sql, values=values,
                                    retry_times=retry_times,
                                    retry_interval=retry_interval)

    async def update(self, sql: str, values: tuple = None,
                     retry_times: int = 0, retry_interval: int = 1) -> int:
        """
        提供重试的更新方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: 更新结果
        """
        return await self._do_query(self._update, sql, values=values,
                                    retry_times=retry_times,
                                    retry_interval=retry_interval)

    async def delete(self, sql: str, values: tuple = None,
                     retry_times: int = 0, retry_interval: int = 1) -> int:
        """
        提供重试的删除方法方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: 删除行数
        """
        return await self._do_query(self._delete, sql, values=values,
                                    retry_times=retry_times,
                                    retry_interval=retry_interval)

    async def query(self, sql: str, values: tuple = None,
                    retry_times: int = 0, retry_interval: int = 1):
        """
        query
        :param sql: sql语句
        :param values: sql语句中的值
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :return: T
        """
        return await self._do_query(self._query, sql, values=values,
                                    retry_times=retry_times,
                                    retry_interval=retry_interval)

    async def _do_query(self, func, sql: str, values: tuple = None,
                        retry_times: int = 0, retry_interval: int = 1):
        loop_times = retry_times if retry_times > 0 else 3
        while loop_times > 0:
            try:
                return await func(sql, values)
            except aiomysql.Error as e:
                errid, errmsg = e.args
                if errid != 2014:  # 不是mysql连接失败错误
                    raise e
            await asyncio.sleep(retry_interval)
        raise aiomysql.MySQLError('mysql connection error')

    async def _query(self, sql: str, values: tuple = None) -> int:
        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                if values is None:
                    result = await cur.execute(sql)
                else:
                    result = await cur.execute(sql, values)
                await conn.commit()
                return result

    async def _select(self, sql: str, values: tuple = None) -> list:
        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                if values is None:
                    result_count = await cur.execute(sql)
                else:
                    result_count = await cur.execute(sql, values)
                if result_count > 0:
                    return await cur.fetchall()
                else:
                    return []

    async def _insert(self, sql: str, values: tuple = None) -> int:
        return await self._query(sql, values)

    async def _update(self, sql: str, values: tuple = None) -> int:
        return await self._query(sql, values)

    async def _delete(self, sql: str, values: tuple = None) -> int:
        return await self._query(sql, values)
