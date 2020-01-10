from bspider.agent import log
from bspider.core import AgentCache
from bspider.core.api import BaseService, GetSuccess, PostSuccess, DeleteSuccess, PatchSuccess


class CodeService(BaseService):

    def __init__(self):
        self.cache = AgentCache()

    def add_code(self, code_id, content):
        self.cache.set_code(code_id, content)
        log.info(f'add code:code_id->{code_id} success')
        return PostSuccess()

    def get_codes(self):
        return GetSuccess(data=self.cache.get_codes())

    def get_code(self, code_id):
        return GetSuccess(data=self.cache.get_code(code_id))

    def update_code(self, code_id, changes):
        project = changes.pop('project')
        self.cache.update_code(code_id, changes, project)
        log.info(f'update code:code_id->{code_id} success')
        return PatchSuccess()

    def delete_code(self, code_id):
        self.cache.delete_code(code_id)
        log.info(f'delete code:code_id->{code_id} success')
        return DeleteSuccess()
