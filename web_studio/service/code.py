# @Time    : 2019/6/23 11:48 AM
# @Author  : 白尚林
# @File    : code
# @Use     :
from pymysql import IntegrityError

from core.api import BaseService
from core.api.exception import Conflict, NotFound
from core.api.resp import PostSuccess, PatchSuccess, PartialSuccess, DeleteSuccess, GetSuccess
from core.lib.remote_mixin import RemoteMixIn
from util.tools import change_dict_key
from web_studio.server import log
from web_studio.service.impl.code_impl import CodeImpl


class CodeService(BaseService, RemoteMixIn):

    def __init__(self):
        self.impl = CodeImpl()

    def add(self, name, description, code_type, content, editor):
        try:
            with self.impl.handler.session() as session:
                data = {
                    'name': name,
                    'description': description,
                    'type': code_type,
                    'content': content,
                    'editor': editor
                }
                code_id = session.insert(*self.impl.add_code(data=data))
            log.info(f'add code success:{name}-{editor}')
            return PostSuccess(msg='add code success', data={'code_id': code_id})
        except IntegrityError:
            log.error(f'add code failed:{name}-{editor} code is already exist')
            return Conflict(msg='code is already exist', errno=40002)

    def update(self, code_id, code_name, changes):
        if 'content' in changes:
            return self.__update_with_content(code_id, code_name, changes)
        else:
            with self.impl.handler.session() as session:
                session.update(*self.impl.update_code(code_id, changes))
            log.info('update code success')
            return PatchSuccess(msg='update code success')

    def __update_with_content(self, code_id, code_name, changes):
        project_list = self.impl.get_project_by_code_id(code_id)
        if len(project_list):
            with self.impl.handler.session() as session:
                session.update(*self.impl.update_code(code_id, changes))
                node_list = self.impl.get_nodes()
                data = {
                    'project_ids': ','.join([str(info['id']) for info in project_list]),
                    'code_name': code_name,
                    'code_type': changes['type'],
                    'content': changes['content']
                }
                result = self.op_update_code(node_list, data)
                if len(result):
                    if len(result) < len(node_list):
                        log.warning(f'not all node update code:{code_name} change {result}')
                        return PartialSuccess(msg=f'not all node update code:{code_name} change', data=result)
                    log.error(f'all node code:{code_name} update failed {result}')
                    raise Conflict(msg='all node code update failed', errno=40003, data=result)
                log.info(f'update code:{code_name} success')
                return PostSuccess(msg=f'update code:{code_name} success')
        else:
            with self.impl.handler.session() as session:
                session.update(*self.impl.update_code(code_id, changes))
            log.info(f'update code:{code_name} success')
            return PatchSuccess(msg='update code success')

    def delete(self, code_id):
        project_list = self.impl.get_project_by_code_id(code_id)
        if len(project_list):
            data = [{'id': info['id'], 'project_name': info['name']} for info in project_list]
            log.error(f'delete code:{code_id} failed: can\'t delete in use code')
            return Conflict(msg='can\'t delete in use code', data=data, errno=40004)
        else:
            self.impl.delete_code(code_id)
            log.info(f'success delete code:{code_id}')
            return DeleteSuccess()

    def get_code(self, code_id):
        infos = self.impl.get_code(code_id)
        if len(infos):
            project = []
            sign = set()
            for info in infos:
                if info['project_id'] and info['project_id'] not in sign:
                    project.append({'id': info['project_id'], 'name': info['project_name']})
                    sign.add(info['project_id'])
            infos[0].pop('project_id')
            infos[0].pop('project_name')
            infos[0]['project'] = project
            print(infos)
            return GetSuccess(msg='get code success', data=[infos[0]])
        else:
            return NotFound(msg='code is not exist', errno=40001)

    def get_codes(self, **param):
        param = change_dict_key('code_type', 'type', param)
        print(param)
        info = self.impl.get_codes(**param)
        return GetSuccess(msg='get code success', data=info)

