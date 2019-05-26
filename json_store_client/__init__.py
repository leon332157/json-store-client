"""Http client for the www.jsonstore.io API

Usage (sync client):

    import json_store_client

    #Initialize the sync client class

    client = json_store_client.Client('insert your token/url here')

Save/Change data in jsonstore with a key

    client.store('test_key', {'a':'B'})
    client.save({'a':'B'}) # Using dict key and value mapping, a is the key and B is the value.

Get data in jsonstore with a key

    test_dict=client.get('test_key')
    test_dict => {'a':'B'}

Delete data in jsonstore with a key

    client.delete('test_key')

Usage (async client):

    import json_store_client

    #Initialize the sync client class

    client = json_store_client.AsyncClient('insert your token/url here')

Save/Change data in jsonstore with a key

    await client.store('test_key', {'a':'B'})
    await client.save({'test_key:{'a':'B'}) # Using dict key and value mapping.

Get data in jsonstore with a key

    test_dict = await client.get('test_key')
    test_dict => {'a':'B'}

Delete data in jsonstore with a key

    await client.delete('test_key')
"""
import json
from warnings import warn

import aiohttp
import jsonpickle
import pkg_resources
import requests

DEFAULT_TIMEOUT_SECONDS = 5
VERSION = '1.0.2'


class JsonstoreError(Exception):
    """Exception for errors occurring in calls to Jsonstore"""
    pass


class EmptyResponseWarning(Warning):
    """Warning for empty response from Jsonstore"""
    pass


class Client:

    def __init__(self, token: str):
        self.session = requests.Session()
        self.version = VERSION
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'User-Agent': f'Mozilla/5.0 Python/json-store-client/{self.version}'
            })
        if not isinstance(token, str):
            raise TypeError("Token must be str, not {}".format(token.__class__.__name__))
        if token.startswith('https://'):
            token = token.split('/')[-1]
        self.__base_url = f'https://www.jsonstore.io/{token}'

    def retrieve(self, key: str, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Get gets value from jsonstore.

        :param key:str Name of key to a resource
        :param timeout:int Timeout of the request in seconds
        :return: The object that was stored
        """
        if not isinstance(key, str):
            raise TypeError("Key must be str, not {}".format(key.__class__.__name__))
        url = self.__finalize_url(key)
        try:
            resp = self.session.get(url, timeout=timeout)
            json_resp = self.__check_response(resp)
            if not json_resp or not json_resp['result']:
                warn('Jsonstore returned null, please make sure something is saved under this key.', EmptyResponseWarning)
                return None
            return jsonpickle.decode(json_resp['result'])
        except (ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    get = retrieve

    def store(self, key: str, data, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Save data in jsonstore under a key.

        :param key:str Name of key to a resource
        :param data:any Data to be updated/saved, will be processed with jsonpickle.
        :param timeout:int Timeout of the request in seconds
        """
        if not isinstance(key, str):
            raise TypeError("Key must be str, not {}".format(key.__class__.__name__))
        url = self.__finalize_url(key)
        json_data = json.dumps(jsonpickle.encode(data))
        resp = self.session.post(url, data=json_data, timeout=timeout)
        self.__check_response(resp)
        return json_data

    save = store

    def store_multiple(self, data: dict, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Save data in jsonstore with a dict mapping.

        :param data:dict A dict of {key(s):value(s)} to be updated. Value(s) can be any python object, will be processed with jsonpickle.
        :param timeout:int Timeout of the request in seconds
        """
        if not isinstance(data, dict):
            raise TypeError("The data must be dict, not {}".format(data.__class__.__name__))
        for key, value in data.items():
            self.store(key, value, timeout)

    save_multiple = store_multiple

    def delete(self, key: str, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Deletes data in jsonstore under a key.

        :param key:str Name of key to a resource
        :param timeout:int Timeout of the request in seconds
        """
        if not isinstance(key, str):
            raise TypeError("Key must be str, not {}".format(key.__class__.__name__))
        url = self.__finalize_url(key)
        resp = self.session.delete(url, timeout=timeout)
        self.__check_response(resp)
        return key

    def __check_response(self, response):
        """Checks if a response is successful raises a JsonstoreError if not.

        :param response: Response to check
        :return: Deserialized json response
        """
        if not isinstance(response, requests.Response):
            raise TypeError('Unexpected type {}'.format(type(response.__class__.__name__)))
        response.raise_for_status()
        resp = response.json()
        if 'ok' not in resp:
            raise JsonstoreError('Call to jsonstore failed')
        return resp

    def __finalize_url(self, key):
        """Creates url for a given key.

        :param key: Key to append to the base url
        :return: URL to resource
        """
        return '{}/{}'.format(self.__base_url, key)


class AsyncClient:
    def __init__(self, token: str):
        self.version = VERSION
        self.session = aiohttp.ClientSession(headers={
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'User-Agent': f'Mozilla/5.0 Python/json-store-client/{self.version}'
            })
        if not isinstance(token, str):
            raise TypeError("Token must be str, not {}".format(token.__class__.__name__))
        if token.startswith('https://'):
            token = token.split('/')[-1]
        self.__base_url = f'https://www.jsonstore.io/{token}'

    async def retrieve(self, key: str, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Get gets value from jsonstore.

        :param key:str Name of key to a resource
        :param timeout:int Timeout of the request in seconds
        :return: The object that was stored
        """
        if not isinstance(key, str):
            raise TypeError("Key must be str, not {}".format(key.__class__.__name__))
        url = await self.__finalize_url(key)
        try:
            async with self.session.get(url, timeout=timeout) as s:
                json_resp = await s.json()
            if not json_resp or not json_resp['result']:
                warn('JSONSTORE WARNING: Jsonstore returned null, please make sure something is saved under this key.')
                return None
            return jsonpickle.decode(json_resp['result'])
        except (ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    get = retrieve

    async def store(self, key: str, data, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Save data in jsonstore under a key.

        :param key:str Name of key to a resource
        :param data:any Data to be updated/saved, will be processed with jsonpickle.
        :param timeout:int Timeout of the request in seconds
        """
        if not isinstance(key, str):
            raise TypeError("Key must be str, not {}".format(key.__class__.__name__))
        url = await self.__finalize_url(key)
        json_data = json.dumps(jsonpickle.encode(data))
        async with self.session.post(url, data=json_data, timeout=timeout) as s:
            s.raise_for_status()
        return json_data

    save = store

    async def store_multiple(self, data: dict, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Save data in jsonstore with a dict mapping.

        :param data:dict A dict of {key(s):value(s)} to be updated. Value(s) can be any python object, will be processed with jsonpickle.
        :param timeout:int Timeout of the request in seconds
        """
        if not isinstance(data, dict):
            raise TypeError("The data must be dict, not {}".format(data.__class__.__name__))
        for key, value in data.items():
            await self.store(key, value, timeout)

    save_multiple = store_multiple

    async def delete(self, key: str, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Deletes data in jsonstore under a key.

        :param key:str Name of key to a resource
        :param timeout:int Timeout of the request in seconds
        """
        if not isinstance(key, str):
            raise TypeError("Key must be str, not {}".format(key.__class__.__name__))
        url = await self.__finalize_url(key)
        async with self.session.delete(url, timeout=timeout) as s:
            s.raise_for_status()
        return key

    async def __finalize_url(self, key):
        """Creates url for a given key.

        :param key: Key to append to the base url
        :return: URL to resource
        """
        return '{}/{}'.format(self.__base_url, key)
