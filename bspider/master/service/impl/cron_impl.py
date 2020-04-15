from bspider.core.api import BaseImpl
from bspider.master import log


class CronImpl(BaseImpl):

    def add_job(self, data: dict) -> int:
        data['status'] = 1
        fields, values = self.make_fv(data)
        sql = f"insert into {self.cron_table} set {fields}"
        log.debug(f'SQL:{sql}')
        return self.mysql_client.insert(sql, values, lastrowid=True)

    def update_job(self, job_id: int, data: dict) -> int:
        data['status'] = 2
        fields, values = self.make_fv(data)
        sql = f"update {self.cron_table} set {fields} where `id` = '{job_id}';"
        log.debug(f'SQL:{sql}')
        return self.mysql_client.update(sql, values)

    def get_job(self, job_id: int) -> list:
        sql = f'select `id`, `project_id`, `code_id`, `type`, `trigger`, `trigger_type`, `next_run_time`, ' \
              f'`description`, `create_time`, `update_time` ' \
              f'from `{self.cron_table}` where `id`={job_id};'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql)

    def get_jobs(self, page: int, limit: int, search: str, sort: str) -> (list, int):

        start = (page - 1) * limit
        fields = self.make_search(search)
        if len(fields):
            sql = f'select `id`, `project_id`, `code_id`, `type`, `trigger`, `trigger_type`, `next_run_time`, ' \
                  f'`description`, `create_time`, `update_time` ' \
                  f'from `{self.cron_table}` ' \
                  f'where {fields} order by `id` {sort} limit {start},{limit};'
        else:
            sql = f'select `id`, `project_id`, `code_id`, `type`, `trigger`, `trigger_type`, `next_run_time`, ' \
                  f'`description`, `create_time`, `update_time` ' \
                  f'from `{self.cron_table}` ' \
                  f'order by `id` {sort} limit {start},{limit};'
        log.debug(f'SQL:{sql}')
        return self.mysql_client.select(sql), self.total_num(search, self.cron_table)

    def delete_job(self, job_id: int) -> int:
        sql = f"update {self.cron_table} set `status`=%s where `id` = '{job_id}';"
        log.debug(f'SQL:{sql}')
        return self.mysql_client.update(sql, (3))
