# @Time    : 2019-08-15 11:19
# @Author  : 白尚林
# @File    : cron_job_forms
# @Use     :
from apscheduler.triggers.cron import CronTrigger
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from core.api.base_form import BaseForm


class AddForm(BaseForm):
    project_id = IntegerField(validators=[DataRequired()])
    project_name = StringField(validators=[DataRequired()])
    class_name = StringField(validators=[DataRequired()])
    trigger = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])


class UpdateForm(BaseForm):
    job_id = IntegerField(validators=[DataRequired()])
    project_name = StringField(validators=[DataRequired()])
    class_name = StringField()
    trigger = StringField()
    description = StringField()

    def validate_trigger(self, value):
        if value.data:
            value.data = CronTrigger.from_crontab(value.data)
