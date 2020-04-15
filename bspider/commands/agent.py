"""
** 检查是否有supervisor.pid文件确认supervisor是否启动，启动则调用rpc接口启动进程 否则：初始化supervisor.conf 启动进程
1. web service
2. 调度器
3. 定时任务管理
"""
import os
from shutil import copy2

from bspider.commands import BSpiderCommand
from bspider.utils.conf import PLATFORM_PATH_ENV, PLATFORM_NAME_ENV
from bspider.utils.exceptions import UsageError
from bspider.utils.template import render_templatefile


class Command(BSpiderCommand):

    def syntax(self):
        return "<op:start|stop>"

    def short_desc(self):
        return "Run BSpider as a agent node"

    def long_desc(self):
        return """Run BSpider by supervisor with one process:
        agent: a web server to manager bspider worker node (by gunicorn and gevent).
        """

    def init_supervisor(self):
        """查看supervisor是否已经启动"""
        platform_path = os.environ[PLATFORM_PATH_ENV]
        platform_name = os.environ[PLATFORM_NAME_ENV]

        tplfile = os.path.join(self.templates_dir, 'tools_cfg', 'agent_gunicorn.py.tmpl')
        copy2(tplfile, os.path.join(platform_path, '.cache', 'agent_gunicorn.py.tmpl'))
        render_templatefile(os.path.join(platform_path, '.cache', 'agent_gunicorn.py.tmpl'),
                            agent_port=self.frame_settings['AGENT']['port'],
                            agent_ip=self.frame_settings['AGENT']['ip'],
                            log_level=self.frame_settings['LOGGER_LEVEL'].lower(),
                            platform_name=platform_name,
                            platform_path=platform_path)

        if os.path.exists(os.path.join(platform_path, '.cache', 'supervisord.pid')):
            return True
        tplfile = os.path.join(self.templates_dir, 'tools_cfg', 'supervisor.conf.tmpl')
        config_path = os.path.join(platform_path, '.cache', 'supervisor.conf')
        copy2(tplfile, config_path)
        render_templatefile(config_path,
                            platform_path=platform_path,
                            bin_path=os.path.join(platform_path, 'bin'),
                            master_ip=self.frame_settings['MASTER']['ip'],
                            supervisor_rpc_port=self.frame_settings['SUPERVISOR_RPC']['port'],
                            supervisor_rpc_username=self.frame_settings['SUPERVISOR_RPC']['username'],
                            supervisor_rpc_password=self.frame_settings['SUPERVISOR_RPC']['password'])

        cmd = 'supervisord -c {}'.format(os.path.join(platform_path, '.cache', 'supervisor.conf'))
        print(os.popen(cmd).read().strip())
        return True

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError('args error')
        self.init_supervisor()
        op = args[0]
        if op not in ('start', 'stop'):
            raise UsageError('unknow op: %s' % (op))
        rpc_socket = os.path.join(os.environ[PLATFORM_PATH_ENV], '.cache', 'supervisor.conf')
        cmd = f'supervisorctl -c {rpc_socket} {op} agent'
        print(cmd)
        print(os.popen(cmd).read().strip())
        print(f'A new BSpider agent node {op} success')


if __name__ == '__main__':
    Command().run(['hello_project'])
