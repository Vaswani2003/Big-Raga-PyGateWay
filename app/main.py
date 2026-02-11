from core.server import RagaServer
from core.config import get_core_settings

def main():
    settings = get_core_settings()

    app = RagaServer(
        host=settings.HOST_IP,
        port=settings.PORT
    )

    app.run()

if __name__ == "__main__":
    main()