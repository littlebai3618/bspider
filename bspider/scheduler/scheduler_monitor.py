# @Time    : 2019/7/5 6:20 PM
# @Author  : 白尚林
# @File    : scheduler_monitor
# @Use     :
import asyncio
import sys
import traceback

from bspider.config import FrameSettings
from bspider.scheduler.scheduler import Scheduler
from bspider.utils.database.mysql import AioMysqlHandler
from bspider.utils.sign import Sign


class SchedulerMonitor(object):

    def __init__(self, log, log_fn):
        self.frame_settings = FrameSettings()
        self.project_table = self.frame_settings['PROJECT_TABLE']
        self.__mysql_handler = AioMysqlHandler.from_settings(self.frame_settings['WEB_STUDIO_DB'])
        self.projects = {}
        self.log = log
        self.log_fn = log_fn

    async def get_projects(self):
        sql = f'select `id`, `name`, `rate` from {self.project_table} where `status`=1'
        return await self.__mysql_handler.select(sql)

    async def sync_config(self):
        while True:
            self.log.info('start sync project!')
            tmp_projects = dict()
            try:
                for info in await self.get_projects():
                    project_obj = self.projects.get(info['id'])
                    cur_sign = Sign(project_name=info['name'], project_id=info['id'], rate=info['rate'])
                    if project_obj is None or project_obj.sign != cur_sign:
                        tmp_projects[info['id']] = self.get_work_obj(
                            info['id'], info['name'], rate=info['rate'], sign=cur_sign)
                    else:
                        tmp_projects[info['id']] = project_obj
                self.projects = tmp_projects
                self.log.info('sync project success with {} projects'.format(len(self.projects)))
            except Exception as e:
                tp, msg, tb = sys.exc_info()
                e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                self.log.error(f'server exec:{e_msg}')
                self.log.error(f'sync project rate error:{e}')
            await asyncio.sleep(4)

    def get_work_obj(self, project_id, project_name: str, rate: int, sign: Sign):
        return Scheduler(project_id, project_name, rate, sign, self.log_fn)



    def close(self):
        pass
