"""
Portfolio Snapshot and Upload History Models

These models enable historical tracking of portfolio states over time:
- PortfolioSnapshot: Captures the complete portfolio state at a specific point in time
- SnapshotPosition: Individual position data within a snapshot
- UploadHistory: Tracks uploaded files to prevent duplicates
"""

import hashlib
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Integer, ForeignKey, Boolean, Text, Index
from sqlalchemy.orm import relationship
from src.models.base import Base


class PortfolioSnapshot(Base):
    """
    Represents a portfolio's state at a specific point in time.

    Created from uploaded statements (GBM PDFs) or periodic snapshots.
    Enables historical analysis, trend visualization, and month-over-month comparisons.
    """
    __tablename__ = "portfolio_snapshots"

    # Primary Key
    id = Column(String, primary_key=True, index=True)  # UUID

    # Foreign Keys
    portfolio_id = Column(String, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    upload_id = Column(String, ForeignKey("upload_history.id", ondelete="SET NULL"), nullable=True, index=True)

    # Snapshot Metadata
    snapshot_date = Column(DateTime, nullable=False, index=True)  # Statement date from PDF
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Portfolio Summary Values (from RESUMEN DEL PORTAFOLIO section)
    equity_value = Column(Numeric(15, 2), nullable=False, default=0.00)  # RENTA VARIABLE
    fixed_income_value = Column(Numeric(15, 2), nullable=False, default=0.00)  # DEUDA
    cash_value = Column(Numeric(15, 2), nullable=False, default=0.00)  # EFECTIVO
    total_value = Column(Numeric(15, 2), nullable=False, default=0.00)  # VALOR DEL PORTAFOLIO

    # Calculated Metrics (computed vs. previous snapshot)
    total_change = Column(Numeric(15, 2), nullable=True)  # Month-over-month change in MXN
    total_change_percent = Column(Numeric(5, 2), nullable=True)  # Month-over-month change %

    # Additional Context
    currency = Column(String, nullable=False, default="MXN")
    account_holder = Column(String, nullable=True)  # From PDF metadata
    notes = Column(Text, nullable=True)  # User notes about this snapshot

    # Relationships
    portfolio = relationship("Portfolio", back_populates="snapshots")
    upload = relationship("UploadHistory", back_populates="snapshot")
    positions = relationship("SnapshotPosition", back_populates="snapshot", cascade="all, delete-orphan")

    # Unique constraint: One snapshot per portfolio per date
    __table_args__ = (
        Index('idx_portfolio_snapshot_date', 'portfolio_id', 'snapshot_date', unique=True),
    )

    def __repr__(self):
        return f"<PortfolioSnapshot(id={self.id}, date={self.snapshot_date}, total={self.total_value})>"


class SnapshotPosition(Base):
    """
    Individual position within a portfolio snapshot.

    Captures the state of a single stock/ETF/bond at the snapshot date.
    """
    __tablename__ = "snapshot_positions"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Foreign Key
    snapshot_id = Column(String, ForeignKey("portfolio_snapshots.id", ondelete="CASCADE"), nullable=False, index=True)

    # Position Identification
    ticker = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    asset_type = Column(String, nullable=True, default="Stock")  # Stock, ETF, Bond, etc.

    # Position Metrics
    quantity = Column(Numeric(15, 4), nullable=False)
    avg_cost = Column(Numeric(15, 2), nullable=False)  # Average purchase price
    current_price = Column(Numeric(15, 2), nullable=False)  # Market price at snapshot date
    market_value = Column(Numeric(15, 2), nullable=False)  # quantity * current_price

    # Performance
    unrealized_gain = Column(Numeric(15, 2), nullable=False)  # (current_price - avg_cost) * quantity
    unrealized_gain_percent = Column(Numeric(8, 2), nullable=False)  # gain / (avg_cost * quantity) * 100

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    snapshot = relationship("PortfolioSnapshot", back_populates="positions")

    __table_args__ = (
        Index('idx_snapshot_ticker', 'snapshot_id', 'ticker'),
    )

    def __repr__(self):
        return f"<SnapshotPosition(ticker={self.ticker}, qty={self.quantity}, value={self.market_value})>"


class UploadHistory(Base):
    """
    Tracks uploaded statement files to prevent duplicate uploads.

    Uses file hash to detect if the same file was uploaded before,
    and validates statement dates to prevent multiple uploads of the same period.
    """
    __tablename__ = "upload_history"

    # Primary Key
    id = Column(String, primary_key=True, index=True)  # UUID

    # Foreign Key
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # File Information
    filename = Column(String, nullable=False)
    file_hash = Column(String(64), nullable=False, index=True)  # SHA256 hash of file content
    file_size_bytes = Column(Integer, nullable=False)

    # Statement Information
    statement_date = Column(DateTime, nullable=False, index=True)  # Extracted from PDF
    account_holder = Column(String, nullable=True)

    # Upload Metadata
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    upload_ip = Column(String, nullable=True)  # Optional: track upload source

    # Processing Status
    status = Column(String, nullable=False, default="processed")  # processed, failed, duplicate
    error_message = Column(Text, nullable=True)  # If processing failed

    # Relationships
    user = relationship("User", back_populates="uploads")
    snapshot = relationship("PortfolioSnapshot", back_populates="upload", uselist=False)

    # Unique constraints
    __table_args__ = (
        Index('idx_user_file_hash', 'user_id', 'file_hash', unique=True),  # Prevent same file twice
        Index('idx_user_statement_date', 'user_id', 'statement_date'),  # Fast date lookups
    )

    @staticmethod
    def compute_file_hash(content: bytes) -> str:
        """Compute SHA256 hash of file content for duplicate detection"""
        return hashlib.sha256(content).hexdigest()

    def __repr__(self):
        return f"<UploadHistory(id={self.id}, file={self.filename}, date={self.statement_date})>"
