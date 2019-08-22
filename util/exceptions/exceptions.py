# @Time    : 2019/6/14 6:01 PM
# @Author  : 白尚林
# @File    : exceptions
# @Use     :
class SettingsError(Exception):
    pass


class MethordError(Exception):
    pass


class ProjectConfigError(Exception):
    pass


class ModuleExistError(Exception):
    pass


class DownloaderError(Exception):
    pass


class ParserError(Exception):
    pass


class MonitorError(Exception):
    pass


class MysqlConfigError(Exception):
    """mysql config error"""
    pass


class RemoteOPError(Exception):
    """mysql config error"""

    def __init__(self, err, fmt):
        err = err.format(fmt)
        super().__init__(err)
