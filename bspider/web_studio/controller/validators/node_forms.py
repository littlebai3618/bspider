# @Time    : 2019-08-01 15:26
# @Author  : 白尚林
# @File    : forms
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import length

from bspider.core.api import BaseForm, ParamRequired


class AddNodeForm(BaseForm):
    ip = StringField(validators=[ParamRequired(), length(min=7, max=15)])
    name = StringField(validators=[ParamRequired(), length(min=3, max=30)])
    description = StringField(validators=[ParamRequired()])


class GetNodeForm(BaseForm):
    is_all = IntegerField(default=0)
    node_ip = StringField()


class UpdateNodeForm(BaseForm):
    name = StringField()
    status = IntegerField()
    description = StringField()


class AddWorkerForm(BaseForm):
    ip = StringField(validators=[ParamRequired(), length(min=7, max=15)])
    name = StringField(validators=[ParamRequired(), length(min=3, max=30)])
    type = StringField(validators=[ParamRequired()])
    description = StringField(validators=[ParamRequired()])
    status = IntegerField(default=1)


class UpdateWorkerForm(BaseForm):
    ip = StringField()
    name = StringField()
    type = StringField()
    description = StringField()
    status = IntegerField()
