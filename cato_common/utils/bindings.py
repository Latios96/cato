import sys

from typing import List


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
