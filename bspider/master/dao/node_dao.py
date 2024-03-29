from bspider.core.api import BaseDao
from bspider.master import log
from bspider.utils.database.mysql import prepare_insert_sql


class NodeDao(BaseDao):

    def get_all_projects(self):
        sql = f'select `id` as `project_id`, `name`, `status`, `r_config` as `config`, `rate` ' \
              f'from {self.project_table} where `type`= "spider"'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql)

    def get_all_data_source(self):
        sql = f'select `name`, `type`, `param` ' \
              f'from {self.data_source_table} ' \
              f'where `status`= 1'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql)

    def get_all_codes(self):
        sql = f'select `id` as `code_id`, `content` from {self.code_table} where `type` in ("pipeline", "middleware", "extractor");'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql)

    def get_all_workers(self, ip):
        sql = f'select `id` as `worker_id`, `name`, `type`, `coroutine_num` ' \
              f'from {self.worker_table} where `ip` = "{ip}" and `status` = 1;'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql)

    def add_node(self, data):
        sql, values = prepare_insert_sql(self.node_table, data, auto_update=True)
        log.debug(f'SQL:{sql} {values}')
        return self.mysql_client.insert(sql, values)

    def delete_node(self, node_id: int, get_sql=False):
        return self.delete('id', node_id, self.node_table, get_sql)

    def delete_worker_by_id(self, worker_id: int, get_sql=False):
        return self.delete('id', worker_id, self.worker_table, get_sql)

    def delete_worker_by_ip(self, node_ip: str, get_sql=False):
        return self.delete('ip', node_ip, self.worker_table, get_sql)

    def update_node(self, node_id: int, data: dict, get_sql=False):
        return self.update('id', node_id, data, self.node_table, get_sql)

    def get_node(self, node_id):
        sql = f'select `id`, `ip`, `name`, `description`, `cpu_num`, ' \
              f'`mem_size`, `disk_size`, `status`, `port`, `create_time`, `update_time` ' \
              f'from {self.node_table} where `id`={node_id}'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql)

    def get_nodes(self, page, limit, search, sort):
        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `ip`, `name`, `description`, `cpu_num`, ' \
                  f'`mem_size`, `disk_size`, `status`, `port`, `create_time`, `update_time` ' \
                  f'from {self.node_table} where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `ip`, `name`, `description`, `cpu_num`, ' \
                  f'`mem_size`, `disk_size`, `status`, `port`, `create_time`, `update_time` ' \
                  f'from {self.node_table} order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql), self.total_num(search, self.node_table)

    def add_worker(self, data, get_sql=False):
        """注册一个节点"""
        fields, values = BaseImpl.make_fv(data)
        sql = f"insert into {self.worker_table} set {fields};"
        log.debug(f'SQL:{sql}')
        if get_sql:
            return sql, values
        return self.mysql_client.insert(sql, values)

    def update_worker(self, worker_id: int, data: dict, get_sql=False):
        return self.update('id', worker_id, data, self.worker_table, get_sql)

    def get_worker(self, worker_id):
        sql = f'select `id`, `ip`, `name`, `type`, `description`, `coroutine_num`, `status`, `create_time`, `update_time` from {self.worker_table} where `id`={worker_id};'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql)

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
        return self.mysql_client.select(sql), self.total_num(search, self.worker_table)
