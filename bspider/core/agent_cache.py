import os

from bspider.core.api import BaseImpl, json
from bspider.utils.conf import PLATFORM_PATH_ENV
from bspider.utils.database import SqlLite3Client


class AgentCache(object):

    def __init__(self):
        self.sqlite3_client = SqlLite3Client(os.path.join(os.environ[PLATFORM_PATH_ENV], '.cache', 'meta.db'))
        self.project_table = 'project_cache'
        self.project_weight_table = 'project_weight_cache'
        self.code_table = 'code_cache'
        self.data_source_table = 'data_source_cache'

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
        DROP table if exists {data_source_table};
        CREATE TABLE `{data_source_table}` (
            `name` varchar(50) PRIMARY KEY NOT NULL,
            `type` varchar(50) NOT NULL,
            `param` text NOT NULL,
            `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ); 
        """.format(
            code_table=self.code_table,
            project_weight_table=self.project_weight_table,
            project_table=self.project_table,
            data_source_table=self.data_source_table
        )
        for sql in sqls.split(';'):
            self.sqlite3_client.query(sql)
        return True, 'ok'

    def get_projects(self):
        sql = f'select `id`, `name`, `config`, `rate`, `timestamp` from {self.project_table} where `status`=1;'
        return [{'id': project_id, 'name': name, 'config': json.loads(config),
                 'rate': rate, 'timestamp': timestamp} for project_id, name, config, rate, timestamp in
                self.sqlite3_client.select(sql)]

    def get_project(self, project_id):
        sql = f'select `id`, `name`, `config`, `rate`, `timestamp`, `status` from project_cache where `id`={project_id};'
        return [{'id': project_id, 'name': name, 'config': json.loads(config),
                 'rate': rate, 'timestamp': timestamp, 'status': status} for
                project_id, name, config, rate, timestamp, status in
                self.sqlite3_client.select(sql)]

    def set_project(self, project_id: int, name: str, config: str, rate: int, status: int):
        sql = f"insert or replace into {self.project_table} values(?, ?, ?, ?, ?, datetime('now'))"
        return self.sqlite3_client.insert(sql, (project_id, name, rate, json.dumps(config), status))

    def delete_project(self, project_id: int):
        sql = f'delete from {self.project_table} where `id`={project_id}'
        return self.sqlite3_client.delete(sql)

    def update_project(self, project_id, data):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.project_table} set {fields} where `id` = {project_id};".replace('%s', '?')
        return self.sqlite3_client.update(sql, values)

    def get_codes(self):
        sql = f'select `id`, `content` from {self.code_table};'
        return [{'id': code_id, 'content': content} for code_id, content in self.sqlite3_client.select(sql)]

    def get_code(self, code_id):
        sql = f'select `id`, `content` from {self.code_table} where `id`={code_id};'
        return [{'id': code_id, 'content': content} for code_id, content in self.sqlite3_client.select(sql)]

    def set_code(self, code_id: int, content: str):
        sql = f"insert or replace into {self.code_table} values(?, ?, datetime('now'))"
        return self.sqlite3_client.insert(sql, (code_id, content))

    def delete_code(self, code_id: str):
        sql = f'delete from {self.code_table} where `id`={code_id}'
        return self.sqlite3_client.delete(sql)

    def update_code(self, code_id: int, data: dict , project: list):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.code_table} set {fields} where `id` = {code_id};".replace('%s', '?')
        self.sqlite3_client.update(sql, values)
        # 在更新代码的时候 更新project 的时间
        for project_id in project:
            sql = f"update {self.project_table} set `timestamp`= CURRENT_TIMESTAMP where `id` = {project_id}"
            self.sqlite3_client.update(sql)


    def get_data_sources(self):
        sql = f'select `name`, `type`, `param` from {self.data_source_table};'
        return [{'name': name,'type': type, 'param': json.loads(param)} for name, type, param in self.sqlite3_client.select(sql)]

    def get_data_source(self, name: str):
        sql = f'select `name`, `type`, `param` from {self.data_source_table} where `name`=?;'
        return [{'name': name,'type': type, 'param': json.loads(param)} for name, type, param in self.sqlite3_client.select(sql, (name,))]

    def set_data_source(self, name: str, type: str, param: dict):
        sql = f"insert or replace into {self.data_source_table} values(?, ?, ?, datetime('now'))"
        return self.sqlite3_client.insert(sql, (name, type, json.dumps(param)))

    def delete_data_source(self, name: str):
        sql = f'delete from {self.data_source_table} where `name`=?'
        return self.sqlite3_client.delete(sql, (name,))

    def update_data_source(self, name: str, data: dict , project: list):
        fields, values = BaseImpl.make_fv(data)
        sql = f"update {self.data_source_table} set {fields} where `name` = '{name}';".replace('%s', '?')
        self.sqlite3_client.update(sql, values)
        # 在更新代码的时候 更新project 的时间
        for project_id in project:
            sql = f"update {self.project_table} set `timestamp`= CURRENT_TIMESTAMP where `id` = {project_id}"
            self.sqlite3_client.update(sql)
