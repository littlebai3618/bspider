# @Time    : 2019/7/5 5:54 PM
# @Author  : 白尚林
# @File    : base_monitor
# @Use     :
import asyncio
import json
import random

from core.lib.broker import RabbitMQBroker
from core.lib.project_cache import ProjectCache


class BaseMonitor(object):
    exchange = ''

    def __init__(self, log):
        """
        :param downloader_tag: 一个下载器的唯一标识，不能和其他下载器一致
        """
        self.log = log
        self.__cache = ProjectCache()
        self.__mq_handler = RabbitMQBroker(log).mq_handler
        self.projects = dict()
        self.__weight = None
        self.__total_sum = 0

    async def sync_config(self):
        """从cache 同步任务数据"""
        while True:
            try:
                await self.__sync_config()
            except Exception as e:
                self.log.error(f'sync project failed:{e}')
            await asyncio.sleep(2)

    async def __sync_config(self):
        tmp_projects = dict()
        tmp_weight = dict()
        projects = self.__cache.get_projects()
        total_sum = 0

        while len(projects):
            info = projects.pop()
            if await self.__mq_handler.get_queue_message_count(
                    queue='{}_{}'.format(self.exchange, info['project_name'])):
                tmp_weight[info['project_name']] = info['rate']
                total_sum += info['rate']

            project_obj = self.projects.get(info['project_name'])
            if project_obj is None or project_obj.sign != info['timestamp']:
                tmp_projects[info['project_name']] = self.get_work_obj(info['project_name'], json.loads(info['config']),
                                                                       sign=info['timestamp'])
            else:
                tmp_projects[info['project_name']] = project_obj

        self.projects = tmp_projects
        self.log.info('sync projects success {}'.format(len(self.projects)))
        self.__weight = sorted(tmp_weight.items(), key=lambda d: d[1], reverse=False)
        self.__total_sum = total_sum
        self.log.info('sync weight success {} total num {}'.format(len(self.__weight), self.__total_sum))

    async def choice_project(self) -> str:
        """
        # 根据project的权重值随机选取一个
        :param weight: list对应的权重序列
        :return:选取的值在原列表里的索引
        """
        if self.__weight is not None and self.__total_sum:
            seed = random.randint(0, self.__total_sum - 1)
            for project_name, weight in self.__weight:
                seed -= weight
                if seed < 0:
                    self.log.debug(f'choice project {project_name}')
                    return project_name
        self.log.debug('project weight is empty')

    def get_work_obj(self, project_name: str, config: dict, sign: str):
        """继承重写 -> 根据配置返回对象"""
        pass

    def close(self):
        del self.__cache
