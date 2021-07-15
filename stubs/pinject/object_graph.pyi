#from . import bindings as bindings, decorators as decorators, errors as errors, finding as finding, injection_contexts as injection_contexts, locations as locations, object_providers as object_providers, providing as providing, scoping as scoping, support as support
from typing import Any, Optional, TypeVar, Type


def new_object_graph(modules: Any = ..., classes: Optional[Any] = ..., binding_specs: Optional[Any] = ..., only_use_explicit_bindings: bool = ..., allow_injecting_none: bool = ..., configure_method_name: str = ..., dependencies_method_name: str = ..., get_arg_names_from_class_name: Any = ..., get_arg_names_from_provider_fn_name: Any = ..., id_to_scope: Optional[Any] = ..., is_scope_usable_from_scope: Any = ..., use_short_stack_traces: bool = ...)->ObjectGraph: ...

T = TypeVar("T")

class ObjectGraph:
    def __init__(self, obj_provider: Any, injection_context_factory: Any, is_injectable_fn: Any, use_short_stack_traces: Any) -> None: ...
    def provide(self, cls: Type[T])->T: ...
