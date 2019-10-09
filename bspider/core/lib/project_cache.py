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


class ProjectCache(object):

    def __init__(self):
        self.handler = SqlLite3Handler(os.path.join(os.environ[PLATFORM_PATH_ENV], 'cache', 'meta.db'))

    def initialization(self) -> bool:
        """初始化bdb"""
        sqls = """
        DROP table if exists project_cache;
        CREATE TABLE `project_cache` (
            `id` int(11) PRIMARY KEY NOT NULL,
            `name` varchar(50) NOT NULL,
            `rate` int(10) NOT NULL,
            `config` text NOT NULL,
            `status` int(2) NOT NULL,
            `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        ); 
        CREATE UNIQUE INDEX `idx_name` on project_cache (`name`);
        CREATE UNIQUE INDEX `idx_id` on project_cache (`id`);
        DROP table if exists project_weight_cache;
        CREATE TABLE `project_weight_cache` (
            `weight_id` int(11) PRIMARY KEY NOT NULL,
            `project_weight` text NOT NULL,
            `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        for sql in sqls.split(';'):
            self.handler.query(sql)
        return True

    def get_projects(self):
        sql = 'select `id` as `project_id`, `name`, `config`, `rate`, `timestamp` from project_cache where `status`=1;'
        return [{'project_id': project_id, 'project_name': project_name, 'config': zlib.decompress(project).decode(),
                 'rate': rate, 'timestamp': timestamp} for project_id, project_name, project, rate, timestamp in
                self.handler.select(sql)]

    def get_project(self, project_id):
        sql = f'select `id` as `project_id`, `name`, `config`, `rate`, `timestamp`, `status` from project_cache where `id`={project_id};'
        return [{'project_id': project_id, 'project_name': project_name, 'config': zlib.decompress(project).decode(),
                 'rate': rate, 'timestamp': timestamp, 'status': status} for
                project_id, project_name, project, rate, timestamp, status in
                self.handler.select(sql)]

    def set_project(self, project_id: int, project_name: str, config: str, rate: int, status: int):
        sql = f"insert or replace into project_cache values(?, ?, ?, ?, ?, datetime('now'))"
        return self.handler.insert(sql, (project_id, project_name, rate, zlib.compress(config.encode()), status))

    def delete_project(self, project_id: int):
        sql = f'delete from project_cache where `id`={project_id}'
        return self.handler.delete(sql)

    def update_project(self, project_id, data):
        if 'config' in data:
            data['config'] = zlib.compress(data['config'].encode())
        fields, values = BaseImpl.make_fv(data)
        sql = f"update project_cache set {fields} where `id` = {project_id};".replace('%s', '?')
        return self.handler.update(sql, values)

    def update_code(self, project_ids, code_name, code_type, content):
        if 'downloader' in code_type:
            key1, key2 = 'downloader_config', 'middlewares'
        else:
            key1, key2 = 'parser_config', 'pipelines'
        for project_id in project_ids:
            info = json.loads(self.get_project(project_id))[0]['content']
            if info[0]:
                mods = info[key1][key2]
                for i, mod in enumerate(mods):
                    if mod[0] == code_name:
                        mods[i] = content
                        break
                self.update_project(project_id, {'project': json.dumps(info)})

    def get_weight(self):
        sql = 'select `project_weight` from project_weight_cache'
        info = self.handler.select(sql)
        if len(info):
            return json.loads(info[0][0])

    def set_weight(self, weight: dict):
        weight = json.dumps(weight)
        sql = f'insert or replace into project_weight_cache values(1, "{weight}");'
        return self.handler.insert(sql)


if __name__ == '__main__':
    print(ProjectCache().handler.query('.databases'))
