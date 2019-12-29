import yaml
from voluptuous import Required, All, Length, Invalid, Schema, Range, MultipleInvalid
from wtforms import StringField, IntegerField

from bspider.core.api import BaseForm, ParamRequired
from bspider.utils.exceptions import ProjectSettingsError


def valid_middleware(middleware: list) -> list:
    for module in middleware:
        if not isinstance(module, dict):
            raise Invalid('Middleware Invalid, must like [{cls: dict(cls_param)}]')
        for cls, param in module.items():
            if not isinstance(cls, str):
                raise Invalid('Middleware %s name Invalid, must be str' % (cls))
            if not isinstance(param, dict):
                raise Invalid('Middleware %s param Invalid, must be dict' % (cls))
    return middleware

def valid_pipeline(pipeline: list) -> list:
    for module in pipeline:
        if not isinstance(module, dict):
            raise Invalid('Pipeline Invalid, must like [{cls: dict(cls_param)}]')
        for cls, param in module.items():
            if not isinstance(cls, str):
                raise Invalid('Pipeline cls %s name Invalid, must be str' % (cls))
            if not isinstance(param, dict):
                raise Invalid('Pipeline %s param Invalid, must be dict' % (cls))
    return pipeline

def valid_task(tasks: list) -> list:
    for task in tasks:
        if not isinstance(task, dict):
            raise Invalid('Task Invalid, must like [{cls: dict(cls_param)}]')
        for cls, param in task.items():
            if not isinstance(cls, str):
                raise Invalid('Task cls %s name Invalid, must be str' % (cls))

            if not isinstance(param, dict):
                raise Invalid('Task cls %s param Invalid, must be dict' % (cls))

            for key in ['crontab', 'description']:
                if key not in param:
                    raise Invalid('Task %s param Invalid, must have %s' % (cls, key))
    return tasks


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
    },
    Required('bcron', default=list()): valid_task
})

class AddForm(BaseForm):
    status = IntegerField()
    config = StringField(validators=[ParamRequired()])
    editor = StringField()

    def validate_config(self, value):
        try:
            value.data = schema(yaml.safe_load(value))
        except MultipleInvalid as e:
            raise ProjectSettingsError(e.error_message)

class UpdateForm(BaseForm):
    status = IntegerField()
    description = StringField()
    editor = StringField()

    def validate_config(self, value):
        try:
            value.data = schema(yaml.safe_load(value))
        except MultipleInvalid as e:
            raise ProjectSettingsError(e.error_message)





