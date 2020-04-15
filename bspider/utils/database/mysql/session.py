

class DBSession(object):

    def __init__(self, pool, select_func):
        """得到一个线程安全连接"""
        self.__conn = pool.dedicated_connection()
        self.__cursor = self.__conn.cursor()
        self.__select = select_func

    def insert(self, sql: str, values: tuple = None, lastrowid: bool = False) -> int:
        return self._query(sql, values, lastrowid)

    def update(self, sql: str, values: tuple = None) -> int:
        return self._query(sql, values)

    def delete(self, sql: str, values: tuple = None) -> int:
        return self._query(sql, values)

    def select(self, sql: str, values: tuple = None,
               retry_times: int = 0, retry_interval: int = 1) -> list:
        return self.__select(sql,
                             values=values,
                             retry_times=retry_times,
                             retry_interval=retry_interval)

    def query(self, sql: str, values: tuple = None, lastrowid: bool = False):
        """
        query func
        :param sql: sql
        :param values: sql中需要初始化的值
        :param lastrowid:
        :return:
        """
        return self._query(sql, values=values, lastrowid=lastrowid)

    def _query(self, sql: str, values: tuple = None, lastrowid: bool = False):
        if values is None:
            result = self.__cursor.execute(sql)
        else:
            result = self.__cursor.execute(sql, values)

        if lastrowid:
            return self.__cursor.lastrowid
        else:
            return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.__cursor.close()
            self.__conn.close()
            return False
        else:
            self.__cursor.close()
            self.__conn.commit()
            self.__conn.close()
            return True
