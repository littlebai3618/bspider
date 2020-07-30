from wtforms import StringField, IntegerField
from wtforms.validators import length

from bspider.core.api import BaseForm, ParamRequired
from .enums import ClientTypeEnum


class LoginForm(BaseForm):
    identity = StringField(validators=[ParamRequired(), length(max=32, min=5)])
    password = StringField()
    client_type = IntegerField(default=101)

    def validate_client_type(self, value):
        try:
            value.data = ClientTypeEnum(value.data).name
        except ValueError as e:
            raise e


class RegisterForm(BaseForm):
    identity = StringField(validators=[ParamRequired(), length(max=32, min=5)])
    username = StringField(validators=[ParamRequired(), length(max=32, min=1)])
    password = StringField(validators=[length(max=32, min=5)])
    role = StringField(validators=[ParamRequired()])
    email = StringField()
    phone = StringField()
    status = IntegerField(default=1)


class UpdateForm(BaseForm):
    username = StringField()
    password = StringField()
    role = StringField()
    email = StringField()
    phone = StringField()
    status = IntegerField()
