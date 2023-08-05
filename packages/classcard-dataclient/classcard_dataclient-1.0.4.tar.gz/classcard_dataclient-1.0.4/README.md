## DataClient

### Introduction
this is a tool which save data to class card server

### Usage
1. init client
```python
client = DataClient()
```

2. call method
```python
data = {
    "xxx": "xxx"
}
code, msg = client.create_section(data=data)
```
> notice:
* when data is dict , code is integer, msg is string, 
* when data is list, the code is list, msg is also list.




