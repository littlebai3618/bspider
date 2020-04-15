from bspider.core.api import BaseImpl
from bspider.master import log


class CodeImpl(BaseImpl):

    def add_code(self, data):
        fields, values = self.make_fv(data)
        sql = f"insert into {self.code_table} set {fields};"
        return sql, values, True

    def get_nodes(self):
        sql = f'select `ip` from {self.node_table} where `status` = 1;'
        return [info['ip'] for info in self.mysql_client.select(sql)]

    def get_project_by_code_id(self, cid):
        sql = f'SELECT `p2c`.`project_id` AS `id`, `project`.`name` AS `name` FROM {self.project_table} AS `project` ' \
              f'LEFT JOIN {self.p2c_table} AS `p2c` ON `project`.`id`=`p2c`.`project_id` ' \
              f'WHERE `p2c`.`customcode_id`={cid};'
        return self.mysql_client.select(sql)

    def update_code(self, code_id, data):
        fields, values = self.make_fv(data)
        sql = f"update {self.code_table} set {fields} where `id` = {code_id};"
        log.debug(f'SQL:{sql}, {values}')
        return sql, values

    def delete_code(self, code_id):
        sql = f'delete from {self.code_table} where `id`={code_id};'
        return sql, ()

    def show_bind_project_code(self, project_id):
        sql = f'SELECT `code`.`name` AS `code_name`,`code`.`type` AS `code_type` ' \
              f'FROM {self.table_name} AS `code` ' \
              f'LEFT JOIN bspider_project_customcode AS `p2c` ON `code`.`id` = `p2c`.`customcode_id` ' \
              f'WHERE `p2c`.`project_id` = {project_id};'
        return self.mysql_client.select(sql)

    def get_code(self, code_id):
        sql = f'SELECT `project`.`name` AS `project_name`,`project`.`id` AS `project_id`,' \
              f'`code`.`name` AS `name`,`code`.`id` AS `id`,`code`.`type`,' \
              f'`code`.`description`,`code`.`content`,`code`.`editor` ' \
              f'FROM {self.code_table} AS `code` ' \
              f'LEFT JOIN bspider_project_customcode AS `p2c` ON `code`.`id`=`p2c`.`customcode_id` ' \
              f'LEFT JOIN bspider_project AS `project` ON `project`.`id`=`p2c`.`project_id` ' \
              f'WHERE `code`.`id`={code_id}'
        return self.mysql_client.select(sql)

    def get_code_by_type(self, code_type):
        sql = f'select `id`, `name`, `description`, `type`, `editor`, `content` ' \
              f'from {self.code_table} ' \
              f'where `type` = "{code_type}";'
        return self.mysql_client.select(sql)

    def get_codes(self, page, limit, search, sort):
        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `name`, `description`, `type`, `editor`, `create_time`, `update_time` ' \
                  f'from {self.code_table} where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `name`, `description`, `type`, `editor`, `create_time`, `update_time` ' \
                  f'from {self.code_table} order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql), self.total_num(search, self.code_table)
