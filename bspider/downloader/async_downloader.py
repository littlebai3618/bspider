# @Time    : 2019/7/2 2:27 PM
# @Author  : 白尚林
# @File    : base_downloader
# @Use     :
"""
下载器基类
执行中间件方法
"""
import asyncio
import sys
import traceback

import aiohttp

from aiohttp import ClientResponse

from bspider.core import ProjectConfigParser
from bspider.http import Request, Response
from bspider.utils.exceptions import DownloaderError
from bspider.utils.importer import import_module_by_code
from bspider.utils.logger import LoggerPool
from bspider.utils.sign import Sign


class AsyncDownloader(object):

    def __init__(self, config: ProjectConfigParser, sign: Sign):
        """传入下载器的配置文件"""
        self.sign = sign
        self.project_name = config.project_name
        self.project_id = config.project_id

        self.log = LoggerPool().get_logger(key=f'project_downloader->{self.project_id}', module='downloader', project=self.project_name)
        # 加载重试次数
        if 'RETRY_TIMES' in config.downloader_settings and isinstance(config.downloader_settings['RETRY_TIMES'], int):
            self.retry_times = config.downloader_settings['RETRY_TIMES']
            self.log.debug(f'{self.project_name} init retry time from settings: {self.retry_times}')
        else:
            self.retry_times = 3
            self.log.debug(f'{self.project_name} init default retry time: {self.retry_times}')
        self.mws = []
        for cls_name, code in config.middleware:
            mod = import_module_by_code('downloader_middleware', code)
            if mod and hasattr(mod, cls_name):
                try:
                    # 通过中间件类名实例化，放入中间件list中
                    mw_instance = getattr(mod, cls_name)(config.downloader_settings, self.log)
                    self.mws.append(mw_instance)
                    self.log.info(f'success load: <{self.project_name}:{cls_name}>!')
                except Exception as e:
                    raise DownloaderError(f'<{self.project_name}:{cls_name}> middleware init failed: {e}')

            else:
                msg = f'<{self.project_name}:{cls_name}> middleware init failed: middleware is invalid!'
                raise DownloaderError(msg)

        if 'ACCEPT_RESPONSE_CODE' in config.downloader_settings and isinstance(
                config.downloader_settings['ACCEPT_RESPONSE_CODE'], list):
            self.accept_response_code = set(config.downloader_settings['ACCEPT_RESPONSE_CODE'])
            self.log.debug(f'{self.project_name} init accept response code from settings: {self.accept_response_code}')
        else:
            self.accept_response_code = set()
            self.log.debug(f'{self.project_name} init default accept response code: {self.accept_response_code}')

    async def download(self, request: Request):
        """
        donwloader入口, 执行整个下载过程
        执行中间件，执行下载时，异步
        :param para: 队列传来的参数，格式为dict
        :param config: 下载器配置项
        :return:
        """
        for retry_index in range(self.retry_times):
            response = None

            # 下载前中间件
            is_req = True
            for mw in self.mws:
                self.log.debug(f'{mw.__class__.__name__} executing process_request')
                result = await mw._exec('process_request', request=request)

                if isinstance(result, Request):
                    request = result
                    continue
                elif req is None:
                    continue
                elif isinstance(result, Response):
                    is_req = False
                    response = result
                    break

            try:
                if is_req:
                    response = await self.__do(request)
            except Exception as e:
                tp, msg, tb = sys.exc_info()
                e_msg = ''.join(traceback.format_exception(tp, msg, tb))
                self.log.exception(e_msg)
                if response is None:
                    response = Response(url=request.url, status=599)
                # 执行下载异常中间件
                for mw in self.mws:
                    self.log.debug(f'{mw.__class__.__name__} executing process_exception')
                    response = await mw._exec('process_exception', request=request, e=e, response=response)
                    if isinstance(response, Response):
                        continue
                    elif response is None:
                        return None

            for mw in self.mws:

                self.log.debug(f'{mw.__class__.__name__} executing process_response')
                response = await mw._exec('process_response', request=request, response=response)
                if isinstance(response, Response):
                    continue
                if response is None:
                    return None

            if response is None:
                return None
            if response.status != 200:
                # 无需重试的情况
                if 900 <= response.status <= 999 or response.status in self.accept_response_code:
                    return response
                self.log.info('download error, retry. url:{} status:{}'.format(request.url, response.status))
            return response

    async def __assemble_response(self, response: ClientResponse, request: Request) -> Response:
        # 这里只处理 str 类型的数据
        text = await response.text(errors='ignore')
        return Response(
            url=str(response.url),
            status=response.status,
            headers=dict(response.headers),
            request=request.dumps(),
            cookies={i.key: i.value for i in response.cookies.values()},
            text=text,
            meta=request.meta,
            sign=request.sign,
            method=request.method
        )

    async def __do(self, req: Request) -> Response:
        """
        执行下载操作
        url': '', # 请求的url 必须
        method': '', # 请求的方法 GET, POST, PUT ,PATCH, OPTIONS, HEAD, DELETE
        request_body': {}, # POST 请求的消息体 字典结构
        cookies': {}, # 请求时携带的cookie 字典结构
        meta': {}, # 请求时携带的上下文信息，通常与本次请求无关
        proxy': str
        allow_redirect': bool, # 下载是否需要重定向
        timeout: int /s
        task_info': {
            name': '', # 任务信息
            task_sign': '', # 一个任务中一个链接中每一次请求的唯一标识
        }
        :param param: dict 下载参数
        :return:
        """
        # sc 在每次请求都要关闭，所以使用上下文管理器进行管理
        temp_timeout = aiohttp.ClientTimeout(total=req.timeout)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method=req.method,
                    url=req.url,
                    headers=req.headers,
                    # post 参数，get时为 None
                    data=req.data,
                    cookies=req.cookies,
                    # 是否允许重定向
                    allow_redirects=req.allow_redirect,
                    timeout=temp_timeout,
                    proxy=req.proxy,
                    # ssl验证
                    ssl=req.verify_ssl,
            ) as resp:
                # 挂起等待下载结果
                return await self.__assemble_response(resp, req)


if __name__ == '__main__':
    bd = AsyncDownloader()

    req = Request(
        url='https://www.baidu.com/',
        method='GET',
        timeout=10
    )

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(bd.__do(req))]

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
