import os
import sys
from configparser import ConfigParser

import bspider

BSPIDER_CONFIG_PATH_ENV = 'BSPIDER_CONFIG_PATH'
BSPIDER_VERSION_ENV = 'BSPIDER_VERSION'
PLATFORM_PATH_ENV = 'PLATFORM_PATH'
PLATFORM_NAME_ENV = 'PLATFORM_NAME'
BSPIDER_FRAME_SETTINGS_MODULE_ENV = 'BSPIDER_FRAME_SETTINGS_MODULE'


def init_platform_env(func):
    """检查是否存在platform.cfg 如存在加载配置"""
    def wrap(*args, **kwargs):
        if os.environ.get(BSPIDER_CONFIG_PATH_ENV) is None:
            bspider_config_path = os.path.expanduser(os.path.join('~', '.bspider.platform.cfg'))
            os.environ[BSPIDER_CONFIG_PATH_ENV] = bspider_config_path
            os.environ[BSPIDER_VERSION_ENV] = bspider.__version__
            if os.path.exists(bspider_config_path):
                cfg = ConfigParser()
                cfg.read([os.environ[BSPIDER_CONFIG_PATH_ENV]], encoding='utf8')
                if cfg.has_option('settings', 'default'):
                    os.environ[BSPIDER_FRAME_SETTINGS_MODULE_ENV] = cfg.get('settings', 'default')
                if cfg.has_option('deploy', 'platform'):
                    os.environ[PLATFORM_NAME_ENV] = cfg.get('deploy', 'platform')
                if cfg.has_option('deploy', 'path'):
                    os.environ[PLATFORM_PATH_ENV] = cfg.get('deploy', 'path')
                    sys.path.append(cfg.get('deploy', 'path'))
        return func(*args, **kwargs)
    return wrap
