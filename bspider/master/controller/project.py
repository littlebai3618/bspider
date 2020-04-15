from flask import Blueprint

from bspider.core.api import auth
from .validators import PageForm
from .validators.project_form import UpdateForm, AddForm
from bspider.master.service.project import ProjectService

project = Blueprint('project_bp', __name__)

project_service = ProjectService()


@project.route('/project/<int:project_id>', methods=['GET'])
@auth.login_required
def get_project(project_id):
    return project_service.get(project_id)


@project.route('/project', methods=['GET'])
@auth.login_required
def get_projects():
    form = PageForm()
    return project_service.gets(**form.to_dict())


@project.route('/project/<int:project_id>', methods=['DELETE'])
@auth.login_required
def delete_project(project_id):
    return project_service.delete(project_id)


@project.route('/project/<int:project_id>', methods=['PATCH'])
@auth.login_required
def update(project_id):
    form = UpdateForm()
    return project_service.update(project_id, form.to_dict())


@project.route('/project', methods=['POST'])
@auth.login_required
def add():
    form = AddForm()
    return project_service.add(**form.to_dict())
