import asyncio
import json
import sys
import traceback

from bspider.core import BaseManager
from bspider.http import Response, ERROR_RESPONSE
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
                parser = self.monitor.projects.get(self.monitor.choice_project())
                if parser is None:
                    # 防止协程抢占无法轮换
                    await asyncio.sleep(1)
                    continue
                e_msg = None
                response = ERROR_RESPONSE

                async with self.broker.mq_client.session() as session:
                    msg_id, data = await session.recv_msg(f'{self.exchange}_{parser.project_id}')
                    if msg_id:
                        try:
                            response = Response.loads(json.loads(data))
                            self.log.info(f'success get a new Response: {response}')
                            requests = await parser.parse(response)
                        except Exception as e:
                            tp, msg, tb = sys.exc_info()
                            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                            e.with_traceback(tb)
                            self.log.exception(e)
                        session.ack(msg_id)

                if msg_id:
                    if e_msg:
                        await self._save_error_result(response, parser.project_name, parser.project_id, e_msg)
                        self.log.warning('parser failed: project:project_id->{} project_name->{} sign: {}'.format(
                            parser.project_id, parser.project_name, response.sign))
                    else:
                        while len(requests):
                            # 发送request到待下载队列
                            await self.broker.set_request(requests.pop(), parser.project_id)
                        await self._save_success_result(response, parser.project_name, parser.project_id)
                        self.log.info('project:project_id->{} project_name->{} complete parser: {}'.format(
                            parser.project_id, parser.project_name, response.url))
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            self.log.error(f'coro error:{e_msg}')


if __name__ == '__main__':
    run_parser('parser-01')
