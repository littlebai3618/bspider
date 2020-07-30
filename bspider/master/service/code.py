from pymysql import IntegrityError

from bspider.core.api import BaseService, Conflict, NotFound, PostSuccess, PatchSuccess, DeleteSuccess, \
    GetSuccess, ParameterException
from bspider.core.api import AgentMixIn
from bspider.master.server import log
from bspider.master.service.impl.code_impl import CodeImpl


class CodeService(BaseService, AgentMixIn):

    def __init__(self):
        self.impl = CodeImpl()

    def add(self, content, editor):
        name, code_type, description, code = content
        try:
            with self.impl.mysql_client.session() as session:
                data = {
                    'name': name,
                    'description': description,
                    'type': code_type,
                    'content': code,
                    'editor': editor
                }
                code_id = session.insert(*self.impl.add_code(data=data, get_sql=True))

                sign, result = self.op_add_code(self.impl.get_all_node_ip(), {'code_id': code_id, 'content': code})
                if not sign:
                    log.warning(f'not all node add code:{name} =>{result}')
                    raise Conflict(msg=f'not all node add code:{name}', data=result, errno=40006)
            log.info(f'add code success:{name}-{editor}')
            return PostSuccess(msg='add code success', data={'code_id': code_id})
        except IntegrityError:
            log.error(f'add code failed:{name}-{editor} code is already exist')
            return Conflict(msg='code is already exist', errno=40002)

    def update(self, code_id, content, editor):
        info = self.impl.get_code(code_id)
        if not len(info):
            return NotFound(msg='code is not exist', errno=40001)

        project = [str(project['id']) for project in info['project']]
        update_info = dict()

        with self.impl.mysql_client.session() as session:
            name, code_type, description, code = content
            if name != info['name']:
                update_info['name'] = name

            if editor != info['editor']:
                update_info['editor'] = editor

            if code_type != info['type']:
                update_info['type'] = code_type

            if description != info['description']:
                update_info['description'] = description

            if code != info['content']:
                if len(project):
                    # 优化，进当有project 使用时通知分节点同步消息
                    sign, result = self.op_update_code(
                        ip_list=self.impl.get_all_node_ip(),
                        code_id=code_id,
                        data={'content': code, 'project': ','.join(project)})
                    if not sign:
                        log.warning(f'code:code_id->:{code_id} update exception')
                        raise Conflict(msg=f'update code:code_id->:{code_id} failed', data=result, errno=40006)
                update_info['content'] = code

            session.update(*self.impl.update_code(code_id, update_info))
        log.info(f'update code success: {update_info}')
        return PatchSuccess(msg='update code success')

    def delete(self, code_id):
        project_list = self.impl.get_project_by_code_id(code_id)
        if len(project_list):
            log.error(f'delete code:{code_id} failed: can\'t delete in use code')
            return Conflict(msg='can\'t delete in use code', data=project_list, errno=40004)
        else:
            with self.impl.mysql_client.session() as session:
                sign, result = self.op_delete_code(self.impl.get_all_node_ip(), code_id)
                if not sign:
                    log.warning(f'code:code_id->:{code_id} delete exec')
                    raise Conflict(msg=f'not all code:code_id->:{code_id} was delete', data=result, errno=40006)
                session.delete(*self.impl.delete_code(code_id))
            log.info(f'success delete code:{code_id}')
            return DeleteSuccess()

    def get_code(self, code_id):
        info = self.impl.get_code(code_id)
        if len(info):
            return GetSuccess(msg='get code success', data=info)
        else:
            return NotFound(msg='code is not exist', errno=40001)

    def get_codes(self, page, limit, search, sort):
        if sort.upper() not in ['ASC', 'DESC']:
            return ParameterException(msg='sort must `asc` or `desc`')

        infos, total = self.impl.get_codes(page, limit, search, sort)

        for info in infos:
            self.datetime_to_str(info)

        return GetSuccess(
            msg='get code list success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })
