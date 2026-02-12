import asyncio
import signal
import sys
from core import OSPlatform, get_core_settings
from core.server import RagaServer

settings = get_core_settings()

app = RagaServer(
    host=settings.HOST_IP,
    port=settings.PORT
)


async def main():
    loop = asyncio.get_running_loop()

    # Only works on Unix
    if sys.platform != OSPlatform.WIN32.value:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, app.stop)

    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Windows fallback
        app.stop()
