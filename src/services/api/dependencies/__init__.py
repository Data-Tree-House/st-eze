from fastapi import HTTPException, Request, status

from constants import c

from ._db import get_session  # noqa
from ._rate_limit import RedisRateLimiter as _RedisRateLimiter
from ._round_robin import RoundRobinTokenPool as _RoundRobinTokenPool

rate_limiter = _RedisRateLimiter(
    redis_host=c.redis_host,
    redis_port=c.redis_port,
)
gsheet_pool = _RoundRobinTokenPool(
    redis_host=c.redis_host,
    redis_port=c.redis_port,
    pool_key="token_pool:gsheet",
    tokens=c.g_worker_ids,
    timeout=c.g_worker_pool_timeout,
)


class RateLimit:
    def __init__(self, max_requests: int, window: int):
        self.max_requests = max_requests
        self.window = window

    def __call__(self, request: Request):
        forwarded = request.headers.get("x-forwarded-for")
        client_host = (
            forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "unknown")
        )
        if client_host == "unknown":
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "For the life of me, I can;t figure out where your traffic is coming from!"
            )
        key = f"rate_limit:{client_host}:{request.url.path}"
        if rate_limiter.is_rate_limited(key, self.max_requests, self.window):
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS,
                "Too many requests",
                headers={
                    "Retry-After": str(self.window),
                },
            )
