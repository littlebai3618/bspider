# @Time    : 2019-08-15 16:22
# @Author  : 白尚林
# @File    : server
# @Use     :
import sys
import traceback

from flask import Flask
from werkzeug.exceptions import HTTPException

from bspider.agent import log
from bspider.core.api import APIException
from bspider.core.lib import ProjectCache, Connection
from bspider.config import FrameSettings
from bspider.agent.controller.project import project
from bspider.agent.controller.node import node
from bspider.utils import singleton


@singleton
class CreateApp(object):

    def __init__(self):
        self.frame_settings = FrameSettings()
        self.client = Connection(self.frame_settings['MASTER'])

    def app(self):
        app = Flask(__name__)
        app.secret_key = self.frame_settings['WEB_SECRET_KEY']
        app.register_blueprint(node)
        app.register_blueprint(project)

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

        self.__register(**self.frame_settings['AGENT'])
        log.info('register job success!')
        return app

    def __register(self, ip, name, description, port):
        cache = ProjectCache()
        if cache.initialization():
            infos = self.client.agent_register(data={'node_ip': ip, 'name': name, 'desc': description, 'port': port})
            if infos['errno'] == 0:
                for project in infos['data']:
                    if not cache.set_project(**project):
                        log.error('project cache init failed')
                        raise Exception('project cache init failed')
            else:
                log.error('master server error:{}'.format(infos))
                raise Exception('master server error')
        del cache
        return True
