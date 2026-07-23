# middleware.py
import time

import redis
from fastapi import HTTPException, Request, status


class RedisRateLimiter:
    def __init__(self, redis_host: str, redis_port: int):
        self.redis_pool = redis.ConnectionPool(
            host=redis_host,
            port=redis_port,
            db=0,
            decode_responses=True,
        )

    def is_rate_limited(self, key: str, max_requests: int, window: int) -> bool:
        current = time.time()
        window_start = current - window
        conn = redis.Redis(connection_pool=self.redis_pool)
        with conn.pipeline() as pipe:
            try:
                # Removes all entries in the sorted set whose score (timestamp) is between 0 and window_start.
                # This deletes requests that are older than the rate-limit window
                # i.e., "forget anything outside the sliding window."
                # Returns the removed count
                pipe.zremrangebyscore(name=key, min=0, max=window_start)  # (ZREMRANGEBYSCORE)

                # Counts how many entries remain in the sorted set after the pruning above.
                # This is the "how many requests has this client made in the current window" number.
                # NB this must always be called second!
                pipe.zcard(name=key)  # Add elements to a Sorted Set (ZSET)

                # Adds the current request's timestamp as a new entry.
                # Both the member and the score are set to current (the current unix timestamp).
                # This records the request that's happening right now.
                pipe.zadd(key, {str(current): current})

                # Sets/refreshes a TTL on the whole key equal to the window length.
                # This is just housekeeping - if a client goes quiet and never sends another request,
                # Redis will auto-clean the key instead of it lingering forever.
                pipe.expire(key, window)
                results = pipe.execute()
            except redis.RedisError as e:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Redis error: {e}") from e
        return results[1] >= max_requests
