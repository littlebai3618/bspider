# @Time    : 2019/6/20 8:06 PM
# @Author  : 白尚林
# @File    : project
# @Use     :
from pymysql import IntegrityError

from bspider.core import ProjectConfigParser
from bspider.utils.exceptions import ProjectConfigError
from bspider.web_studio import log
from bspider.web_studio.service.impl.project_impl import ProjectImpl
from bspider.core.api import BaseService, Conflict, NotFound, PostSuccess, DeleteSuccess, GetSuccess, \
    PatchSuccess, ParameterException, AgentMixIn


class ProjectService(BaseService, AgentMixIn):

    def __init__(self):
        self.impl = ProjectImpl()

    def __get_config_obj(self, config: str) -> ProjectConfigParser:
        try:
            pc_obj = ProjectConfigParser.loads(config)
        except ProjectConfigError as e:
            raise Conflict(errno=30003, msg=f'{e}')

        # 检测中间件是否存在并将code_name 映射为code_id
        middleware_dict = {info['name']: info['id'] for info in
                           self.impl.get_middleware_by_code_name(pc_obj.middleware)}
        if len(middleware_dict) != len(pc_obj.middleware):
            raise Conflict(
                msg='lack of necessary middleware!',
                data=[code_name for code_name in pc_obj.middleware if code_name not in middleware_dict],
                errno=30003)

        pipeline_dict = {info['name']: info['id'] for info in self.impl.get_pipeline_by_code_name(pc_obj.pipeline)}
        if len(pipeline_dict) != len(pc_obj.pipeline):
            raise Conflict(
                msg='lack of necessary pipeline!',
                data=[code_name for code_name in pc_obj.pipeline if code_name not in pipeline_dict],
                errno=30003)

        pc_obj.pipeline = [str(pipeline_dict[code_name]) for code_name in pc_obj.pipeline]
        pc_obj.middleware = [str(middleware_dict[code_name]) for code_name in pc_obj.middleware]
        return pc_obj

    def add(self, name, status, project_type, group, description, editor, rate, config):
        """
        1. 预执行配置文件方法
        2. 通知节点接收配置文件 调用接口
        2. 持久化project配置
        """
        pc_obj = self.__get_config_obj(config)

        try:
            with self.impl.handler.session() as session:
                self.impl.bind_queue(project_name=name)
                log.debug(f'bind new project:{name} queue success!')

                data = {
                    'name': name,
                    'status': status,
                    'type': project_type,
                    'group': group,
                    'description': description,
                    'editor': editor,
                    'rate': rate,
                    'config': config
                }
                project_id = session.insert(*self.impl.add_project(data), lastrowid=True)
                self.impl.add_project_binds(pc_obj.middleware.extend(pc_obj.pipeline), project_id)
                info = {
                    'project_id': project_id,
                    'name': name,
                    'rate': rate,
                    'config': pc_obj.dumps(),
                    'status': status
                }
                node_list = self.impl.get_nodes()
                sign, result = self.op_add_project(node_list, info)
                if not sign:
                    log.error(f'not all node add project:{name} =>{result}')
                    return Conflict(msg=f'not all node add project:{name}', data=result, errno=30007)
                log.info(f'add project:{name} success')
                return PostSuccess(msg=f'add project:{name} success', data={'project_id': project_id})
        except IntegrityError as e:
            if e.args[0] == 1062:
                log.error(f'all project add failed:{name} =>project is already exist')
                return Conflict(errno=30002, msg='project is already exist')
            raise e

    def update(self, project_id, changes):
        remote_param = {}
        for key in ('name', 'config', 'rate', 'status'):
            if key in changes and key == 'config':
                remote_param['config'] = self.__get_config_obj(changes['config']).dumps()
            else:
                remote_param[key] = changes[key]

        if len(remote_param):
            with self.impl.handler.session() as session:
                session.update(*self.impl.update_project(project_id, changes))
                sign, result = self.op_update_project(self.impl.get_nodes(), project_id, remote_param)
                if not sign:
                    log.warning(f'not all node update project:project_id->{project_id} =>{result}')
                    return Conflict(msg=f'not all node update this project change', data=result, errno=30007)
        else:
            with self.impl.handler.session() as session:
                session.update(*self.impl.update_project(project_id, changes))

        log.info(f'update project:project_id->{project_id} success')
        return PatchSuccess(msg=f'update project success')

    def delete(self, project_id):
        with self.impl.handler.session() as session:
            session.update(*self.impl.delete_project(project_id))
            sign, result = self.op_delete_project(self.impl.get_nodes(), project_id)
            if not sign:
                log.error(f'all project delete failed:{project_id} =>{result}')
                raise Conflict(msg='project delete failed', data=result, errno=30007)
            log.info(f'delete project:{project_id} success')
            if self.impl.unbind_queue(project_id):
                return DeleteSuccess()
            else:
                raise Conflict(msg='project\'s queue is not exist', errno=30001)

    def get(self, project_id):
        infos = self.impl.get_project(project_id)
        if len(infos):
            return GetSuccess(data=infos[0])
        else:
            return NotFound(msg='project not exist', errno=30001)

    def gets(self, page, limit, search, sort):
        if sort.upper() not in ['ASC', 'DESC']:
            return ParameterException(msg='sort must `asc` or `desc`')

        infos, total = self.impl.get_projects(page, limit, search, sort)

        for info in infos:
            self.datetime_to_str(info)

        return GetSuccess(
            msg='get user list success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })
