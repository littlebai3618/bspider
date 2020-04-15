"""
** 检查是否有supervisor.pid文件确认supervisor是否启动，启动则调用rpc接口启动进程 否则：初始化supervisor.conf 启动进程
1. web service
2. 调度器
3. 定时任务管理

# 如果MySQL表未创建的实例化表和初始数据
"""
# 忽略PyMySQL警告
from warnings import filterwarnings
import pymysql
filterwarnings('ignore', category = pymysql.Warning)

import os
import re
import string
import time
from shutil import ignore_patterns, copy2

from werkzeug.security import generate_password_hash

from bspider.commands import BSpiderCommand
from bspider.utils.conf import PLATFORM_PATH_ENV, PLATFORM_NAME_ENV
from bspider.utils.database import prepare_insert_sql
from bspider.utils.exceptions import UsageError
from bspider.utils.template import render_templatefile

IGNORE = ignore_patterns('*.pyc', '.svn')


def init_custom_code(templates_dir, table):
    sql = list()
    desc = re.compile('@([A-Za-z]+)=(.*?)\n')

    for dirpath, _, filenames in os.walk(os.path.join(templates_dir, 'inner_module')):
        for filename in filenames:
            if filename.startswith('__'):
                continue

            if filename.endswith('.module'):
                with open(os.path.join(dirpath, filename)) as f:
                    text = f.read()
                    result_dict = dict(content=text)
                    param = desc.findall(text)
                    for k, v in param:
                        result_dict[k] = v.strip()
            sql.append(prepare_insert_sql(table, data=result_dict))
    return sql


PLAIN_TABLE = [
    ('bspider_cron', dict()),
    ('bspider_customcode', dict()),
    ('bspider_downloader_status', dict()),
    ('bspider_node', dict()),
    ('bspider_node_status', dict()),
    ('bspider_parser_status', dict()),
    ('bspider_project', dict()),
    ('bspider_project_customcode', dict()),
    ('bspider_user', dict(password=generate_password_hash('admin'))),
    ('bspider_worker', dict())
]


class Command(BSpiderCommand):

    def syntax(self):
        return "<op:start|stop>"

    def short_desc(self):
        return "Run/stop BSpider as a master node"

    def long_desc(self):
        return """Run/stop BSpider by supervisor with three process:
        master: a web server to manager spiders (by gunicorn and gevent).
        bcorn: a cronjob process to manager cron task.
        scheduler: dispatch all spider project.
        ** first start master service this cmd will try to create some MySQL table"""

    def init_supervisor(self):
        """查看supervisor是否已经启动"""
        platform_path = os.environ[PLATFORM_PATH_ENV]
        platform_name = os.environ[PLATFORM_NAME_ENV]

        tplfile = os.path.join(self.templates_dir, 'tools_cfg', 'master_gunicorn.py.tmpl')
        copy2(tplfile, os.path.join(platform_path, '.cache', 'master_gunicorn.py.tmpl'))
        render_templatefile(os.path.join(platform_path, '.cache', 'master_gunicorn.py.tmpl'),
                            master_port=self.frame_settings['MASTER']['port'],
                            master_ip=self.frame_settings['MASTER']['ip'],
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
        print('start supervisor')
        print(f'cmd: {cmd}')
        print(os.popen(cmd).read().strip())
        time.sleep(3)
        return True

    def init_database(self):
        from bspider.utils.database import MysqlClient
        mysql_client = MysqlClient.from_settings(self.frame_settings['WEB_STUDIO_DB'])

        sql = 'show tables;'
        remote_table = set()
        for table in mysql_client.select(sql):
            for table_name in table.values():
                if table_name.startswith('bspider_'):
                    remote_table.add(table_name)

        if set([table[0] for table in PLAIN_TABLE]) == remote_table:
            return True
        else:
            print('Warning: Mysql Table is not create or destroyed')
            while True:
                in_content = input("Initialize MySQL table or not (Y/N)：")
                if in_content.upper() == "N":
                    exit(1)
                elif in_content.upper() == "Y":
                    break

            # 初始化表
            for table, param in PLAIN_TABLE:
                sql_path = os.path.join(self.templates_dir, 'table_sql', f'{table}.sql')
                with open(sql_path) as f:
                    sql_list = string.Template(f.read().strip()).substitute(**param)
                    for sql in sql_list.split(';\n'):
                        if len(sql):
                            mysql_client.query(sql)
                print(f'init table:{table} success')

            sql_list = init_custom_code(self.templates_dir, 'bspider_customcode')
            print(f'insert {len(sql_list)} inner module')
            for sql, value in sql_list:
                mysql_client.insert(sql, value)

        return True

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError('args error')
        op = args[0]
        if op not in ('start', 'stop'):
            raise UsageError('unknow op: %s' % (op))

        if op == 'start':
            self.init_database()
            self.init_supervisor()
        rpc_socket = os.path.join(os.environ[PLATFORM_PATH_ENV], '.cache', 'supervisor.conf')

        print('=======supervisor output ========')
        for module in ('master', 'bcorn', 'scheduler'):
            cmd = f'supervisorctl -c {rpc_socket} {op} {module}'
            print(os.popen(cmd).read().strip())
        print('=================================')
        print(f'A new BSpider master node {op}!')
        print(f'see /platform/logs/supervisor/{module}.log to check process status!')
