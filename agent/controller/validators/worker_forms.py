# @Time    : 2019-08-01 15:26
# @Author  : 白尚林
# @File    : forms
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length

from core.api.base_form import BaseForm


class RegisterForm(BaseForm):
    name = StringField(validators=[DataRequired(), length(max=32, min=5)])
    coroutine_num = IntegerField(validators=[DataRequired()])
    worker_type = StringField(validators=[DataRequired()])

class CommonForm(BaseForm):
    name = StringField()
    is_all = IntegerField(default=0)
