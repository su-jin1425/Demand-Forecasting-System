from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.db.redis import redis_client

from app.api.auth import router as auth_router
from app.api.models import router as models_router
from app.api.analytics import router as analytics_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to Redis
    await redis_client.connect()
    
    # Ensure model artifact directory exists
    os.makedirs(settings.MODEL_STORAGE_DIR, exist_ok=True)
    
    yield
    # Shutdown: Disconnect Redis
    await redis_client.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(models_router, prefix=f"{settings.API_V1_STR}/models", tags=["models"])
app.include_router(analytics_router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
