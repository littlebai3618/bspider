# @Time    : 2019/6/18 3:45 PM
# @Author  : 白尚林
# @File    : base_service
# @Use     :
import json
from datetime import datetime

from bspider.config import FrameSettings
from bspider.downloader import AsyncDownloader
from bspider.parser.async_parser import AsyncParser
from bspider.utils.exceptions import ProjectConfigError


class BaseService(object):

    frame_settings = FrameSettings()

    @staticmethod
    def config_parser(config):
        """返回涉及到的中间件"""
        config = json.loads(config)
        mw = []
        pipe = []
        if 'downloader_config' in config:
            if 'middleware' in config['downloader_config']:
                mw = config['downloader_config']['middleware']
        else:
            raise ProjectConfigError('you project config must have downloader_config')

        if 'parser_config' in config:
            if 'pipeline' in config['parser_config']:
                pipe = config['parser_config']['pipeline']
        else:
            raise ProjectConfigError('you project config must have parser_config')
        return mw, pipe, config

    def make_remote_config(self, cfg, middlewares, pipelines, project_name) -> dict:
        for i, mw_name in enumerate(cfg['downloader_config']['middleware']):
            cfg['downloader_config']['middleware'][i] = (mw_name, middlewares[mw_name])
        for i, mw_name in enumerate(cfg['parser_config']['pipeline']):
            cfg['parser_config']['pipeline'][i] = (mw_name, pipelines[mw_name])

        AsyncDownloader(project_name, cfg['downloader_config'], sign='test')
        AsyncParser(project_name, cfg['parser_config'], sign='test')
        return cfg

    @staticmethod
    def serializer_project(infos):
        result = []
        projects = {}
        code = {}
        for info in infos:
            project_id = info.pop('project_id')
            config = info.pop('config')
            project_name = info.pop('project_name')
            rate = info.pop('rate')
            status = info.pop('project_status')
            if project_id not in projects:
                projects[project_id] = (project_name, json.loads(config), rate,  status)

            code[info.pop('code_name')] = info['code']

        for project_id, project in projects.items():
            project_name, project_config, rate, status = project
            for i, mw in enumerate(project_config['downloader_config']['middleware']):
                project_config['downloader_config']['middleware'][i] = (mw, code[mw])
            for i, pipe in enumerate(project_config['parser_config']['pipeline']):
                project_config['parser_config']['pipeline'][i] = (pipe, code[pipe])
            result.append({
                'project_id': project_id,
                'project_name': project_name,
                'rate': rate,
                'status': status,
                'config': json.dumps(project_config)
            })
        return result

    def datetime_to_str(self, d: dict) -> None:
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = value.strftime("%Y-%m-%d %H:%M:%S")




