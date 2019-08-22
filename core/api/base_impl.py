# @Time    : 2019/6/18 3:47 PM
# @Author  : 白尚林
# @File    : base_impl
# @Use     :
from util.database.mysql.handler import MysqlHandler
from config.frame_settings import WEB_STUDIO_DB


class BaseImpl(object):

    def __init__(self):
        self.handler = MysqlHandler.from_settings(WEB_STUDIO_DB)

    @staticmethod
    def make_fv(data: dict) -> tuple:
        """
        给定字典，返回fields 和 values
        :param info: dict
        :return:
        """
        fields = ','.join([' `%s`=%%s ' % (key) for key in data.keys()])
        values = [data[key] for key in data.keys()]
        return fields, tuple(values)


# def remove(self, unique_value, unique_key='id'):
    #     sql = f"update {self.table_name} set `status`=%s where `{unique_key}` = '{unique_value}';"
    #     return self.handler.update(sql, (-1))
    #
    # def update(self, unique_value, data, unique_key='id'):
    #     fields, values = self.make_fv(data)
    #     sql = f"update {self.table_name} set {fields} where `{unique_key}` = '{unique_value}';"
    #     return sql, values
    #
    # def add(self, data):
    #     fields, values = self.make_fv(data)
    #     sql = f"insert into {self.table_name} set {fields};"
    #     return self.handler.insert(sql, values, lastrowid=True)
