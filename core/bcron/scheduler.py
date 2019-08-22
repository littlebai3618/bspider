# @Time    : 2019/6/15 4:28 PM
# @Author  : 白尚林
# @File    : scheduler
# @Use     : 定时任务调度器
"""
重写内置的调度器，增加信息回调方便封装api
"""
import six
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED
from apscheduler.util import undefined
from core.bcron.job import MySQLJob


class MySQLScheduler(BackgroundScheduler):

    def add_job(self, func, trigger=None, args=None, kwargs=None, id=None, name=None,
                misfire_grace_time=undefined, coalesce=undefined, max_instances=undefined,
                next_run_time=undefined, jobstore='default', executor='default', status=0,
                description='', replace_existing=False, **trigger_args):
        """
        新增了两个属性：
        :param status: 任务状态
        :param description: 任务描述
        :return: str callback msg
        """
        job_kwargs = {
            'trigger': self._create_trigger(trigger, trigger_args),
            'executor': executor,
            'func': func,
            'args': tuple(args) if args is not None else (),
            'kwargs': dict(kwargs) if kwargs is not None else {},
            'id': id,
            'name': name,
            'misfire_grace_time': misfire_grace_time,
            'coalesce': coalesce,
            'max_instances': max_instances,
            'next_run_time': next_run_time,
            # 新增两个属性
            'status': status,
            'description': description
        }
        job_kwargs = dict((key, value) for key, value in six.iteritems(job_kwargs) if
                          value is not undefined)
        job = MySQLJob(self, **job_kwargs)

        # Don't really add jobs to job stores before the scheduler is up and running
        with self._jobstores_lock:
            if self.state == STATE_STOPPED:
                self._pending_jobs.append((job, jobstore, replace_existing))
                self._logger.info('Adding job tentatively -- it will be properly scheduled when '
                                  'the scheduler starts')
            else:
                self._real_add_job(job, jobstore, replace_existing)

        return job

    def scheduled_job(self, trigger, args=None, kwargs=None, id=None, name=None,
                      misfire_grace_time=undefined, coalesce=undefined, max_instances=undefined,
                      next_run_time=undefined, jobstore='default', executor='default', status=0,
                      description='', **trigger_args):
        """
        新增了两个属性：
        :param status: 任务状态
        :param description: 任务描述
        :return: func
        """
        def inner(func):
            self.add_job(func, trigger, args, kwargs, id, name, misfire_grace_time, coalesce,
                         max_instances, next_run_time, jobstore, executor, status, description,
                         True, **trigger_args)
            return func
        return inner
