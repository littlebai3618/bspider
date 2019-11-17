# @Time    : 2019/7/5 5:54 PM
# @Author  : 白尚林
# @File    : base_monitor
# @Use     :
import asyncio
import random
import sys
import traceback

from bspider.config.default_settings import EXCHANGE_NAME
from bspider.utils.rabbitMQ import AioRabbitMQHandler
from bspider.utils.sign import Sign
from bspider.utils.tools import find_class_name_by_content

from .broker import RabbitMQBroker
from .agent_cache import AgentCache
from .project_config_parser import ProjectConfigParser


class BaseMonitor(object):
    exchange = ''

    def __init__(self, log, log_fn, mq_handler: AioRabbitMQHandler):
        """
        :param downloader_tag: 一个下载器的唯一标识，不能和其他下载器一致
        """
        self.log = log
        self.__cache = AgentCache()
        self.__mq_handler = mq_handler
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
            if await self.__mq_handler.get_queue_message_count(queue='{}_{}'.format(self.exchange, info['id'])) != 0:
                tmp_weight[info['id']] = info['rate']
                total_sum += info['rate']

            project_obj = self.projects.get(info['id'])
            pc_obj = ProjectConfigParser.loads(info['config'])

            pc_obj.project_name = info['name']
            pc_obj.project_id = info['id']
            # code_id映射为中间件代码
            if self.exchange == EXCHANGE_NAME[2]:
                pc_obj.pipeline = self.code_id_to_content(pc_obj.pipeline)
                sign = Sign(project_timestamp=info['timestamp'], module=pc_obj.pipeline)
            else:
                pc_obj.middleware = self.code_id_to_content(pc_obj.middleware)
                sign = Sign(project_timestamp=info['timestamp'], module=pc_obj.middleware)

            if project_obj is None or project_obj.sign != sign:
                tmp_projects[info['id']] = self.get_work_obj(pc_obj, sign=sign)
            else:
                tmp_projects[info['id']] = project_obj

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
            for project_id, weight in self.__weight:
                seed -= weight
                if seed < 0:
                    # self.log.debug(f'choice project:project_id->{project_id}')
                    return project_id
        # self.log.debug('project weight is empty')

    def code_id_to_content(self, code_ids: list):
        res = list()
        for code_id in code_ids:
            content = self.__cache.get_code(code_id)[0]['content']
            _, cls_name, _ = find_class_name_by_content(content)
            res.append((cls_name, content))

        return res

    def get_work_obj(self, config: ProjectConfigParser, sign: Sign):
        """继承重写 -> 根据配置返回对象"""
        pass

    def close(self):
        del self.__cache
