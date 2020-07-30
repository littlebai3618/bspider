import asyncio
import json
import traceback

import sys

from bspider.core import BaseManager
from bspider.config.default_settings import EXCHANGE_NAME
from bspider.http import Request, ERROR_RESPONSE

from .downloader_monitor import DownloaderMonitor


def run_downloader(unique_sign, coro_num=1):
    """A factory to make a download process"""
    dm = DownloaderManager(unique_sign, DownloaderMonitor, coro_num)
    dm.run()


class DownloaderManager(BaseManager):
    """全异步操作的下载器管理器"""
    manager_type = 'downloader'
    exchange = EXCHANGE_NAME[1]

    async def do_work(self):
        try:
            while True:
                downloader = self.monitor.projects.get(self.monitor.choice_project())
                if downloader is None:
                    # 防止协程抢占无法轮换
                    await asyncio.sleep(1)
                    continue

                # 异常占位符
                e_msg = None
                response = ERROR_RESPONSE
                sign = False
                async with self.broker.mq_client.session() as session:
                    msg_id, data = await session.recv_msg(f'{self.exchange}_{downloader.project_id}')
                    if msg_id:
                        try:
                            request = Request.loads(json.loads(data))
                            self.log.info(f'success get a new Request: {request}')
                            if request.life_cycle is None or request.life_cycle > 0:
                                response, sign, e_msg = await downloader.download(request)
                                if isinstance(request.life_cycle, int):
                                    response.request.life_cycle -= 1
                            else:
                                self.log.warning(f'Request life_cycle <= 0 ignore it: {request}')
                        except Exception:
                            tp, msg, tb = sys.exc_info()
                            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                        session.ack(msg_id)

                # 分开写是因为要提前释放channel,防止channel 被用光影响性能
                if msg_id:
                    await self.broker.set_response(response, downloader.project_id)
                    if e_msg or not sign:
                        self.log.info(
                            f'project:project_id->{downloader.project_id} project_name->{downloader.project_name} fail download: {request}')
                        await self._save_error_result(response, downloader.project_name, downloader.project_id, e_msg)
                    else:
                        # 持久化下载结果
                        await self._save_success_result(response, downloader.project_name, downloader.project_id)
                        self.log.info('project:project_id->{} project_name->{} complete download: {}'.format(
                            downloader.project_id, downloader.project_name, response.url))
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            self.log.error(f'coro error:{e_msg}')


if __name__ == '__main__':
    run_downloader('downloader01')
