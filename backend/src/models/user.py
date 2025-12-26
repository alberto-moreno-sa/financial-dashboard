import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from src.models.base import Base


class User(Base):
    """
    User model - Stores local copy of Auth0 users.

    This allows us to:
    - Have a stable user_id for foreign keys
    - Store additional user metadata not in Auth0
    - Maintain data ownership even if we migrate from Auth0
    - Enable offline/cached user lookups
    """
    __tablename__ = "users"

    # Primary key - our internal UUID
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Auth0 identifier - UNIQUE and indexed for fast lookups
    auth0_id = Column(String, unique=True, nullable=False, index=True)

    # User profile information (synced from Auth0)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)  # Avatar URL from social login

    # Account status
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)

    # Timestamps (timezone-naive to match PostgreSQL TIMESTAMP WITHOUT TIME ZONE)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    portfolios = relationship("Portfolio", back_populates="owner", cascade="all, delete-orphan")
    uploads = relationship("UploadHistory", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, auth0_id={self.auth0_id})>"
