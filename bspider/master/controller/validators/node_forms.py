from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import length

from bspider.core.api import BaseForm, ParamRequired


class AddNodeForm(BaseForm):
    ip = StringField(validators=[ParamRequired(), length(min=7, max=15)])
    name = StringField(validators=[ParamRequired(), length(min=3, max=30)])
    description = StringField(validators=[ParamRequired()])
    cpu_num = IntegerField(validators=[ParamRequired()])
    mem_size = FloatField(validators=[ParamRequired()])
    disk_size = FloatField(validators=[ParamRequired()])
    port = IntegerField(validators=[ParamRequired()])

class UpdateNodeForm(BaseForm):
    name = StringField()
    status = IntegerField()
    description = StringField()
    cpu_num = IntegerField()
    mem_size = IntegerField()
    disk_size = IntegerField()


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
