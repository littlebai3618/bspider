# @Time    : 2019/6/18 1:22 PM
# @Author  : 白尚林
# @File    : cron_job_impl
# @Use     :
"""
这里
"""

from core.api import BaseImpl
from core.lib import CRON_JOB_STORE_TABLE


class CronJobImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.table_name = CRON_JOB_STORE_TABLE

    def add_job(self, data):
        data['status'] = 1
        fields, values = self.make_fv(data)
        sql = f"insert into {self.table_name} set {fields}"
        return self.handler.insert(sql, values, lastrowid=True)

    def update_job(self, job_id, data):
        data['status'] = 2
        fields, values = self.make_fv(data)
        sql = f"update {self.table_name} set {fields} where `id` = '{job_id}';"
        return self.handler.update(sql, values)

    def get_job(self, job_id):
        sql = f'SELECT `cronjob`.`id`,`cronjob`.`project_name`,`project`.`id` AS `project_id`,' \
              f'`cronjob`.`class_name`,`code`.`id` AS `code_id`,`cronjob`.`trigger`,`cronjob`.`trigger_type`,' \
              f'`cronjob`.`description`,`cronjob`.`next_run_time` ' \
              f'FROM {self.table_name} AS `cronjob` ' \
              f'LEFT JOIN bspider_project AS `project` ON `cronjob`.`project_name`=`project`.`name` ' \
              f'LEFT JOIN bspider_customcode AS `code` ON `cronjob`.`class_name`=`code`.`name` ' \
              f'where `cronjob`.`id`={job_id};'
        return self.handler.select(sql)

    def get_jobs(self):
        sql = f'SELECT `cronjob`.`id`,`cronjob`.`project_name`,`project`.`id` AS `project_id`,' \
              f'`cronjob`.`class_name`,`code`.`id` AS `code_id`,`cronjob`.`trigger`,`cronjob`.`trigger_type`,' \
              f'`cronjob`.`description`,`cronjob`.`next_run_time` ' \
              f'FROM {self.table_name} AS `cronjob` ' \
              f'LEFT JOIN bspider_project AS `project` ON `cronjob`.`project_name`=`project`.`name` ' \
              f'LEFT JOIN bspider_customcode AS `code` ON `cronjob`.`class_name`=`code`.`name`;'
        return self.handler.select(sql)

    def delete_job(self, job_id):
        sql = f"update {self.table_name} set `status`=%s where `id` = '{job_id}';"
        return self.handler.update(sql, (3))



