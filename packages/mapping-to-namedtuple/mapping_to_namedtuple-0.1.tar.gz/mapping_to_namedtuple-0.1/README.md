Convertor of Python Mappings to namedtuples
===

This project contains a function that converts a Python Mapping or dict to a namedtuple. 
The conversion works recursively and the input can contain other mappings or lists.


Usage
===

```python
from mapping_to_namedtuple import mapping_to_named_tuple

mapping = {"a": "b", "c": "d", "e": [1, 2]}

namedtuple = mapping_to_named_tuple(mapping, "test_tuple")
```

