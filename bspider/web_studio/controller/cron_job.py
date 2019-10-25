# @Time    : 2019/6/20 7:22 PM
# @Auth    : 白尚林
# @File    : cron_job
# @Use     :
from flask import Blueprint

from bspider.core.api import auth
from bspider.web_studio.service.cron_job import CronJobService
from .validators.cron_job_forms import AddForm, UpdateForm

cron_job = Blueprint('cron_bp', __name__)

cron_job_service = CronJobService()


@cron_job.route('/cron', methods=['POST'])
@auth.login_required
def add():
    form = AddForm()
    return cron_job_service.add_job(form.project_id.data, form.project_name.data, form.class_name.data, form.trigger.data,
                                    form.description.data)


@cron_job.route('/cron/<int:job_id>', methods=['DELETE'])
@auth.login_required
def delete(job_id):
    return cron_job_service.delete_job(job_id)


@cron_job.route('/cron<int:job_id>', methods=['PATCH'])
@auth.login_required
def update(job_id):
    form = UpdateForm()
    changes = form.get_dict()
    project_name = changes.pop('project_name')
    return cron_job_service.update_job(job_id, project_name, **changes)


@cron_job.route('/cron/<int:job_id>', methods=['GET'])
@auth.login_required
def get(job_id):
    return cron_job_service.get_job(job_id)

@cron_job.route('/cron', methods=['GET'])
@auth.login_required
def gets():
    return cron_job_service.get_jobs()