"""
Portfolio Snapshot Service

Handles creation, validation, and retrieval of portfolio snapshots.
All heavy lifting happens in the backend - frontend just displays results.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from sqlalchemy.orm import selectinload

from src.models.snapshot import PortfolioSnapshot, SnapshotPosition, UploadHistory
from src.models.portfolio import Portfolio


class SnapshotService:
    """
    Service for managing portfolio snapshots and calculating changes over time.

    Philosophy: Backend does ALL calculations and validations.
    Frontend only displays the data.
    """

    @staticmethod
    async def check_duplicate_upload(
        db: AsyncSession,
        user_id: str,
        file_hash: str,
        statement_date: datetime
    ) -> Optional[UploadHistory]:
        """
        Check if a file was already uploaded by this user.

        Returns the existing UploadHistory record if duplicate found, None otherwise.
        """
        # Check by file hash (exact same file)
        result = await db.execute(
            select(UploadHistory)
            .where(and_(
                UploadHistory.user_id == user_id,
                UploadHistory.file_hash == file_hash
            ))
        )
        existing_by_hash = result.scalar_one_or_none()
        if existing_by_hash:
            return existing_by_hash

        # Check by statement date (different file, same period)
        result = await db.execute(
            select(UploadHistory)
            .where(and_(
                UploadHistory.user_id == user_id,
                UploadHistory.statement_date == statement_date
            ))
        )
        existing_by_date = result.scalar_one_or_none()
        return existing_by_date

    @staticmethod
    async def create_snapshot(
        db: AsyncSession,
        portfolio_id: str,
        upload_data: dict,
        file_content: bytes,
        filename: str,
        user_id: str,
        upload_ip: Optional[str] = None
    ) -> PortfolioSnapshot:
        """
        Create a complete portfolio snapshot from uploaded statement data.

        This method:
        1. Creates UploadHistory record with file hash
        2. Creates PortfolioSnapshot with summary data
        3. Creates SnapshotPosition records for each holding
        4. Calculates month-over-month changes vs. previous snapshot
        5. Commits everything in a transaction

        Args:
            db: Database session
            portfolio_id: ID of the portfolio this snapshot belongs to
            upload_data: Parsed data from PDF (dict with metadata, portfolio_summary, breakdown)
            file_content: Raw file bytes for hash calculation
            filename: Original filename
            user_id: ID of the user uploading
            upload_ip: Optional IP address of uploader

        Returns:
            The created PortfolioSnapshot with all relationships loaded
        """
        # 1. Create upload history record
        file_hash = UploadHistory.compute_file_hash(file_content)
        upload_id = str(uuid.uuid4())

        upload_history = UploadHistory(
            id=upload_id,
            user_id=user_id,
            filename=filename,
            file_hash=file_hash,
            file_size_bytes=len(file_content),
            statement_date=datetime.fromisoformat(upload_data["statement_date"]),
            account_holder=upload_data["account_holder"],
            uploaded_at=datetime.utcnow(),
            upload_ip=upload_ip,
            status="processed"
        )
        db.add(upload_history)

        # 2. Get previous snapshot for change calculation
        previous_snapshot = await SnapshotService.get_latest_snapshot(db, portfolio_id)

        # 3. Create portfolio snapshot
        snapshot_id = str(uuid.uuid4())
        statement_date = datetime.fromisoformat(upload_data["statement_date"])
        portfolio_summary = upload_data["portfolio_summary"]

        total_value = Decimal(str(portfolio_summary["total_value"]))
        total_change = None
        total_change_percent = None

        if previous_snapshot:
            total_change = total_value - previous_snapshot.total_value
            if previous_snapshot.total_value > 0:
                total_change_percent = (total_change / previous_snapshot.total_value) * 100

        portfolio_snapshot = PortfolioSnapshot(
            id=snapshot_id,
            portfolio_id=portfolio_id,
            upload_id=upload_id,
            snapshot_date=statement_date,
            created_at=datetime.utcnow(),
            equity_value=Decimal(str(portfolio_summary["equity_value"])),
            fixed_income_value=Decimal(str(portfolio_summary["fixed_income_value"])),
            cash_value=Decimal(str(portfolio_summary["cash_value"])),
            total_value=total_value,
            total_change=total_change,
            total_change_percent=total_change_percent,
            currency=upload_data["currency"],
            account_holder=upload_data["account_holder"]
        )
        db.add(portfolio_snapshot)

        # 4. Create snapshot positions
        for position_data in upload_data["breakdown"]:
            position = SnapshotPosition(
                snapshot_id=snapshot_id,
                ticker=position_data["ticker"],
                name=position_data["name"],
                asset_type="Stock",  # Could be inferred from ticker if needed
                quantity=Decimal(str(position_data["quantity"])),
                avg_cost=Decimal(str(position_data["avg_cost"])),
                current_price=Decimal(str(position_data["current_price"])),
                market_value=Decimal(str(position_data["market_value"])),
                unrealized_gain=Decimal(str(position_data["unrealized_gain"])),
                unrealized_gain_percent=Decimal(str(position_data["unrealized_gain_percent"])),
                created_at=datetime.utcnow()
            )
            db.add(position)

        # 5. Commit transaction
        await db.commit()

        # 6. Return the snapshot object directly
        # Note: positions are not loaded to avoid session issues in bulk operations
        return portfolio_snapshot

    @staticmethod
    async def get_latest_snapshot(
        db: AsyncSession,
        portfolio_id: str
    ) -> Optional[PortfolioSnapshot]:
        """Get the most recent snapshot for a portfolio with positions eagerly loaded"""
        result = await db.execute(
            select(PortfolioSnapshot)
            .options(selectinload(PortfolioSnapshot.positions))
            .where(PortfolioSnapshot.portfolio_id == portfolio_id)
            .order_by(desc(PortfolioSnapshot.snapshot_date))
            .limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_snapshots_history(
        db: AsyncSession,
        portfolio_id: str,
        limit: int = 12
    ) -> List[PortfolioSnapshot]:
        """
        Get historical snapshots for a portfolio, ordered by date descending.
        Default limit of 12 for 12 months of data.
        """
        result = await db.execute(
            select(PortfolioSnapshot)
            .options(selectinload(PortfolioSnapshot.positions))
            .where(PortfolioSnapshot.portfolio_id == portfolio_id)
            .order_by(desc(PortfolioSnapshot.snapshot_date))
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_snapshot_by_id(
        db: AsyncSession,
        snapshot_id: str
    ) -> Optional[PortfolioSnapshot]:
        """Get a specific snapshot with all positions"""
        result = await db.execute(
            select(PortfolioSnapshot)
            .options(selectinload(PortfolioSnapshot.positions))
            .where(PortfolioSnapshot.id == snapshot_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_snapshot(
        db: AsyncSession,
        snapshot_id: str
    ) -> bool:
        """
        Delete a snapshot and all its positions.
        Upload history is preserved (SET NULL on upload_id).
        Returns True if deleted, False if not found.
        """
        result = await db.execute(
            select(PortfolioSnapshot)
            .where(PortfolioSnapshot.id == snapshot_id)
        )
        snapshot = result.scalar_one_or_none()

        if not snapshot:
            return False

        await db.delete(snapshot)
        await db.commit()
        return True
