import sys
from typing import List, Type, TypeVar
from pinject.object_graph import ObjectGraph
from cato_common.utils.typing import safe_cast

T = TypeVar("T")


def _is_in_module_with_name(module_names, module):
    for module_name in module_names:
        if getattr(module, "__file__", None) is None:
            return False
        if module_name in getattr(module, "__file__", None):
            return True
    return False


def imported_modules(module_names: List[str]):
    all_imported_modules = list(sys.modules.values())
    return list(
        filter(
            lambda x: _is_in_module_with_name(module_names, x),
            all_imported_modules,
        )
    )


def provide_safe(obj_graph: ObjectGraph, cls: Type[T]) -> T:
    return safe_cast(cls, obj_graph.provide(cls))
