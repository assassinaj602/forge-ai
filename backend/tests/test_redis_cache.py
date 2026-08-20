import pytest
from app.services.cache.redis_cache import RedisCacheService

@pytest.mark.asyncio
async def test_redis_cache_service():
    await RedisCacheService.set("test_key", "test_val")
    val = await RedisCacheService.get("test_key")
    assert val == "test_val"
    
    await RedisCacheService.delete("test_key")
    val2 = await RedisCacheService.get("test_key")
    assert val2 is None
