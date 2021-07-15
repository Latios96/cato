from . import binding_keys as binding_keys, provider_indirections as provider_indirections
from typing import Any, Optional

class ArgBindingKey:
    binding_key: Any = ...
    provider_indirection: Any = ...
    def __init__(self, arg_name: Any, binding_key: Any, provider_indirection: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...
    def can_apply_to_one_of_arg_names(self, arg_names: Any): ...
    def conflicts_with_any_arg_binding_key(self, arg_binding_keys: Any): ...

def get_unbound_arg_names(arg_names: Any, arg_binding_keys: Any): ...
def create_kwargs(arg_binding_keys: Any, provider_fn: Any): ...
def new(arg_name: Any, annotated_with: Optional[Any] = ...): ...
