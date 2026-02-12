import socket
import asyncio
from typing import Optional
from . import RagaLifeCycle, BigLogger

logger = BigLogger(__name__)

class RagaServer:

    __slots__ = (
        'host',
        'port',
        'title',
        'description',
        'life_cycle',
        '_shutdown_event'
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
        self._shutdown_event = asyncio.Event()

    async def run(self):
        try:
            # Server startup
            if self.life_cycle:
                await self.life_cycle.on_startup()
            else:
                await self.init_server()

            logger.info("Server is running... Press Ctrl+C to stop.")
            await self._shutdown_event.wait()

        except asyncio.CancelledError:
            logger.warning("Server Cancelled")

        finally:
            # Shutdown
            if self.life_cycle:
                await self.life_cycle.on_shutdown()
            else:
                await self.shut_server()

    def stop(self):
        logger.warning("Shutdown signal received.")
        self._shutdown_event.set()

    async def init_server(self):
        logger.info("Initializing server...")
        logger.info(f"Server can be accessed on - {self.host}:{self.port}")
        logger.info(f"** This is a simulation")

    async def shut_server(self):
        logger.info(f"Shutting server at {self.host}:{self.port}")
        logger.info("Shutdown complete")

