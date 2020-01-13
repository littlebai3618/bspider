"""
生成用于启动agent服务的app对象，是整个agent服务的入口
"""
import sqlite3
import sys
import traceback

from flask import Flask
from werkzeug.exceptions import HTTPException

from bspider.agent import log
from bspider.core.api import APIException, MasterMixIn
from bspider.core import AgentCache
from bspider.config import FrameSettings

from bspider.agent.controller.project import project
from bspider.agent.controller.node import node, node_service
from bspider.agent.controller.code import code

from bspider.utils.exceptions import RemoteOPError
from bspider.utils.system import System


class CreateApp(MasterMixIn):

    def __init__(self):
        self.frame_settings = FrameSettings()

    def app(self):
        app = Flask(__name__)
        app.secret_key = self.frame_settings['WEB_SECRET_KEY']
        app.register_blueprint(node)
        app.register_blueprint(project)
        app.register_blueprint(code)

        @app.errorhandler(Exception)
        def framework_error(error):
            if isinstance(error, APIException):
                return error
            if isinstance(error, HTTPException):
                return APIException(error.code, error.description, 10000)
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            log.error(f'server exec:{e_msg}')
            return APIException()

        if self.__init_agent(**self.frame_settings['AGENT']):
            log.info('Agent:{name}->{ip}:{port} run success!'.format(**self.frame_settings['AGENT']))
            app.logger.addHandler(log)
            return app
        else:
            exit()

    def __init_agent(self, ip, name, description, port) -> bool:
        cache = AgentCache()
        system = System()
        try:
            # 初始化缓存、获取缓存数据
            cache.initialization()
            data = self.op_add_node({
                'ip': ip,
                'description': description,
                'name': name,
                'cpu_num': system.cpu_num,
                'mem_size': system.mem_size,
                'disk_size': system.disk_size,
                'port': port
            })
        except sqlite3.Error:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            log.error(f'AgentCache init failed exec:{e_msg}')
            return False
        except RemoteOPError:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            log.error(f'Master server exec:{e_msg}')
            return False

        log.debug(
            'start to load master\'s data: project->{} code->{}'.format(len(data['projects']), len(data['codes'])))
        try:
            # 向缓存中写入数据
            for code in data['codes']:
                cache.set_code(**code)

            for project in data['projects']:
                cache.set_project(**project)
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            log.error(f'AgentCache init failed exec:{e_msg}')
            return False

        log.info('cache init complete!! project->{} code->{}'.format(len(data['projects']), len(data['codes'])))
        log.debug('start to recover Agent\'s worker: count->{}'.format(len(data['workers'])))

        # 恢复节点下工作的worker
        for worker in data['workers']:
            if node_service.start_worker(worker['worker_id'], worker['type'], worker['coroutine_num']).errno != 0:
                log.error('worker init failed: {worker_id} {type} {coroutine_num}'.format(**worker))
                return False

        log.info(' Agent\'s worker recover complete !! count->{}'.format(len(data['workers'])))
        return True
