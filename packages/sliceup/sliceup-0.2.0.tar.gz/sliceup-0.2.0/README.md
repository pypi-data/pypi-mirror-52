# Sliceup

![PyPI](https://img.shields.io/pypi/v/sliceup) ![PyPI - Downloads](https://img.shields.io/pypi/dm/sliceup) ![GitHub](https://img.shields.io/github/license/sliceup/sliceup-python)

Python client of the SliceUp API

Installing
---
```bash
$ pip install sliceup
```

Examples
---

### Importing

```python
from sliceup import *
```

### Database summary

```python
from sliceup import *

sliceup = Sliceup('demo.sliceup.co')

response = sliceup.summary()

if response:
    print(response.content)
else:
    print('An error has occurred.')
```

### Create a table

```python
from sliceup import *

sliceup = Sliceup('demo.sliceup.co')

response = sliceup.create({
    'name': 'orders',
    'columns': [
       {'name': 'time', 'type': 'time'},
       {'name': 'qty', 'type': 'int'},
       {'name': 'price', 'type': 'float'}
    ],
    'recreate': True
})

if response:
    print(response.content)
else:
    print('An error has occurred.')
```

### Insert data

```python
from sliceup import *

sliceup = Sliceup('demo.sliceup.co')

response = sliceup.insert({
    'name': 'orders', 
    'rows': [
        {'time': '00:00:00', 'qty': 2, 'price': 9.0},
        {'time': '00:30:09', 'qty': 2, 'price': 2.0},
        {'time': '01:45:01', 'qty': 4, 'price': 1.0},
        {'time': '12:10:33', 'qty': 10, 'price': 16.0},
        {'time': '16:00:09', 'qty': 4, 'price': 8.0},
        {'time': '22:00:00', 'qty': 4, 'price': 23.0},
        {'time': '22:31:49', 'qty': 4, 'price': 45.0},
        {'time': '22:59:19', 'qty': 4, 'price': 17.0},
    ]
})

if response:
    print(response.content)
else:
    print('An error has occurred.')
```

### Query data
*Check out in [RunKit](https://runkit.com/sliceup/5d7c162cea9933001c32a424)*

#### Select from table

```python
from sliceup import *

sliceup = Sliceup('demo.sliceup.co')

response = sliceup.query({
    'select': ['time', 'qty', 'price'],
    'from': 'orders'
})

if response:
    print(response.content)
else:
    print('An error has occurred.')
```

#### Visualize data

```python
from sliceup import *

sliceup = Sliceup('demo.sliceup.co')

response = sliceup.query({
    'select': ['time', 'qty', 'price'],
    'from': 'orders'
})

if response:
    print(response.content)
else:
    print('An error has occurred.')
```

#### Query table statistics

```python
from sliceup import *

sliceup = Sliceup('demo.sliceup.co')

response = sliceup.query({
   'select': [max('time'), min('time'), min('qty'), max('qty'), min('price'), max('price')],
   'from': 'orders'
})

if response:
    print(response.content)
else:
    print('An error has occurred.')
```

#### Slice the data into hour buckets

```python
from sliceup import *

sliceup = Sliceup('demo.sliceup.co')

response = sliceup.query({
  'select': count('price'),
  'by': bar('time', time(1,0,0)),
  'from': 'orders'
})

if response:
    print(response.content)
else:
    print('An error has occurred.')
```

#### Slice and group the quantity by bars of 2

```python
from sliceup import *

sliceup = Sliceup('demo.sliceup.co')

response = sliceup.query({
   'select': count('price'),
   'by': bar('qty', 2),
   'from': 'orders'
})

if response:
    print(response.content)
else:
    print('An error has occurred.')
```

License
---

Sliceup is copyright (c) 2019-present SliceUp, Inc.

Sliceup is free software, licensed under the MIT. See the LICENSE file for more details.
