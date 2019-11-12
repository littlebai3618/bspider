# @Time    : 2019/7/1 11:17 AM
# @Author  : 白尚林
# @File    : node_impl
# @Use     :
from bspider.core.api import BaseImpl
from bspider.master import log
from bspider.utils.database.mysql import prepare_insert_sql


class NodeImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.node_table = self.frame_settings['NODE_TABLE']
        self.worker_table = self.frame_settings['WORKER_TABLE']
        self.node_status_table = self.frame_settings['NODE_STATUS_TABLE']
        self.project_table = self.frame_settings['PROJECT_TABLE']
        self.code_table = self.frame_settings['CODE_STORE_TABLE']
        self.p2c = self.frame_settings['P2C_TABLE']

    def get_all_projects(self):
        sql = f'select `id` as `project_id`, `name`, `status`, `config`, `rate` ' \
              f'from {self.project_table} where `type`= "spider"'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql)

    def get_all_codes(self):
        sql = f'select `id` as `code_id`, `content` from {self.code_table}'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql)

    def get_all_workers(self, ip):
        sql = f'select `id` as `worker_id`, `name`, `type`, `coroutine_num` ' \
              f'from {self.worker_table} where `ip` = "{ip}" and `status` = 1;'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql)

    def add_node(self, data):
        sql, values = prepare_insert_sql(self.node_table, data, auto_update=True)
        log.debug(f'SQL:{sql} {values}')
        return self.handler.insert(sql, values)

    def delete_node(self, node_id, get_sql=False):
        """a common delete func"""
        sql = f"delete from {self.node_table} where `id`={node_id};"
        log.debug(f'SQL:{sql}')
        if get_sql:
            return sql,
        return self.handler.delete(sql)

    def delete_worker_by_id(self, worker_id, get_sql=False):
        sql = f"delete from {self.worker_table} where `id` = '{worker_id}';"
        log.debug(f'SQL:{sql}')
        if get_sql:
            return sql,
        return self.handler.delete(sql)

    def delete_worker_by_ip(self, node_ip , get_sql=False):
        sql = f"delete from {self.worker_table} where `ip` = '{node_ip}';"
        log.debug(f'SQL:{sql}')
        if get_sql:
            return sql,
        return self.handler.delete(sql)

    def update_node(self, node_id, data, get_sql=False):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.node_table} set {fields} where `id` = {node_id};"
        log.debug(f'SQL:{sql}')
        if get_sql:
            return sql, values
        return self.handler.update(sql, values)

    def get_node(self, node_id):
        sql = f'select `id`, `ip`, `name`, `description`, `create_time`, `update_time` ' \
              f'from {self.node_table} where `id`={node_id}'
        log.debug(f'SQL:{sql}')
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
        log.debug(f'SQL:{sql}')
        if get_sql:
            return sql, values
        return self.handler.insert(sql, values)

    def update_worker(self, worker_id, data, get_sql=False):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.worker_table} set {fields} where `id` = {worker_id};"
        log.debug(f'SQL:{sql}')
        if get_sql:
            return sql, values
        return self.handler.update(sql, values)

    def get_worker(self, worker_id):
        sql = f'select `id`, `ip`, `name`, `type`, `description`, `coroutine_num`, `status`, `create_time`, `update_time` from {self.worker_table} where `id`={worker_id};'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql)

    def get_workers(self, page, limit, search, sort):
        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `ip`, `name`, `type`, `description`, `coroutine_num`, `status`, `create_time`, `update_time` ' \
                  f'from {self.worker_table} where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `ip`, `name`, `type`, `description`, `coroutine_num`, `status`, `create_time`, `update_time` ' \
                  f'from {self.worker_table} order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql), self.total_num(search, self.worker_table)
