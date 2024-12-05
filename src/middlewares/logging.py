import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import inspect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get the function name (route being called)
        method = request.scope["method"]

        # Get the parameters passed to the route
        path = request.scope["path"]

        # Log the function name and parameters
        logger.info(f"Method: {method}")
        logger.info(f"Path : {path}")

        # Call the next middleware or route handler
        response = await call_next(request)

        # Return the response to the client
        return response
