class MethodError(Exception):
    pass


class ProjectConfigError(Exception):
    pass


class ModuleExistError(Exception):
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


class MiddleWareParamError(Exception):
    pass


class PipelineParamError(Exception):
    pass


class OperationParamError(Exception):
    pass


class TaskParamError(Exception):
    pass
