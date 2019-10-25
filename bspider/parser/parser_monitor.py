# @Time    : 2019/7/9 2:27 PM
# @Author  : 白尚林
# @File    : parser_monitor
# @Use     :
"""解析器监听器"""
from bspider.config.default_settings import EXCHANGE_NAME
from bspider.core.lib import BaseMonitor
from bspider.parser.async_parser import AsyncParser


class ParserMonitor(BaseMonitor):
    exchange = EXCHANGE_NAME[2]

    def get_work_obj(self, job_name: str, config: dict, sign: str):
        return AsyncParser(job_name, config['parser_config'], sign)