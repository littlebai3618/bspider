# @Time    : 2019-08-01 15:26
# @Author  : 白尚林
# @File    : forms
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import length

from bspider.core.api import BaseForm, ParamRequired


class RegisterForm(BaseForm):
    name = StringField(validators=[ParamRequired(), length(max=32, min=5)])
    coroutine_num = IntegerField(validators=[ParamRequired()])
    worker_type = StringField(validators=[ParamRequired()])

class CommonForm(BaseForm):
    name = StringField()
    is_all = IntegerField(default=0)
