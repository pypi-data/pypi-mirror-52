# HippyBase
HippyBase is a Python library to interact with Apache Hbase through its REST api.

## Installation
```bash
pip install hippybase
```

## Example
```python
import hippybase

connection = hippybase.Connection('hostname')
table=connection.table('table_name')

table.put('row_key', {'family:qual': 'value'})

row = table.row('row_key')

for key, data in table.scan():
    print(key, data)
```