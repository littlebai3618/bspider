# @Time    : 2019-07-29 15:11
# @Author  : 白尚林
# @File    : project_cache
# @Use     :
import json
import os
import zlib

from bspider.core.api import BaseImpl
from bspider.utils.conf import PLATFORM_PATH_ENV
from bspider.utils.database import SqlLite3Handler


class AgentCache(object):

    def __init__(self):
        self.handler = SqlLite3Handler(os.path.join(os.environ[PLATFORM_PATH_ENV], 'cache', 'meta.db'))
        self.project_table = 'project_cache'
        self.project_weight_table = 'project_weight_cache'
        self.code_table = 'code_table'

    def initialization(self) -> (bool, str):
        """初始化bdb"""
        sqls = """
        DROP table if exists {project_table};
        CREATE TABLE `{project_table}` (
            `id` int(11) PRIMARY KEY NOT NULL,
            `name` varchar(50) NOT NULL,
            `rate` int(10) NOT NULL,
            `config` text NOT NULL,
            `status` int(2) NOT NULL,
            `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ); 
        CREATE UNIQUE INDEX `idx_name` on {project_table} (`name`);
        CREATE UNIQUE INDEX `idx_id` on {project_table} (`id`);
        DROP table if exists {project_weight_table};
        CREATE TABLE `{project_weight_table}` (
            `weight_id` int(11) PRIMARY KEY NOT NULL,
            `project_weight` text NOT NULL,
            `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        DROP table if exists {code_table};
        CREATE TABLE `{code_table}` (
            `id` int(11) PRIMARY KEY NOT NULL,
            `content` text NOT NULL,
            `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ); 
        """.format(
            code_table=self.code_table,
            project_weight_table=self.project_weight_table,
            project_table=self.project_table
        )
        for sql in sqls.split(';'):
            self.handler.query(sql)
        return True, 'ok'

    def get_projects(self):
        sql = f'select `id`, `name`, `config`, `rate`, `timestamp` from {self.project_table} where `status`=1;'
        return [{'id': project_id, 'name': name, 'config': config,
                 'rate': rate, 'timestamp': timestamp} for project_id, name, config, rate, timestamp in
                self.handler.select(sql)]

    def get_project(self, project_id):
        sql = f'select `id`, `name`, `config`, `rate`, `timestamp`, `status` from project_cache where `id`={project_id};'
        return [{'id': project_id, 'name': name, 'config': config,
                 'rate': rate, 'timestamp': timestamp, 'status': status} for
                project_id, name, config, rate, timestamp, status in
                self.handler.select(sql)]

    def set_project(self, project_id: int, name: str, config: str, rate: int, status: int):
        sql = f"insert or replace into {self.project_table} values(?, ?, ?, ?, ?, datetime('now'))"
        return self.handler.insert(sql, (project_id, name, rate, config, status))

    def delete_project(self, project_id: int):
        sql = f'delete from {self.project_table} where `id`={project_id}'
        return self.handler.delete(sql)

    def update_project(self, project_id, data):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update project_cache set {fields} where `id` = {project_id};".replace('%s', '?')
        return self.handler.update(sql, values)

    def get_codes(self):
        sql = f'select `id`, `content` from {self.code_table};'
        return [{'id': code_id, 'content': content} for code_id, content in self.handler.select(sql)]

    def get_code(self, code_id):
        sql = f'select `id`, `content` from {self.code_table} where `id`={code_id};'
        return [{'id': code_id, 'content': content} for code_id, content in self.handler.select(sql)]

    def set_code(self, code_id: int, content: str):
        sql = f"insert or replace into {self.code_table} values(?, ?, datetime('now'))"
        return self.handler.insert(sql, (code_id, content))

    def delete_code(self, code_id: str):
        sql = f'delete from {self.code_table} where `id`={code_id}'
        return self.handler.delete(sql)

    def update_code(self, code_id, data):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.code_table} set {fields} where `id` = {code_id};".replace('%s', '?')
        return self.handler.update(sql, values)

    # def update_code(self, project_ids, code_name, code_type, content):
    #     if 'downloader' in code_type:
    #         key1, key2 = 'downloader_config', 'middlewares'
    #     else:
    #         key1, key2 = 'parser_config', 'pipelines'
    #     for project_id in project_ids:
    #         info = json.loads(self.get_project(project_id))[0]['content']
    #         if info[0]:
    #             mods = info[key1][key2]
    #             for i, mod in enumerate(mods):
    #                 if mod[0] == code_name:
    #                     mods[i] = content
    #                     break
    #             self.update_project(project_id, {'project': json.dumps(info)})

    # def get_weight(self):
    #     sql = 'select `project_weight` from project_weight_cache'
    #     info = self.handler.select(sql)
    #     if len(info):
    #         return json.loads(info[0][0])
    #
    # def set_weight(self, weight: dict):
    #     weight = json.dumps(weight)
    #     sql = f'insert or replace into project_weight_cache values(1, "{weight}");'
    #     return self.handler.insert(sql)
