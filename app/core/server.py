import asyncio
from typing import Optional
from . import RagaLifeCycle, BigLogger, get_core_settings

logger = BigLogger(__name__)
settings = get_core_settings()

class RagaServer:

    __slots__ = (
        'host',
        'port',
        'title',
        'description',
        'life_cycle',
        '_shutdown_event',
        'server_'
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
        self.server_ = None

    async def run(self):
        """
        
        Main server loop. Handles startup, shutdown, and lifecycle events.
        Asynchronously waits for shutdown signal and ensures proper cleanup on exit.

        Args:
            None

        Returns:
            None

        """

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

        """
        
        Function to signal the server to stop. Sets the shutdown event which is awaited in the main run loop.
        This allows for graceful shutdown of the server and any associated resources.

        """

        logger.warning("Shutdown signal received.")
        self._shutdown_event.set()

    @logger.error_decorator()
    async def init_server(self):
        logger.info(f"Starting server at {self.host}:{self.port}")
        
        
        try:
            self.server_ = await asyncio.start_server(
                client_connected_cb=self.handle_client,
                host=self.host,
                port=self.port
            )

            logger.info(f"Server started successfully at {self.host}:{self.port}")

            pass

        except Exception as e:
            raise RuntimeError(f"Failed to start server: {str(e)}")


    async def shut_server(self):
        logger.info(f"Shutting server at {self.host}:{self.port}")
        logger.info("Shutdown complete")

    
    @logger.error_decorator()
    async def handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ):
        """
        
        Function to handle incoming client connections. This is where the core request processing logic is implemented.

        
        Args:
            reader (asyncio.StreamReader): The stream reader for the client connection.
            writer (asyncio.StreamWriter): The stream writer for the client connection.
        
        Returns:
            None

        """

        """
        FLOW :

        Connection accepted
                ↓
        Read HTTP request
                ↓
        Parse request
                ↓
        Route request
                ↓
        Execute handler
                ↓
        Build response
                ↓
        Send response
                ↓
        Close or keep alive
        
        """

        try:
            logger.info("Accepting client connection from {}".format(writer.get_extra_info('peername')))

            raw_data = await reader.read(settings.MAX_REQUEST_SIZE)
            decoded_data = raw_data.decode('utf-8')

            logger.debug(f"Received raw data: {decoded_data}")

            # TODO : Implement request parsing, routing, and response building logic here.
            body = "<html><body><h1>BigRaga is running</h1><p>Your browser reached handle_client successfully.</p></body></html>"
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                "Connection: close\r\n\r\n"
                f"{body}"
            )

            writer.write(response.encode('utf-8'))
            await writer.drain()
            writer.close()
            await writer.wait_closed()


        except Exception as e:
            raise RuntimeError(f"Error handling client: {str(e)}")

