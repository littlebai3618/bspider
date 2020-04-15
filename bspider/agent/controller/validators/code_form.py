from wtforms import IntegerField, StringField

from bspider.core.api import BaseForm, ParamRequired


class AddForm(BaseForm):
    code_id = IntegerField(validators=[ParamRequired()])
    content = StringField(validators=[ParamRequired()])


class UpdateForm(BaseForm):
    content = StringField()
    project = StringField(default='')

    def validate_project(self, value):
        value.data = value.data.split(',')
