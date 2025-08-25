import asyncio
from typing import cast

from hypercorn.asyncio import serve
from hypercorn.config import Config
from hypercorn.typing import ASGIFramework

from src.common.utils.logger import logger
from src.config.settings import SERVER_HOST, SERVER_PORT, SERVER_USE_RELOADER
from src.endpoints import app


def run_service():
    provider_config = Config()
    provider_config.bind = f"{SERVER_HOST}:{SERVER_PORT}"
    provider_config.use_reloader = SERVER_USE_RELOADER

    loop = asyncio.get_event_loop()

    # Cast FastAPI app to ASGIFramework for type checker
    asgi_app: ASGIFramework = cast(ASGIFramework, app)
    loop.create_task(serve(asgi_app, provider_config))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass  # Handle graceful exit
    finally:
        loop.stop()
        logger.warning("Server operation has been stopped gracefully")


if __name__ == "__main__":
    if SERVER_USE_RELOADER:
        # Use Hypercorn CLI-style runner when reload is enabled
        import uvicorn
        uvicorn.run("src.endpoints:app", host=SERVER_HOST, port=int(SERVER_PORT), reload=True)
    else:
        # Run production server with Hypercorn
        run_service()