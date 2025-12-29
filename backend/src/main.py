from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    # Swagger UI location
    docs_url="/docs",
    # ReDoc location (alternative documentation)
    redoc_url="/redoc",
)

# CORS Configuration
# This allows your React frontend to communicate with this Backend
if settings.AUTH0_DOMAIN == "demo":
    # Demo mode: Allow all origins for easier testing
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,  # Must be False when allow_origins is ["*"]
        allow_methods=["*"],
        allow_headers=["*"],
    )
elif settings.BACKEND_CORS_ORIGINS:
    # Production mode: Use specific origins
    origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    """Redirects to documentation for ease of use"""
    return {"message": "Welcome to Financial Dashboard API. Go to /docs for Swagger UI"}