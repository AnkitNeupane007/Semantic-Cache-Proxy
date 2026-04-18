import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

class ServiceException(Exception):
    """Base exception for service failures (e.g. Redis, LLM)"""
    def __init__(self, service_name: str, message: str):
        self.service_name = service_name
        self.message = message
        super().__init__(self.message)

async def service_exception_handler(request: Request, exc: ServiceException):
    logger.error(f"ServiceException in {exc.service_name}: {exc.message}")
    return JSONResponse(
        status_code=502, # Bad Gateway
        content={
            "error": "Service Unavailable",
            "service": exc.service_name,
            "details": exc.message
        }
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": "An unexpected error occurred"}
    )
