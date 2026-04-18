from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.redis import create_vector_index, redis_client
from app.api.routes import router
from app.core.exceptions import ServiceException, service_exception_handler, global_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to Redis on startup
    try:
        await create_vector_index()
        print("Redis vector index ready")
    except Exception as e:
        print(f"Error initializing Redis vector index: {e}")
    yield
    # Close Redis connection on shutdown
    if redis_client:
        await redis_client.close()

app = FastAPI(title="Semantic Cache Proxy", lifespan=lifespan)

app.add_exception_handler(ServiceException, service_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Include routes
app.include_router(router)

