# @Time    : 2019/7/17 2:52 PM
# @Author  : 白尚林
# @File    : work
# @Use     :
import asyncio
import traceback

import sys

from bspider.downloader.downloader_monitor import DownloaderMonitor
from bspider.core.lib import BaseManager


def run_downloader(unique_sign, coro_num=1):
    """A factory to make a download process"""
    dm = DownloaderManager(unique_sign, DownloaderMonitor)
    dm.run(coro_num)


class DownloaderManager(BaseManager):
    """全aio操作的下载器管理器"""
    async def do_work(self):
        try:
            while True:
                msg_id, request, downloader, project_name = await self.__get_request()
                if request:
                    try:
                        response = await downloader.download(request)
                    except Exception as e:
                        tp, msg, tb = sys.exc_info()
                        e_msg = '\n'.join(traceback.format_exception(tp, msg, tb))
                        self.log.info('{} fail download: {}'.format(project_name, request.url))
                        self.log.exception(e)
                        self._save_error_result(request, project_name, e_msg)
                        continue

                    if response and response.status != 599:
                        await self.broker.set_response(response, project_name)
                        self.log.info('{} complete download: {}'.format(project_name, response.url))
                        # 持久化下载结果
                        self._save_success_result(request, response, project_name)
                    await self.broker.report_ack(msg_id)
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = '\n'.join(traceback.format_exception(tp, msg, tb))
            self.log.error(f'coro error:{e_msg}')

    async def __get_request(self):
        """由于for 循环不兼容 await 所以单独剥离出来"""
        project_name = await self.monitor.choice_project()
        if project_name is not None:
            msg_id, request = await self.broker.get_request(project_name)
            if msg_id:
                return msg_id, request, self.monitor.projects[project_name], project_name
        else:
            self.log.debug('no task in all candidate queue empty sleep 2s!')
            await asyncio.sleep(2)
        return None, None, None, None


if __name__ == '__main__':
    run_downloader('downloader01')
