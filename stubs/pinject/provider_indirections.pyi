from typing import Any

class ProviderIndirection:
    def StripIndirectionIfNeeded(self, provide_fn: Any): ...

class NoProviderIndirection:
    def StripIndirectionIfNeeded(self, provide_fn: Any): ...

INDIRECTION: Any
NO_INDIRECTION: Any
