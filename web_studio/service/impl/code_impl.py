# @Time    : 2019/6/21 10:49 AM
# @Author  : 白尚林
# @File    : code_impl
# @Use     :
from core.api import BaseImpl
from core.lib import NODE_TABLE, WORKER_TABLE, NODE_STATUS_TABLE, PROJECT_TABLE, CODE_STORE_TABLE, P2C_TABLE


class CodeImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.node_table = NODE_TABLE
        self.worker_table = WORKER_TABLE
        self.node_status_table = NODE_STATUS_TABLE
        self.project_table = PROJECT_TABLE
        self.code_table = CODE_STORE_TABLE
        self.p2c = P2C_TABLE

    def add_code(self, data):
        fields, values = self.make_fv(data)
        sql = f"insert into {self.code_table} set {fields};"
        return sql, values, True

    def get_nodes(self):
        sql = f'select `ip` from {self.node_table};'
        return [info['ip'] for info in self.handler.select(sql)]

    def get_project_by_code_id(self, cid):
        sql = f'SELECT `p2c`.`project_id` AS `id`, `project`.`name` AS `project_name` FROM {self.project_table} AS `project` ' \
            f'LEFT JOIN {self.p2c} AS `p2c` ON `project`.`id`=`p2c`.`project_id` ' \
            f'WHERE `p2c`.`customcode_id`={cid};'
        return self.handler.select(sql)

    def update_code(self, code_id, data):
        fields, values = self.make_fv(data)
        sql = f"update {self.code_table} set {fields} where `id` = {code_id};"
        return sql, values

    def delete_code(self, code_id):
        sql = f'delete from {self.code_table} where `id`={code_id};'
        return self.handler.delete(sql)

    def add_bind_project_code(self, binds):
        values = ', '.join([f'({pid}, {cid})' for pid, cid in binds])
        sql = f'insert into bspider_project_customcode(`project_id`, `customcode_id`)' \
            f' values {values};'
        return sql

    def show_bind_project_code(self, project_id):
        sql = f'SELECT `code`.`name` AS `code_name`,`code`.`type` AS `code_type` ' \
            f'FROM {self.table_name} AS `code` ' \
            f'LEFT JOIN bspider_project_customcode AS `p2c` ON `code`.`id` = `p2c`.`customcode_id` ' \
            f'WHERE `p2c`.`project_id` = {project_id};'
        return self.handler.select(sql)

    def get_code(self, code_id):
        sql = f'SELECT `project`.`name` AS `project_name`,`project`.`id` AS `project_id`,' \
            f'`code`.`name` AS `name`,`code`.`id` AS `id`,`code`.`type`,' \
            f'`code`.`description`,`code`.`content`,`code`.`editor` ' \
            f'FROM {self.code_table} AS `code` ' \
            f'LEFT JOIN bspider_project_customcode AS `p2c` ON `code`.`id`=`p2c`.`customcode_id` ' \
            f'LEFT JOIN bspider_project AS `project` ON `project`.`id`=`p2c`.`project_id` ' \
            f'WHERE `code`.`id`={code_id}'
        return self.handler.select(sql)

    def get_codes(self, **param):
        if len(param):
            fields, values = self.make_fv(param)
            fields = fields.replace(',', ' and ')
            sql = f'select `id`, `name`, `description`, `type`, `editor` from {self.code_table} where {fields}'
            return self.handler.select(sql, values)
        sql = f'select `id`, `name`, `description`, `type`, `editor` from {self.code_table} '
        return self.handler.select(sql)

    def get_code_by_type(self, code_type):
        sql = f'select `id`, `name`, `description`, `type`, `editor`, `content` ' \
            f'from {self.code_table} ' \
            f'where `type` = "{code_type}";'
        return self.handler.select(sql)
