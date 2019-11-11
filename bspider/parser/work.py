# @Time    : 2019/7/17 3:02 PM
# @Author  : 白尚林
# @File    : work
# @Use     :
import json
import sys
import traceback
import asyncio

from bspider.core import BaseManager
from bspider.utils.tools import make_sign
from .parser_monitor import ParserMonitor


def run_parser(unique_sign, coro_num=3):
    dm = ParserManager(unique_sign, ParserMonitor)
    dm.run(coro_num)


class ParserManager(BaseManager):

    async def do_work(self):
        try:
            while True:
                msg_id, response, parser = await self.__get_response()
                if msg_id:
                    try:
                        requests = await parser.parse(response)
                        while requests:
                            # 发送request到待下载队列
                            request = requests.pop()
                            if request.data:
                                request.sign = make_sign(parser.project_name, request.url, json.dumps(request.data))
                            else:
                                request.sign = make_sign(parser.project_name, request.url)
                            await self.broker.set_request(requests.pop(), parser.project_id)
                        await self._save_success_result(response.request, response, parser.project_name, parser.project_id)
                        self.log.info('project:project_id->{} project_name->{} complete parser: {}'.format(
                            parser.project_id, parser.project_name, response.url))
                    except Exception as e:
                        tp, msg, tb = sys.exc_info()
                        e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                        self.log.exception(e)
                        await self._save_error_result(response.request, parser.project_name, parser.project_id, e_msg,
                                                status=-1)

                    await self.broker.report_ack(msg_id)
                else:
                    await asyncio.sleep(2)
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            self.log.error(f'coro error:{e_msg}')

    async def __get_response(self):
        """由于for 循环不兼容 await 所以单独剥离出来"""
        project_id = await self.monitor.choice_project()
        if project_id is None:
            self.log.debug('no task in all download queue empty sleep 2s!')
            await asyncio.sleep(2)
            return None, None, None

        parser = self.monitor.projects[project_id]
        msg_id, response = await self.broker.get_response(parser.project_id)

        return msg_id, response, parser


if __name__ == '__main__':
    run_parser('parser-01')
