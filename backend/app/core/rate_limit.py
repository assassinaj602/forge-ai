"""
Rate Limiting Middleware for FastAPI
"""
import time
from typing import Dict, Tuple
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Token bucket / window rate limiting middleware per client IP."""

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.client_requests: Dict[str, list] = {}

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        # Clean old timestamps
        if client_ip in self.client_requests:
            self.client_requests[client_ip] = [
                ts for ts in self.client_requests[client_ip] if now - ts < self.window_seconds
            ]
        else:
            self.client_requests[client_ip] = []

        if len(self.client_requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Please try again later."}
            )

        self.client_requests[client_ip].append(now)
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(
            self.max_requests - len(self.client_requests[client_ip])
        )
        return response
