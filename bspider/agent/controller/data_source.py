"""
    封装对cache中data_source信息的操作为api
"""
from flask import Blueprint

from bspider.core.api import auth
from .validators.data_source_form import AddForm, UpdateForm
from bspider.agent.service.data_source import DataSourceService

data_source = Blueprint('data_source_bp', __name__)
data_source_service = DataSourceService()


@data_source.route('/data_source', methods=['POST'])
@auth.login_required
def add_data_source():
    form = AddForm()
    return data_source_service.add_data_source(**form.to_dict())

@data_source.route('/data_source/<string:name>', methods=['PATCH'])
@auth.login_required
def update_data_source(name):
    form = UpdateForm()
    return data_source_service.update_data_source(name, form.to_dict())

@data_source.route('/data_source/<string:name>', methods=['DELETE'])
@auth.login_required
def delete_data_source(name):
    return data_source_service.delete_data_source(name)


@data_source.route('/data_source', methods=['GET'])
@auth.login_required
def get_data_sources():
    return data_source_service.get_data_sources()


@data_source.route('/data_source/<string:name>', methods=['GET'])
def get_data_source(name):
    return data_source_service.get_data_source(name)
