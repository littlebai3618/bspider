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


def do(**kwargs):
    # 模式判断
    if kwargs.get('pattern') is None:
        run_spider_project(kwargs['class_name'], kwargs['project_name'])
    elif kwargs.get('pattern') == 'operation':
        run_operation_project(kwargs['class_name'], kwargs['project_name'])
    else:
        print(f'WARNING: UNKNOW CRON JOB PARAMS: {kwargs}')


def run_spider_project(class_name, project_name):
    """
    执行自动加载脚本的定时任务
    先检查定时任务状态，如果为1，就执行否则跳出
    :param self:
    :return:
    """
    log = LoggerPool().get_logger('bcorn', module='bcorn', project=project_name)
    log.info(f'corn_job: {project_name} run as spider pattern')
    PROJECT_TABLE = __frame_settings['PROJECT_TABLE']
    sql = f'select `config`, `status` from {PROJECT_TABLE} where `name`="{project_name}"'
    log.debug(f'run spider_project cron_job select sql:{sql}')

    infos = __handler.select(sql)
    if not len(infos):
        log.warning(f'spider project job:{project_name} is not exist')
        ding(f'cron job error: spider project job:{project_name} is not exist')

    info = infos[0]
    if info['status'] != 1:
        log.warning(f'spider project job:{project_name} is not run')
        ding(f'spider project job:{project_name} is not run')

    run_status, run_msg = run_corn_job_code(class_name, project_name, config=info['config'])
    if run_status:
        log.info(run_msg)
    else:
        log.error(run_msg)
        ding(run_msg)


def run_operation_project(class_name, project_name):
    log = LoggerPool().get_logger('bcorn', module='bcorn', project=project_name)
    run_status, run_msg = run_corn_job_code(class_name, project_name, config={"desc": "operation cron job"})
    if run_status:
        log.info(run_msg)
    else:
        log.error(run_msg)
        ding(run_msg)


def run_corn_job_code(class_name, project_name, config):
    CODE_STORE_TABLE = __frame_settings['CODE_STORE_TABLE']
    sql = f'select `content` from {CODE_STORE_TABLE} where `name`="{class_name}"'
    tmp = __handler.select(sql)
    if not len(tmp):
        return False, f'{project_name}:{class_name} is not exist in remote code store'
    content = tmp[0]['content']
    mod = import_module_by_code(class_name, content, project_name)
    if hasattr(mod, class_name):
        try:
            project_config = json.loads(config)
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            return False, f'{project_name}:{class_name} config\'type must json str:\n{e_msg}'
        try:
            instance = getattr(mod, class_name)(project_config, project_name)
            instance.execute_task()
            return True, f'{project_name}:{class_name} run succeed'
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = ''.join(traceback.format_exception(tp, msg, tb))
            return False, f'{project_name}:{class_name} cron job run failed:\n{e_msg}'
    return False, f'{project_name}:{class_name} don\'t have {class_name}'
