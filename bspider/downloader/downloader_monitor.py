# @Time    : 2019/7/8 2:36 PM
# @Author  : 白尚林
# @File    : downloader_monitor
# @Use     :
from bspider.downloader import AsyncDownloader
from bspider.config.default_settings import EXCHANGE_NAME
from bspider.core.lib import BaseMonitor


class DownloaderMonitor(BaseMonitor):

    exchange = EXCHANGE_NAME[1]

    def get_work_obj(self, job_name: str, config: dict, sign: str):
        return AsyncDownloader(job_name, config['downloader_config'], sign)

