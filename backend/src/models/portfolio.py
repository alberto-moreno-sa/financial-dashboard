import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from src.models.base import Base


class Portfolio(Base):
    """
    Portfolio model - Represents a user's investment portfolio.

    A user can have multiple portfolios (e.g., Personal, Retirement, Business).
    Each portfolio contains positions (assets/holdings).
    """
    __tablename__ = "portfolios"

    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Owner relationship - CRITICAL for multi-tenancy
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Portfolio metadata
    name = Column(String, nullable=False, default="My Portfolio")  # e.g., "Personal", "Retirement", "Business"
    description = Column(String, nullable=True)
    currency = Column(String, nullable=False, default="MXN")  # Base currency for this portfolio

    # Calculated values (updated by backend services)
    # Using Numeric for financial precision (never use Float for money!)
    total_net_worth = Column(Numeric(precision=15, scale=2), nullable=False, default=Decimal("0.00"))
    cash_balance = Column(Numeric(precision=15, scale=2), nullable=False, default=Decimal("0.00"))
    invested_value = Column(Numeric(precision=15, scale=2), nullable=False, default=Decimal("0.00"))

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps (timezone-naive to match PostgreSQL TIMESTAMP WITHOUT TIME ZONE)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # Relationships
    owner = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio", cascade="all, delete-orphan")
    snapshots = relationship("PortfolioSnapshot", back_populates="portfolio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Portfolio(id={self.id}, name={self.name}, user_id={self.user_id})>"


class Position(Base):
    """
    Position model - Represents a holding/asset within a portfolio.

    Examples: 100 shares of VOO, 5000 CETES, $10,000 USD cash, etc.
    """
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(String, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)

    # Asset identification
    ticker = Column(String, nullable=False)  # e.g., "VOO", "CETES", "USD"
    name = Column(String, nullable=False)    # e.g., "Vanguard S&P 500 ETF"
    asset_type = Column(String, default="Stock")  # Stock, Bond, Cash, Crypto, etc.

    # Holding details (using Numeric for precision)
    quantity = Column(Numeric(precision=15, scale=4), nullable=False)  # Shares, units, or currency amount
    avg_cost = Column(Numeric(precision=15, scale=2), nullable=False)  # Average cost per unit
    current_price = Column(Numeric(precision=15, scale=2), nullable=False)  # Current market price
    market_value = Column(Numeric(precision=15, scale=2), nullable=False)  # quantity * current_price

    # Timestamps (timezone-naive to match PostgreSQL TIMESTAMP WITHOUT TIME ZONE)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")

    def __repr__(self):
        return f"<Position(id={self.id}, ticker={self.ticker}, quantity={self.quantity})>"
