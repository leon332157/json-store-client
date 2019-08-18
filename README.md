# json-store-client
A Python client for [jsonstore.io](https://www.jsonstore.io/)

## Installation
```bash
pip install json-store-client
```
#### An optional installation of [ujson](https://pypi.org/project/ujson/) is recommended for faster json processing.
##### Also installing [cchardet](https://pypi.org/project/cchardet/) and [aiodns](https://pypi.org/project/aiodns/) are recommended by aiohttp for faster performance.

## Usage

#### Demo of storing a Python json-friendly object with json-store-client in async on [repl.it](https://repl.it/@leon332157/json-store-client-demo).

```python
import json_store_client

jsonStoreToken = '...' # Insert your token here.
client = json_store_client.AsyncClient(jsonStoreToken)
async def demo_function():
 # Save data to the 'foo' key.
 await client.store('foo', {'alfa': 'bravo', 'charlie': 'delta'})

 # Save data with dict mapping
 await client.save_multiple({'foo':{'alfa': 'bravo', 'charlie': 'delta'}})

 # Get the data from the 'foo' key.
 data = await client.retrieve('foo')

 print(data['alfa']) # => 'bravo'

 # Deletes the data after printing parts of it.
 await client.delete('foo')
```

## json-store-client API

### json_store_client.Client(token)
### json_store_client.AsyncClient(token)

Returns the client to use for data operations.

###### token (str): The API token from [jsonstore.io](https://www.jsonstore.io)


### client.store(key, data[, timeout])
### await client.store(key, data[, timeout])

Storing data in jsonstore with a key

###### key (str): The key to be stored on jsonstore
###### data (any): The data to be stored under the key. It can be any Python objects.
###### timeout (int): The timeout for the http request. Default 5 seconds

### client.store_multiple(data[, timeout])
### await client.store_multiple(data[, timeout])

Storing data in jsonstore with a dict mapping

###### data (dict):  A dict of {key(s):value(s)} to be updated. 
###### timeout (int): The timeout for the http request. Default 5 seconds

### client.retrieve(key[, timeout])
### await clent.retrieve(key[, timeout])
Retrieve data in jsonstore with a key

##### If nothing is saved under the key, it will return None.

###### key (str): The key to get on jsonstore
###### timeout (int): The timeout for the http request. Default 5 seconds


### client.delete(key[, timeout])
### await client.delete(key[, timeout])

Delete data in jsonstore with a key

###### key (str): The key to get on jsonstore
###### timeout (int): The timeout for the http request. Default 5 seconds
