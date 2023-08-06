# https://stackoverflow.com/questions/53376099/python-dataclass-from-dict#answer-53505530

import dataclasses
import importlib
import sys


def dataclass_object_dump(ob):
    datacls = type(ob)
    if not dataclasses.is_dataclass(datacls):
        raise TypeError(f"Expected dataclass instance, got '{datacls!r}' object")
    mod = sys.modules.get(datacls.__module__)
    if mod is None or not hasattr(mod, datacls.__qualname__):
        raise ValueError(f"Can't resolve '{datacls!r}' reference")
    ref = f"{datacls.__module__}.{datacls.__qualname__}"
    fields = (f.name for f in dataclasses.fields(ob))
    return {**{f: getattr(ob, f) for f in fields}, '__dataclass__': ref}


def dataclass_object_load(d):
    ref = d.pop('__dataclass__', None)
    if ref is None:
        return d
    try:
        modname, hasdot, qualname = ref.rpartition('.')
        module = importlib.import_module(modname)
        datacls = getattr(module, qualname)
        if not dataclasses.is_dataclass(datacls) or not isinstance(datacls, type):
            raise ValueError
        return datacls(**d)
    except (ModuleNotFoundError, ValueError, AttributeError, TypeError):
        raise ValueError(f"Invalid dataclass reference {ref!r}") from None
