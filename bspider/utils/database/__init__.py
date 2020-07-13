from .sqlite3_client import SqlLite3Client
from .redis_client import RedisClient
from .mysql.client import MysqlClient
from .mysql.async_client import AioMysqlClient
from .mysql import prepare_insert_sql
from ..exceptions import DataSourceTypeError

invalid_data_source = {
    'mysql': MysqlClient
}

def valid(param: dict, conn_type: str):
    if conn_type in invalid_data_source:
        return invalid_data_source[conn_type](param).test_conn()
    raise DataSourceTypeError('Invalid data source type: %s' % (conn_type))


