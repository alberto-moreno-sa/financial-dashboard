from fastapi import APIRouter
from src.api.v1 import auth, portfolio, health, users, import_data, demo_portfolio
from src.core.config import settings
from src.core.demo_auth import is_demo_mode

api_router = APIRouter()

# Demo mode: use in-memory storage endpoints
if is_demo_mode(settings.AUTH0_DOMAIN):
    api_router.include_router(demo_portfolio.router, prefix="/portfolio", tags=["demo-portfolio"])
    print("🎭 DEMO MODE ENABLED - Using in-memory storage (no database)")
else:
    # Production mode: use regular database endpoints
    api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
    api_router.include_router(import_data.router, prefix="/import", tags=["import"])

# Include auth, users, and health routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(health.router, tags=["health"])