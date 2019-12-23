import json

from bspider.utils.exceptions import ProjectConfigError


class ProjectConfigParser(object):

    def __init__(self, config: str):
        try:
            self.__config = json.loads(config)
        except Exception as e:
            raise ProjectConfigError('this config is illegal json str: %s' % (e))

        # 设置默认属性
        self.project_name: str = 'default'
        self.project_id: int = 0

        downloader = self.__valid_key_in_dict('downloader', dict, self.__config)
        middleware = self.__valid_key_in_dict('middleware', list, downloader)
        self.middleware: list = self.__valid_key_in_list('downloader.middleware', str, middleware)
        self.downloader_settings: dict = self.__valid_key_in_dict('settings', dict, downloader)

        parser = self.__valid_key_in_dict('parser', dict, self.__config)
        pipeline = self.__valid_key_in_dict('pipeline', list, parser)
        self.pipeline: list = self.__valid_key_in_list('parser.pipeline', str, pipeline)
        self.parser_settings: dict = self.__valid_key_in_dict('settings', dict, parser)

    @classmethod
    def loads(cls, config: str):
        return cls(config)

    def dumps(self):
        return json.dumps({
            'downloader': {
                'middleware': self.middleware,
                'settings': self.downloader_settings
            },
            'parser': {
                'pipeline': self.pipeline,
                'settings': self.parser_settings
            }
        })

    def __valid_key_in_dict(self, key: str, key_type: type, data: dict):
        if key not in data:
            raise ProjectConfigError('%s is not exist' % (key))

        if not isinstance(data[key], key_type):
            raise ProjectConfigError('%s is must be %s' % (key, key_type))

        return data[key]

    def __valid_key_in_list(self, name, element_type: type, data: list):
        if not isinstance(data, list):
            raise ProjectConfigError('%s is must be list' % (name))

        for d in data:
            if not isinstance(d, element_type):
                raise ProjectConfigError('\'%s\' elenent is must be %s' % (name, element_type))

        if not (len(data) == len(set(data))):
            raise ProjectConfigError(f'%s is must be unique' % (name))

        return data
