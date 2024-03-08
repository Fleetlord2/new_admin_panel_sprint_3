from typing import Optional

import backoff
from redis import Redis

from config import BACKOFF_CFG, REDIS_DSN


@backoff.on_exception(**BACKOFF_CFG)
def redis_client() -> Redis:
    """Create new Redis connection."""
    return Redis(**REDIS_DSN)


def get_state(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get state by the key from Redis."""
    redis = redis_client()
    data = redis.get(key)
    if data:
        return data.decode()
    return default


def set_state(key: str, value: str) -> None:
    """Save state in Redis storage."""
    redis = redis_client()
    redis.set(key, value.encode())
