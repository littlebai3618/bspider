"""
下载器基类
执行中间件方法
"""
import asyncio
import sys
import traceback

import aiohttp
from aiohttp import ClientResponse

from bspider.core import Project
from bspider.http import Request, Response
from bspider.utils.exceptions import DownloaderError
from bspider.utils.importer import import_module_by_code
from bspider.utils.logger import LoggerPool
from bspider.utils.sign import Sign


class AsyncDownloader(object):

    def __init__(self, project: Project, sign: Sign, log_fn: str):
        """传入下载器的配置文件"""
        self.sign = sign
        self.project_name = project.project_name
        self.project_id = project.project_id

        self.log = LoggerPool().get_logger(
            key=f'project_downloader->{self.project_id}', fn=log_fn, module='downloader', project=self.project_name)
        # 加载重试次数
        self.retry_times = project.downloader_settings.max_retry_times
        self.log.debug(f'{self.project_name} init retry time from settings: {self.retry_times}')

        self.ignore_retry_http_code = set(project.downloader_settings.ignore_retry_http_code)
        self.ignore_retry_http_code.add(599)
        self.ignore_retry_http_code.add(200)
        self.log.debug(
            f'{self.project_name} init accept response code from settings: {self.ignore_retry_http_code}')

        self.mws = []
        for middleware in project.downloader_settings.middleware:
            for cls, params in middleware.items():
                cls_name, code = cls
                if isinstance(code, str):
                    mod = import_module_by_code(cls_name, code)
                else:
                    mod = code
                if mod and hasattr(mod, cls_name):
                    try:
                        self.mws.append(
                            getattr(mod, cls_name)(project, {**project.global_settings, **params}, self.log))
                        self.log.info(f'success load: <{self.project_name}:{cls_name}>!')
                    except Exception as e:
                        raise DownloaderError('<%s:%s> middleware init failed: %s' % (self.project_name, cls_name, e))

                else:
                    msg = f'<{self.project_name}:{cls_name}> middleware init failed: middleware is invalid!'
                    raise DownloaderError(msg)

    async def download(self, request: Request) -> (Response, bool, str):
        self.log.info(f'===>> start download sign:{request.sign} {request}')
        response = Response(url=request.url, status=599, request=request)
        # 异常占位符
        e_msg = None
        for retry_index in range(self.retry_times):
            is_req = True
            # 下载前中间件
            for mw in self.mws:
                self.log.debug(f'{mw.__class__.__name__} executing process_request')
                result = await mw._exec('process_request', request)

                if isinstance(result, Request):
                    request = result
                    continue
                elif result is None:
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
                e.with_traceback(tb)
                self.log.exception(e_msg)
                # 执行下载异常中间件
                for mw in self.mws:
                    self.log.debug(f'{mw.__class__.__name__} executing process_response')
                    result = await mw._exec('process_exception', request, e, response)
                    if result is None:
                        self.log.info(f'===>> complete download sign:{request.sign} {request}')
                        return response, True, e_msg
                continue

            for mw in self.mws:
                self.log.debug(f'{mw.__class__.__name__} executing process_response')
                result = await mw._exec('process_response', request, response)
                if result is None:
                    break

            if response.status in self.ignore_retry_http_code:
                self.log.debug(f'response.status == {response.status}: url->{request.url} ignore retry')
                self.log.info(f'===>> complete download sign:{request.sign} {request}')
                return response, True, None
            self.log.info(f'Retry download: url->{request.url} status->{response.status} time:{retry_index + 1}')
        self.log.info(f'===>> complete download sign:{request.sign} {request}')
        return response, True, e_msg

    async def __assemble_response(self, response: ClientResponse, request: Request) -> Response:
        # 这里只处理 str 类型的数据
        text = await response.text(errors='ignore')
        return Response(
            url=str(response.url),
            status=response.status,
            headers=dict(response.headers),
            request=request,
            cookies={i.key: i.value for i in response.cookies.values()},
            text=text
        )

    async def __do(self, req: Request) -> Response:
        # ClientSession 在每次请求都要关闭，所以使用上下文管理器进行管理
        temp_timeout = aiohttp.ClientTimeout(total=20, connect=req.timeout)
        self.log.debug(f'set time out {temp_timeout.connect}')
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method=req.method,
                    url=req.url,
                    headers=req.headers,
                    params=req.params,
                    # post 参数，get时为 None
                    data=req.data,
                    cookies=req.cookies,
                    # 是否允许重定向
                    allow_redirects=req.allow_redirect,
                    timeout=temp_timeout,
                    proxy=None if not isinstance(req.proxy, dict) else req.proxy.get('proxy'),
                    # ssl验证
                    ssl=req.verify_ssl,
            ) as resp:
                # 挂起等待下载结果
                self.log.debug(f'aiohttp finish {temp_timeout.connect}')
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
