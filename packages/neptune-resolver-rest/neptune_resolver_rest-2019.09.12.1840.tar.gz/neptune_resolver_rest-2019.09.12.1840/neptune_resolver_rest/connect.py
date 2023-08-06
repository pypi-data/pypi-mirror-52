import json

import aiohttp

from .resolver import Resolver


class Connection:

    def __init__(self,
                 loop,
                 base_url,
                 username=None,
                 password=None):
        self.loop = loop
        self.base_url = base_url
        self.username = username
        self.password = password
        self._session = aiohttp.ClientSession()
        self.Resolver = Resolver(self)

    async def get(self, type, cls, name) -> dict:
        async with self._session.get(self.base_url + f'{type}/{cls}/{name}/') as resp:
            if resp.status == 200:
                return json.loads(await resp.text())
            raise Exception(
                f'Got status code {resp.status} while trying to get ' + self.base_url + f'{type}/{cls}/{name}/')

    async def init_connection(self) -> None:
        pass
