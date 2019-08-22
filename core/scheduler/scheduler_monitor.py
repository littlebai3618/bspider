# @Time    : 2019/7/5 6:20 PM
# @Author  : 白尚林
# @File    : scheduler_monitor
# @Use     :
import asyncio
import random

from config import frame_settings
from core.lib import PROJECT_TABLE
from core.scheduler.scheduler import Scheduler
from util.database.mysql import AioMysqlHandler


class SchedulerMonitor(object):

    def __init__(self, log):
        """一个下载器的唯一标识，不能和其他下载器一致"""
        self.project_table = PROJECT_TABLE
        self.__mysql_handler = AioMysqlHandler.from_settings(frame_settings.WEB_STUDIO_DB)
        self.projects = {}
        self.log = log

    async def sync_config(self):
        while True:
            self.log.info('start sync project!')
            tmp_projects = dict()
            try:
                for info in await self.get_projects():
                    project_obj = self.projects.get(info['project_name'])
                    if project_obj is None or \
                            project_obj.sign != info['timestamp']:
                        tmp_projects[info['project_name']] = self.get_work_obj(project_name=info['project_name'],
                                                                               rate=info['rate'],
                                                                               sign=info['timestamp'])
                    else:
                        tmp_projects[info['project_name']] = project_obj
                self.projects = tmp_projects
                self.log.info('sync project success with {} projects'.format(len(self.projects)))
            except Exception as e:
                self.log.error(f'sync project rate error:{e}')
            await asyncio.sleep(4)

    async def choice_project(self) -> dict:
        """根据project的权重值随机选取一个"""
        if len(self.projects):
            self.log.info('project is empty')
            return {}
        return random.choice(self.projects)

    @staticmethod
    def get_work_obj(project_name: str, rate: int, sign: str):
        return Scheduler(project_name, rate, sign)

    async def get_projects(self):
        sql = f'select `name` as `project_name`,`rate`, `update_time` as `timestamp` ' \
            f'from {self.project_table} where `status`=1'
        return await self.__mysql_handler.select(sql)

    def close(self):
        pass
