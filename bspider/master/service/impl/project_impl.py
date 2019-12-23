from bspider.config.default_settings import EXCHANGE_NAME
from bspider.core.api import BaseImpl
from bspider.utils.rabbitMQ import RabbitMQClient
from bspider.master import log


class ProjectImpl(BaseImpl):

    def __init__(self):
        self.__mq_client = RabbitMQClient(self.frame_settings['RABBITMQ_CONFIG'])

    def get_project(self, project_id):
        sql = f'select `id`, `name`, `status`, `type`, `group`, `description`, `editor`, `rate`, `config`, `create_time`, `update_time` ' \
              f'from {self.project_table} where `id`="{project_id}";'
        return self.mysql_client.select(sql)

    def get_projects(self, page, limit, search, sort):
        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `name`, `status`, `type`, `group`, `description`, `editor`, `rate`, `create_time`, `update_time` ' \
                  f'from {self.project_table} where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `name`, `status`, `type`, `group`, `description`, `editor`, `rate`, `create_time`, `update_time` ' \
                  f'from {self.project_table} order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql), self.total_num(search, self.code_table)

    def add_project(self, data):
        fields, values = self.make_fv(data)
        sql = f"insert into {self.project_table} set {fields};"
        return sql, values

    def delete_project_binds(self, project_id):
        sql = f'delete from {self.p2c_table} where `project_id`={project_id};'
        return sql,

    def delete_job(self, project_id: int):
        sql = f"update {self.cron_table} set `status`=%s where `project_id` = '{project_id}';"
        log.debug(f'SQL:{sql}')
        return sql, (3)

    def add_project_binds(self, cids, pid):
        values = ', '.join([f'({pid}, {cid})' for cid in cids])
        sql = f'replace into `{self.p2c_table}`(`project_id`, `customcode_id`) ' \
              f'values{values};'
        log.debug(sql)
        return sql,

    def update_project(self, unique_value, data, unique_key='id'):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.project_table} set {fields} where `{unique_key}` = '{unique_value}';"
        return sql, values

    def get_middleware_by_code_name(self, code_names):
        """通过名称返回中间件的id 方便进行多对多绑定"""
        if code_names:
            cl = ', '.join(["'%s'" % code for code in code_names])
            sql = f'select `id`, `name` from {self.code_table} ' \
                  f'where `name` in ({cl}) and `type`="middleware"'
            return self.mysql_client.select(sql)
        return []

    def get_pipeline_by_code_name(self, code_names):
        """通过名称返回中间件的id 方便进行多对多绑定"""
        if len(code_names):
            cl = ', '.join(["'%s'" % code for code in code_names])
            sql = f'select `id`, `name` from {self.code_table} ' \
                  f'where `name` in ({cl}) and `type`="pipeline" or `type`="extractor"'
            return self.mysql_client.select(sql)
        return []

    def get_job_id_by_project_name(self, code_names):
        """通过名称返回定时任务的id 方便进行多对多绑定"""
        cl = ', '.join(["'%s'" % code for code in code_names])
        sql = f'select `id`, `name`, `description`, `type`, `content`, `editor` from {self.code_table} ' \
              f'where `name` in ({cl}) and `type`="crontask"'
        return self.mysql_client.select(sql)

    def show_bind_project_code(self, project_id):
        sql = f'SELECT `code`.`name` AS `code_name`,`code`.`type` AS `code_type` ' \
              f'FROM {self.code_table} AS `code` ' \
              f'LEFT JOIN bspider_project_customcode AS `p2c` ON `code`.`id` = `p2c`.`customcode_id` ' \
              f'WHERE `p2c`.`project_id` = {project_id};'
        return self.mysql_client.select(sql)

    def delete_project(self, project_id):
        sql = f'delete from {self.project_table} where `id`={project_id};'
        return sql,

    def bind_queue(self, project_id):
        for exchange in EXCHANGE_NAME:
            queue_name = '{}_{}'.format(exchange, project_id)
            self.__bind(exchange, queue_name, str(project_id))
        return True

    def __bind(self, exchange, queue_name, routing_key):
        self.__mq_client.exchange_declare(exchange)
        self.__mq_client.queue_declare(queue_name)
        self.__mq_client.queue_bind(queue_name, exchange, routing_key)

    def unbind_queue(self, project_id):
        for exchange in EXCHANGE_NAME:
            res = self.__mq_client.queue_delete(queue=f'{exchange}_{project_id}')
            log.debug(f'delete queue: {exchange}_{project_id} => res:{res}')
        return True

    def get_nodes(self):
        sql = f'select `ip` from {self.node_table} where `status` = 1'
        return [info['ip'] for info in self.mysql_client.select(sql)]
