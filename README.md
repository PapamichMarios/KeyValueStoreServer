# KeyValueStoreServer

# Tools used
- Python 3.8
- PyCharm
- Windows 10

# Files

### Python
- **./data_creation/createData.py**: creates data and stores them in dataToIndex.txt
- **kvBroker.py**: key value store broker
- **kvServer.py**: key value store server
- **utils.py**: utility functions
- **logging.py**: functions for logging
- **properties.py**: strings and other properties
- **errors.py**: error functions
- **trie.py**: class for the trie data structure

### Text
- **dataToIndex.txt**: contains data for kvBroker.py indexing
- **keyFile.txt**: contains data for createData.py. 
The data types available are: [string, float, int, set]. Set symbolizes a nested value e.g. location set -> "location" : { "key" : "value" }
- **serverFile.txt**: contains ip and ports for the kvServer.py

# How to run

From root directory:

- Create data:

```python ./data_creation/createData.py -k ./data_creation/keyFile.txt -n 1000 -d 3 -l 4 -m 5```

or 

```python ./data_creation/createData.py -k ./data_creation/keyFile.txt```

- Run Key Value Servers

```
python kvServer.py -a 127.0.0.1 -p 65432
python kvServer.py -a 127.0.0.1 -p 65433
python kvServer.py -a 127.0.0.1 -p 65434
```

or 

```
python kvServer.py -p 65432
python kvServer.py -p 65433
python kvServer.py -p 65434
```

for localhost with different ports

- Run Key Value Broker

```python kvBroker.py -s serverFile.txt -i ./data_creation/dataToIndex.txt -k 2```

# Summary
The kvBroker.py indexes data between k kvServer.py replicas and then is open to queries:

- **GET**: retrieves top level key, if k servers are down prints warning message

- **QUERY**: retrieves any level key, if k servers are down prints warning message

- **DELETE**: deletes key from all the servers, if at least one server is down prints error message and does not execute

# Sample Execution
Let's say that we have 3 kvServer.py instances running in 3 different ports and two of them contain:
 
```"key_0" : {"street": "dkbfx" ; "address": {"level": 33} ; "height": 91.21095965769372 ; "level": 41}```

```"key_1" : {"location": {"location": {"height": 5.104534969166997}} ; "level": 28}```

```
kv_broker$:  GET key_0 
  "key_0": {"street": "dkbfx", "address": {"level": 33}, "height": 91.21095965769372, "level": 41}
```
  
```
kv_broker$:  QUERY key_0
  "key_0": {"street": "dkbfx", "address": {"level": 33}, "height": 91.21095965769372, "level": 41}
```
  
```
kv_broker$: QUERY key_0.address.level
  "key_0.address.level": 33
```
  
```
kv_broker$:  GET kEsda
  ERROR: NOT_FOUND
```
  
```
kv_broker$:  DELETE key_0
  OK
```
  
```
kv_broker$:  GET key_0
  ERROR: NOT_FOUND
```
  
Let's say one server dies unexpectedly:

```
kv_broker$:  DELETE key_1
  ERROR - REPLICA_IS_DOWN: CANNOT_EXECUTE
```
  
Now another one dies (remember k=2)

```
kv_broker$:  GET key_1
  WARNING - REPLICA_IS_DOWN: CANNOT_GUARANTEE_CORRECT_OUTPUT
```
