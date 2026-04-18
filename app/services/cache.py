import uuid
import numpy as np

from app.db.redis import redis_client, search_similar
from app.services.embeddings import generate_embeddings
from app.services.metrics import increment_request, record_cache_hit
from app.services.llm import generate_response
from app.core.config import settings
from app.core.exceptions import ServiceException

async def process_chat_request(prompt: str) -> dict:
    try:
        await increment_request()
    except Exception as e:
        raise ServiceException("Redis", f"Failed to increment metrics: {str(e)}")

    try:
        embedding = generate_embeddings(prompt)
        embedding_bytes = embedding.astype(np.float32).tobytes()
    except Exception as e:
        raise ServiceException("Embedding", f"Failed to generate embeddings: {str(e)}")

    try:
        results = await search_similar(embedding_bytes)
    except Exception as e:
        raise ServiceException("Redis", f"Similarity search failed: {str(e)}")

    if results.docs:
        top = results.docs[0]
        distance = float(top.vector_score)     
        similarity = 1 - distance              

        if similarity >= settings.SIMILARITY_THRESHOLD:
            cache_key = f"cache:{top.id.replace('cache:', '')}"
            
            try:
                await redis_client.hincrby(cache_key, "hit_count", 1)     
                await record_cache_hit(int(top.token_count))
            except Exception as e:
                # Log but continue to ensure cache hits still return gracefully 
                pass
            
            return {
                "status": "cache_hit",
                "data": {
                    "stored_prompt": top.prompt,
                    "stored_response": top.response,
                    "similarity": similarity,
                    "tokens_used": int(top.token_count),
                    "hit_count": int(top.hit_count)
                }
            }

    # Cache miss
    key = str(uuid.uuid4())
    
    response = generate_response(prompt)
    token_count = response.usage.total_tokens
    response_content = response.choices[0].message.content

    try:
        await redis_client.hset(
            f"cache:{key}",
            mapping={
                "prompt": prompt,
                "embedding": embedding_bytes,
                "response": response_content,
                "hit_count": 1,
                "token_count": token_count
            }
        )
        await redis_client.expire(f"cache:{key}", 60 * 60 * 24)
    except Exception as e:
        pass

    return {
        "status": "cache_miss",
        "data": {
            "prompt": prompt, 
            "response": response_content
        },
        "tokens_used": token_count
    }
