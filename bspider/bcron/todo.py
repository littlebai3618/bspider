"""
这个是实际执行的方法，这个方法接收参数，通过参数决定行为
"""
import sys
import traceback

import yaml

from bspider.config import FrameSettings
from bspider.core import Project
from bspider.utils.database import MysqlClient
from bspider.utils.logger import LoggerPool
from bspider.utils.importer import import_module_by_code
from bspider.utils.notify import ding

__frame_settings = FrameSettings()
__mysql_client = MysqlClient.from_settings(__frame_settings['WEB_STUDIO_DB'])
__log = LoggerPool().get_logger(key='bcorn-todo', fn='bcorn', module='bcorn')


# def do(**kwargs):
#     # 这里使用主线程的时间循环，因为异步MYSQL使用默认时间循环
#     func = None
#     if kwargs.get('type') == 'operation':
#         func = run_operation_project
#     elif kwargs.get('type') == 'crawl':
#         func = run_spider_project
#     else:
#         __log.warning(f'WARNING: UNKNOW CRON JOB PARAMS: {kwargs}')
#
#     if func:
#         loop = asyncio.get_event_loop()
#         try:
#             future = asyncio.run_coroutine_threadsafe(func(**kwargs), loop)
#             loop.run_until_complete(future)
#             __log.debug('future run success!')
#         except Exception as e:
#             tp, msg, tb = sys.exc_info()
#             e_msg = '> '.join(traceback.format_exception(tp, msg, tb))
#             e.with_traceback(tb)
#             __log.error(f'thread event loop error:\n{e_msg}')
#             ding(f'> {e_msg} \n', 'bcron thread event loop')


def do(**kwargs):
    # 模式判断
    if kwargs.get('type') == 'operation':
        run_operation_project(**kwargs)
    elif kwargs.get('type', 'crawl') == 'crawl':
        run_spider_project(**kwargs)
    else:
        __log.warning(f'WARNING: UNKNOW CRON JOB PARAMS: {kwargs}')


def run_spider_project(project_id, code_id, **kwargs):
    """
    执行自动加载脚本的定时任务
    先检查定时任务状态，如果为1，就执行否则跳出
    :param self:
    :return:
    """
    __log.info(f'corn job: {project_id, code_id} run as crawl pattern')
    PROJECT_TABLE = __frame_settings['PROJECT_TABLE']
    sql = f'select `id`, `name`, `config`, `status` from {PROJECT_TABLE} where `id`="{project_id}"'

    infos = __mysql_client.select(sql)
    __log.debug(f'run spider_project cron_job select sql:{sql}')

    if not len(infos):
        __log.warning(f'project is not exist project_id:{project_id}, spider project job:{project_id}-{code_id}')
        ding(f'cron job error: \nproject is not exist project_id:{project_id}')

    info = infos[0]
    if info['status'] != 1:
        __log.warning(f'project_id:{project_id} is not run')
        # ding(f'spider project job:{project_name} is not run')

    run_status, run_msg = run_corn_job_code(code_id, info['id'], info['config'])
    __log.debug(info['config'])
    if run_status:
        __log.info(run_msg)
    else:
        __log.error(f'{run_msg}\narg:{kwargs}')
        ding(run_msg, 'crawl task')


def run_operation_project(code_id, **kwargs):
    run_status, run_msg = run_corn_job_code(
        code_id=code_id,
        project_id=0,
        do_type='operation')
    if run_status:
        __log.info(run_msg)
    else:
        __log.error(f'{run_msg}\narg:{kwargs}')
        ding(run_msg, 'operation task')


def run_corn_job_code(code_id, project_id, do_type, config: str = None):
    CODE_STORE_TABLE = __frame_settings['CODE_STORE_TABLE']
    sql = f'select `name`, `content` from {CODE_STORE_TABLE} where `id`="{code_id}"'
    tmp = __mysql_client.select(sql)
    if not len(tmp):
        return False, f'{code_id} is not exist in remote code store'
    content = tmp[0]['content']
    class_name = tmp[0]['name']
    mod = import_module_by_code(class_name, content)
    instance_arg = list()
    if hasattr(mod, class_name):
        if do_type == 'operation':
            instance_arg.append(LoggerPool().get_logger(
                key=f'bcorn-{class_name}',
                fn='bcorn',
                module='bcorn',
                project='operation'))
        else:
            try:
                project = Project(yaml.safe_load(config))
                project.project_id = project_id
                instance_arg.append(project)
                instance_arg.append(project.global_settings)
                instance_arg.append(LoggerPool().get_logger(
                    key=project.project_name,
                    fn='bcorn',
                    module='bcorn',
                    project=project.project_name))
            except Exception:
                tp, msg, tb = sys.exc_info()
                e_msg = '> '.join(traceback.format_exception(tp, msg, tb))
                return False, f'{project_id}-{code_id}:\n > {e_msg}'

        try:
            getattr(mod, class_name)(*instance_arg).execute_task()
            return True, f'{project_id}-{code_id} run succeed'
        except Exception:
            tp, msg, tb = sys.exc_info()
            e_msg = '> '.join(traceback.format_exception(tp, msg, tb))
            return False, f'{project_id}-{code_id} cron job run failed:\n > {e_msg}'

    return False, f'{project_id}-{code_id} don\'t have {class_name}'
