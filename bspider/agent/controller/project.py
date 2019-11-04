# @Time    : 2019-08-13 16:52
# @Author  : 白尚林
# @File    : project
# @Use     :
from flask import Blueprint

from bspider.core.api import auth
from .validators.project_form import AddForm, UpdateForm
from bspider.agent.service.project import ProjectService

project = Blueprint('project_bp', __name__)
project_service = ProjectService()


@project.route('/project', methods=['POST'])
@auth.login_required
def add_project():
    form = AddForm()
    return project_service.add_project(**form.to_dict())

@project.route('/project/<int:project_id>', methods=['PATCH'])
@auth.login_required
def update_project(project_id):
    form = UpdateForm()
    return project_service.update_project(project_id, form.to_dict())

@project.route('/project/<int:project_id>', methods=['DELETE'])
@auth.login_required
def delete_project(project_id):
    return project_service.delete_project(project_id)


@project.route('/project', methods=['GET'])
@auth.login_required
def get_projects():
    return project_service.get_projects()


@project.route('/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    return project_service.get_project(project_id)
