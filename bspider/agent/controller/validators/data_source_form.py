import json

from wtforms import StringField

from bspider.core.api import BaseForm, ParamRequired


class AddForm(BaseForm):
    name = StringField(validators=[ParamRequired()])
    type = StringField(validators=[ParamRequired()])
    param = StringField(validators=[ParamRequired()])

    def validate_param(self, value):
        print(type(value), value)
        value.data = json.loads(value.data)

class UpdateForm(BaseForm):
    type = StringField(validators=[ParamRequired()])
    param = StringField(validators=[ParamRequired()])
    project = StringField(default='')

    def validate_param(self, value):
        value.data = json.loads(value.data)

    def validate_project(self, value):
        value.data = [int(project_id) for project_id in value.data.split(',')]
