# @Time    : 2019-08-01 15:26
# @Author  : 白尚林
# @File    : forms
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length

from bspider.core.api import BaseForm
from .enums import ClientTypeEnum


class GetCodeListForm(BaseForm):
    type = StringField()

class ValidateForm(BaseForm):
    data = StringField(validators=[DataRequired()])
