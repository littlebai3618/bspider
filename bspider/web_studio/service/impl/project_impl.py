# @Time    : 2019/6/21 10:32 AM
# @Author  : 白尚林
# @File    : project_impl
# @Use     :
from bspider.config.default_settings import EXCHANGE_NAME
from bspider.core.api import BaseImpl
from bspider.utils.rabbitMQ import RabbitMQHandler


class ProjectImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.project_table = self.frame_settings['PROJECT_TABLE']
        self.code_table = self.frame_settings['CODE_STORE_TABLE']
        self.cron_table = self.frame_settings['CRON_JOB_STORE_TABLE']
        self.node_table = self.frame_settings['NODE_TABLE']
        self.p2c_table = self.frame_settings['P2C_TABLE']
        self.__mq_handler = RabbitMQHandler(self.frame_settings['RABBITMQ_CONFIG'])

    def get_project(self, project_id):
        sql = f'select `id`, `name`, `status`, `type`, `group`, ' \
              f'`description`, `editor`, `rate`, `config` from {self.project_table} ' \
              f'where `id`="{project_id}"'
        return self.handler.select(sql)

    def get_projects(self):
        sql = f'select `id`, `name`, `status`, `type`, `group`, ' \
              f'`description`, `editor`, `rate` from {self.project_table} where status != -1'
        return self.handler.select(sql)

    def add_project(self, data):
        fields, values = self.make_fv(data)
        sql = f"insert into {self.project_table} set {fields};"
        return sql, values

    def add_cron(self, data):
        fields, values = self.make_fv(data)
        sql = f"insert into {self.cron_table} set {fields};"
        return sql, values

    def add_code(self, data):
        fields, values = self.make_fv(data)
        sql = f"insert into {self.code_table} set {fields};"
        return sql, values

    def delete_project_binds(self, project_id):
        sql = f'delete from {self.p2c_table} where `project_id`={project_id};'
        return sql

    def add_project_binds(self, cids, pid):
        values = ', '.join([f'({pid}, {cid})' for cid in cids])
        sql = f'insert into {self.p2c_table}(`project_id`, `customcode_id`)' \
              f' values {values};'
        return sql

    def update_project(self, unique_value, data, unique_key='id'):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.project_table} set {fields} where `{unique_key}` = '{unique_value}';"
        return sql, values

    def get_middlewares_by_code_name(self, code_names):
        """通过名称返回中间件的id 方便进行多对多绑定"""
        if code_names:
            cl = ', '.join(["'%s'" % code for code in code_names])
            sql = f'select `id`, `name`, `content` from {self.code_table} ' \
                  f'where `name` in ({cl}) and `type`="middleware"'
            return self.handler.select(sql)
        return []

    def get_pipeline_by_code_name(self, code_names):
        """通过名称返回中间件的id 方便进行多对多绑定"""
        if len(code_names):
            cl = ', '.join(["'%s'" % code for code in code_names])
            sql = f'select `id`, `name`, `content` from {self.code_table} ' \
                  f'where `name` in ({cl}) and `type`="pipeline"'
            return self.handler.select(sql)
        return []

    def get_job_id_by_project_name(self, code_names):
        """通过名称返回定时任务的id 方便进行多对多绑定"""
        cl = ', '.join(["'%s'" % code for code in code_names])
        sql = f'select `id`, `name`, `description`, `type`, `content`, `editor` from {self.code_table} ' \
              f'where `name` in ({cl}) and `type`="crontask"'
        return self.handler.select(sql)

    def show_bind_project_code(self, project_id):
        sql = f'SELECT `code`.`name` AS `code_name`,`code`.`type` AS `code_type` ' \
              f'FROM {self.code_table} AS `code` ' \
              f'LEFT JOIN bspider_project_customcode AS `p2c` ON `code`.`id` = `p2c`.`customcode_id` ' \
              f'WHERE `p2c`.`project_id` = {project_id};'
        return self.handler.select(sql)

    def delete_project(self, project_id):
        sql = f'delete from {self.project_table} where `project_id`={project_id};'
        return sql

    def bind_queue(self, project_name):
        for exchange in EXCHANGE_NAME:
            queue_name = '{}_{}'.format(exchange, project_name)
            self.__bind(exchange, queue_name, project_name)
        return True

    def __bind(self, exchange, queue_name, routing_key):
        self.__mq_handler.declare_exchange(exchange)
        self.__mq_handler.declare_queue(queue_name)
        self.__mq_handler.bind_queue(queue_name, exchange, routing_key)

    def unbind_queue(self, project_id):
        project_name = self.get_project(project_id)
        if not len(project_name):
            return False
        project_name = project_name[0]['name']
        for exchange in EXCHANGE_NAME:
            queue_name = '{}_{}'.format(exchange, project_name)
            self.__mq_handler.remove_queue(queue=queue_name)
        return True

    def get_nodes(self):
        sql = f'select `ip`, `name` from {self.node_table} '
        return [info['ip'] for info in self.handler.select(sql)]
