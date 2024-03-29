import json

import yaml
from apscheduler.util import obj_to_ref
from pymysql import IntegrityError

from bspider.bcron import do
from bspider.core import Project
from bspider.core.my_tuple import TupleC
from bspider.master import log
from bspider.master.controller.validators.project_form import schema
from bspider.master.dao import ProjectDao
from bspider.core.api import BaseService, Conflict, NotFound, PostSuccess, DeleteSuccess, GetSuccess, \
    PatchSuccess, ParameterException, AgentMixIn
from bspider.utils.database.mysql.session import DBSession
from bspider.utils.tools import class_name2module_name, get_crontab_next_run_time


class ProjectService(BaseService, AgentMixIn):
    impl = ProjectDao()

    def bind_project_relation(self, session: DBSession, project_id: int, r_config: dict):
        self.impl.bind_queue(project_id=project_id)
        log.debug(f'bind new project=>{r_config["project_name"]} queue success!')
        # log.info(json.dumps(r_config))
        code_ids = [items[0] for items in r_config['downloader']['middleware']]
        pipeline = {key: value for key, value in r_config['parser']['pipeline']}
        code_ids.extend(pipeline.keys())
        log.debug(f'code num: {code_ids}')
        if len(code_ids):
            session.insert(*self.impl.add_project_code_binds(code_ids, project_id))
        # 解析data_source
        d_name = [param['data_source'] for param in pipeline.values() if 'data_source' in param]
        log.debug(f'data_source list: {d_name}')
        if len(d_name):
            session.insert(*self.impl.add_project_data_source_binds(d_name, project_id))

    def unbind_project_relation(self, session: DBSession, project_id: int):
        self.impl.unbind_queue(project_id=project_id)
        log.debug(f'unbind project=>{project_id} queue success!')
        session.delete(*self.impl.delete_project_code_binds(project_id))
        # 解析data_source
        session.delete(*self.impl.delete_project_data_source_binds(project_id))

    def add(self, editor: str, config: list, status: int):
        project = Project(config[0],
                          middleware_serializer_method=self.get_module_id_by_name,
                          pipeline_serializer_method=self.get_module_id_by_name)

        log.debug(
            f'pc_obj->pipeline:{project.parser_settings.pipeline}, middleware:{project.downloader_settings.middleware}')

        try:
            with self.impl.mysql_client.session() as session:
                r_config = project.dumps()
                data = {
                    'name': project.project_name,
                    'status': status,
                    'type': 'spider',
                    'group': project.group,
                    'description': project.description,
                    'editor': editor,
                    'rate': project.rate,
                    'config': config[1],
                    'r_config': r_config
                }

                project_id = session.insert(*self.impl.add_project(data), lastrowid=True)
                self.bind_project_relation(session, project_id, r_config)
                timestamp, next_run_time = get_crontab_next_run_time(project.scheduler_settings.trigger, self.tz)
                value = {
                    'project_id': project_id,
                    'code_id': self.get_module_id_by_name(project.parser_settings.extractor, dict())[0],
                    'type': 'crawl',
                    'trigger': project.scheduler_settings.trigger,
                    'trigger_type': project.scheduler_settings.trigger_type,
                    'func': obj_to_ref(do),
                    'executor': 'thread_pool',
                    'description': project.scheduler_settings.description,
                    'next_run_time': timestamp,
                }
                job_id = session.insert(*self.impl.add_cron_job(value))
                log.info(f'add cron job:{project.project_name} success')

                info = {
                    'project_id': project_id,
                    'name': project.project_name,
                    'rate': project.rate,
                    'config': r_config,
                    'status': status
                }
                node_list = self.impl.get_all_node_ip()
                sign, result = self.op_add_project(node_list, info)
                if not sign:
                    log.error(f'not all node add project:{project.project_name} =>{result}')
                    return Conflict(msg=f'not all node add project:{project.project_name}', data=result, errno=30007)
                log.info(f'add project:{project.project_name} success')
                return PostSuccess(msg=f'add project:{project.project_name} success',
                                   data={'project_id': project_id, 'job_id': job_id})
        except IntegrityError as e:
            if e.args[0] == 1062:
                log.error(f'all project add failed:{project.project_name} =>project is already exist')
                return Conflict(errno=30002, msg='project is already exist')
            raise e

    def update(self, project_id, changes):
        remote_param = dict()
        cron_param = dict()
        log.debug(f'change:{changes}')
        if 'status' in changes:
            remote_param['status'] = changes['status']

        if 'config' in changes:

            infos = self.impl.get_project(project_id)
            if not len(infos):
                return NotFound(msg='project not exist', errno=30001)

            new_project = Project(changes['config'][0],
                                  middleware_serializer_method=self.get_module_id_by_name,
                                  pipeline_serializer_method=self.get_module_id_by_name)
            try:
                old_project = Project(schema(yaml.safe_load(infos[0]['config'])))
            except Exception as e:
                log.warning(f'update error: old project yaml load failed:{e}')
                return Conflict(msg=f'update error: old project yaml load failed:{e}', errno=30003)

            if old_project.project_name != new_project.project_name:
                remote_param['name'] = new_project.project_name
                changes['name'] = new_project.project_name

            if old_project.rate != new_project.rate:
                remote_param['rate'] = new_project.rate
                changes['rate'] = new_project.rate

            if old_project.group != new_project.group:
                changes['group'] = new_project.group

            if old_project.description != new_project.description:
                changes['description'] = new_project.description

            if old_project.scheduler_settings != new_project.scheduler_settings:
                cron_param = new_project.scheduler_settings.dumps()
                cron_param.pop('rate')

            sign = [
                old_project.downloader_settings == new_project.downloader_settings,
                old_project.parser_settings == new_project.parser_settings
            ]
            if False in sign:
                remote_param['config'] = new_project.dumps()
                changes['r_config'] = remote_param['config']

            changes['config'] = changes['config'][1]

        if len(remote_param):
            with self.impl.mysql_client.session() as session:
                session.update(*self.impl.update_project(project_id, changes))
                r_config = changes.get('r_config')
                log.debug(r_config)
                if r_config:
                    self.unbind_project_relation(session, project_id)
                    self.bind_project_relation(session, project_id, r_config)
                    if len(cron_param):
                        session.insert(*self.impl.update_cron_job_by_project_id(project_id, cron_param))
                sign, result = self.op_update_project(self.impl.get_all_node_ip(), project_id, remote_param)
                if not sign:
                    log.warning(f'not all node update project:project_id->{project_id} =>{result}')
                    return Conflict(msg=f'not all node update this project change', data=result, errno=30007)
        else:
            with self.impl.mysql_client.session() as session:
                session.update(*self.impl.update_project(project_id, changes))
                if len(cron_param):
                    session.insert(*self.impl.update_cron_job_by_project_id(project_id, cron_param))

        log.info(f'update project:project_id->{project_id} success')
        return PatchSuccess(msg=f'update project success')

    def delete(self, project_id):
        with self.impl.mysql_client.session() as session:
            self.unbind_project_relation(session, project_id)
            session.delete(*self.impl.delete_cron_job(project_id))
            sign, result = self.op_delete_project(self.impl.get_all_node_ip(), project_id)
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
            msg='get project list success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })

    def get_module_id_by_name(self, cls_name: str, param: dict) -> TupleC:
        module_type = class_name2module_name(cls_name).split('_')[-1]
        data = self.impl.get_module_id_by_name_and_type(cls_name, module_type)
        if not len(data):
            raise Conflict(
                msg=f'lack of necessary module {module_type} <{cls_name}>!',
                errno=30003)

        if param.get('data_source'):
            data_source = self.impl.get_data_source_by_name(param.get('data_source'))
            if not len(data_source):
                raise Conflict(
                    msg=f'Invalid data_source {data_source}!',
                    errno=70003)

        return TupleC(data[0]['id'], param)
