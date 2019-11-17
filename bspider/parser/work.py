# @Time    : 2019/7/17 3:02 PM
# @Author  : 白尚林
# @File    : work
# @Use     :
import json
import sys
import traceback

from bspider.core import BaseManager
from bspider.http import Response
from bspider.utils.tools import make_sign
from bspider.config.default_settings import EXCHANGE_NAME

from .parser_monitor import ParserMonitor


def run_parser(unique_sign, coro_num=3):
    dm = ParserManager(unique_sign, ParserMonitor, coro_num)
    dm.run()


class ParserManager(BaseManager):
    manager_type = 'parser'
    exchange = EXCHANGE_NAME[2]

    async def do_work(self):
        try:
            while True:
                parser = self.monitor.projects.get(await self.monitor.choice_project())
                if parser is None:
                    continue
                e_msg = None
                async with self.broker.mq_handler.session() as session:
                    msg_id, data = await session.recv_msg(f'{self.exchange}_{parser.project_id}')
                    response = Response.loads(json.loads(data))
                    self.log.info(f'success get a new Response: {response}')
                    if msg_id:
                        try:
                            requests = await parser.parse(response)
                        except Exception as e:
                            tp, msg, tb = sys.exc_info()
                            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                            e.with_traceback(tb)
                            self.log.exception(e)
                        session.ack(msg_id)

                if msg_id:
                    if e_msg:
                        await self._save_error_result(response.request, parser.project_name, parser.project_id, e_msg,
                                                      status=-1)
                        self.log.warning('parser failed: project:project_id->{} project_name->{} sign: {}'.format(
                            parser.project_id, parser.project_name, response.sign))
                    else:
                        while len(requests):
                            # 发送request到待下载队列
                            request = requests.pop()
                            if request.data:
                                request.sign = make_sign(parser.project_name, request.url, json.dumps(request.data))
                            else:
                                request.sign = make_sign(parser.project_name, request.url)
                            await self.broker.set_request(requests.pop(), parser.project_id)
                        await self._save_success_result(response.request, response, parser.project_name,
                                                        parser.project_id)
                        self.log.info('project:project_id->{} project_name->{} complete parser: {}'.format(
                            parser.project_id, parser.project_name, response.url))
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            self.log.error(f'coro error:{e_msg}')


if __name__ == '__main__':
    run_parser('parser-01')
