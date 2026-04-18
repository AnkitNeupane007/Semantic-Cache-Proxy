import redis.asyncio as redis
from redis.commands.search.field import TextField, VectorField, NumericField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from app.core.config import settings

# Global redis client
redis_client = redis.from_url(
    settings.REDIS_HOST,
    decode_responses=False  # Store embeddings as bytes
)

async def create_vector_index():
    try:
        await redis_client.ft("cache_idx").info()  # already exists
    except Exception:
        schema = (
            TextField("prompt"),
            TextField("response"),
            NumericField("hit_count"),
            NumericField("token_count"),
            VectorField(
                "embedding",
                "HNSW",                          # approximate nearest neighbour
                {
                    "TYPE": "FLOAT32",
                    "DIM": 384,                 # match your embedding dimension
                    "DISTANCE_METRIC": "COSINE",
                }
            )
        )
        await redis_client.ft("cache_idx").create_index(
            schema,
            definition=IndexDefinition(
                prefix=["cache:"],               # indexes all keys with this prefix
                index_type=IndexType.HASH
            )
        )

async def search_similar(query_embedding: bytes):
    q = (
        Query("*=>[KNN 1 @embedding $vec AS vector_score]")
        .sort_by("vector_score")               # COSINE distance: lower = more similar
        .return_fields("prompt", "response", "vector_score", "hit_count", "token_count")
        .dialect(2)
    )
    
    return await redis_client.ft("cache_idx").search(
        q, query_params={"vec": query_embedding}
    )
