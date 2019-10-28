# @Time    : 2019-08-13 17:35
# @Author  : 白尚林
# @File    : project_form
# @Use     :

from wtforms import IntegerField, StringField

from bspider.core.api import ParameterException, BaseForm, ParamRequired


class AddProjectForm(BaseForm):
    project_id = IntegerField(validators=[ParamRequired()])
    project_name = StringField(validators=[ParamRequired()])
    config = StringField(validators=[ParamRequired()])
    rate = IntegerField(validators=[ParamRequired()])
    status = IntegerField(default=0)


class UpdateProjectForm(BaseForm):
    project_id = IntegerField(validators=[ParamRequired()])
    project_name = StringField()
    config = StringField()
    rate = IntegerField()
    status = IntegerField()


class UpdateCodeForm(BaseForm):
    project_ids = StringField(validators=[ParamRequired()])
    code_name = StringField(validators=[ParamRequired()])
    code_type = StringField(validators=[ParamRequired()])
    content = StringField(validators=[ParamRequired()])

    def validate_project_ids(self, value):
        try:
            value.data = value.data.split(',')
        except ValueError as e:
            raise e

    def validate_code_type(self, value):
        if value.data not in ['downloader_config', 'parser_config']:
            raise ParameterException(msg=f'unknow module type: {value.data}')
