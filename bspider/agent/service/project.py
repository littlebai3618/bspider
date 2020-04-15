from bspider.agent import log
from bspider.core.api import BaseService, GetSuccess, PostSuccess, DeleteSuccess, PatchSuccess
from bspider.core import AgentCache


class ProjectService(BaseService):

    def __init__(self):
        self.cache = AgentCache()

    def add_project(self, project_id, name, config, rate, status):
        self.cache.set_project(project_id, name, config, rate, status)
        log.info(f'add project:project_id->{project_id} project_name->{name} {status} success')
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
