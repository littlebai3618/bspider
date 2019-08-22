# @Time    : 2019/7/1 11:17 AM
# @Author  : 白尚林
# @File    : node_impl
# @Use     :
from core.api import BaseImpl
from core.lib import NODE_TABLE, WORKER_TABLE, NODE_STATUS_TABLE, PROJECT_TABLE, CODE_STORE_TABLE, P2C_TABLE
from util.database.mysql.mysql_stream import MysqlOutputStream


class NodeImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.node_table = NODE_TABLE
        self.worker_table = WORKER_TABLE
        self.node_status_table = NODE_STATUS_TABLE
        self.project_table = PROJECT_TABLE
        self.code_table = CODE_STORE_TABLE
        self.p2c = P2C_TABLE

    def get_jobs(self):
        sql = f"SELECT `p`.`status` as `project_status`, `p`.`id` AS `project_id`,`p`.`name` AS `project_name`," \
            f"`p`.`config` AS `config`, `p`.`rate` AS `rate`,`c`.`name` AS `code_name`," \
            f"`c`.`content` AS `code`,`c`.`type` AS `code_type` FROM `{self.project_table}` AS `p` " \
            f"LEFT JOIN `{self.p2c}` AS `p2c` ON p.id=p2c.project_id " \
            f"LEFT JOIN `{self.code_table}` AS `c` ON c.id=p2c.customcode_id " \
            f"WHERE `p`.`status`=1"
        return self.handler.select(sql)

    def add_node(self, data):
        return MysqlOutputStream(self.handler, self.node_table).write(data)

    def delete_node(self, key, value, get_sql=False):
        """a common delete func"""
        sql = f"delete from {self.node_table} where `{key}` = '{value}';"
        if get_sql:
            return sql
        return self.handler.delete(sql)

    def delete_worker(self, key, value, get_sql=False):
        sql = f"delete from {self.worker_table} where `{key}` = '{value}';"
        if get_sql:
            return sql
        return self.handler.delete(sql)

    def get_worker_by_ip(self, node_ip):
        sql = f'select `name`, `type`, `ip`, `status` from {self.worker_table} where `ip`="{node_ip}"'
        return self.handler.select(sql)

    def update_node(self, unique_value, data, unique_key='id', get_sql=False):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.node_table} set {fields} where `{unique_key}` = '{unique_value}';"
        if get_sql:
            return sql
        return self.handler.update(sql, values)

    def get_node(self, node_ip):
        sql = f'select `ip`, `name` from {self.node_table} ' \
            f'where `id`="{node_ip}"'
        return self.handler.select(sql)

    def get_nodes(self):
        sql = f'select `ip`, `name` from {self.node_table} '
        return self.handler.select(sql)

    def add_worker(self, data, get_sql=False):
        """注册一个节点"""
        fields, values = BaseImpl.make_fv(data)
        sql = f"insert into {self.worker_table} set {fields};"
        if get_sql:
            return sql, values
        return self.handler.insert(sql, values)

    def update_worker(self, unique_value, data, unique_key='id', get_sql=False):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.worker_table} set {fields} where `{unique_key}` = '{unique_value}';"
        if get_sql:
            return sql
        return self.handler.update(sql, values)

    def get_worker(self, name):
        sql = f'select `ip`, `name`, `type`, `description` from {self.worker_table} where `name`="{name}";'
        return self.handler.select(sql)

    def get_workers(self):
        sql = f'select `ip`, `name`, `type`, `description` from {self.worker_table};'
        return self.handler.select(sql)
