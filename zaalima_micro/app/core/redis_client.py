import redis
from app.core.config import settings

def get_redis_client():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True,
    )

# Shared, module-level Redis connection used across the app (cache.py imports this directly)
redis_db = get_redis_client()
