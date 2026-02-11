import socket
from typing import Optional
from .life_cycle import RagaLifeCycle
from .big_logger import BigLogger

logger = BigLogger(__name__)

class RagaServer:

    __slots__ = (
        'host',
        'port',
        'title',
        'description',
        'life_cycle'
    )

    def __init__(
            self,
            host: str = '0.0.0.0',
            port: int = 8000,
            title: str = "BigRaga API Gateway",
            description: str = None,
            life_cycle: Optional[RagaLifeCycle] = None
    ):
        self.host: str = host
        self.port: int = port
        self.title: str = title
        self.description: str = description
        self.life_cycle: Optional[RagaLifeCycle]  = life_cycle

    def run(self):

        if self.life_cycle:
            self.life_cycle.on_startup()
        else:
            self.init_server()


    def shutdown(self):
        if self.life_cycle:
            self.life_cycle.on_shut_down()

        else:
            self.shut_server()

    def init_server(self):
        logger.info("Initializing server...")
        logger.info(f"Server can be accessed on - {self.host}:{self.port}")
        logger.info(f"** This is a simulation")

    def shut_server(self):
        logger.info("Server shuting down...")
        logger.info("Shutdown complete")