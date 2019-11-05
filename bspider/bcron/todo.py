# @Time    : 2019/6/15 5:55 PM
# @Author  : 白尚林
# @File    : do
# @Use     :
"""
这个是实际执行的方法，这个方法接收参数，通过参数决定行为
"""
import json
import sys
import traceback

from bspider.config import FrameSettings
from bspider.utils.database.mysql import MysqlHandler
from bspider.utils.logger import LoggerPool
from bspider.utils.importer import import_module_by_code
from bspider.utils.notify import ding

__frame_settings = FrameSettings()
__handler = MysqlHandler.from_settings(__frame_settings['WEB_STUDIO_DB'])
__log = LoggerPool().get_logger(key='bcorn-todo', module='bcorn')


def do(**kwargs):
    # 模式判断
    if kwargs.get('type', 'spider') == 'spider':
        run_spider_project(**kwargs)
    elif kwargs.get('type') == 'operation':
        run_operation_project(**kwargs)
    else:
        __log.warning(f'WARNING: UNKNOW CRON JOB PARAMS: {kwargs}')


def run_spider_project(project_id, code_id, **kwargs):
    """
    执行自动加载脚本的定时任务
    先检查定时任务状态，如果为1，就执行否则跳出
    :param self:
    :return:
    """
    __log.info(f'corn job: {project_id, code_id} run as spider pattern')
    PROJECT_TABLE = __frame_settings['PROJECT_TABLE']
    sql = f'select `name`, `config`, `status` from {PROJECT_TABLE} where `id`="{project_id}"'

    infos = __handler.select(sql)
    __log.debug(f'run spider_project cron_job select sql:{sql}')

    if not len(infos):
        __log.warning(f'project is not exist project_id:{project_id}, spider project job:{project_id}-{code_id}')
        ding(f'cron job error: \nproject is not exist project_id:{project_id}')

    info = infos[0]
    if info['status'] != 1:
        __log.warning(f'project_id:{project_id} is not run')
        # ding(f'spider project job:{project_name} is not run')

    run_status, run_msg = run_corn_job_code(code_id, **info)
    if run_status:
        __log.info(run_msg)
    else:
        __log.error(f'{run_msg}\narg:{kwargs}')
        ding(run_msg)


def run_operation_project(code_id, **kwargs):
    run_status, run_msg = run_corn_job_code(code_id, 'operation', '{"desc": "operation cron job"}')
    if run_status:
        __log.info(run_msg)
    else:
        __log.error(f'{run_msg}\narg:{kwargs}')
        ding(run_msg)


def run_corn_job_code(code_id, name, config):
    CODE_STORE_TABLE = __frame_settings['CODE_STORE_TABLE']
    sql = f'select `name`, `content` from {CODE_STORE_TABLE} where `id`="{code_id}"'
    tmp = __handler.select(sql)
    if not len(tmp):
        return False, f'{name}-code_id:{code_id} is not exist in remote code store'
    content = tmp[0]['content']
    class_name = tmp[0]['name']
    mod = import_module_by_code(class_name, content)
    if hasattr(mod, class_name):
        try:
            project_config = json.loads(config)
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            return False, f'{name}-{class_name} config\'s type must json str:\n{e_msg}'
        try:
            instance = getattr(mod, class_name)(project_config, name)
            instance.execute_task()
            return True, f'{name}-{class_name} run succeed'
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            return False, f'{name}-{class_name} cron job run failed:\n{e_msg}'
    return False, f'{name}-{class_name} don\'t have {class_name}'
