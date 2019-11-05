# @Time    : 2019/6/18 11:40 AM
# @Author  : baii
# @File    : work
# @Use     :
"""
解决 gunicorn + Flask 启动多次实例化APSchedule导致定时任务多次执行的bug

这里采用单独进程处理任务调度
"""
import sys
import time
import traceback

import pytz
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger

from bspider.config import FrameSettings
from bspider.bcron import do
from bspider.bcron.jobstore import MySQLJobStore
from bspider.bcron.scheduler import MySQLScheduler
from bspider.utils.logger import LoggerPool
from bspider.utils.database.mysql import MysqlHandler

def run_bcorn():
    """A factory to make a download process"""
    dm = BCronManager()
    dm.run()


class BCronManager(object):

    def __init__(self):
        self.frame_settings = FrameSettings()
        self.log = LoggerPool().get_logger(key='bcorn_manager', module='bcorn')
        self.handler = MysqlHandler.from_settings(self.frame_settings['WEB_STUDIO_DB'])
        self.table_name = self.frame_settings['CRON_JOB_STORE_TABLE']
        self.tz = pytz.timezone(self.frame_settings['TIMEZONE'])
        self.interval = self.frame_settings['CRON_JOB_REFRESH_TIME']

        store = MySQLJobStore(self.handler, self.tz, self.log, self.table_name)

        executors = {
            'thread_pool': ThreadPoolExecutor(self.frame_settings['CRON_JOB_THREAD_NUM'])
            # 'processpool': ProcessPoolExecutor(frame_settings.CRON_JOB_PROCESS_NUM)
        }
        self.log.debug(
            'success make executors, process num: {} thread num:{}'.format(self.frame_settings['CRON_JOB_PROCESS_NUM'],
                                                                           self.frame_settings['CRON_JOB_THREAD_NUM']))

        self.scheduler = MySQLScheduler(
            jobstores={'default': store},
            executors=executors,
            timezone=self.tz
        )
        # 之前检查的时间
        self.pre_time = self.get_now()

    def get_now(self):
        return datetime.now(self.tz).strftime("%Y-%m-%d %H:%M:%S.%f")

    def check_change(self):

        sql = f'select `id`, `project_id`, `code_id`, `trigger`, `trigger_type`, ' \
              f'`description`, `next_run_time`, `status` from {self.table_name} ' \
              f'where update_time >= date_sub(now(), interval {self.interval} second)         ' \
              f'and `status` != 0;'
        infos = self.handler.select(sql)

        for info in infos:
            if info['status'] == 1:
                self.real_add_job(info)
            elif info['status'] == 2:
                self.real_update_job(info)
            elif info['status'] == 3:
                self.real_remove_job(info['id'])

    def real_remove_job(self, job_id):
        self.scheduler.remove_job(job_id)
        self.log.info('remove job success!')

    def real_update_job(self, info):
        # 防止报错，先去掉trigger_type
        info.pop('trigger_type')
        info['name'] = '{project_id}-{code_id}'.format(**info)
        info['status'] = 0
        self.scheduler.modify_job(
            job_id=info.pop('id'),
            change=info
        )

    def real_add_job(self, info):
        name = '{project_id}-{code_id}'.format(**info)
        cron = CronTrigger.from_crontab(info['trigger'])
        now = datetime.now(self.tz)
        next_run_time = cron.get_next_fire_time(None, now)
        try:
            self.scheduler.add_job(
                do, cron, name=name,
                kwargs={'project_id': info['project_id'], 'code_id': info['code_id'], 'type': info['type']},
                description=info['description'],
                next_run_time=next_run_time,
                id=info['id']
            )
        except Exception as e:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            self.log.exception(e_msg)
            self.log.error(f'real add job failed: {name} {e} {info}')
            return
        self.log.info(f'success add job {name}, it run at {next_run_time}')

    def run(self):
        self.log.debug('success init scheduler!')
        self.scheduler.start()
        self.log.info('success start MySQLScheduler')
        # 每三秒检查一下定时任务是否有变化
        while True:
            self.check_change()
            time.sleep(self.interval)


if __name__ == '__main__':
    BCM = BCronManager()
    BCM.run()