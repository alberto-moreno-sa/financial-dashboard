from fastapi import APIRouter, status, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from pydantic import BaseModel
from datetime import datetime
import os

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    environment: str
    timestamp: str
    database: str
    version: str

@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint for monitoring and orchestration tools.
    Verifies database connectivity and returns service status.
    """
    # Check database connection
    db_status = "disconnected"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "version": "1.0.0"
    }

@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness():
    """
    Kubernetes liveness probe endpoint.
    Returns 200 if the application is running.
    """
    return {"status": "alive"}

@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness(db: AsyncSession = Depends(get_db)):
    """
    Kubernetes readiness probe endpoint.
    Returns 200 if the application is ready to accept traffic.
    """
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
