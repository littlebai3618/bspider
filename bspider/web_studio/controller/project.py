# @Time    : 2019/6/21 1:23 PM
# @Author  : 白尚林
# @File    : project
# @Use     :
from flask import Blueprint

from bspider.core.api import auth
from bspider.web_studio.controller.validators.project_form import UpdateForm, AddForm
from bspider.web_studio.service.project import ProjectService

project = Blueprint('project_bp', __name__)

project_service = ProjectService()


@project.route('/project/<int:project_id>', methods=['GET'])
@auth.login_required
def get_project(project_id):
    return project_service.get(project_id)


@project.route('/project', methods=['GET'])
@auth.login_required
def get_projects():
    return project_service.gets()


@project.route('/project/<int:project_id>', methods=['DELETE'])
@auth.login_required
def delete_project(project_id):
    return project_service.delete(project_id)


@project.route('/project', methods=['PATCH'])
@auth.login_required
def update():
    form = UpdateForm()
    changes = form.get_dict()
    project_id = changes.pop('project_id')
    project_name = changes.pop('name')
    return project_service.update(project_id, project_name, changes)


@project.route('/project', methods=['POST'])
@auth.login_required
def add():
    form = AddForm()
    return project_service.add_project(form.name.data, form.status.data, form.type.data, form.group.data,
                                       form.description.data, form.editor.data, form.rate.data, form.config.data)

