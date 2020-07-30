import os
from os import remove
from shutil import rmtree

from bspider.commands import BSpiderCommand
from bspider.utils.conf import PLATFORM_NAME_ENV, BSPIDER_CONFIG_PATH_ENV, PLATFORM_PATH_ENV
from bspider.utils.exceptions import UsageError


class Command(BSpiderCommand):

    def syntax(self):
        return "<platform_name>"

    def short_desc(self):
        return "remove current platform"

    def run(self, args, opts):
        if len(args) not in (1, 2):
            raise UsageError('args error')

        platform_name = args[0]
        platform_path = os.environ[PLATFORM_PATH_ENV]


        if not os.environ.get(PLATFORM_NAME_ENV):
            print(f'Error: platform:{platform_name} is not exists')
            self.exitcode = 1
            return

        # 停止supervisor
        try:
            with open(os.path.join(platform_path, '.cache', 'supervisord.pid')) as f:
                pid = f.read().strip()
            print(os.popen(f'kill {pid}').read().strip())
            print('Stop supervisor process success')
        except Exception:
            print(f'warning: supervisor process is not running')


        print('Clean platform file ...')
        # 删除文件
        rmtree(os.environ[PLATFORM_PATH_ENV], ignore_errors=True)
        remove(os.environ[BSPIDER_CONFIG_PATH_ENV])
        print(f"BSpider platform '{platform_name}' remove success")
