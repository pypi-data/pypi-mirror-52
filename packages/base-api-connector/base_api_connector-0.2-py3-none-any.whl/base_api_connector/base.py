import requests
import inspect
import aiohttp


POSSIBLE_COMMANDS = ('list', 'create', 'retrieve', 'update', 'destroy')


# TODO: not sure if I like this concept...
class CommandsMethodHolder:  # TODO: upgrade Response object r with helpful stuff like accessing the id when using create
    def get_full_url(self, pk=None):
        raise NotImplementedError

    def list(self):  # TODO: also, do I want validation for data?
        def list(**kwargs):
            url = self.get_full_url()
            r = requests.get(url, **kwargs)
            return r
        return list

    def create(self):
        def create(data=None, **kwargs):
            if isinstance(data, AsDictObject):
                data = data.as_dict()
            url = self.get_full_url()
            r = requests.post(url, data, **kwargs)
            return r
        return create

    def retrieve(self):
        def retrieve(pk, **kwargs):
            url = self.get_full_url(pk)
            r = requests.get(url, **kwargs)
            return r
        return retrieve

    def update(self):
        def update(pk, data=None, **kwargs):
            if isinstance(data, AsDictObject):
                data = data.as_dict()
            url = self.get_full_url(pk)
            r = requests.patch(url, data, **kwargs)
            return r
        return update

    def destroy(self):
        def destroy(pk, **kwargs):
            url = self.get_full_url(pk)
            r = requests.delete(url, **kwargs)
            return r
        return destroy

class AsyncCommandsMethodHolder:
    def get_full_url(self, pk=None):
        raise NotImplemented
    
    def list(self):
        async def list(**kwargs):
            async with aiohttp.ClientSession() as session: 
                url = self.get_full_url()
                r = await session.get(url=url, **kwargs)
                return r
        return list
    
    def create(self):
        async def create(data=None, **kwargs):
            async with aiohttp.ClientSession() as session:
                url = self.get_full_url()
                r = await session.post(url=url, data=data, **kwargs)
                return r
        return create
    
    def retrieve(self):
        async def retrieve(pk, **kwargs):
            async with aiohttp.ClientSession() as session:
                url = self.get_full_url(pk)
                r = await session.get(url=url, **kwargs)
                return r
        return retrieve
    
    def update(self):
        async def update(pk, data=None, **kwargs):
            async with aiohttp.ClientSession() as session:
                url = self.get_full_url(pk)
                r = await session.patch(url=url, data=None, **kwargs)
                return r
        return update
    
    def destroy(self):
        async def destroy(pk, data=None, **kwargs):
            async with aiohttp.ClientSession() as session:
                url = self.get_full_url(pk)
                r = await session.delete(url=url, data=None, **kwargs)
                return r
        return destroy


# TODO: right now all methods appear no matter which commands you pass, I don't want that
# maybe make it so you have to create a class, pass in mixins and instantiate it immediately?
class APIResource: 
    api = type('EmptyAPIConnector', (), {'base_api_url': '/'})
    name = ''
    commands = POSSIBLE_COMMANDS

    def list(self, **kwargs):
        raise NotImplementedError

    def create(self, data, **kwargs):
        raise NotImplementedError

    def retrieve(self, pk, **kwargs):
        raise NotImplementedError

    def update(self, pk, data, **kwargs):
        raise NotImplementedError

    def destroy(self, pk, **kwargs):
        raise NotImplementedError

    def __init__(self, commands, is_async=False, api=None, name=None, *args, **kwargs):
        self.is_async = is_async
        if commands != 'all':
            self.commands = tuple(commands)
        self._assign_commands(is_async)

        if api is not None:
            self.api = api
        if name is not None:
            self.name = name

    def __call__(self, is_async=False):
        if self.is_async != is_async:
            # create instance with is async methods
            return APIResource(self.commands, is_async=is_async, api=self.api, name=self.name)
        else:
            return self

    def _assign_commands(self, is_async):
        if self.is_async:
            for command in self.commands:
                setattr(self, command, getattr(AsyncCommandsMethodHolder, command)(self))
        else:
            for command in self.commands:
                setattr(self, command, getattr(CommandsMethodHolder, command)(self))

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


# TODO: maybe make a program that can go through django and generate code for a connector that you can copy paste into where you use it
