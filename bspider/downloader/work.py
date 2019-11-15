# @Time    : 2019/7/17 2:52 PM
# @Author  : 白尚林
# @File    : work
# @Use     :
import asyncio
import traceback

import sys

from bspider.core import BaseManager

from .downloader_monitor import DownloaderMonitor


def run_downloader(unique_sign, coro_num=1):
    """A factory to make a download process"""
    dm = DownloaderManager(unique_sign, DownloaderMonitor)
    dm.run(coro_num)


class DownloaderManager(BaseManager):
    """全aio操作的下载器管理器"""
    manager_type = 'downloader'

    async def do_work(self):
        try:
            while True:
                msg_id, request, downloader = await self.__get_request()
                if msg_id:
                    try:
                        response = await downloader.download(request)
                    except Exception as e:
                        tp, msg, tb = sys.exc_info()
                        e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                        self.log.info(
                            'project:project_id->{} project_name->{} fail download: {}'.format(
                                downloader.project_id, downloader.project_name, request.url))
                        self.log.exception(e)
                        await self._save_error_result(request, downloader.project_name, downloader.project_id, e_msg)
                        continue

                    if response and response.status != 599:
                        await self.broker.set_response(response, downloader.project_id)
                        self.log.info('project:project_id->{} project_name->{} complete download: {}'.format(
                            downloader.project_id, downloader.project_name, response.url))
                        # 持久化下载结果
                        await self._save_success_result(request, response, downloader.project_name, downloader.project_id)
                    await self.broker.report_ack(msg_id)
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            self.log.error(f'coro error:{e_msg}')

    async def __get_request(self):
        """由于for 循环不兼容 await 所以单独剥离出来"""
        project_id = await self.monitor.choice_project()
        if project_id is None:
            # self.log.debug('no task in all candidate queue empty sleep 2s!')
            await asyncio.sleep(2)
            return None, None, None

        downloader = self.monitor.projects[project_id]
        msg_id, request = await self.broker.get_request(downloader.project_id)
        return msg_id, request, downloader


if __name__ == '__main__':
    run_downloader('downloader01')
