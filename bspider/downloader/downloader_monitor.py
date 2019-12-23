from bspider.config.default_settings import EXCHANGE_NAME
from bspider.core import BaseMonitor, ProjectConfigParser
from bspider.utils.sign import Sign

from .async_downloader import AsyncDownloader


class DownloaderMonitor(BaseMonitor):

    exchange = EXCHANGE_NAME[1]

    def get_work_obj(self, config: ProjectConfigParser, sign: Sign):
        return AsyncDownloader(config, sign, self.log_fn)

