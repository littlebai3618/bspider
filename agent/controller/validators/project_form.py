# @Time    : 2019-08-13 17:35
# @Author  : 白尚林
# @File    : project_form
# @Use     :
import json

from wtforms import IntegerField, StringField, FieldList
from wtforms.validators import DataRequired

from core.api.base_form import BaseForm
from core.api.exception import ParameterException


class AddProjectForm(BaseForm):
    project_id = IntegerField(validators=[DataRequired()])
    project_name = StringField(validators=[DataRequired()])
    config = StringField(validators=[DataRequired()])
    rate = IntegerField(validators=[DataRequired()])
    status = IntegerField(default=0)


class UpdateProjectForm(BaseForm):
    project_id = IntegerField(validators=[DataRequired()])
    project_name = StringField()
    config = StringField()
    rate = IntegerField()
    status = IntegerField()


class UpdateCodeForm(BaseForm):
    project_ids = StringField(validators=[DataRequired()])
    code_name = StringField(validators=[DataRequired()])
    code_type = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])

    def validate_project_ids(self, value):
        try:
            value.data = value.data.split(',')
        except ValueError as e:
            raise e

    def validate_code_type(self, value):
        if value.data not in ['downloader_config', 'parser_config']:
            raise ParameterException(msg=f'unknow module type: {value.data}')
