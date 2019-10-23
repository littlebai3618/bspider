# @Time    : 2019-08-01 15:26
# @Author  : 白尚林
# @File    : forms
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length

from bspider.core.api import BaseForm, ParamRequired
from .enums import OpTypeEnum


class AddNodeForm(BaseForm):
    node_ip = StringField(validators=[DataRequired(), length(min=7, max=15)])
    name = StringField(validators=[DataRequired(), length(min=3, max=30)])
    desc = StringField(validators=[DataRequired()])


class DeleteNodeForm(BaseForm):
    node_ip = StringField(validators=[DataRequired(), length(min=7, max=15)])


class GetNodeForm(BaseForm):
    is_all = IntegerField(default=0)
    node_ip = StringField()


class UpdateNodeForm(BaseForm):
    name = StringField()
    status = IntegerField()

    def validate_status(self, value):
        try:
            value.data = OpTypeEnum(value.data).name
        except ValueError as e:
            raise e


class AddWorkerForm(BaseForm):
    ip = StringField(validators=[DataRequired(), length(min=7, max=15)])
    name = StringField(validators=[DataRequired(), length(min=3, max=30)])
    type = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])


class DeleteWorkerForm(BaseForm):
    node_ip = StringField(validators=[DataRequired(), length(min=7, max=15)])
    worker_type = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired(), length(min=3, max=30)])


class ChangeWorkerForm(BaseForm):
    node_ip = StringField(validators=[DataRequired(), length(min=7, max=15)])
    op = StringField(validators=[DataRequired()])
    worker_type = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired(), length(min=3, max=30)])

class GetWorkerForm(BaseForm):
    is_all = IntegerField(default=0)
    node_ip = StringField()
    name = StringField()



