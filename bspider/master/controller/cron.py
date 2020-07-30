from flask import Blueprint

from bspider.core.api import auth
from bspider.utils.tools import change_dict_key
from .validators import PageForm
from bspider.master.service.cron import CronService
from .validators.cron_forms import AddForm, UpdateForm

cron = Blueprint('cron_bp', __name__)

cron_service = CronService()


@cron.route('/cron', methods=['POST'])
@auth.login_required
def add():
    form = AddForm()
    return cron_service.add_cron(**change_dict_key('type', 'cron_type', form.to_dict()))


@cron.route('/cron/<int:cron_id>', methods=['DELETE'])
@auth.login_required
def delete(cron_id):
    return cron_service.delete_job(cron_id)


@cron.route('/cron/<int:cron_id>', methods=['PATCH'])
@auth.login_required
def update(cron_id):
    form = UpdateForm()
    return cron_service.update_job(cron_id, changes=form.to_dict())


@cron.route('/cron/<int:cron_id>', methods=['GET'])
@auth.login_required
def get(cron_id):
    return cron_service.get_job(cron_id)

@cron.route('/cron', methods=['GET'])
@auth.login_required
def gets():
    form = PageForm()
    return cron_service.get_jobs(**form.to_dict())
