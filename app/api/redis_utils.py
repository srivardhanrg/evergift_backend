"""
Redis connection pool helper for API endpoints.

Provides safe access to Redis pool with proper error handling.
"""

from fastapi import HTTPException, Request
from typing import Any


def get_redis_pool(request: Request) -> Any:
    """
    Get Redis pool from request state, raising 503 if unavailable.

    Args:
        request: FastAPI request object

    Returns:
        Redis pool instance

    Raises:
        HTTPException: 503 if Redis pool is not initialized
    """
    redis_pool = getattr(request.app.state, "redis_pool", None)

    if redis_pool is None:
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable. Please try again in a moment."
        )

    return redis_pool
