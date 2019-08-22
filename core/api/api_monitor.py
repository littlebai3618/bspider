# @Time    : 2019/7/9 4:47 PM
# @Author  : 白尚林
# @File    : api_monitor
# @Use     :
import json
from functools import wraps

from pymysql import IntegrityError

from core.downloader.async_downloader import AsyncDownloader
from core.lib import inner_settings
from core.parser.async_parser import AsyncParser
from util import RabbitMQHandler, MysqlHandler
from util.exception.exceptions import ProjectConfigError, DownloaderError, ParserError


class ApiMonitor(object):

    def __init__(self):
        self.mq_handler: RabbitMQHandler = inner_settings.RABBITMQ_MANAGER_HANDLER
        self.mysql_handler: MysqlHandler = inner_settings.WEB_STUDIO_DB_HANDLER
        self.project_table = inner_settings.PROJECT_TABLE

    def send_order(self, project_id, action, rate=None, config=None, run_test=False):
        """
        1. 执行代码可执行测试
        2. 向各子节点发送命令
        :return:
        """
        if action == 'add':
            project_name = project_id
        else:
            # 查询必须元素：
            sql = f'select `name`, `config`, `status`, `rate` from {self.project_table} where `id`={project_id}'
            info = self.mysql_handler.select(sql)[0]
            project_name = info['name']

            # 如果任务状态不是运行态并且 进行的操作不是 停止或启动 不需要向节点发送命令
            if info['status'] != 1 and action not in ['stop', 'start']:
                return

            if config is None:
                config = json.loads(info['config'])

            if rate is None:
                rate = int(info['rate'])

        # 可执行测试
        order = {
            'type': 'project_change',
            'action': action,
            'project_name': project_name,
            'config': config,
            'rate': rate
        }
        if run_test:
            try:
                AsyncDownloader(project_name, config['downloader_config'])
                AsyncParser(project_name, config['parser_config'])
            except KeyError as e:
                raise ProjectConfigError(f'配置文件不合法：{e}')

        self.mq_handler.send_message(
            exchange=inner_settings.EXCHANGE_NAME[3],
            routing_key='order',
            body=json.dumps(order)
        )

def order(func):
    @wraps(func)
    def check(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except IntegrityError:
            return 1, '内容已经存在'
        except DownloaderError as e:
            return 9, f'下载器中间件初始化异常 {e}'
        except ParserError as e:
            return 9, f'解析器中间件初始化异常 {e}'
        except ProjectConfigError as e:
            return 9, f'{e}'
        # except Exception as e:
        #     return -1, f'未知错误，操作失败{e}'
    return check