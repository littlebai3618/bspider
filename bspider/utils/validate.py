# @Time    : 2019/10/29 4:01 下午
# @Author  : baii
# @File    : validate_code
# @Use     : 第三方代码检测
from bspider.utils.tools import find_class_name_by_content


def valid_code(name: str, code_type: str, content: str) -> (bool, str):
    sign, class_name, sub_class_name = find_class_name_by_content(content)
    if not sign:
        return False, f'can\'t find module class_name'
    if not class_name == name:
        return False, f'module class_name and module_name must be equal'
    code_type_map = {
        'BaseTask': 'task',
        'BaseOperation': 'operation',
        'BasePipeline': 'pipeline',
        'BaseMiddleware': 'middleware',
        'BaseExtractor': 'extractor'
    }

    module_type = code_type_map.get(sub_class_name)
    if module_type is None:
        return False, f'Unknown module type->{sub_class_name}'
    if not code_type_map.get(sub_class_name) == code_type:
        return False, f'Invalid module type->{module_type}, Please check code'

    # pre_exec
    try:
        exec(content)
    except Exception as e:
        return False, f'module code has a exception:{e}'

    return True, 'ok!'
