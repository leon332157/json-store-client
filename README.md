# json-store-client
A Python client for jsonstore.io

## Installation

```bash
pip install json-store-client
```

## Usage

```python
import json_store_client

# Initialize the client class

client = json_store_client.Client('insert your token/url here')
```
#### Parameters:
##### token (required[str]): The token or the url you get from jsonstore.io

### Store data in jsonstore with a key

```python

client.store('test_key', {'a':'B'})
```

#### Parameters:
##### key (required[str]): The key to be stored on jsonstore.
##### data (required[any]): The data to be stored under the key. It can be any Python objects. Will be processed with [jsonpickle](https://github.com/jsonpickle/jsonpickle)
##### timeout (optional[int]): The timeout for the http request. Default 5 seconds.

## Retrieve data in jsonstore with a key

```python

test_dict=client.retrieve('test_key')
# test_dict => {'a':'B'}

```

#### Parameters:
##### key (required[str]): The key to get on jsonstore.
##### timeout (optional[int]): The timeout for the http request. Default 5 seconds.

## Delete data in jsonstore with a key

```python
client.delete('test_key')
```

#### Parameters:
##### key (required[str]): The key to get on jsonstore.
##### timeout (optional[int]): The timeout for the http request. Default 5 seconds.