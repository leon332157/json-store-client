import json

import jsonpickle
import requests
import pkg_resources

DEFAULT_TIMEOUT_SECONDS = 5


class JsonstoreError(Exception):
    """Exception for errors occurring in calls to Jsonstore"""
    pass


class Client:
    """Http client for the www.jsonstore.io API

    Usage:

        import json_store_client

        #Initialize the client class

        client = json_store_client.Client('insert your token/url here')

    Save/Change data in jsonstore with a key

        client.save('test_key', {'a':'B'})

    Get data in jsonstore with a key

        test_dict=client.get('test_key')
        test_dict => {'a':'B'}

    Delete data in jsonstore with a key

        client.delete('test_key')

    """

    def __init__(self, token: str):
        self.session = requests.Session()
        self.version = pkg_resources.require("json-store-client")[0].version
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'User-Agent': f'Mozilla/5.0 Python/json-store-client/{self.version}'
            }
            )
        if token.startswith('https://'):
            token = token.split('/')[-1]
        self.__base_url = f'https://www.jsonstore.io/{token}'

    def retrieve(self, key: str, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Get gets value from jsonstore.

        :param key:str Name of key to a resource
        :param timeout:int Timeout of the request in seconds
        :return: The object that was stored
        """
        url = self.__finalize_url(key)
        try:
            resp = self.session.get(url, timeout=timeout)
            json_resp = self.__check_response(resp)
            if not json_resp:
                return None
            return jsonpickle.decode(json_resp['result'])
        except (ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    get = retrieve

    def store(self, key: str, data, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Save data in jsonstore under a key.

        :param key:str Name of key to a resource
        :param data:any Data to be updated, will be dumped with jsonpickle.
        :param timeout:int Timeout of the request in seconds
        """
        url = self.__finalize_url(key)
        json_data = json.dumps(jsonpickle.encode(data))
        try:
            resp = self.session.post(url, data=json_data, timeout=timeout)
            self.__check_response(resp)
        except (ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    save = store

    def delete(self, key: str, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Deletes data in jsonstore under a key.

        :param key:str Name of key to a resource
        :param timeout:int Timeout of the request in seconds
        """
        url = self.__finalize_url(key)
        try:
            resp = self.session.delete(url,
                                       timeout=timeout)
            self.__check_response(resp)
        except (ValueError, KeyError) as e:
            raise JsonstoreError(str(e))

    def __check_response(self, response):
        """Checks if a response is successful raises a JsonstoreError if not.

        :param response: Response to check
        :return: Deserialized json response
        """
        if not isinstance(response, requests.Response):
            raise TypeError('Unexpected type {}'.format(type(response)))
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
