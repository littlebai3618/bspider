import asyncio
import json
import random
import sys
import traceback

from bspider.config.default_settings import EXCHANGE_NAME
from bspider.utils.rabbitMQ import AioRabbitMQClient
from bspider.utils.sign import Sign
from bspider.utils.tools import find_class_name_by_content

from .agent_cache import AgentCache
from .project import Project


class BaseMonitor(object):
    exchange = ''

    def __init__(self, log, log_fn, mq_client: AioRabbitMQClient):
        self.log = log
        self.__cache = AgentCache()
        self.log.info(f'init cache success! {self.__cache}')
        self.mq_client = mq_client
        self.projects = dict()
        self.__weight = None
        self.__total_sum = 0
        self.log_fn = log_fn

    async def sync_config(self):
        """从cache 同步任务数据"""
        while True:
            try:
                await self.__sync_config()
            except Exception as e:
                tp, msg, tb = sys.exc_info()
                e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                self.log.error(f'sync project failed:{e_msg}')
                self.log.error(f'sync project failed:{e}')
            await asyncio.sleep(2)

    async def __sync_config(self):
        """
        如果不是第一次同步
        获取当前时间戳 -10s
        :return:
        """
        tmp_projects = dict()
        tmp_weight = dict()
        projects = self.__cache.get_projects()
        total_sum = 0

        while len(projects):
            info = projects.pop()
            if await self.mq_client.get_queue_message_count(queue='{}_{}'.format(self.exchange, info['id'])) != 0:
                tmp_weight[info['id']] = info['rate']
                total_sum += info['rate']

            worker_obj = self.projects.get(info['id'])
            if isinstance(info['config'], str):
                info['config'] = json.loads(info['config'])
            project = Project(
                settings=info['config'],
                pipeline_serializer_method=self.code_id_to_content,
                middleware_serializer_method=self.code_id_to_content
            )
            project.project_id = info['id']

            # code_id映射为中间件代码
            if self.exchange == EXCHANGE_NAME[2]:
                sign = Sign(project_timestamp=info['timestamp'], module=str(project.parser_settings.pipeline))
            else:
                sign = Sign(project_timestamp=info['timestamp'], module=str(project.downloader_settings.middleware))

            if worker_obj is None or worker_obj.sign != sign:
                tmp_projects[project.project_id] = self.get_work_obj(project, sign=sign)
            else:
                tmp_projects[info['id']] = worker_obj

        self.projects = tmp_projects
        self.log.debug('sync projects success {}'.format(len(self.projects)))
        self.__weight = sorted(tmp_weight.items(), key=lambda d: d[1], reverse=False)
        self.__total_sum = total_sum
        self.log.debug('sync weight success {} total num {}'.format(len(self.__weight), self.__total_sum))

    def choice_project(self) -> int:
        """
        # 根据project的权重值随机选取一个
        :return:选取的值在原列表里的索引
        """
        if self.__weight is not None and self.__total_sum:
            seed = random.randint(0, self.__total_sum - 1)
            for project_id, weight in self.__weight:
                seed -= weight
                if seed < 0:
                    return project_id

    def code_id_to_content(self, code_id):
        content = self.__cache.get_code(code_id)[0]['content']
        cls_name, _ = find_class_name_by_content(content)
        return cls_name, content

    def get_work_obj(self, project: Project, sign: Sign):
        """继承重写 -> 根据配置返回对象"""
        pass
