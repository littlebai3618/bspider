# @Time    : 2019/7/1 11:17 AM
# @Author  : 白尚林
# @File    : node_impl
# @Use     :
from bspider.core.api import BaseImpl
from bspider.utils.database.mysql import MysqlOutputStream
from bspider.web_studio import log


class NodeImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.node_table = self.frame_settings['NODE_TABLE']
        self.worker_table = self.frame_settings['WORKER_TABLE']
        self.node_status_table = self.frame_settings['NODE_STATUS_TABLE']
        self.project_table = self.frame_settings['PROJECT_TABLE']
        self.code_table = self.frame_settings['CODE_STORE_TABLE']
        self.p2c = self.frame_settings['P2C_TABLE']

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
        sql = f'select `name`, `type`, `ip`, `status`, `coroutine_num` from {self.worker_table} where `ip`="{node_ip}"'
        return self.handler.select(sql)

    def update_node(self, unique_value, data, unique_key='id', get_sql=False):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.node_table} set {fields} where `{unique_key}` = '{unique_value}';"
        if get_sql:
            return sql
        return self.handler.update(sql, values)

    def get_node(self, node_id):
        sql = f'select `id`, `ip`, `name`, `description`, `create_time`, `update_time` ' \
            f'from {self.node_table} where `id`="{node_id}"'
        return self.handler.select(sql)

    def get_nodes(self, page, limit, search, sort):
        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `ip`, `name`, `description`, `create_time`, `update_time` ' \
                  f'from {self.node_table} where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `ip`, `name`, `description`, `create_time`, `update_time` ' \
                  f'from {self.node_table} order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql), self.total_num(search, self.node_table)

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

    def get_worker(self, worker_id):
        sql = f'select `id`, `ip`, `name`, `type`, `description`, `coroutine_num`, `create_time`, `update_time` from {self.worker_table} where `id`="{worker_id}";'
        return self.handler.select(sql)

    def get_workers(self, page, limit, search, sort):
        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `ip`, `name`, `type`, `description`, `coroutine_num`, `create_time`, `update_time` ' \
                  f'from {self.worker_table} where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `ip`, `name`, `type`, `description`, `create_time`, `coroutine_num`, `update_time` ' \
                  f'from {self.worker_table} order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql), self.total_num(search, self.worker_table)
