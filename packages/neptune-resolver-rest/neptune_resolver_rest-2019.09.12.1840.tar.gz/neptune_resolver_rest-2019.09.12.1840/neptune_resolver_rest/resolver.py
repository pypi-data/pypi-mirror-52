import json


class Resolver:
    can_save = False

    def __init__(self, connection):
        self.connection = connection

    async def find(self, name, type, cls) -> dict:
        return self.connection.get(type, cls, name)

    async def save(self, name, type, cls, data,  expire=600) -> None:
        pass
