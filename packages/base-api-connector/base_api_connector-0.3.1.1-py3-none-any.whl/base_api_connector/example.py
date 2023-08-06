from base import GenericAPIConnector, AsDictObject, CommandsMethodHolder, APIResource

class UserObject(AsDictObject):
    name = 'test'


# class ImplementedAPIConnector(GenericAPIConnector):
#     base_api_url = 'http://127.0.0.1:8000/notes-backend/'
#     users = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))
#     postboxes = APIResource(('retrieve',))
#     notes = APIResource('all')
#     tags = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))
#     types = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))

class TestAPIConnector(GenericAPIConnector):
    base_headers = {'cool-token': 'yourpasswordhere'}
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    notes = APIResource(('list', 'create', 'retrieve', 'update', 'destroy'))

conn = TestAPIConnector()
# print(conn.notes.list())
# print(dir(CommandsMethodHolder))
# conn.users.list()
# print(conn.notes.list().json())
# async def test():
#     r = await conn.notes(is_async=True).list()
#     data = await r.json()
#     print(data)
# import asyncio
# asyncio.run(test())

print(conn.notes.update(2, {'detail': 'phew'}).json())
import inspect
print(conn.notes.retrieve.__name__)
print(inspect.getfullargspec(conn.notes.retrieve))
print(conn.notes.retrieve(2).json())
# print(conn.notes.list().json())
# print(conn.notes(is_async=True).retrieve.__name__)
# print(inspect.getfullargspec(conn.notes(is_async=True).retrieve))


if __name__ == "__main__":
    pass
