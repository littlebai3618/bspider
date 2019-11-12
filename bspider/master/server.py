# @Time    : 2019-08-15 16:24
# @Author  : 白尚林
# @File    : server
# @Use     :
import sys
import traceback

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from bspider.config import FrameSettings
from bspider.core.api import APIException
from bspider.master import log
from bspider.master.controller.cron import cron
from bspider.master.controller.code import code
from bspider.master.controller.project import project
from bspider.master.controller.node import node
from bspider.master.controller.user import user
from bspider.master.controller.tools import tools


def create_app():
    app = Flask(__name__)
    CORS(app)
    frame_settings = FrameSettings()
    app.secret_key = frame_settings['WEB_SECRET_KEY']
    # 用户管理模块
    app.register_blueprint(user)
    # project管理模块
    app.register_blueprint(project)
    # 节点管理模块
    app.register_blueprint(node)
    # code管理模块
    app.register_blueprint(code)
    # cron_job
    app.register_blueprint(cron)
    # tools
    app.register_blueprint(tools, url_prefix="/tools")

    @app.errorhandler(Exception)
    def framework_error(error):
        if isinstance(error, APIException):
            return error
        if isinstance(error, HTTPException):
            return APIException(error.code, error.description, 10000)
        tp, msg, tb = sys.exc_info()
        e_msg = ''.join(traceback.format_exception(tp, msg, tb))
        log.error(e_msg)
        return APIException(msg=str(error))

    return app