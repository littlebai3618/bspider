"""给定str 代码，加载成为对象"""
import importlib.machinery
import importlib.util
from importlib import import_module
from pkgutil import iter_modules


def import_module_by_code(module_name: str, code: str):
    """
    通过str加载第三方模块
    :param class_name:
    :param code:
    :param project_name:
    :return:
    """
    spec = importlib.util.spec_from_loader(module_name, None)
    mod = importlib.util.module_from_spec(spec)
    # 模拟exec_module()方法
    compiled_code = compile(code, f'<{module_name}>', 'exec')
    exec(compiled_code, mod.__dict__)
    return mod


def import_module_by_path(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
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
