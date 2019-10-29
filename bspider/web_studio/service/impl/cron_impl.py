# @Time    : 2019/6/18 1:22 PM
# @Author  : 白尚林
# @File    : cron_job_impl
# @Use     :
from bspider.core.api import BaseImpl
from bspider.web_studio import log


class CronImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.table_name = self.frame_settings['CRON_JOB_STORE_TABLE']

    def add_job(self, data: dict) -> int:
        data['status'] = 1
        fields, values = self.make_fv(data)
        sql = f"insert into {self.table_name} set {fields}"
        log.debug(f'SQL:{sql}')
        return self.handler.insert(sql, values, lastrowid=True)

    def update_job(self, job_id: int, data: dict) -> int:
        data['status'] = 2
        fields, values = self.make_fv(data)
        sql = f"update {self.table_name} set {fields} where `id` = '{job_id}';"
        log.debug(f'SQL:{sql}')
        return self.handler.update(sql, values)

    def get_job(self, job_id: int) -> list:
        sql = f'select `id`, `project_id`, `code_id`, `type`, `trigger`, `trigger_type`, `next_run_time`, ' \
              f'`description`, `create_time`, `update_time` ' \
              f'from `{self.table_name}` where `id`={job_id};'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql)

    def get_jobs(self, page: int, limit: int, search: str, sort: str) -> list:

        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `project_id`, `code_id`, `type`, `trigger`, `trigger_type`, `next_run_time`, ' \
                  f'`description`, `create_time`, `update_time` ' \
                  f'from `{self.table_name}` ' \
                  f'where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `project_id`, `code_id`, `type`, `trigger`, `trigger_type`, `next_run_time`, ' \
                  f'`description`, `create_time`, `update_time` ' \
                  f'from `{self.table_name}` ' \
                  f'order by `cronjob`.`id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.handler.select(sql), self.total_num(search, self.table_name)

    def delete_job(self, job_id: int) -> int:
        sql = f"update {self.table_name} set `status`=%s where `id` = '{job_id}';"
        log.debug(f'SQL:{sql}')
        return self.handler.update(sql, (3))



