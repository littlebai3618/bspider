"""
@name=AutoClearOperation
@description=自动清理各种status表并保留近7天记录 保留最近7天记录
@type=operation
@editor=bspider
"""

import datetime

from bspider.bcron import BaseOperation
from bspider.config import FrameSettings
from bspider.utils.database import MysqlClient
from bspider.utils.notify import ding


class AutoClearOperation(BaseOperation):
    """
    自动清理各种status表并保留近7天记录
    """
    def execute_task(self):
        """do you work to produce start urls"""
        frame_settings = FrameSettings()
        tables = {
            frame_settings['DOWNLOADER_STATUS_TABLE']: '`project_id`,`project_name`,`sign`,`method`,`data`,`url`,`status`,`url_sign`,`exception`,`response`,`create_time`',
            frame_settings['PARSER_STATUS_TABLE']: '`project_id`,`project_name`,`sign`,`method`,`data`,`url`,`status`,`url_sign`,`exception`,`response`,`create_time`',
            frame_settings['NODE_STATUS_TABLE']: '`ip`,`memory`,`cpu`,`disk`,`create_time`',
        }
        handler = MysqlClient(frame_settings['WEB_STUDIO_DB'])
        msg = list()

        for table, fields in tables.items():
            try:

                with handler.session() as session:
                    for sql in [
                        f"create table {table}_new like {table};",
                        f"ALTER TABLE {table} RENAME TO {table}_bak;",
                        f"ALTER TABLE {table}_new RENAME TO {table};"
                    ]:
                        session.query(sql)

                start_time = datetime.datetime.now()
                stop_time = start_time - datetime.timedelta(days=7)

                while start_time > stop_time:
                    max_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
                    start_time = start_time - datetime.timedelta(minutes=20)
                    min_time = start_time.strftime('%Y-%m-%d %H:%M:%S')

                    sql = f"insert ignore into {table} ({fields}) " \
                          f"select {fields} from {table}_bak " \
                          f"where `create_time`> '{min_time}' AND `create_time`< '{max_time}';"

                    handler.insert(sql)

                    self.log.info(f"data {min_time} - {max_time} insert {table} success!")

                # 需要再优化
                delete_sql = f"DROP TABLE {table}_bak;"
                handler.delete(delete_sql)
                self.log.info(f'{table} clear success!')
            except Exception as e:
                msg.append(f'> {table} clear failed->{e}!')


        if len(msg):
            ding('\n'.join(msg), 'clear exception')
            self.log.info(f'send table clear exception alert msg: {msg}')
