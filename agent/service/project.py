# @Time    : 2019-08-13 16:51
# @Author  : 白尚林
# @File    : project
# @Use     :
from agent import log
from core.api import BaseService
from core.api.resp import GetSuccess, PostSuccess, DeleteSuccess, PatchSuccess
from core.lib.project_cache import ProjectCache


class ProjectService(BaseService):

    def __init__(self):
        self.cache = ProjectCache()

    def add_project(self, project_id, project_name, project, rate, status):
        self.cache.set_project(project_id, project_name, project, rate, status)
        log.info(f'add project:{project_name}-{status} success')
        return PostSuccess()

    def get_projects(self):
        return GetSuccess(data=self.cache.get_projects())

    def get_project(self, project_id):
        return GetSuccess(data=self.cache.get_project(project_id))

    def update_project(self, project_id, changes):
        self.cache.update_project(project_id, changes)
        log.info(f'update project:{project_id} success')
        return PatchSuccess()

    def delete_project(self, project_id):
        self.cache.delete_project(project_id)
        log.info(f'delete project:{project_id} success')
        return DeleteSuccess()

    def get_weight(self):
        return GetSuccess(data=self.cache.get_weight())

    def set_weight(self, weight):
        self.cache.set_weight(weight)
        log.info(f'add weight:{weight}success')
        return PostSuccess()

    def update_code(self, project_ids, code_name, code_type, content):
        self.cache.update_code(project_ids, code_name, code_type, content)
        log.info(f'update project_code:{project_ids}success')
        return PatchSuccess()
