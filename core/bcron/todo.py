# @Time    : 2019/6/15 5:55 PM
# @Author  : 白尚林
# @File    : do
# @Use     :
"""
这个是实际执行的方法，这个方法接收参数，通过参数决定行为
"""
import json

from config.frame_settings import WEB_STUDIO_DB
from core.lib import PROJECT_TABLE, CODE_STORE_TABLE
from util.database.mysql import MysqlHandler
from util.logger import LoggerPool
from util.moduler import ModuleImporter
from util.notify import ding


def do(**kwargs):
    # 模式判断
    if kwargs.get('model') is None:
        run_custom_code(kwargs['class_name'], kwargs['project_name'])

def run_custom_code(class_name, project_name):
    """
    执行自动加载脚本的定时任务
    先检查定时任务状态，如果为1，就执行否则跳出
    :param self:
    :return:
    """
    log = LoggerPool().get_logger('bcorn', module='bcorn', project=project_name)
    sql = f'select `config`, `status` from {PROJECT_TABLE} where `name`="{project_name}"'
    log.debug(f'run custom_code select sql:{sql}')
    handler = MysqlHandler.from_settings(WEB_STUDIO_DB)

    info = handler.select(sql)
    if len(info) == 1: 
        if info[0]['status'] == 0:
            log.warning('job is not run because project {} is stop'.format(project_name))
            return
        config = info[0]['config']
        sql = f'select `content` from {CODE_STORE_TABLE} where `name`="{class_name}"'
        tmp = handler.select(sql)
        if len(tmp):
            content = tmp[0]['content']
            mod = ModuleImporter.import_module(class_name, content, project_name)
            if hasattr(mod, class_name):
                try:
                    instance = getattr(mod, class_name)(json.loads(config), project_name)
                    instance.execute_task()
                    log.info(f'{project_name}:{class_name} run succeed')
                except Exception as e:
                    log.error(f'bcorn {class_name} run execute_task() {e}')
                    ding(msg=f'{project_name}的定时任务在执行 {class_name}.execute_task() 发生异常 {e}')
        else:
            log.error(f'{project_name}的定时任务未能找到代码：{class_name}')
            ding(msg=f'{project_name}的定时任务未能找到代码：{class_name}')
    else:
        log.warning(f'not found {project_name}:{class_name} from remote store {PROJECT_TABLE}!')