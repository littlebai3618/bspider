# @Time    : 2019/7/17 3:02 PM
# @Author  : 白尚林
# @File    : work
# @Use     :
import sys
import traceback
import asyncio

from bspider.core import BaseManager
from .parser_monitor import ParserMonitor


def run_parser(unique_sign, coro_num=3):
    dm = ParserManager(unique_sign, ParserMonitor)
    dm.run(coro_num)


class ParserManager(BaseManager):

    async def do_work(self):
        try:
            while True:
                all_queue_is_none = True

                msg_id, response, parser, project_name = await self.__get_response()
                if response:
                    all_queue_is_none = False
                    try:
                        requests = await parser.parse(response)
                        while requests:
                            # 发送request到待下载队列
                            await self.broker.set_request(requests.pop(), project_name)
                        self._save_success_result(response.request, response, project_name)
                        self.log.info('{} complete parse: {}'.format(project_name, response.url))
                    except Exception as e:
                        tp, msg, tb = sys.exc_info()
                        e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                        self.log.exception(e)
                        self._save_error_result(response.request, project_name, e_msg, status=-1)
                        # await self.broker.report_ack(msg_id)
                        # continue

                    await self.broker.report_ack(msg_id)

                if all_queue_is_none:
                    # 所有队列都是空的 就沉睡2s
                    await asyncio.sleep(2)
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = '\n'.join(traceback.format_exception(tp, msg, tb))
            self.log.error(f'coro error:{e_msg}')


    async def __get_response(self):
        """由于for 循环不兼容 await 所以单独剥离出来"""
        project_name = await self.monitor.choice_project()
        if project_name is not None:
            msg_id, response = await self.broker.get_response(project_name)
            if msg_id:
                return msg_id, response, self.monitor.projects[project_name], project_name
        else:
            self.log.debug('no task in all download queue empty sleep 2s!')
            await asyncio.sleep(2)
        return None, None, None, None


if __name__ == '__main__':
    run_parser('parser-01')
