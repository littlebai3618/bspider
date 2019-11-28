# @Time    : 2019/6/19 2:36 PM
# @Author  : 白尚林
# @File    : user_impl
# @Use     :
from bspider.core.api import BaseImpl
from bspider.master import log


class UserImpl(BaseImpl):

    def get_user(self, id):
        """暂时先这样，后面增加复杂密码验证"""
        sql = f'select `id`, `identity`, `username`, `password`, `role`, `email`, `phone`, `status`, `create_time`, `update_time` ' \
              f'from {self.user_table} where `identity`=%s;'
        return self.handler.select(sql, id)

    def get_user_by_id(self, id):
        """暂时先这样，后面增加复杂密码验证"""
        sql = f'select `id`, `identity`, `username`, `role`, `email`, `phone`, `status`, `create_time`, `update_time`  ' \
              f'from {self.user_table} where `id`=%s;'
        return self.handler.select(sql, id)

    def add_user(self, data):
        fields, values = self.make_fv(data)
        sql = f'insert into {self.user_table} set {fields};'
        return self.handler.insert(sql, values, lastrowid=True)

    def remove_user(self, user_id):
        sql = f"update {self.user_table} set `status`=-1 where `id` = '{user_id}';"
        return self.handler.update(sql)

    def update_user(self, user_id, data):
        fields, values = self.make_fv(data)
        sql = f"update {self.user_table} set {fields} where `id` = '{user_id}';"
        return self.handler.update(sql, values)

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
        return self.handler.select(sql), self.total_num(search, self.user_table)
