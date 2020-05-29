import re
import sys
import traceback

from flask import g
from wtforms import StringField

from bspider.core.api import BaseForm, ParamRequired, Forbidden
from bspider.master import log
from bspider.utils.exceptions import ModuleError
from bspider.utils.tools import find_class_name_by_content
from bspider.utils.importer import import_module_by_code


def valid_code(content):
    description = 'default'
    pre_description = re.compile('@description=(.*?)\n').findall(content)
    if len(pre_description):
        description = pre_description[0]

    class_name, sub_class_name = find_class_name_by_content(content)

    # 非admin角色不能新增operation 类
    if class_name.lower().rfind('operation') != -1 and g.user.role != 'admin':
        raise Forbidden(msg='role has no permission!', errno=10004)

    code_type_map = {
        'BaseOperation': 'operation',
        'BasePipeline': 'pipeline',
        'BaseMiddleware': 'middleware',
        'BaseExtractor': 'extractor',
        # 'BaseSaver': 'saver'
    }

    module_type = code_type_map.get(sub_class_name)
    if module_type is None:
        raise ModuleError('Invalid module type->%s(%s)' % (class_name, sub_class_name))

    # pre_exec
    try:
        import_module_by_code('ModuleTest', content)
    except Exception as e:
        tp, msg, tb = sys.exc_info()
        e_msg = ''.join(traceback.format_exception(tp, msg, tb))
        log.error(e_msg)
        raise ModuleError('module code has a exception:%s' % (e))

    return class_name, module_type, description, content


class AddForm(BaseForm):
    content = StringField(validators=[ParamRequired()])
    editor = StringField(validators=[ParamRequired()])

    def validate_content(self, value):
        value.data = valid_code(value.data)


class UpdateForm(BaseForm):
    content = StringField()
    editor = StringField()

    def validate_content(self, value):
        if value.data:
            value.data = valid_code(value.data)
