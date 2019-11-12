# @Time    : 2019-07-26 11:56
# @Author  : 白尚林
# @File    : __init__.py
# @Use     :
from .handler import MysqlHandler
from .async_handler import AioMysqlHandler

def prepare_insert_sql(table: str, data: dict, **kwargs) -> (str, tuple):
    """
    dict数据 -> sql
    :param table: mysql表名
    :param data: 插入的数据
    :param kwargs: 其他参数
        当 auto_update bool
        immutable_fields list：当auto_update = True时 生效，忽略一些参数的更新
    :return: sql, value
    """
    import io
    sbuf = io.StringIO()
    sbuf.write('INSERT INTO %s SET ' % table)
    sbuf.write(','.join([
        ' %s=%%s ' % (key) for key in data.keys() if data.get(key)
    ]))
    values = [data[key] for key in data.keys() if data.get(key)]

    if not kwargs.get('auto_update'):
        return sbuf.getvalue(), tuple(values)

    sbuf.write('ON DUPLICATE KEY UPDATE ')
    sbuf.write(','.join([
        ' %s=%%s ' % (key) for key in data.keys()
        if data.get(key) and key not in kwargs.get('immutable_fields', [])
    ]))

    values.extend([
        data[key] for key in data.keys()
        if data.get(key) and key not in kwargs.get('immutable_fields', [])
    ])
    return sbuf.getvalue(), tuple(values)
