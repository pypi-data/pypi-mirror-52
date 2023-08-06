from .base import GenericAPIConnector, AsDictObject, CommandsMethodHolder, APIResource

class UserObject(AsDictObject):
    name = 'test'


class ImplementedAPIConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    users = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))
    postboxes = APIResource(('retrieve',))
    notes = APIResource('all')
    tags = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))
    types = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))


conn = ImplementedAPIConnector()
# print(conn.notes.list())
print(dir(CommandsMethodHolder))
# conn.users.list()
print(conn.notes.list().json())
async def test():
    r = await conn.notes(is_async=True).list()
    data = await r.json()
    print(data)
import asyncio
asyncio.run(test())


if __name__ == "__main__":
    pass
