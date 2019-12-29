from bspider.core.custom_module import BaseCustomModule
from bspider.utils.exceptions import MethodError


class BaseOperation(BaseCustomModule):

    def execute_task(self):
        raise MethodError('you must rebuild execute_task()')
