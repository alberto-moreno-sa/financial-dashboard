"""
User Management Endpoints

Handles user synchronization between Auth0 and our local PostgreSQL database.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from pydantic import BaseModel

from src.core.database import get_db
from src.core.auth0 import get_current_user_from_token
from src.models.user import User
from src.models.portfolio import Portfolio

router = APIRouter()


class UserResponse(BaseModel):
    id: str
    auth0_id: str
    email: str
    name: str | None
    picture: str | None
    email_verified: bool
    is_active: bool
    created_at: str
    has_default_portfolio: bool

    class Config:
        from_attributes = True


class UserSyncResponse(BaseModel):
    user: UserResponse
    is_new_user: bool
    message: str


@router.post("/sync", response_model=UserSyncResponse)
async def sync_user(
    current_user_token: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    """
    Sync user from Auth0 to local database.

    This endpoint should be called after successful Auth0 login to:
    1. Create user in PostgreSQL if it's their first login
    2. Update user info if it already exists
    3. Create a default portfolio for new users
    4. Return the user's internal database ID

    The frontend should call this immediately after Auth0 authentication
    and store the returned user_id for future requests.
    """
    auth0_id = current_user_token["auth0_id"]
    email = current_user_token["email"]
    name = current_user_token.get("name")
    picture = current_user_token.get("picture")
    email_verified = current_user_token.get("email_verified", False)

    # Check if user already exists in our database
    result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    existing_user = result.scalars().first()

    is_new_user = existing_user is None

    if existing_user:
        # Update existing user information
        existing_user.email = email
        existing_user.name = name
        existing_user.picture = picture
        existing_user.email_verified = email_verified
        existing_user.last_login_at = datetime.now(timezone.utc).replace(tzinfo=None)
        existing_user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

        await db.commit()
        await db.refresh(existing_user)

        user = existing_user
        message = "User information updated successfully"

    else:
        # Create new user
        user = User(
            auth0_id=auth0_id,
            email=email,
            name=name,
            picture=picture,
            email_verified=email_verified,
            is_active=True,
            last_login_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )

        db.add(user)
        await db.flush()  # Get the user.id without committing

        # Create default portfolio for new user
        default_portfolio = Portfolio(
            user_id=user.id,
            name="Mi Portafolio Principal",
            description="Portafolio creado automáticamente",
            currency="MXN",
            is_active=True,
        )

        db.add(default_portfolio)
        await db.commit()
        await db.refresh(user)

        message = "New user created successfully with default portfolio"

    # Check if user has at least one portfolio
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id).limit(1)
    )
    has_default_portfolio = portfolio_result.scalars().first() is not None

    return UserSyncResponse(
        user=UserResponse(
            id=user.id,
            auth0_id=user.auth0_id,
            email=user.email,
            name=user.name,
            picture=user.picture,
            email_verified=user.email_verified,
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            has_default_portfolio=has_default_portfolio,
        ),
        is_new_user=is_new_user,
        message=message,
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_token: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current authenticated user's information.

    This endpoint requires a valid Auth0 JWT token.
    Returns the user's information from our local database.
    """
    auth0_id = current_user_token["auth0_id"]

    result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in database. Please call /sync endpoint first.",
        )

    # Check if user has portfolios
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id).limit(1)
    )
    has_default_portfolio = portfolio_result.scalars().first() is not None

    return UserResponse(
        id=user.id,
        auth0_id=user.auth0_id,
        email=user.email,
        name=user.name,
        picture=user.picture,
        email_verified=user.email_verified,
        is_active=user.is_active,
        created_at=user.created_at.isoformat(),
        has_default_portfolio=has_default_portfolio,
    )
