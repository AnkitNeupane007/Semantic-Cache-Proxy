from app.db.redis import redis_client

async def increment_request():
    await redis_client.incr("metrics:total_requests")

async def record_cache_hit(tokens_saved: int):
    await redis_client.incr("metrics:cache_hits")
    await redis_client.incrby("metrics:tokens_saved", tokens_saved)

async def get_all_metrics():
    total_requests = await redis_client.get("metrics:total_requests") or 0
    cache_hits = await redis_client.get("metrics:cache_hits") or 0
    tokens_saved = await redis_client.get("metrics:tokens_saved") or 0

    return {
        "total_requests": int(total_requests),
        "cache_hits": int(cache_hits),
        "tokens_saved": int(tokens_saved)
    }
