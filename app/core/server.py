import socket
from typing import Callable

class RagaServer:

    __slots__ = (
        'host',
        'port',
        'app_name',
        'life_cycle'
    )

    def __init__(
            self,
            host: str = '0.0.0.0',
            port: int = 8000,
            app_name: str = "BigRaga API Gateway",
            life_cycle: Callable = None
    ):
        self.host: str = host
        self.port: int = port
        self.app_name: str = app_name
        self.life_cycle: Callable = life_cycle
