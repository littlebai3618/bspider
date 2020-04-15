"""
    返回一个包含配置的默认字典
"""
import os

from bspider.config import default_settings
from bspider.utils import singleton
from bspider.utils.conf import init_platform_env, PLATFORM_PATH_ENV
from bspider.utils.importer import import_module_by_path


@init_platform_env
@singleton
class FrameSettings(object):

    def __init__(self):
        """FrameSettings('${platform_name}.config.frame_settings')"""
        self.__settings = dict()

        for key in dir(default_settings):
            if key.isupper():
                self.__settings[key] = getattr(default_settings, key)
        # 优化错误处理
        module = import_module_by_path('frame_settings',
                                       os.path.join(os.environ[PLATFORM_PATH_ENV], 'config', 'frame_settings.py'))
        for key in dir(module):
            if key.isupper():
                self.__settings[key] = getattr(module, key)

    def get(self, key, default=None):
        if default:
            return self.__settings.get(key, default)
        else:
            return self.__settings[key]

    def __getitem__(self, item):
        return self.__settings[item]


if __name__ == '__main__':
    print(FrameSettings())
