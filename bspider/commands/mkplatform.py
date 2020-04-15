"""
1. 初始化config文件
2. 初始化cache文件夹
3. 初始化模板
"""
import os
import string
from os import mkdir
from os.path import join, abspath
from shutil import copy2

from bspider.commands import BSpiderCommand
from bspider.utils.conf import PLATFORM_NAME_ENV, PLATFORM_PATH_ENV, BSPIDER_CONFIG_PATH_ENV
from bspider.utils.exceptions import UsageError
from bspider.utils.template import render_templatefile

TEMPLATES_TO_RENDER = (
    ('config', 'frame_settings.py.tmpl'),
    ('config', '__init__.py.tmpl'),
    ('bin', 'agent_manager.py.tmpl'),
    ('bin', 'bcorn_manager.py.tmpl'),
    ('bin', 'scheduler_manager.py.tmpl'),
    ('bin', 'master_manager.py.tmpl'),
    ('bin', '__init__.py.tmpl'),
    ('middleware', '__init__.py.tmpl'),
    ('pipeline', '__init__.py.tmpl'),
    ('projects', '__init__.py.tmpl'),
    ('.', '__init__.py.tmpl'),
)


class Command(BSpiderCommand):

    def syntax(self):
        return "<platform_name>"

    def short_desc(self):
        return "Create new platform in current path"

    def run(self, args, opts):
        if len(args) not in (1, 2):
            raise UsageError('args error')

        platform_name = args[0]

        if os.environ.get(PLATFORM_NAME_ENV):
            self.exitcode = 1
            print(f'Error: platform:{os.environ[PLATFORM_NAME_ENV]} already exists in {os.environ[PLATFORM_PATH_ENV]}')
            return

        if not self._is_valid_name(platform_name):
            self.exitcode = 1
            return

        # 拷贝模板
        self._copytree(join(self.templates_dir, 'platform'), abspath(platform_name))

        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tplfile = join(platform_name,
                           string.Template(path).substitute(platform_name=platform_name))
            render_templatefile(tplfile, platform_name=platform_name)

        mkdir(join(abspath(platform_name), 'log'))
        mkdir(join(abspath(platform_name), 'log', 'supervisor'))
        mkdir(join(abspath(platform_name), '.cache'))

        tplfile = join(self.templates_dir, 'tools_cfg', '.bspider.platform.cfg.tmpl')
        copy2(tplfile, os.environ[BSPIDER_CONFIG_PATH_ENV])
        render_templatefile(os.environ[BSPIDER_CONFIG_PATH_ENV], platform_name=platform_name,
                            platform_path=abspath(platform_name))

        print(f"New BSpider platform '{platform_name}' init success")
        print(f"    template directory:\n    '{self.templates_dir}'")
        print(f"    platform at:\n    '{abspath(platform_name)}'")
        print("Please change frame_settings in ")
        print(f"{abspath(platform_name)}/frame_settings.py")
        print("You can development your first spider with:")
        print(f"    cd {abspath(platform_name)}/projects")
        print("then you can init you spider code by template")
        print("     bspider mkspider <spider_name>")


if __name__ == '__main__':
    Command().run(['hello_project'])
