from fastapi import APIRouter
from src.api.v1 import auth, portfolio, health, users, import_data

api_router = APIRouter()

# Incluimos las rutas de autenticación, usuarios, portafolio y health checks
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(import_data.router, prefix="/import", tags=["import"])
api_router.include_router(health.router, tags=["health"])