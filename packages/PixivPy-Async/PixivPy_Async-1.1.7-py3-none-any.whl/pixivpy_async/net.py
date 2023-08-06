import aiohttp
import random
import asyncio
from .retry import retry


class Net(object):
    def __init__(self, **requests_kwargs):
        self.requests_kwargs = requests_kwargs

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def down(self, _url, _referer):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as _session:
            async with _session.get(_url, headers={'Referer': _referer}, **self.requests_kwargs) as response:
                return await response.read()

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def auth(self, _url, _headers, _data):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as _session:
            async with _session.post(_url, headers=_headers, data=_data, **self.requests_kwargs) as response:
                return await response.json(), response.status in [200, 301, 302], response.status

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def fetch(self, _url, _headers, _params):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as _session:
            async with _session.get(_url, headers=_headers, params=_params,
                                    **self.requests_kwargs) as response:
                return await response.json()

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def post(self, _url, _data, _headers, _params):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as _session:
            async with _session.post(_url, data=_data, headers=_headers,
                                     params=_params, **self.requests_kwargs) as response:
                return await response.json()

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def delete(self, _url, _headers, _params):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as _session:
            async with _session.delete(_url, headers=_headers, params=_params,
                                       **self.requests_kwargs) as response:
                return await response.json()
