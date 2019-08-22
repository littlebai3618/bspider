# @Time    : 2019-08-14 17:16
# @Author  : 白尚林
# @File    : code_forms
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length

from core.api.base_form import BaseForm


class GetForm(BaseForm):
    code_type = StringField()
    editor = StringField()


class AddForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])
    type = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])
    editor = StringField(validators=[DataRequired()])


class UpdateForm(BaseForm):
    code_id = IntegerField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    description = StringField()
    type = StringField()
    content = StringField()
    editor = StringField()