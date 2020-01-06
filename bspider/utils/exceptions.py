class MethodError(Exception):
    pass


class ProjectSettingsError(Exception):
    pass

class ModuleError(Exception):
    pass

class ModuleExistError(ModuleError):
    pass


class DownloaderError(Exception):
    pass


class ParserError(Exception):
    pass


class RemoteOPError(Exception):
    pass


class ExtractorCallbackError(Exception):
    pass


class UsageError(Exception):
    pass


class MiddleWareParamError(ModuleError):
    pass


class PipelineParamError(ModuleError):
    pass


class OperationParamError(ModuleError):
    pass


class TaskParamError(ModuleError):
    pass
