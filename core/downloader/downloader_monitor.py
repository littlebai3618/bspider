# @Time    : 2019/7/8 2:36 PM
# @Author  : 白尚林
# @File    : downloader_monitor
# @Use     :
from core.downloader.async_downloader import AsyncDownloader
from core.lib import EXCHANGE_NAME
from core.lib.base_monitor import BaseMonitor


class DownloaderMonitor(BaseMonitor):

    exchange = EXCHANGE_NAME[1]

    def get_work_obj(self, job_name: str, config: dict, sign: str):
        return AsyncDownloader(job_name, config['downloader_config'], sign)

