import redis
from fastapi import HTTPException, status


class RoundRobinTokenPool:
    def __init__(
        self,
        pool_key: str,
        tokens: list[str],
        timeout: float | None = None,
        redis_client: redis.Redis | None = None,
        redis_host: str = "127.0.0.1",
        redis_port: int = 6379,
    ):
        if not tokens:
            raise ValueError("No tokens to add to pool")
        self.pool_key = f"{pool_key}:available"
        self.default_timeout = timeout
        self._client = redis_client or redis.Redis(
            connection_pool=redis.ConnectionPool(host=redis_host, port=redis_port, db=0, decode_responses=True)
        )
        # Additive, idempotent seeding: only pushes tokens not already
        # present anywhere in the system (available OR checked out).
        # Safe for every service/replica to call on every startup.
        registry_key = f"{pool_key}:registry"  # tracks "known" tokens, ever-growing
        for token in tokens:
            added_to_registry = self._client.sadd(registry_key, token)
            if added_to_registry:  # first time this token has ever been seen
                self._client.rpush(self.pool_key, token)

    def __call__(self):
        redis_timeout = 0 if self.default_timeout is None else self.default_timeout
        try:
            result = self._client.blpop([self.pool_key], timeout=redis_timeout)
        except redis.RedisError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Redis error: {e}") from e
        if result is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "No tokens available")
        _key, token = result
        try:
            yield token
        finally:
            self._client.rpush(self.pool_key, token)
