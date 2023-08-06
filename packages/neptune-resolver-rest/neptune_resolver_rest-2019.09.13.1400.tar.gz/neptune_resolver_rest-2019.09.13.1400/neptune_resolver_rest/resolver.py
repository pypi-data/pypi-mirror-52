import json


class Resolver:
    can_save = False

    def __init__(self, connection):
        self.connection = connection

    async def find(self, type, cls, name) -> dict:
        async with self.connection._session.get(self.connection.base_url + f'{type}/{cls}/{name}/') as resp:
            if resp.status == 200:
                return json.loads(await resp.text())
            raise Exception(
                f'Got status code {resp.status} while trying to get ' + self.connection.base_url + f'{type}/{cls}/{name}/')

    async def save(self, name, type, cls, data,  expire=600) -> None:
        pass
