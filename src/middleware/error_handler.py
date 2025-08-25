import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from src.common.exceptions.service_custom_exception import ServiceCustomException
from src.common.utils.logger import logger


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        body = await request.body()
        logger.info(
            f"Incoming Request: {request.method} {request.url} - Body: {body.decode('utf-8') or 'No Body'}"
        )

        try:
            response = await call_next(request)

            # Log Outgoing Response
            process_time = time.time() - start_time
            logger.info(
                f"Outgoing Response: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.2f}s"
            )

            return response

        except ServiceCustomException as exc:
            logger.error(f"Custom Error: {exc.message}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": exc.message},
            )

        except Exception as exc:
            logger.error(f"Unhandled Exception: {str(exc)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )
