# @Time    : 2019/11/5 10:28 下午
# @Author  : baii
# @File    : base_operation
# @Use     : 系统运维任务基类
from bspider.core.custom_module import BaseCustomModule
from bspider.utils.exceptions import MethodError
from bspider.utils.logger import LoggerPool


class BaseOperation(BaseCustomModule):

    def __init__(self, settings: dict, project_name: str):
        self.log = LoggerPool().get_logger(key=project_name, fn='bcorn', module='bcorn', project=project_name)
        self.settings = settings
        self.project_name = project_name


    def execute_task(self):
        raise MethodError('you must rebuild execute_task()')
