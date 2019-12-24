from pymysql import IntegrityError

from bspider.core import ProjectConfigParser
from bspider.utils.exceptions import ProjectConfigError
from bspider.master import log
from bspider.master.service.impl.project_impl import ProjectImpl
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

    def add(self, name, status, type, group, description, editor, rate, config):
        """
        1. 预执行配置文件方法
        2. 通知节点接收配置文件 调用接口
        2. 持久化project配置
        """
        pc_obj = self.__get_config_obj(config)
        log.debug(f'pc_opj->pipeline:{pc_obj.pipeline}, middleware:{pc_obj.middleware}')

        try:
            with self.impl.mysql_client.session() as session:
                data = {
                    'name': name,
                    'status': status,
                    'type': type,
                    'group': group,
                    'description': description,
                    'editor': editor,
                    'rate': rate,
                    'config': config,
                    'r_config': pc_obj.dumps()
                }
                project_id = session.insert(*self.impl.add_project(data), lastrowid=True)
                self.impl.bind_queue(project_id=project_id)
                log.debug(f'bind new project=>{name} queue success!')

                cids = pc_obj.middleware.copy() + pc_obj.pipeline.copy()
                log.debug(f'code num: {cids}')
                session.insert(*self.impl.add_project_binds(cids, project_id))
                info = {
                    'project_id': project_id,
                    'name': name,
                    'rate': rate,
                    'config': data['r_config'],
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
            if key in changes:
                if key == 'config':
                    remote_param['config'] = self.__get_config_obj(changes['config'])
                    changes['r_config'] = remote_param['config'].dumps()
                else:
                    remote_param[key] = changes[key]

        if len(remote_param):
            with self.impl.mysql_client.session() as session:
                session.update(*self.impl.update_project(project_id, changes))
                pc_obj = remote_param.get('config')
                if pc_obj:
                    cids = pc_obj.middleware.copy() + pc_obj.pipeline.copy()
                    log.debug(f'code num: {cids}')
                    session.insert(*self.impl.add_project_binds(cids, project_id))
                    remote_param['config'] = pc_obj.dumps()
                sign, result = self.op_update_project(self.impl.get_nodes(), project_id, remote_param)
                if not sign:
                    log.warning(f'not all node update project:project_id->{project_id} =>{result}')
                    return Conflict(msg=f'not all node update this project change', data=result, errno=30007)
        else:
            with self.impl.mysql_client.session() as session:
                session.update(*self.impl.update_project(project_id, changes))

        log.info(f'update project:project_id->{project_id} success')
        return PatchSuccess(msg=f'update project success')

    def delete(self, project_id):
        with self.impl.mysql_client.session() as session:
            session.delete(*self.impl.delete_project(project_id))
            session.delete(*self.impl.delete_project_binds(project_id))
            session.delete(*self.impl.delete_job(project_id))
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
        for info in infos:
            self.datetime_to_str(info)

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
