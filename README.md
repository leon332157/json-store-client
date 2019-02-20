# json-store-client
A Python client for [jsonstore.io](https://www.jsonstore.io/)

## Installation
```bash
pip install json-store-client
```

## Usage

#### Demo of storing a Python object with json-store-client on [repl.it](https://repl.it/@leon332157/json-store-client-demo).

```python
import json_store_client

jsonStoreToken = "..." # Insert your token here.
client = json_store_client.Client(jsonStoreToken)

# Save data to the "foo" key.
client.store("foo", {"alfa": "bravo", "charlie": "delta"})

# Get the data from the "foo" key.
data = client.retrieve("foo")

print(data["alfa"]) # => "bravo"

# Deletes the data after printing parts of it.
client.delete("foo")
```

## json-store-client API

### json_store_client.Client(token)

Returns the client to use for data operations.

###### token (str): The API token from [jsonstore.io](https://www.jsonstore.io)


### client.store(key, data[, timeout])

Storing data in jsonstore with a key

###### key (str): The key to be stored on jsonstore
###### data (any): The data to be stored under the key. It can be any Python objects. Will be processed with [jsonpickle](https://github.com/jsonpickle/jsonpickle)
###### timeout (int): The timeout for the http request. Default 5 seconds


### client.retrieve(key[, timeout])

Retrieve data in jsonstore with a key

##### If nothing is saved under the key, it will return None.

###### key (str): The key to get on jsonstore
###### timeout (int): The timeout for the http request. Default 5 seconds


### client.delete(key[, timeout])

Delete data in jsonstore with a key

###### key (str): The key to get on jsonstore
###### timeout (int): The timeout for the http request. Default 5 seconds
