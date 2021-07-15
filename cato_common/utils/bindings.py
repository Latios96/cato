import inspect
import os
from typing import Type, TypeVar

from pinject.object_graph import ObjectGraph

from cato_common.utils.typing import safe_cast

T = TypeVar("T")


def _is_in_module_with_path(module_paths, module):
    for module_path in module_paths:
        if getattr(module, "__file__", None) is None:
            return False
        if getattr(module, "__file__", None).startswith(module_path):
            return True
    return False


def iter_module(seen, module, module_paths):
    if module in seen:
        return
    seen.add(module)
    if not _is_in_module_with_path(module_paths, module):
        return
    for name, mod in inspect.getmembers(module, inspect.ismodule):
        iter_module(seen, mod, module_paths)


def imported_modules(modules):
    all_found = set()
    for module in modules:
        name__ = module.__file__
        iter_module(all_found, module, [os.path.dirname(name__)])
    return all_found


def provide_safe(obj_graph: ObjectGraph, cls: Type[T]) -> T:
    return safe_cast(cls, obj_graph.provide(cls))
