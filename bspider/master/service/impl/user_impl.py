from bspider.core.api import BaseImpl
from bspider.master import log


class UserImpl(BaseImpl):

    def get_user(self, identity: str):
        sql = f'select `id`, `identity`, `username`, `password`, `role`, `email`, `phone`, `status`, `create_time`, `update_time` ' \
              f'from {self.user_table} where `identity`=%s;'
        return self.mysql_client.select(sql, identity)

    def get_user_by_id(self, user_id: int):
        sql = f'select `id`, `identity`, `username`, `role`, `email`, `phone`, `status`, `create_time`, `update_time` ' \
              f'from {self.user_table} where `id`=%s;'
        return self.mysql_client.select(sql, user_id)

    def add_user(self, data):
        fields, values = self.make_fv(data)
        sql = f'insert into {self.user_table} set {fields};'
        return self.mysql_client.insert(sql, values, lastrowid=True)

    def remove_user(self, user_id):
        sql = f"update {self.user_table} set `status`=-1 where `id` = '{user_id}';"
        return self.mysql_client.update(sql)

    def update_user(self, user_id, data):
        fields, values = self.make_fv(data)
        sql = f"update {self.user_table} set {fields} where `id` = '{user_id}';"
        return self.mysql_client.update(sql, values)

    def get_users(self, page, limit, search, sort):
        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `identity`, `username`, `password`, `role`, `email`, `phone`, `status`, `create_time`, `update_time` ' \
                  f'from {self.user_table} where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `identity`, `username`, `password`, `role`, `email`, `phone`, `status`, `create_time`, `update_time` ' \
                  f'from {self.user_table} order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql), self.total_num(search, self.user_table)
