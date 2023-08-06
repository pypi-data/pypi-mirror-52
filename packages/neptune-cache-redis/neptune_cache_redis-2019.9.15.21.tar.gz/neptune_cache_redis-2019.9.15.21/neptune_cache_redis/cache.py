import json


class Cache:

    def __init__(self, connection):
        self.connection = connection

    async def get(self, name, type, cls) -> dict:
        return json.loads(self.connection._con.get(f'{{"name": {name}, "type": {type}, "class": {cls}}}'))

    async def set(self, name, type, cls, data,  expire=600) -> None:
        self.connection._con.set(f'{{"name": {name}, "type": {type}, "class": {cls}}}',
                                 json.dumps(data))
        self.connection._con.expire(f'{{"name": {name}, "type": {type}, "class": {cls}}}', expire)