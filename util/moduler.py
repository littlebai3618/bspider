# @Time    : 2018/10/15 上午11:46
# @Author  : 白尚林
# @File    : moduler
# @Use     : 负责加载执行mysql中的代码
"""给定str 代码，加载成为对象"""
import importlib.machinery
import importlib.util


class ModuleImporter(object):

    @staticmethod
    def import_module(class_name: str, code: str, job_name: str='default'):
        """
        加载第三方模块
        :param script_name: 脚本名称
        :param class_name: 类名
        :param model: 模式名称
        :return: None or obj
        """
        spec = importlib.machinery.ModuleSpec(class_name.lower(), None)
        mod = importlib.util.module_from_spec(spec)
        compiled_code = compile(code, f'<{job_name}:{class_name}>', 'exec')
        exec(compiled_code, mod.__dict__)
        return mod
