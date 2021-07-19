from . import errors as errors, locations as locations, scoping as scoping
from typing import Any

class InjectionContextFactory:
    def __init__(self, is_scope_usable_from_scope_fn: Any) -> None: ...
    def new(self, injection_site_fn: Any): ...

class _InjectionContext:
    def __init__(self, injection_site_fn: Any, binding_stack: Any, scope_id: Any, is_scope_usable_from_scope_fn: Any) -> None: ...
    def get_child(self, injection_site_fn: Any, binding: Any): ...
    def get_injection_site_desc(self): ...