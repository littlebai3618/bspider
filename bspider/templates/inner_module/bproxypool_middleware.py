"""
@name='BProxyPoolMiddleware',
@description='使用 bproxypool服务 为请求头添加proxy',
@type='middleware',
@editor='bspider'
"""
import json

import aiohttp.client_exceptions
from bspider.downloader import BaseMiddleware
from bspider.utils.exceptions import DownloaderError, MiddleWareParamError


class BProxyPoolMiddleware(BaseMiddleware):
    """
    使用 bproxypool服务 为请求头添加proxy
    """

    def __init__(self, settings, log):
        super().__init__(settings, log)
        bproxypool_url = self.settings.get('PROXY_POOL_API')
        if bproxypool_url is None:
            raise MiddleWareParamError('\'PROXY_POOL_API\' is Required like http://127.0.0.1:80/proxy/')
        self.timeout = self.settings.get('PROXY_POOL_TIMEOUT', 3)
        self.retry_time = self.settings.get('PROXY_POOL_RETRY_TIME', 3)
        virtual_pool = self.settings.get('VIRTUAL_PROXY_POOL')
        self.cool_down_time = self.settings.get('PROXY_COOL_DOWN_TIME')
        ignore = self.settings.get('PROXY_COOL_DOWN_CODE', list())
        ignore.append(599)
        self.ignore = set(ignore)
        if virtual_pool:
            self.proxy_url = f'{bproxypool_url}{virtual_pool}'
        else:
            self.proxy_url = bproxypool_url

    # by coroutine
    # async process_request(self, request):
    async def process_request(self, request):
        """
        执行下载前的操作
        返回Response类型，作为response完成下载，跳过后面的下载阶段，直接进入下载后的中间件
        返回空或其他返回值 继续下一个中间件
        """
        for index in range(self.retry_time):
            try:
                proxy_req = await self.get_proxy()
                request.proxy = {
                    'proxy': 'http://{}'.format(proxy_req['data']['proxy']),
                    'source': proxy_req['data']['source']
                }
                self.log.info('success add proxy in {} {}'.format(
                    request,
                    request.proxy
                ))
                return request
            except Exception as e:
                self.log.warning(f'get proxy failed: {e} {request} retry:{index}')

        raise DownloaderError('Proxy get failed, please check proxy service!')

    async def process_exception(self, request, e, response):
        if isinstance(e, aiohttp.ClientProxyConnectionError):
            await self.delete_proxy(request.proxy)
            self.log.info('{proxy} {source} is invalid delete it'.format(
                **request.proxy
            ))
        elif response.status not in self.ignore:
            await self.cool_down_proxy(request.proxy)
            self.log.info('{proxy} {source} success to cool down'.format(
                **request.proxy
            ))
        return response

    async def get_proxy(self) -> dict:
        temp_timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method='GET',
                    url=self.proxy_url,
                    timeout=temp_timeout
            ) as resp:
                # 挂起等待下载结果
                return json.loads(await resp.text())

    async def delete_proxy(self, proxy: dict) -> bool:
        temp_timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method='DELETE',
                    url=self.proxy_url,
                    timeout=temp_timeout,
                    data=proxy
            ) as resp:
                # 挂起等待下载结果
                return resp.status == 204

    async def cool_down_proxy(self, proxy: dict) -> bool:
        temp_timeout = aiohttp.ClientTimeout(total=self.timeout)
        data = {'proxy': proxy['proxy']}
        if self.cool_down_time:
            data['expire'] = self.cool_down_time
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method='PATCH',
                    url=self.proxy_url,
                    timeout=temp_timeout,
                    data=data
            ) as resp:
                # 挂起等待下载结果
                return resp.status == 200
