from bspider.utils.database import MysqlClient
from bspider.config import FrameSettings
from bspider.utils.tools import make_fields_values


class BaseImpl(object):
    frame_settings = FrameSettings()
    project_table = frame_settings['PROJECT_TABLE']
    code_table = frame_settings['CODE_STORE_TABLE']
    cron_table = frame_settings['CRON_JOB_STORE_TABLE']
    node_table = frame_settings['NODE_TABLE']
    user_table = frame_settings['USER_TABLE']
    p2c_table = frame_settings['P2C_TABLE']

    downloader_status_table = frame_settings['DOWNLOADER_STATUS_TABLE']
    parser_status_table = frame_settings['PARSER_STATUS_TABLE']

    worker_table = frame_settings['WORKER_TABLE']
    node_status_table = frame_settings['NODE_STATUS_TABLE']

    mysql_client = MysqlClient.from_settings(frame_settings['WEB_STUDIO_DB'])

    @staticmethod
    def make_fv(data: dict) -> tuple:
        """
        给定字典，返回fields 和 values
        :param info: dict
        :return:
        """
        return make_fields_values(data)

    @staticmethod
    def make_search(search: str) -> str:
        """
        给定字典，返回fields 和 values
        :param info: dict
        :return:
        """
        field = list()
        if len(search):
            for kv in search.split(','):
                k, v = kv.split('=')
                field.append('`{}` like \'%%{}%%\' '.format(k, v))
        return ' and '.join(field)

    def total_num(self, search, table_name):
        fields = self.make_search(search)
        if len(fields):
            sql = f"select count(1) as total from `{table_name}` where {fields}; "
        else:
            sql = f"select count(1) as total from `{table_name}`; "
        return self.mysql_client.select(sql)[0]['total']

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
