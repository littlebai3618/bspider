"""
上报下载结果 -> log
监听配置变化 -> sqlite
"""
import asyncio
import base64
import json

import signal
import zlib

from bspider.http import Response
from bspider.utils.database import AioMysqlClient
from bspider.utils.logger import LoggerPool

from .broker import RabbitMQBroker
from .api import BaseImpl


class BaseManager(object):
    manager_type = ''

    def __init__(self, unique_tag, monitor_cls, coro_num):
        # 记录协程数
        self.coro_num = coro_num

        if self.manager_type == 'scheduler':
            self.log = LoggerPool().get_logger(
                key=unique_tag,
                fn=f'{self.manager_type}',
                module=self.manager_type,
                name=unique_tag)
            self.broker = RabbitMQBroker(self.log, 10)
            self.monitor = monitor_cls(self.log, self.manager_type)
        else:
            self.log = LoggerPool().get_logger(
                key=unique_tag,
                fn=f'{self.manager_type}-{unique_tag}',
                module=self.manager_type,
                name=unique_tag)
            self.broker = RabbitMQBroker(self.log, self.coro_num)
            self.monitor = monitor_cls(self.log, f'{self.manager_type}-{unique_tag}', self.broker.mq_client)

        self.log.info('manager init success')
        # 注册 任务中间人

        if self.manager_type == 'downloader':
            self.status_table = self.broker.frame_settings['DOWNLOADER_STATUS_TABLE']
        elif self.manager_type == 'parser':
            self.status_table = self.broker.frame_settings['PARSER_STATUS_TABLE']

        if self.manager_type != 'scheduler':
            self.mysql_client = AioMysqlClient(self.broker.frame_settings['WEB_STUDIO_DB'])

        # 注册信号量保证程序安全退出
        self.sign = signal.signal(signal.SIGTERM, handler=self.close)
        self.is_close = False

    def run(self):
        tasks = [asyncio.ensure_future(self.monitor.sync_config())]
        for i in range(self.coro_num):
            tasks.append(asyncio.ensure_future(self.do_work()))
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(asyncio.wait(tasks))
        except (KeyboardInterrupt, SystemExit):
            self.loop.run_until_complete(asyncio.sleep(1))
        finally:
            self.close('SIGINT', '')

    def close(self, signum, frame):
        """进程结束回调"""
        if not self.is_close:
            self.log.info('recv signal:{} {}'.format(signum, frame))
            try:
                self.loop.stop()
                self.loop.close()
            except Exception as e:
                # 吞掉异常
                self.log.debug(f'close event loop! {e}')
            # self.monitor.close()
            self.log.info('have fun Bye!')
            exit()
        self.is_close = True

    async def do_work(self):
        raise NotImplementedError

    async def _save_success_result(self,
                                   response: Response,
                                   project_name: str,
                                   project_id: int):
        data = {
            'project_id': project_id,
            'project_name': project_name,
            'sign': response.sign,
            'method': response.method,
            'url': response.url,
            'status': response.status,
            'url_sign': response.url,
        }
        if hasattr(response.request, 'data'):
            data['data'] = json.dumps(response.request.data)
        else:
            data['data'] = None
        fields, values = BaseImpl.make_fv(data)
        sql = f'insert into {self.status_table} set {fields};'.replace('`url_sign`=%s', '`url_sign`=md5(%s)')
        await self.mysql_client.insert(sql, values)
        self.log.info('send success info [{}]'.format(fields % values))

    async def _save_error_result(self,
                                 response: Response,
                                 project_name: str,
                                 project_id: int,
                                 exception: str):
        request = response.request
        data = {
            'project_id': project_id,
            'project_name': project_name,
            'sign': request.sign,
            'method': request.method,
            'url': request.url,
            'status': response.status,
            'url_sign': request.url,
            'exception': exception,
            'response': base64.b64encode(zlib.compress(json.dumps(response.dumps()).encode()))
        }
        if hasattr(request, 'data'):
            data['data'] = json.dumps(request.data)
        else:
            data['data'] = None
        fields, values = BaseImpl.make_fv(data)
        sql = f'insert into {self.status_table} set {fields};'
        await self.mysql_client.insert(sql.replace('`url_sign`=%s', '`url_sign`=md5(%s)'), values)
        self.log.info('send error info [{}]'.format(fields % values))
