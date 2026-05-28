from typing import Optional, Any
import json, structlog
from src.config import settings

logger = structlog.get_logger()
_redis = None

async def init_cache():
    global _redis
    try:
        import redis.asyncio as aioredis
        _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await _redis.ping()
    except: pass

async def get_cache(key: str) -> Optional[Any]:
    if _redis is None: return None
    try:
        v = await _redis.get(key)
        return json.loads(v) if v else None
    except: return None

async def set_cache(key: str, value: Any, ttl: int = 300):
    if _redis is None: return
    try: await _redis.set(key, json.dumps(value), ex=ttl)
    except: pass
