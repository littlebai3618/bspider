from wtforms import StringField, IntegerField

from bspider.core.api import BaseForm, ParamRequired


class RegisterForm(BaseForm):
    worker_id = IntegerField(validators=[ParamRequired()])
    coroutine_num = IntegerField(validators=[ParamRequired()])
    worker_type = StringField(validators=[ParamRequired()])
