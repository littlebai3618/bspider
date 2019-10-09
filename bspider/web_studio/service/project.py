# @Time    : 2019/6/20 8:06 PM
# @Author  : 白尚林
# @File    : project
# @Use     :
import json

from pymysql import IntegrityError

from bspider.core.api import BaseService, Conflict, NotFound, PartialSuccess, PostSuccess, DeleteSuccess, GetSuccess, PatchSuccess
from bspider.core.lib import RemoteMixIn
from bspider.web_studio import log
from bspider.web_studio.service.impl.project_impl import ProjectImpl


class ProjectService(BaseService, RemoteMixIn):

    def __init__(self):
        self.impl = ProjectImpl()

    def check_config(self, name, config):
        middleware, pipeline, cfg = self.config_parser(config)
        cid = []
        mws_code = {}
        for info in self.impl.get_middlewares_by_code_name(middleware):
            cid.append(info['id'])
            mws_code[info['name']] = info['content']

        if len(middleware) != len(mws_code):
            result = []
            for mw in middleware:
                if mw not in mws_code:
                    result.append(mw)
            raise Conflict(msg='lack of necessary middleware!', data=result, errno=30003)

        pipe_code = {}
        for info in self.impl.get_pipeline_by_code_name(pipeline):
            cid.append(info['id'])
            pipe_code[info['name']] = info['content']
        if len(pipeline) != len(pipe_code):
            result = []
            for pipe in pipeline:
                if pipe not in pipe_code:
                    result.append(pipe)
            raise Conflict(msg='lack of necessary pipeline!', data=result, errno=30003)
        return self.make_remote_config(cfg, mws_code, pipe_code, name), cid

    def add_project(self, name, status, project_type, group, description, editor, rate, config):
        """
        1. 预执行配置文件方法
        2. 通知节点接收配置文件 调用接口
        2. 持久化project配置
        """
        cfg, cids = self.check_config(name, config)
        self.impl.bind_queue(project_name=name)
        log.info(f'bind now project:{name} queue success!')
        try:
            with self.impl.handler.session() as session:
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
                self.impl.add_project_binds(cids, project_id)
                info = {'project_id': project_id, 'project_name': name, 'rate': rate, 'config': json.dumps(cfg),
                        'status': status}
                node_list = self.impl.get_nodes()
                result = self.op_add_project(node_list, info)
                if len(result):
                    if len(result) < len(node_list):
                        log.warning(f'not all node add project:{name} =>{result}')
                        return PartialSuccess(msg=f'not all node add project:{name}', data=result)
                    log.error(f'all project add failed:{name} =>{result}')
                    raise Conflict(msg='all project add failed', data=result, errno=30004)
                log.info(f'add project:{name} success')
                return PostSuccess(msg=f'add project:{name} success', data={'project_id': project_id})
        except IntegrityError as e:
            if e.args[0] == 1062:
                log.error(f'all project add failed:{name} =>project is already exist')
                return Conflict(errno=30002, msg='project is already exist')
            raise e

    def update(self, project_id, project_name, changes):
        if 'config' in changes:
            return self.__update_with_config(project_id, project_name, changes)
        elif 'rate' in changes or 'status' in changes:
            return self.__update_with_remote_param(project_id, project_name, changes)
        else:
            return self.__update(project_id, project_name, changes)

    def __update_with_config(self, project_id, project_name, changes):
        cfg, cids = self.check_config(project_name, changes['config'])
        with self.impl.handler.session() as session:
            session.update(*self.impl.update_project(project_id, changes))
            session.delete(self.impl.delete_project_binds(project_id))
            session.insert(self.impl.add_project_binds(cids, project_id))
            node_list = self.impl.get_nodes()
            info = {'config': json.dumps(cfg), 'project_id': project_id}
            if 'rate' in changes:
                info['rate'] = changes['rate']
            if 'status' in changes:
                info['status'] = changes['status']
            result = self.op_update_project(node_list, info)
            if len(result):
                if len(result) < len(node_list):
                    log.warning(f'not all node update project:{project_name} =>{result}')
                    return PartialSuccess(msg=f'not all node update project:{project_name}', data=result)
                log.error(f'all project update failed:{project_name} =>{result}')
                raise Conflict(msg='all project update failed', data=result, errno=30005)
            log.info(f'update project:{project_name} success')
            return PatchSuccess(msg=f'update project:{project_name} success', data={'project_id': project_id})

    def __update_with_remote_param(self, project_id, project_name, changes):
        with self.impl.handler.session() as session:
            session.update(*self.impl.update_project(project_id, changes))
            node_list = self.impl.get_nodes()
            info = {'project_id': project_id}
            if 'rate' in changes:
                info['rate'] = changes['rate']
            if 'status' in changes:
                info['status'] = changes['status']
            result = self.op_update_project(node_list, info)
            if len(result):
                if len(result) < len(node_list):
                    log.warning(f'not all node update project:{project_name} =>{result}')
                    return PartialSuccess(msg=f'not all node update project:{project_name}', data=result)
                log.error(f'all project update failed:{project_name} =>{result}')
                raise Conflict(msg='all project update failed', data=result, errno=30005)
            log.info(f'update project:{project_name} success')
            return PatchSuccess(msg=f'update project:{project_name} success', data={'project_id': project_id})

    def __update(self, project_id, project_name, changes):
        with self.impl.handler.session() as session:
            session.update(*self.impl.update_project(project_id, changes))
        log.info(f'update project:{project_name} success')
        return PatchSuccess(msg=f'update project:{project_name} success')

    def delete(self, project_id):
        with self.impl.handler.session() as session:
            session.update(*self.impl.delete_project(project_id))
            node_list = self.impl.get_nodes()
            result = self.op_delete_project(node_list, project_id)
            if len(result):
                if len(result) < len(node_list):
                    log.warning(f'not all node delete project:{project_id} =>{result}')
                    return PartialSuccess(msg=f'not all node delete project', data=result)
                log.error(f'all project delete failed:{project_id} =>{result}')
                raise Conflict(msg='all project delete failed', errno=30006)
            log.info(f'delete project:{project_id} success')
            if self.impl.unbind_queue(project_id):
                return DeleteSuccess()
            else:
                return Conflict(msg='project is not exist', errno=30001)

    def get(self, project_id):
        info = self.impl.get_project(project_id)
        if len(info):
            return GetSuccess(data=info)
        else:
            return NotFound(msg='project not exist', errno=30001)

    def gets(self):
        info = self.impl.get_projects()
        return GetSuccess(data=info)
