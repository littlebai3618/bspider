from bspider.core.api import BaseImpl
from bspider.master import log


class DataSourceImpl(BaseImpl):

    def add_data_source(self, data: dict, get_sql=True):
        return self.insert(data, self.data_source_table, lastrowid=True, get_sql=get_sql)

    def get_data_source(self, name: str) -> dict:
        # 根据data_source_id 获取数据源的使用情况
        sql = f'SELECT `project`.`name` AS `project_name`,`project`.`id` AS `project_id`,`data_source`.`name` AS `name`,`data_source`.`id` AS `id`,`data_source`.`type`,`data_source`.`description`,`data_source`.`param`,`data_source`.`status` ' \
              f'FROM {self.data_source_table} AS `data_source` ' \
              f'LEFT JOIN {self.p2ds_table} AS `p2ds` ON `data_source`.`id`=`p2ds`.`data_source_id` ' \
              f'LEFT JOIN {self.project_table} AS `project` ON `project`.`id`=`p2ds`.`project_id` ' \
              f'WHERE `data_source`.`name`=%s'

        return self.mini_record(self.mysql_client.select(sql, (name)))
    
    def get_data_sources(self, page, limit, search, sort):
        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `name`, `description`, `type`, `status`, `create_time`, `update_time` ' \
                  f'from {self.data_source_table} where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `name`, `description`, `type`, `status`, `create_time`, `update_time` ' \
                  f'from {self.data_source_table} order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql), self.total_num(search, self.data_source_table)


    def update_data_source(self, name: str, data: dict, get_sql=True):
        return self.update('name', name, data, self.data_source_table, get_sql)

    def get_project_by_data_source_name(self, name: str):
        sql = f'SELECT `p2ds`.`project_id` AS `id`, `project`.`name` AS `name` FROM {self.project_table} AS `project` ' \
              f'LEFT JOIN {self.p2ds_table} AS `p2ds` ON `project`.`id`=`p2c`.`project_id` ' \
              f'WHERE `p2c`.`data_source_name`=%s;'
        return self.mysql_client.select(sql, (name))

    def delete_data_source(self, name: str):
        return self.delete('name', name, self.data_source_table, False)
