# @Time    : 2019-08-14 17:16
# @Author  : 白尚林
# @File    : code_forms
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from bspider.core.api import BaseForm


class AddForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])
    type = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])
    editor = StringField(validators=[DataRequired()])


class UpdateForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    description = StringField()
    type = StringField()
    content = StringField()
    editor = StringField()
