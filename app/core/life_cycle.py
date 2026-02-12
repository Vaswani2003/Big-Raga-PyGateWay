from typing import Protocol
from typing_extensions import runtime_checkable

@runtime_checkable
class RagaLifeCycle(Protocol):
    async def on_startup(self) -> None: ...

    async def on_shutdown(self) -> None: ...
