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
    data_source_table = frame_settings['DATA_SOURCE_TABLE']
    p2ds_table = frame_settings['P2DS_TABLE']

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
    def mini_record(data: list) -> dict:
        if not len(data):
            return dict()
        project = []
        sign = set()
        for row in data:
            if row['project_id'] and row['project_id'] not in sign:
                project.append({'id': row['project_id'], 'name': row['project_name']})
                sign.add(row['project_id'])
        data[0]['project'] = project
        return data[0]

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

    def insert(self, data: dict, table_name: str, lastrowid=True, get_sql=False):
        fields, values = self.make_fv(data)
        sql = f"insert into {table_name} set {fields};"
        if get_sql:
            return sql, values, lastrowid
        return self.mysql_client.insert(sql, values, lastrowid=lastrowid)

    def get_all_node_ip(self) -> list:
        """
        返回列表形式的ip列表
        :return: ['127.0.0.1', ...]
        """
        sql = f'select `ip` from {self.node_table} where `status` = 1;'
        return [info['ip'] for info in self.mysql_client.select(sql)]

    def update(self, unique_key: str, unique_value, data: dict, table_name: str, get_sql=False):
        fields, values = self.make_fv(data)
        values = list(values)
        values.append(unique_value)
        sql = f"update {table_name} set {fields} where `{unique_key}` = %s;"
        if get_sql:
            return sql, values
        return self.mysql_client.update(sql, values)

    def delete(self, unique_key: str, unique_value, table_name: str, get_sql=False):
        sql = f"delete from {table_name} where `{unique_key}`= %s;"
        if get_sql:
            return sql, (unique_value)
        return self.mysql_client.delete(sql, (unique_value))
