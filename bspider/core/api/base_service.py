from datetime import datetime

import pytz

from bspider.config import FrameSettings


class BaseService(object):
    frame_settings = FrameSettings()
    tz = pytz.timezone(frame_settings['TIMEZONE'])

    def datetime_to_str(self, d: dict) -> None:
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(value, dict):
                self.datetime_to_str(value)
