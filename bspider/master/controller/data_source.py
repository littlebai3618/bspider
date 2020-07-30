# @Time    : 2020/5/20 6:56 下午
# @Author  : baii
# @File    : data_source
# @Use     : 数据源管理模块
from flask import Blueprint

from bspider.core.api import auth
from .validators.data_source_forms import AddForm, UpdateForm
from .validators import PageForm
from bspider.master.service.data_source import DataSourceService

data_source = Blueprint('data_source_bp', __name__)

data_source_service = DataSourceService()


@data_source.route('/data_source/<string:name>', methods=['GET'])
@auth.login_required
def get(name):
    return data_source_service.get_data_source(name)


@data_source.route('/data_source', methods=['GET'])
@auth.login_required
def gets():
    form = PageForm()
    return data_source_service.get_data_sources(**form.to_dict())


@data_source.route('/data_source', methods=['POST'])
@auth.login_required
def add():
    form = AddForm()
    return data_source_service.add(**form.to_dict())


@data_source.route('/data_source/<string:name>', methods=['DELETE'])
@auth.login_required
def delete(name):
    return data_source_service.delete(name)


@data_source.route('/data_source/<string:name>', methods=['PATCH'])
@auth.login_required
def update(name):
    form = UpdateForm()
    return data_source_service.update(name, **form.to_dict())

