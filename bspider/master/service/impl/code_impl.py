from bspider.core.api import BaseImpl
from bspider.master import log


class CodeImpl(BaseImpl):

    def add_code(self, data, get_sql=True):
        return self.insert(data, self.code_table, lastrowid=True, get_sql=get_sql)

    def get_project_by_code_id(self, cid):
        sql = f'SELECT `p2c`.`project_id` AS `id`, `project`.`name` AS `name` FROM {self.project_table} AS `project` ' \
              f'LEFT JOIN {self.p2c_table} AS `p2c` ON `project`.`id`=`p2c`.`project_id` ' \
              f'WHERE `p2c`.`customcode_id`={cid};'
        return self.mysql_client.select(sql)

    def update_code(self, code_id: int, data: dict, get_sql=True):
        return self.update('id', code_id, data, self.data_source_table, get_sql)
    
    def delete_code(self, code_id: int):
        return self.delete('id', code_id, self.code_table, False)

    def get_code(self, code_id):
        sql = f'SELECT `project`.`name` AS `project_name`,`project`.`id` AS `project_id`,' \
              f'`code`.`name` AS `name`,`code`.`id` AS `id`,`code`.`type`,' \
              f'`code`.`description`,`code`.`content`,`code`.`editor` ' \
              f'FROM {self.code_table} AS `code` ' \
              f'LEFT JOIN {self.p2c_table} AS `p2c` ON `code`.`id`=`p2c`.`customcode_id` ' \
              f'LEFT JOIN {self.project_table} AS `project` ON `project`.`id`=`p2c`.`project_id` ' \
              f'WHERE `code`.`id`={code_id}'
        return self.mini_record(self.mysql_client.select(sql))

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
