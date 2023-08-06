import json
import aiohttp

class Resolver:

    def __init__(self, connection):
        self.connection = connection

    async def find(self, type: int, cls: int, name: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.connection.base_url + f'{type}/{cls}/{name}/') as resp:
                if resp.status == 200:
                    return json.loads(await resp.text())
                raise Exception(
                    f'Got status code {resp.status} while trying to get ' + self.connection.base_url + f'{type}/{cls}/{name}/')