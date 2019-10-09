# @Time    : 2018/10/15 上午11:46
# @Author  : 白尚林
# @File    : importer
# @Use     : 负责加载执行mysql中的代码
"""给定str 代码，加载成为对象"""
import importlib.machinery
import importlib.util
from importlib import import_module
from pkgutil import iter_modules


def import_module_by_code(class_name: str, code: str, project_name: str = 'default'):
    """
    通过str加载第三方模块
    :param class_name:
    :param code:
    :param project_name:
    :return:
    """
    spec = importlib.machinery.ModuleSpec(class_name.lower(), None)
    mod = importlib.util.module_from_spec(spec)
    compiled_code = compile(code, f'<{project_name}:{class_name}>', 'exec')
    exec(compiled_code, mod.__dict__)
    return mod

def import_module_by_path(class_name: str, path: str, project_name: str = 'default'):
    spec = importlib.util.spec_from_file_location(class_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def walk_modules(path):
    """
    参照scrapy的方法，递归搜索整个包下面的所有模块
    """
    mods = list()
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods
