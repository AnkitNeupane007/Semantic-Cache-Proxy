from fastapi import APIRouter
from app.schemas.models import ChatRequest
from app.services.cache import process_chat_request
from app.services.metrics import get_all_metrics
from app.db.redis import redis_client

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to the Semantic Cache Proxy"}

@router.post("/chat")
async def chat(request: ChatRequest):
    return await process_chat_request(request.prompt)

@router.get("/metrics")
async def metrics():
    return await get_all_metrics()

@router.get("/health")
async def health_check():
    try:
        ping = await redis_client.ping()
        redis_status = "ok" if ping else "failed"
    except Exception as e:
        redis_status = f"error: {str(e)}"
        
    return {"status": "ok", "redis": redis_status}
