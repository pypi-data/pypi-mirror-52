import json


class Cache:

    def __init__(self, connection):
        self.connection = connection

    async def get(self, name, type, cls) -> dict:
        result = await self.connection._con.get(f'{{"name": {name}, "type": {type}, "class": {cls}}}')
        if result:
            return json.loads(result)
        return {}

    async def set(self, name: str, type: int, cls: int, data: str, expire: int = 600) -> None:
        await self.connection._con.set(f'{{"name": {name}, "type": {type}, "class": {cls}}}', data)
        await self.connection._con.expire(f'{{"name": {name}, "type": {type}, "class": {cls}}}', expire)
