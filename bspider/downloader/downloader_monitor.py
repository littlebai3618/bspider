from bspider.config.default_settings import EXCHANGE_NAME
from bspider.core import BaseMonitor, Project
from bspider.utils.sign import Sign

from .async_downloader import AsyncDownloader


class DownloaderMonitor(BaseMonitor):

    exchange = EXCHANGE_NAME[1]

    def get_work_obj(self, project: Project, sign: Sign):
        return AsyncDownloader(project, sign, self.log_fn)

