"""
定时任务子模块
# 会初始化一个定时任务句柄
提供对定时任务的基本操作
-- 这里采用额外开启一个线程来控制整个定时任务模块
-- 考虑到多核cpu和一些 cpu密集型程序，
-- 这里采用 多线程的方式执行定时任务
"""
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger
from apscheduler.util import datetime_to_utc_timestamp, obj_to_ref, utc_timestamp_to_datetime
from pymysql import IntegrityError

from bspider.core.api import BaseService, Conflict, PostSuccess, PatchSuccess, DeleteSuccess, GetSuccess, NotFound, \
    ParameterException
from bspider.bcron.todo import do
from bspider.master import log
from bspider.master.service.impl.cron_impl import CronImpl
from bspider.utils.tools import get_crontab_next_run_time


class CronService(BaseService):

    def __init__(self):
        self.impl = CronImpl()

    def add_cron(self, project_id, code_id, cron_type, trigger, description):
        timestamp, next_run_time = get_crontab_next_run_time(trigger, self.tz)
        value = {
            'project_id': project_id,
            'code_id': code_id,
            'type': cron_type,
            'trigger': trigger,
            'trigger_type': 'cron',
            'func': obj_to_ref(do),
            'executor': 'thread_pool',
            'description': description,
            'next_run_time': timestamp,
        }
        try:
            cron_id = self.impl.add_job(data=value)
            log.info(f'cron job->project_id:{project_id}-code_id:{code_id} add success')
            return PostSuccess(msg='add cron job success', data={'cron_id': cron_id})
        except IntegrityError:
            log.error(f'cron job->project_id:{project_id}-code_id:{code_id} is already exist')
            return Conflict(msg='cron job is already exist', errno=50001)

    def update_job(self, cron_id, changes):
        self.impl.update_job(cron_id, changes)
        log.info(f'update cron job->cron_id:{cron_id}->{changes} success')
        return PatchSuccess(msg=f'cron job update success')

    def delete_job(self, cron_id):
        self.impl.delete_job(cron_id)
        log.info(f'delete cron job->cron_id:{cron_id} success')
        return DeleteSuccess()

    def get_job(self, cron_id):
        infos = self.impl.get_job(cron_id)

        for info in infos:
            info['next_run_time'] = utc_timestamp_to_datetime(info['next_run_time']).astimezone(self.tz)
            self.datetime_to_str(info)

        if len(infos):
            return GetSuccess(msg='get cron job success', data=infos[0])
        return NotFound(msg='job is not exist', errno=50001)

    def get_jobs(self, page, limit, search, sort):
        if sort.upper() not in ['ASC', 'DESC']:
            return ParameterException(msg='sort must `asc` or `desc`')

        infos, total = self.impl.get_jobs(page, limit, search, sort)

        for info in infos:
            info['next_run_time'] = utc_timestamp_to_datetime(info['next_run_time']).astimezone(self.tz)
            self.datetime_to_str(info)

        return GetSuccess(
            msg='get cron job list success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })
