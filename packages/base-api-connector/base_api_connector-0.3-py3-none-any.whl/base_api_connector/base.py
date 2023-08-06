import requests
import inspect
import functools
import aiohttp

# TODO: maybe make a program that can go through django and generate code for a connector that you can copy paste into where you use it

POSSIBLE_COMMANDS = ('list', 'create', 'retrieve', 'update', 'destroy')
COMMAND_TO_METHOD = dict(zip(POSSIBLE_COMMANDS, ('get', 'post', 'get', 'patch', 'delete')))
COMMAND_TO_ARGS = dict(zip(POSSIBLE_COMMANDS, ((), ('load',), ('pk',), ('pk', 'load'), ('pk',))))



# class CommandsMethodHolder:  # TODO: upgrade Response object r with helpful stuff like accessing the id when using create
#     def get_full_url(self, pk=None):
#         raise NotImplementedError

#     def list(self):  # TODO: also, do I want validation for data?
#         def list(**kwargs):
#             url = self.get_full_url()
#             r = requests.get(url, **kwargs)
#             return r
#         return list

#     def create(self):
#         def create(data=None, **kwargs):
#             if isinstance(data, AsDictObject):
#                 data = data.as_dict()
#             url = self.get_full_url()
#             r = requests.post(url, data, **kwargs)
#             return r
#         return create

#     def retrieve(self):
#         def retrieve(pk, **kwargs):
#             url = self.get_full_url(pk)
#             r = requests.get(url, **kwargs)
#             return r
#         return retrieve

#     def update(self):
#         def update(pk, data=None, **kwargs):
#             if isinstance(data, AsDictObject):
#                 data = data.as_dict()
#             url = self.get_full_url(pk)
#             r = requests.patch(url, data, **kwargs)
#             return r
#         return update

#     def destroy(self):
#         def destroy(pk, **kwargs):
#             url = self.get_full_url(pk)
#             r = requests.delete(url, **kwargs)
#             return r
#         return destroy


# class AsyncCommandsMethodHolder:
#     def get_full_url(self, pk=None):
#         raise NotImplemented

#     def list(self):
#         async def list(**kwargs):
#             async with aiohttp.ClientSession() as session:
#                 url = self.get_full_url()
#                 r = await session.get(url=url, **kwargs)
#                 return r
#         return list

#     def create(self):
#         async def create(data=None, **kwargs):
#             async with aiohttp.ClientSession() as session:
#                 url = self.get_full_url()
#                 r = await session.post(url=url, data=data, **kwargs)
#                 return r
#         return create

#     def retrieve(self):
#         async def retrieve(pk, **kwargs):
#             async with aiohttp.ClientSession() as session:
#                 url = self.get_full_url(pk)
#                 r = await session.get(url=url, **kwargs)
#                 return r
#         return retrieve

#     def update(self):
#         async def update(pk, data=None, **kwargs):
#             async with aiohttp.ClientSession() as session:
#                 url = self.get_full_url(pk)
#                 r = await session.patch(url=url, data=None, **kwargs)
#                 return r
#         return update

#     def destroy(self):
#         async def destroy(pk, data=None, **kwargs):
#             async with aiohttp.ClientSession() as session:
#                 url = self.get_full_url(pk)
#                 r = await session.delete(url=url, data=None, **kwargs)
#                 return r
#         return destroy


# TODO: right now all methods appear no matter which commands you pass, I don't want that
# maybe make it so you have to create a class, pass in mixins and instantiate it immediately?
class APIResource:
    api = type('EmptyAPIConnector', (), {'base_api_url': '/'})
    name = ''
    commands = POSSIBLE_COMMANDS

    def list(self, **kwargs):
        raise NotImplementedError

    def create(self, load, load_mode='json', **kwargs):
        raise NotImplementedError

    def retrieve(self, pk, **kwargs):
        raise NotImplementedError

    def update(self, pk, load, load_mode='json', **kwargs):
        raise NotImplementedError

    def destroy(self, pk, **kwargs):
        raise NotImplementedError

    # replace with enum or constants for async?
    def __init__(self, commands, is_async=False, api=None, resource_name=None, *args, **kwargs):
        self.is_async = is_async
        if commands != 'all':
            self.commands = tuple(commands)
        self.assign_command_type(is_async)

        if api is not None:
            self.api = api
        if resource_name is not None:
            self.name = resource_name

    def __call__(self, is_async=False,):
        if self.is_async != is_async:
            # create instance with is async methods
            return APIResource(self.commands, is_async=is_async, api=self.api, resource_name=self.name)
        else:
            return self

    def assign_command_type(self, is_async=False):
        if self.is_async:
            self._assign_commands(_generate_async_method)
        else:
            self._assign_commands(_generate_requests_method)

    def _assign_commands(self, generate_func):
        for command in self.commands:
            setattr(self, command, generate_func(self, command))

    def get_full_url(self, pk=''):
        return f'{self.api.base_api_url}{self.name}/' + (f'{pk}/' if pk else '')


class GenericAPIConnector:
    def __new__(cls):
        for name in dir(cls):
            attr = getattr(cls, name)
            if isinstance(attr, APIResource):
                attr.api = cls
                attr.name = name
        return object.__new__(cls)

    base_data = {}  # add base data
    base_headers = {}  # add base headers
    resource_config = None
    # TODO: could make a list of resources, which will be generated automatically, ahh, but no autocomplete then...

    @property
    def base_api_url(self):
        raise NotImplementedError


class AsDictObject:
    def as_dict(self):
        attributes = inspect.getmembers(self, lambda a: not inspect.isroutine(a))
        dict_repr = {}
        for name, value in attributes:
            if '_' not in name[0]:
                if isinstance(value, AsDictObject):
                    value = value.as_dict()
                elif isinstance(value, list):
                    value = [i.as_dict() if isinstance(i, AsDictObject) else i for i in value]

                if callable(value):
                    dict_repr[name] = value()
                else:
                    dict_repr[name] = value
        return dict_repr


def check_request_args(command, args):
    if len(args) != len(COMMAND_TO_ARGS[command]):
        raise TypeError(f'{command}() takes {len(COMMAND_TO_ARGS[command])} positional arguments but {len(args)} was given')


def _validate_request(inst, command, args, kwargs):
    check_request_args(command, args)
    for i, key in enumerate(COMMAND_TO_ARGS[command]):
        if key == 'load':
            key = kwargs.pop('load_mode')
            print(key)
        kwargs[key] = args[i]

    if isinstance(kwargs.get('json'), AsDictObject):
        kwargs['json'] = kwargs['json'].as_dict()
    if isinstance(kwargs.get('data'), AsDictObject):
        kwargs['data'] = kwargs['data'].as_dict()

    headers = kwargs.get('headers', {})
    headers.update(inst.api.base_headers)
    kwargs['headers'] = headers

    kwargs['url'] = inst.get_full_url(kwargs.pop('pk', None))

    return kwargs

# TODO: could you return other, custom, useful stuff with the response?

def _generate_requests_method(inst: APIResource, command):
    @functools.wraps(getattr(inst, command))
    def _(*args, load_mode='json', **kwargs):
        if command in ('create', 'update'):
            kwargs['load_mode'] = load_mode
        kwargs = _validate_request(inst, command, args, kwargs)
        print(kwargs)
        r = getattr(requests, COMMAND_TO_METHOD[command])(**kwargs)
        return r
    return _


def _generate_async_method(inst: APIResource, command):
    @functools.wraps(getattr(inst, command))
    async def _(*args, **kwargs):
        kwargs = _validate_request(inst, command, args, kwargs)
        async with aiohttp.ClientSession() as session:
            r = await getattr(session, COMMAND_TO_METHOD[command])(**kwargs)
            return r
    return _


# class MetaNewCommandsMethodHolder(type):
#     def __getattr__(self, name):
#         return lambda func, inst: _generate_requests_method(func, inst, name)

# class NewCommandsMethodHolder(metaclass=MetaNewCommandsMethodHolder):
#     pass
#     # def list(func, self):
#     #     @functools.wraps(func)
#     #     def _(**kwargs):
#     #         return _generate_request_logic(self, 'get', kwargs)
#     #     return _

#     # def create(func, self):
#     #     @functools.wraps(func)
#     #     def _(data, **kwargs):
#     #         return _generate_request_logic(self, 'post', kwargs, data=data)
#     #     return _

#     # def retrieve(func, self):
#     #     return _generate_requests_method(func, self, 'retrieve')
#     #     # return functools.wraps(func)(lambda pk,**kw: generate_request_logic(self, 'get', kw, pk=pk))
#     #     @functools.wraps(func)
#     #     def _(pk, **kwargs):
#     #         return _generate_request_logic(self, 'get', kwargs, pk=pk)
#     #     return _
