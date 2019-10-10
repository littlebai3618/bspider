# @Time    : 2019/9/20 10:59 上午
# @Author  : baii
# @File    : master
# @Use     :
"""
** 检查是否有supervisor.pid文件确认supervisor是否启动，启动则调用rpc接口启动进程 否则：初始化supervisor.conf 启动进程
1. web service
2. 调度器
3. 定时任务管理
"""
import os
import time
from shutil import ignore_patterns, copy2

from bspider.commands import BSpiderCommand
from bspider.utils.conf import PLATFORM_PATH_ENV, PLATFORM_NAME_ENV
from bspider.utils.exceptions import UsageError
from bspider.utils.template import render_templatefile

IGNORE = ignore_patterns('*.pyc', '.svn')


class Command(BSpiderCommand):

    def syntax(self):
        return "<op:start|stop>"

    def short_desc(self):
        return "Run BSpider as a master node"

    def long_desc(self):
        return """Run BSpider by supervisor with three process:
        master: a web server to manager spiders (by gunicorn and gevent).
        bcorn: a cronjob process to manager cron task.
        scheduler: dispatch all spider project.
        """

    def init_supervisor(self):
        """查看supervisor是否已经启动"""
        platform_path = os.environ[PLATFORM_PATH_ENV]
        platform_name = os.environ[PLATFORM_NAME_ENV]

        tplfile = os.path.join(self.templates_dir, 'tools_cfg', 'master_gunicorn.py.tmpl')
        copy2(tplfile, os.path.join(platform_path, 'cache', 'master_gunicorn.py.tmpl'))
        render_templatefile(os.path.join(platform_path, 'cache', 'master_gunicorn.py.tmpl'),
                            master_port=self.settings['MASTER']['port'],
                            master_ip=self.settings['MASTER']['ip'],
                            log_level=self.settings['LOGGER_LEVEL'].lower(),
                            platform_name=platform_name,
                            platform_path=platform_path)

        if os.path.exists(os.path.join(platform_path, 'cache', 'supervisord.pid')):
            return True
        tplfile = os.path.join(self.templates_dir, 'tools_cfg', 'supervisor.conf.tmpl')
        config_path = os.path.join(platform_path, 'cache', 'supervisor.conf')
        copy2(tplfile, config_path)
        render_templatefile(config_path,
                            platform_path=platform_path,
                            bin_path=os.path.join(platform_path, 'bin'),
                            master_ip=self.settings['MASTER']['ip'],
                            supervisor_rpc_port=self.settings['SUPERVISOR_RPC']['port'],
                            supervisor_rpc_username=self.settings['SUPERVISOR_RPC']['username'],
                            supervisor_rpc_password=self.settings['SUPERVISOR_RPC']['password'])

        cmd = 'supervisord -c {}'.format(os.path.join(platform_path, 'cache', 'supervisor.conf'))
        print(os.popen(cmd).read().strip())
        time.sleep(3)
        return True

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError('args error')
        self.init_supervisor()
        op = args[0]
        if op not in ('start', 'stop'):
            raise UsageError(f'unknow op: {op}')
        rpc_socket = os.path.join(os.environ[PLATFORM_PATH_ENV], 'cache', 'supervisor.conf')

        for module in ('master', 'bcorn', 'scheduler'):
            cmd = f'supervisorctl -c {rpc_socket} {op} {module}'
            print(os.popen(cmd).read().strip())
        # print(f'A new BSpider master node {op} success')


if __name__ == '__main__':
    Command().run(['hello_project'])
