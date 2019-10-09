# @Time    : 2019-08-01 15:26
# @Author  : 白尚林
# @File    : forms
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length

from bspider.core.api import BaseForm
from .enums import ClientTypeEnum


class LoginForm(BaseForm):
    identity = StringField(validators=[DataRequired(), length(max=32, min=5)])
    password = StringField()
    client_type = IntegerField(default=101)

    def validate_client_type(self, value):
        try:
            value.data = ClientTypeEnum(value.data).name
        except ValueError as e:
            raise e


class RegisterForm(BaseForm):
    identity = StringField(validators=[DataRequired(), length(max=32, min=5)])
    username = StringField(validators=[DataRequired(), length(max=10, min=1)])
    password = StringField(validators=[length(max=20, min=5)])
    role = StringField(validators=[DataRequired()])
    email = StringField()
    phone = StringField()


class UpdateForm(BaseForm):
    username = StringField()
    password = StringField()
    role = StringField()
    email = StringField()
    phone = StringField()
