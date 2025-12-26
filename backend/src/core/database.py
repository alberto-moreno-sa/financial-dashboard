from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

# Create engine using the URI from settings
# echo=False disables SQL query logging for cleaner output
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()