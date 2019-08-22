# @Time    : 2019/6/18 11:40 AM
# @Author  : 白尚林
# @File    : bcorn_manager
# @Use     :
"""
解决gunicorn + Flask 启动多次实例化APSchedule导致定时任务多次执行的bug

这里采用单独进程处理任务调度
"""
import time
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger

from config import frame_settings
from core.bcron.jobstore import MySQLJobStore
from core.bcron.scheduler import MySQLScheduler
from core.bcron.todo import do
from core.lib import CRON_JOB_STORE_TABLE, TZ
from util.logger.log_handler import LoggerPool
from util.database.mysql import MysqlHandler


class BCronManager(object):

    def __init__(self):
        self.log = LoggerPool().get_logger(key='bcorn', module='bcorn')
        self.handler = MysqlHandler.from_settings(frame_settings.WEB_STUDIO_DB)
        self.table_name = CRON_JOB_STORE_TABLE
        self.tz = TZ
        self.interval = frame_settings.CRON_JOB_REFRESH_TIME

        store = MySQLJobStore(self.handler, self.tz, self.log, self.table_name)

        executors = {
            'default': ThreadPoolExecutor(frame_settings.CRON_JOB_THREAD_NUM)
            # 'processpool': ProcessPoolExecutor(frame_settings.CRON_JOB_PROCESS_NUM)
        }
        self.log.debug(
            'success make executors, process num: {} thread num:{}'.format(
                frame_settings.CRON_JOB_THREAD_NUM, frame_settings.CRON_JOB_THREAD_NUM))

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

        sql = f'select `id`, `project_name`, `class_name`, `trigger`, `trigger_type`, ' \
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
        info.pop('trigger_type')
        project_name = info.pop('project_name')
        class_name = info.pop('class_name')
        info['name'] = f'{project_name}|{class_name}'
        info['status'] = 0
        self.scheduler.modify_job(
            job_id=info.pop('id'),
            change=info
        )

    def real_add_job(self, info):
        name = '{project_name}|{class_name}'.format(**info)
        cron = CronTrigger.from_crontab(info['trigger'])
        now = datetime.now(self.tz)
        next_run_time = cron.get_next_fire_time(None, now)
        try:
            self.scheduler.add_job(
                do, cron, name=name,
                kwargs={'project_name': info['project_name'], 'class_name': info['class_name']},
                description=info['description'],
                next_run_time=next_run_time,
                id=info['id']
            )
        except Exception as e:
            self.log.error(f'real add job failed: {name} {e}')
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

    # 新增是1 更新是2 删除是3









