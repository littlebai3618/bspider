# @Time    : 2019-08-15 16:22
# @Author  : 白尚林
# @File    : server
# @Use     :
import sys
import traceback

from flask import Flask
from werkzeug.exceptions import HTTPException

from agent import log
from config import frame_settings
from core.api.exception import APIException
from core.lib.connection import Connection
from core.lib.project_cache import ProjectCache
from config.node_settings import IP, NAME, DESC
from agent.controller.project import project
from agent.controller.node import node
from util import singleton


@singleton
class CreateApp(object):

    def __init__(self):
        self.__register(IP, NAME, DESC)
        log.info('register job success!')

    @staticmethod
    def app():
        app = Flask(__name__)
        app.secret_key = frame_settings.WEB_SECRET_KEY
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

        return app

    @staticmethod
    def __register(ip, name, desc):
        cache = ProjectCache()
        client = Connection()
        if cache.initialization():
            infos = client.agent_register(data={'node_ip': ip, 'name': name, 'desc': desc})
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
