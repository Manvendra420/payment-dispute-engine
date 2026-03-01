"""Logging and monitoring utilities."""

import logging
from datetime import datetime
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        """Log incoming requests and outgoing responses."""
        request_id = request.headers.get("X-Request-ID", "unknown")
        
        logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"[ID: {request_id}]"
        )
        
        try:
            response = await call_next(request)
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"Status: {response.status_code} [ID: {request_id}]"
            )
            return response
        except Exception as e:
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"Error: {str(e)} [ID: {request_id}]"
            )
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for centralized error handling."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        """Handle errors and return proper JSON responses."""
        try:
            response = await call_next(request)
            return response
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "error": "Validation error",
                    "detail": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Internal server error",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
