import json

from bspider.agent import log
from bspider.core.api import BaseService, GetSuccess, PostSuccess, DeleteSuccess, PatchSuccess
from bspider.core import AgentCache
from bspider.utils.database import valid


class DataSourceService(BaseService):

    def __init__(self):
        self.cache = AgentCache()

    def add_data_source(self, name: str, type: str, param: dict):
        if valid(conn_type=type, param=param):
            self.cache.set_data_source(name, type, param)
            log.info(f'add data_source:data_source_name->{name} success')
            return PostSuccess()

    def get_data_sources(self):
        return GetSuccess(data=self.cache.get_data_sources())

    def get_data_source(self, name: str):
        return GetSuccess(data=self.cache.get_data_source(name))

    def update_data_source(self, name: str, changes):
        project = changes.pop('project')
        if valid(conn_type=changes['type'], param=changes['param']):
            self.cache.update_data_source(name, changes, project)
            log.info(f'update data_source:{name} success')
            return PatchSuccess()

    def delete_data_source(self, name: str):
        self.cache.delete_data_source(name)
        log.info(f'delete data_source:{name} success')
        return DeleteSuccess()
