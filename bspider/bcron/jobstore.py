import datetime
from apscheduler.jobstores.base import BaseJobStore, JobLookupError
from apscheduler.triggers.cron import CronTrigger

from apscheduler.util import utc_timestamp_to_datetime, datetime_to_utc_timestamp

from bspider.bcron.job import MySQLJob
from bspider.utils.database import MysqlClient


class MySQLJobStore(BaseJobStore):
    """
    Stores jobs in a database table using pymysql.
    if table doesn't exist in the database, you must build it by yourself.
    :param mysql_client: a pymysql conn obj
    :param str tablename: name of the table to store jobs in
    """

    TABLE_FIELDS = ('`id`', '`project_id`', '`code_id`', '`trigger`', '`trigger_type`', '`type`',
                    '`next_run_time`', '`executor`', '`func`', '`status`', '`description`')

    def __init__(self, mysql_client: MysqlClient, tz, log, table_name='bspider_cronjob'):
        super().__init__()
        # 重构获取一个mysql连接池
        self.mysql_client = mysql_client
        self.table_name = table_name
        self.tz = tz
        self.log = log

    def _reconstitute_job(self, job_state: dict) -> MySQLJob:
        """
        mysql返回的字典解析成 job对象
        :param job_state:
        :return:
        """
        job_state['jobstore'] = self
        job_state['name'] = '{project_id}-{code_id}'.format(**job_state)
        if job_state['trigger_type'] == 'cron':
            job_state['trigger'] = CronTrigger.from_crontab(job_state['trigger'])
        job_state['misfire_grace_time'] = None
        job_state['coalesce'] = True
        job_state['max_instances'] = 1
        job_state['args'] = []
        job_state['kwargs'] = {
            'project_id': job_state['project_id'],
            'code_id': job_state['code_id'],
            'type': job_state['type']
        }
        job_state['id'] = job_state['id']
        job_state['next_run_time'] = datetime.datetime.fromtimestamp(job_state['next_run_time'], self.tz)
        job = MySQLJob.__new__(MySQLJob)
        job.__setstate__(job_state)
        job._scheduler = self._scheduler
        job._jobstore_alias = self._alias
        return job

    def __make_fv(self, job: MySQLJob) -> tuple:
        fields = ','.join([' %s=%%s ' % (key) for key in self.TABLE_FIELDS])
        project_id, code_id = job.name.split('-')

        trigger_type = job.trigger.__str__().split('[')[0]

        if trigger_type == 'cron':
            options = {f.name: f.__str__() for f in job.trigger.fields if not f.is_default}
            trigger = '{minute} {hour} {day} {month} {day_of_week}'.format(**options)

        else:
            trigger = ''

        values = (job.id, project_id, code_id, trigger, trigger_type, job.cron_type,
                  job.next_run_time if isinstance(job.next_run_time, float) else datetime_to_utc_timestamp(job.next_run_time),
                  job.executor, job.func_ref, job.status, job.description)

        return (fields, values)

    def add_job(self, job: MySQLJob):
        """因为拆分问题，增加job 的操作交给API模块完成"""
        update = f"update {self.table_name} set `status`=%s where `id` = '{job.id}';"
        self.mysql_client.update(update, (0,))
        self.log.info(f'sync job:{job.name} success')

    def lookup_job(self, job_id):
        sql = f"select * from {self.table_name} where `id` = '{job_id}'"
        job_state = self.mysql_client.select(sql)
        return self._reconstitute_job(job_state[0]) if len(job_state) else None

    def get_due_jobs(self, now):
        timestamp = datetime_to_utc_timestamp(now)
        return self._get_jobs(timestamp)

    def get_next_run_time(self):
        selectable = f'select `next_run_time` from {self.table_name} ' \
            f'where `next_run_time` is not null ' \
            f'order by `next_run_time` limit 1'
        info = self.mysql_client.select(selectable)

        return utc_timestamp_to_datetime(info[0]['next_run_time']) if len(info) else None

    def get_all_jobs(self):
        jobs = self._get_jobs()
        self._fix_paused_jobs_sorting(jobs)
        return jobs

    def update_job(self, job: MySQLJob):
        fields, values = self.__make_fv(job)
        update = f"update {self.table_name} set {fields} where `id` = '{job.id}';"
        self.log.debug(update % values)
        result = self.mysql_client.update(update, values)
        if result == 0:
            self.log.debug(f'job: {job.name} is nothing to change！')
        else:
            self.log.debug(f'job: {job.name} is update success！')

    def remove_job(self, job_id):
        delete = f'DELETE FROM {self.table_name} WHERE `id` = {job_id};'
        result = self.mysql_client.delete(delete)
        if result == 0:
            raise JobLookupError(job_id)

    def remove_all_jobs(self):
        delete = f'DELETE FROM {self.table_name};'
        self.mysql_client.delete(delete)

    def shutdown(self):
        self.log.warning('mysql job store shutdown the conn pool!')

    def _get_jobs(self, timestamp=None):
        jobs = []
        failed_job_ids = set()
        fields = ','.join(self.TABLE_FIELDS)

        if timestamp:
            selectable = f'select {fields} from {self.table_name} ' \
                f'where `next_run_time` <= {timestamp}' \
                f'order by `next_run_time`;'
        else:
            selectable = f'select {fields} from {self.table_name} ' \
                f'order by `next_run_time`;'

        for row in self.mysql_client.select(selectable):
            try:
                jobs.append(self._reconstitute_job(row))
            except BaseException:
                self._logger.exception('unable to restore job "%s" -- removing it', row['id'])
                failed_job_ids.add(row['id'])
        return jobs

    def __repr__(self):
        return '<%s (engine=%s)>' % (self.__class__.__name__, 'MySQL')
