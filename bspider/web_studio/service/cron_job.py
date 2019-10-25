# @Time    : 2019/6/14 5:40 PM
# @Author  : 白尚林
# @File    : cron_job
# @Use     :
"""
定时任务子模块
# 会初始化一个定时任务句柄
提供对定时任务的基本操作
-- 这里采用额外开启一个线程来控制整个定时任务模块
-- 考虑到多核cpu和一些 cpu密集型程序，
-- 这里采用 多进程和 + 多线程的方式执行定时任务
"""
import json
from datetime import datetime

import pytz
from apscheduler.triggers.cron import CronTrigger
from apscheduler.util import datetime_to_utc_timestamp, obj_to_ref
from pymysql import IntegrityError

from bspider.core.api import BaseService, Conflict, PostSuccess, PatchSuccess, DeleteSuccess, GetSuccess, NotFound, \
    ParameterException
from bspider.bcron.todo import do
from bspider.web_studio import log
from bspider.web_studio.service.impl.cron_job_impl import CronJobImpl


class CronJobService(BaseService):

    def __init__(self):
        self.impl = CronJobImpl()
        self.tz = pytz.timezone(self.frame_settings['TIMEZONE'])

    def __next_run_time(self, trigger):
        """将crontab 表达式转换为 下次执行的UTC时间戳"""
        crontab = CronTrigger.from_crontab(trigger)
        now = datetime.now(self.tz)
        next_run_time = crontab.get_next_fire_time(None, now)
        return datetime_to_utc_timestamp(next_run_time), next_run_time

    def make_kwargs(self, project_name, class_name):
        kwargs = {'project_name': project_name, 'class_name': class_name}
        if project_name == 'operation':
            kwargs['pattern'] = project_name
        return json.dumps(kwargs)



    def add_job(self, project_id, project_name, class_name, trigger, description):
        timestamp, next_run_time = self.__next_run_time(trigger)
        value = {
            'project_id': project_id,
            'project_name': project_name,
            'class_name': class_name,
            'args': '[]',
            'kwargs': self.make_kwargs(project_name, class_name),
            'trigger': trigger,
            'trigger_type': 'cron',
            'func': obj_to_ref(do),
            'executor': 'default',
            'description': description,
            'next_run_time': timestamp,
        }
        try:
            job_id = self.impl.add_job(data=value)
            log.info(f'add cron_job:{project_name}-{class_name} success')
            return PostSuccess(msg='add cron job success', data={'job_id': job_id})
        except IntegrityError:
            log.error(f'cron job:{project_name}-{class_name} is already exist')
            return Conflict(msg='cron job is already exist', errno=50001)

    def update_job(self, job_id, project_name, **kwargs):
        if 'class_name' in kwargs:
            kwargs['kwargs'] = self.make_kwargs(project_name, kwargs.pop('class_name'))
        self.impl.update_job(job_id, kwargs)
        if 'trigger' in kwargs:
            timestamp, next_run_time = self.__next_run_time(kwargs['trigger'])
            return PatchSuccess(msg=f'update success next run at:{next_run_time}')
        log.info(f'update cron_job:{job_id} success')
        return PatchSuccess(msg=f'update success')

    def delete_job(self, job_id):
        self.impl.delete_job(job_id)
        log.info(f'delete cron_job:{job_id} success')
        return DeleteSuccess()

    def get_job(self, job_id):
        infos = self.impl.get_job(job_id)

        for info in infos:
            self.datetime_to_str(info)

        if len(infos):
            return GetSuccess(msg='get cron job success', data=infos)
        return NotFound(msg='job is not exist', errno=50001)

    def get_jobs(self, page, limit, search, sort):
        if sort.upper() not in ['ASC', 'DESC']:
            return ParameterException(msg='sort must `asc` or `desc`')

        infos, total = self.impl.get_jobs(page, limit, search, sort)

        for info in infos:
            self.datetime_to_str(info)

        return GetSuccess(
            msg='get cron job list success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })
