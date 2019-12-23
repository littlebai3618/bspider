"""解析器监听器"""
from bspider.config.default_settings import EXCHANGE_NAME
from bspider.core import BaseMonitor, ProjectConfigParser
from bspider.parser.async_parser import AsyncParser
from bspider.utils.sign import Sign


class ParserMonitor(BaseMonitor):
    exchange = EXCHANGE_NAME[2]

    def get_work_obj(self, config: ProjectConfigParser, sign: Sign) -> AsyncParser:
        return AsyncParser(config, sign, self.log_fn)