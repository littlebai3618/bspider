from pymysql import IntegrityError

from bspider.core.api import BaseService, Conflict, NotFound, PostSuccess, PatchSuccess, DeleteSuccess, \
    GetSuccess, ParameterException
from bspider.core.api import AgentMixIn, json
from bspider.master.server import log
from bspider.master.service.impl.data_source_impl import DataSourceImpl


class DataSourceService(BaseService, AgentMixIn):

    def __init__(self):
        self.impl = DataSourceImpl()

    def add(self, name: str, type: str, param: dict, description: str):
        try:
            with self.impl.mysql_client.session() as session:
                data = {
                    'name': name,
                    'description': description,
                    'type': type,
                    'param': param,
                    'status': 1
                }
                session.insert(*self.impl.add_data_source(data=data, get_sql=True))

                sign, result = self.op_add_data_source(
                    ip_list=self.impl.get_all_node_ip(),
                    data={'type': type, 'param': param, 'name': data['name']})

                if not sign:
                    log.error(f'not all node success connect data_source: {name} =>{result}')
                    raise Conflict(msg=f'add data_source:{name} failed', data=result, errno=70001)

            log.info(f'add data_source:{name} success')
            return PostSuccess(msg='add data_source success', data=data)
        except IntegrityError:
            log.error(f'add data_source failed:{name} data_source is already exist')
            return Conflict(msg='data_source is already exist', errno=70002)

    def update(self, name: str, param: dict, description: str):
        info = self.impl.get_data_source(name)
        if not len(info):
            return NotFound(msg='data_source is not exist', errno=70003)

        update_info = dict()

        with self.impl.mysql_client.session() as session:

            if description != info['description']:
                update_info['description'] = description

            if param != json.loads(info['param']):
                project = [str(project['id']) for project in info['project']]
                if len(project):

                    sign, result = self.op_update_data_source(
                        self.impl.get_all_node_ip(),
                        name=name,
                        data={'param': param, 'project': ','.join(project)})
                    if not sign:
                        log.warning(f'data_source:name->:{name} update exception')
                        raise Conflict(msg=f'update data_source:name->:{name} failed', data=result, errno=70004)
                update_info['param'] = param

            session.update(*self.impl.update_data_source(name, update_info, get_sql=True))
        log.info(f'update code success: {update_info}')
        return PatchSuccess(msg='update code success')

    def delete(self, name: str):
        project_list = self.impl.get_project_by_data_source_name(name)
        if len(project_list):
            log.error(f'delete data_source:{name} failed: can\'t delete in use data_source')
            return Conflict(msg='can\'t delete in use data_source', data=project_list, errno=70005)
        else:
            with self.impl.mysql_client.session() as session:
                sign, result = self.op_delete_data_source(self.impl.get_all_node_ip(), name)
                if not sign:
                    log.warning(f'data_source:name->:{name} delete exec')
                    raise Conflict(msg=f'data_source:name->:{name} was delete', data=result, errno=70005)
                session.delete(*self.impl.delete_data_source(name))
            log.info(f'success delete data_source:name->:{name}')
            return DeleteSuccess()

    def get_data_source(self, name: str):
        info = self.impl.get_data_source(name)
        if len(info):
            return GetSuccess(msg='get data_source success', data=info)
        else:
            return NotFound(msg='data_source is not exist', errno=70003)

    def get_data_sources(self, page, limit, search, sort):
        if sort.upper() not in ['ASC', 'DESC']:
            return ParameterException(msg='sort must `asc` or `desc`')

        infos, total = self.impl.get_data_sources(page, limit, search, sort)

        for info in infos:
            self.datetime_to_str(info)

        return GetSuccess(
            msg='get data_source list success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })
