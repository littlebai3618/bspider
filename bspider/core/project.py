'''
1. 实现一个validator 校验yaml配置文件的正确性
2. 返回ProjectSettings对象
    - DownloaderSettings
        - MiddleWareSettings:
    - PipelineSettings
        - PipelineSettings
    - BCronSettings
    - SchedulerSettings
'''
import operator
import types

from bspider.utils.exceptions import ProjectSettingsError


class Project(object):

    def __init__(self,
                 settings: dict,
                 project_id_serializer_method = None,
                 middleware_serializer_method= None,
                 pipeline_serializer_method = None):
        self.__project_name = settings['project_name']
        self.__project_id = None
        self.__global_settings = settings['global_settings']
        self.__group = settings['group']
        self.__description = settings['description']
        self.__downloader = settings['downloader']
        self.__parser = settings['parser']
        self.__scheduler = settings['scheduler']

        # 初始化序列化器 序列化器完成 id<->name的转化
        self.__project_id_serializer_method = project_id_serializer_method
        self.__pipeline_serializer_method = pipeline_serializer_method
        self.__middleware_serializer_method = middleware_serializer_method

    @property
    def project_name(self):
        return self.__project_name

    @property
    def project_id(self):
        if self.__project_id is not None:
            return self.__project_id
        if self.__project_id_serializer_method:
            self.__project_id = self.__project_id_serializer_method(self.project_name)
            return self.__project_id
        raise ProjectSettingsError('project_id_serializer_method is None')

    @project_id.setter
    def project_id(self, project_id):
        self.__project_id = project_id

    @property
    def rate(self):
        return self.scheduler_settings.rate

    @property
    def group(self):
        return self.__group

    @property
    def description(self):
        return self.__description

    @property
    def global_settings(self):
        return self.__global_settings

    @property
    def downloader_settings(self):
        return DownloaderSettings(
            max_retry_times=self.__downloader['max_retry_times'],
            ignore_retry_http_code=self.__downloader['ignore_retry_http_code'],
            middleware=self.__downloader['middleware'],
            serializer_method=self.__middleware_serializer_method
        )

    @property
    def parser_settings(self):
        return ParserSettings(
            pipeline=self.__parser['pipeline'],
            serializer_method=self.__pipeline_serializer_method
        )

    @property
    def scheduler_settings(self):
        return SchedulerSettings(settings=self.__scheduler)

    def dumps(self):
        '''dumps 方法需要serializer 方法支持'''
        return {
            'project_name': self.project_name,
            'group': self.group,
            'description': self.description,
            'global_settings': self.__global_settings,
            'downloader': self.downloader_settings.dumps(),
            'parser': self.parser_settings.dumps(),
            'scheduler': self.scheduler_settings.dumps()
        }


class DownloaderSettings(object):

    def __init__(self,
                 max_retry_times: int,
                 ignore_retry_http_code: list,
                 middleware: list,
                 serializer_method: types.MethodType = None):
        self.__max_retry_times = max_retry_times
        self.__ignore_retry_http_code = ignore_retry_http_code
        self.__middleware = middleware
        self.__serializer_method = serializer_method

    @property
    def ignore_retry_http_code(self):
        return self.__ignore_retry_http_code

    @property
    def max_retry_times(self):
        return self.__max_retry_times

    @property
    def middleware(self):
        return MiddlewareSettings(self.__middleware, self.__serializer_method, ['middleware'])

    def dumps(self):
        return {
            'max_retry_times': self.__max_retry_times,
            'ignore_retry_http_code': self.__ignore_retry_http_code,
            'middleware': list(self.middleware)
        }


class ParserSettings(object):

    def __init__(self,
                 pipeline: list,
                 serializer_method: types.MethodType = None):
        self.__pipeline = pipeline
        self.__serializer_method = serializer_method



    @property
    def extractor(self):
        for pipeline in self.__pipeline:
            for key, _ in pipeline.items():
                if key.endswith('Extractor'):
                    return key


    @property
    def pipeline(self):
        return PipelineSettings(self.__pipeline, self.__serializer_method, ['pipeline', 'extractor'])

    def dumps(self):
        return {
            'pipeline': list(self.pipeline)
        }


class SchedulerSettings(object):

    def __init__(self, settings: dict):
        self.__rate = settings['rate']
        self.__trigger_type = settings['trigger_type']
        self.__trigger = settings['trigger']
        self.__description = settings['description']

    @property
    def rate(self):
        return self.__rate

    @property
    def trigger(self):
        return self.__trigger

    @property
    def trigger_type(self):
        return self.__trigger_type

    @property
    def description(self):
        return self.__description

    def dumps(self):
        return {
            'rate': self.__rate,
            'trigger': self.__trigger,
            'description': self.__description
        }

    def __eq__(self, other):
        return other.trigger == self.__trigger \
               and other.trigger_type == self.__trigger_type \
               and other.description == self.description \
               and other.rate == self.rate


class BaseModuleSettings(object):

    def __init__(self, data: list, serializer_method: types.MethodType, module_type: list):
        self.__data = data
        self.__serializer_method = serializer_method
        self.__end = len(data)
        self.__cur = -1
        self.module_type = module_type

    def __iter__(self):
        return self

    def __next__(self) -> (str, dict):
        self.__cur += 1
        if self.__cur == self.__end:
            raise StopIteration()

        for cls, params in self.__data[self.__cur].items():
            if self.__serializer_method:
                return {self.__serializer_method(cls): params}
            return {cls: params}
            # raise ProjectSettingsError('serializer_method is None')

    def __eq__(self, other):
        return operator.eq(self.__data, other)

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        result = list()
        for module in self.__data:
            for cls, _ in module.items():
                result.append(str(cls))
        return '<{}: {} items>'.format(self.__class__.__name__, '->'.join(result))

    __str__ = __repr__


class MiddlewareSettings(BaseModuleSettings):
    pass


class PipelineSettings(BaseModuleSettings):
    pass
