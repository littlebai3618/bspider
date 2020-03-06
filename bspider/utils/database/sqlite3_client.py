import sqlite3

from bspider.utils import singleton


@singleton
class SqlLite3Client(object):

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    @staticmethod
    def _do_query(func, sql: str, values: tuple = None, lastrowid: bool = False):
        if lastrowid:
            return func(sql, values, lastrowid)
        else:
            return func(sql, values)

    def select(self, sql: str, values: tuple = None) -> list:
        """
        提供重试的查询方法
        :param sql: sql语句
        :param values: sql语句中的值
        :return: 查询结果
        """
        return self._do_query(self._select, sql, values=values)

    def insert(self, sql: str, values: tuple = None, lastrowid: bool = False) -> int:
        """
        提供重试的插入方法
        :param sql: sql语句
        :param values: sql语句中的值
        :param lastrowid: 是否返回自增id
        :return: 插入结果
        """
        return self._do_query(self._insert, sql, values=values, lastrowid=lastrowid)

    def update(self, sql: str, values: tuple = None) -> int:
        """
        提供重试的更新方法
        :param sql: sql语句
        :param values: sql语句中的值
        :return: 更新结果
        """
        return self._do_query(self._update, sql, values=values)

    def delete(self, sql: str, values: tuple = None) -> int:
        """
        提供重试的删除方法方法
        :param sql: sql语句
        :param values: sql语句中的值
        :return: 删除行数
        """
        return self._do_query(self._delete, sql, values=values)

    def query(self, sql: str, values: tuple = None):
        """
        query
        :param sql: sql语句
        :param values: sql语句中的值
        :return: T
        """
        return self._do_query(self._query, sql, values=values)

    def _select(self, sql: str, values: tuple = None) -> list:
        cursor = None
        try:
            cursor = self.conn.cursor()
            if values is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, values)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

    def _insert(self, sql: str, values: tuple = None) -> int:
        return self._query(sql, values)

    def _update(self, sql: str, values: tuple = None) -> int:
        return self._query(sql, values)

    def _delete(self, sql: str, values: tuple = None) -> int:
        return self._query(sql, values)

    def _query(self, sql: str, values: tuple = None, lastrowid: bool = False):
        cursor = None
        try:
            cursor = self.conn.cursor()
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
            self.conn.commit()
