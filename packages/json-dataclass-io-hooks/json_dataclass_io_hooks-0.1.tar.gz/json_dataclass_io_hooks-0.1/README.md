JSON encoder/decoder hooks for Python dataclasses
===

This project contains custom hooks that can be used with Python's json package. 
These hooks can be to produce JSON from and to predefined existing dataclasses.

Source: https://stackoverflow.com/questions/53376099/python-dataclass-from-dict#answer-53505530

Usage
===

```python
json_str = json.dumps(dataclass_object, default=dataclass_object_dump)

dataclass_object = json.loads(json_str, object_hook=dataclass_object_load)
```

