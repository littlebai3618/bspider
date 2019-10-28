# @Time    : 2019-08-15 11:19
# @Author  : 白尚林
# @File    : cron_job_forms
# @Use     :
from apscheduler.triggers.cron import CronTrigger
from wtforms import StringField, IntegerField

from bspider.core.api import BaseForm, ParamRequired


class AddForm(BaseForm):
    project_id = IntegerField(validators=[ParamRequired()])
    project_name = StringField(validators=[ParamRequired()])
    class_name = StringField(validators=[ParamRequired()])
    trigger = StringField(validators=[ParamRequired()])
    description = StringField(validators=[ParamRequired()])


class UpdateForm(BaseForm):
    project_name = StringField(validators=[ParamRequired()])
    class_name = StringField()
    trigger = StringField()
    description = StringField()

    def validate_trigger(self, value):
        if value.data:
            value.data = CronTrigger.from_crontab(value.data)
