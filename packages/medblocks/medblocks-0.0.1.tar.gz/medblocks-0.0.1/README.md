# Medblocks.py

## Installation
```
pip install -r requirements.txt
```


## Usage
```python
from medblocks import Client

api = Client("165.22.211.124")
api.register("email@example.com", "yoursecretpassword")
api.login("email@example.com", "yoursecretpassword")
api.list()
# Returns all medblocks on the blockchain
api.addBlock("file.txt", "anotheremail@example.com")

```
