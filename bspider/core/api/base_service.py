# @Time    : 2019/6/18 3:45 PM
# @Author  : 白尚林
# @File    : base_service
# @Use     :
from datetime import datetime

from bspider.config import FrameSettings


class BaseService(object):
    frame_settings = FrameSettings()

    def datetime_to_str(self, d: dict) -> None:
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(value, dict):
                self.datetime_to_str(value)
