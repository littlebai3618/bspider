import yaml
from voluptuous import Required, All, Length, Invalid, Schema, Range, MultipleInvalid
from wtforms import StringField, IntegerField

from bspider.core.api import BaseForm, ParamRequired
from bspider.utils.exceptions import ProjectSettingsError


def valid_middleware(middleware: list) -> list:
    return valid_module('Middleware', middleware)

def valid_pipeline(pipeline: list) -> list:
    return valid_module('Pipeline', pipeline)

def valid_module(module_type, data):
    for index, module in enumerate(data):
        if isinstance(module, str):
            data[index] = { module: dict() }
        elif isinstance(module, dict):
            for cls, param in module.items():
                if not isinstance(cls, str):
                    raise Invalid('%s cls %s name Invalid, must be str' % (module_type, cls))
                if not isinstance(param, dict):
                    raise Invalid('%s %s param Invalid, must be dict or None' % (module_type, cls))
        else:
            raise Invalid('Module %s Invalid, must like \'cls\' or [{cls: dict(cls_param)}]' % (module_type))
    return data

schema = Schema({
    Required('project_name'): All(str, Length(min=1, max=99)),
    Required('rate'): All(int, Range(min=5)),
    Required('group', default='default'): All(str, Length(min=1, max=99)),
    Required('description', default='default'): All(str),
    Required('global_settings', default=dict()): All(dict),
    Required('downloader'): {
        Required('max_retry_times', default=3): All(int, Range(min=1, max=10)),
        Required('ignore_retry_http_code', default=list()): All(list),
        Required('middleware', default=list()): valid_middleware
    },
    Required('parser'): {
        Required('pipeline', default=list()): valid_pipeline
    }
})

class AddForm(BaseForm):
    status = IntegerField(default=1)
    config = StringField(validators=[ParamRequired()])
    editor = StringField(validators=[ParamRequired()])

    def validate_config(self, value):
        try:
            value.data = schema(yaml.safe_load(value.data))
        except MultipleInvalid as e:
            raise ProjectSettingsError(e.error_message)

class UpdateForm(BaseForm):
    status = IntegerField()
    config = StringField()
    editor = StringField()

    def validate_config(self, value):
        try:
            value.data = schema(yaml.safe_load(value.data))
        except MultipleInvalid as e:
            raise ProjectSettingsError(e.error_message)





