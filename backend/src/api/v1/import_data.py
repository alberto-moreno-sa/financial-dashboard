from datetime import datetime
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.services.pdf_parser import parse_gbm_pdf
from src.services.snapshot_service import SnapshotService
from src.schemas.import_data import (
    PortfolioSnapshotResponse,
    Metadata,
    PortfolioSummary,
    PositionBreakdown,
    SaveSnapshotRequest,
    SnapshotHistoryResponse,
    SnapshotDetailResponse,
    SnapshotSummary,
    SnapshotPositionDetail,
    BulkUploadResponse,
    FileUploadResult
)
from src.core.auth0 import get_current_user_from_token
from src.core.database import get_db
from src.models.user import User
from src.models.portfolio import Portfolio
from src.models.snapshot import UploadHistory

router = APIRouter()


@router.post("/upload", response_model=PortfolioSnapshotResponse)
async def upload_file(
    file: UploadFile = File(..., description="GBM PDF statement file"),
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and parse a GBM PDF statement to extract portfolio data.
    Validates duplicates and returns data for user confirmation.

    This endpoint receives a PDF file from GBM (Grupo Bursátil Mexicano)
    and extracts:
    - Portfolio Summary (Equity, Fixed Income, Cash)
    - Individual Positions Breakdown (ticker, quantity, market value, etc.)
    - Metadata (filename, date, account holder)

    Returns the extracted data for user confirmation before saving to database.
    """
    # 1. Get user from database
    auth0_id = current_user.get("auth0_id")
    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Validation
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # 3. Read file content
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error reading file: {str(e)}"
        )

    # 4. Parse PDF and extract data
    try:
        data = parse_gbm_pdf(content)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing PDF: {str(e)}")

    # 5. Check for duplicate uploads
    file_hash = UploadHistory.compute_file_hash(content)
    statement_date = datetime.fromisoformat(data["statement_date"])

    duplicate = await SnapshotService.check_duplicate_upload(
        db=db,
        user_id=user.id,
        file_hash=file_hash,
        statement_date=statement_date
    )

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail=f"Statement already exists for {duplicate.statement_date.strftime('%B %Y')}. "
                   f"Uploaded on {duplicate.uploaded_at.strftime('%m/%d/%Y')}."
        )

    # 6. Build response matching the specification
    return PortfolioSnapshotResponse(
        status="success",
        metadata=Metadata(
            filename=file.filename or "statement.pdf",
            detected_date=data["statement_date"],
            account_holder=data["account_holder"],
            currency=data["currency"]
        ),
        portfolio=PortfolioSummary(**data["portfolio_summary"]),
        breakdown=[PositionBreakdown(**pos) for pos in data["breakdown"]]
    )


@router.post("/save-snapshot")
async def save_snapshot(
    request_body: SaveSnapshotRequest,
    request: Request,
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Save a user-confirmed snapshot to the database.

    This endpoint:
    - Creates the upload_history record
    - Creates the snapshot with all positions
    - Calculates monthly change compared to previous snapshot
    - Returns the created snapshot with its ID

    Backend handles ALL calculations - frontend only displays.
    """
    # 1. Get user from database
    auth0_id = current_user.get("auth0_id")
    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Get user's portfolio (or create default one)
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id).limit(1)
    )
    portfolio = portfolio_result.scalar_one_or_none()

    if not portfolio:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found. Please create one first."
        )

    # 3. Get client IP for tracking
    client_ip = request.client.host if request.client else None

    # 4. Create snapshot with all positions
    snapshot = await SnapshotService.create_snapshot(
        db=db,
        portfolio_id=portfolio.id,
        upload_data=request_body.snapshot_data,
        file_content=request_body.file_hash.encode(),  # Use file_hash as proxy for content
        filename=request_body.snapshot_data["metadata"]["filename"],
        user_id=user.id,
        upload_ip=client_ip
    )

    # 5. Return created snapshot
    return {
        "status": "success",
        "snapshot_id": snapshot.id,
        "message": f"Snapshot saved successfully for {snapshot.snapshot_date.strftime('%B %Y')}",
        "total_change": float(snapshot.total_change) if snapshot.total_change else None,
        "total_change_percent": float(snapshot.total_change_percent) if snapshot.total_change_percent else None
    }


@router.get("/history", response_model=SnapshotHistoryResponse)
async def get_snapshot_history(
    limit: int = 12,
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the user's portfolio snapshot history.

    Returns up to `limit` snapshots ordered by date descending (most recent first).
    Each snapshot includes calculated change from previous month.

    Backend handles ALL calculations - frontend only visualizes.
    """
    # 1. Get user from database
    auth0_id = current_user.get("auth0_id")
    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Get user's portfolio
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id).limit(1)
    )
    portfolio = portfolio_result.scalar_one_or_none()

    if not portfolio:
        return SnapshotHistoryResponse(snapshots=[], total_count=0)

    # 3. Get snapshot history from service
    snapshots = await SnapshotService.get_snapshots_history(
        db=db,
        portfolio_id=portfolio.id,
        limit=limit
    )

    # 4. Convert to response models
    snapshot_summaries = [
        SnapshotSummary(
            id=s.id,
            snapshot_date=s.snapshot_date,
            total_value=float(s.total_value),
            equity_value=float(s.equity_value),
            fixed_income_value=float(s.fixed_income_value),
            cash_value=float(s.cash_value),
            total_change=float(s.total_change) if s.total_change else None,
            total_change_percent=float(s.total_change_percent) if s.total_change_percent else None,
            created_at=s.created_at
        )
        for s in snapshots
    ]

    return SnapshotHistoryResponse(
        snapshots=snapshot_summaries,
        total_count=len(snapshot_summaries)
    )


@router.get("/snapshot/{snapshot_id}", response_model=SnapshotDetailResponse)
async def get_snapshot_detail(
    snapshot_id: str,
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the complete detail of a specific snapshot, including all positions.

    This allows the user to see the exact state of their portfolio at a given time.
    """
    # 1. Get user from database
    auth0_id = current_user.get("auth0_id")
    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Get snapshot
    snapshot = await SnapshotService.get_snapshot_by_id(db=db, snapshot_id=snapshot_id)

    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # 3. Verify ownership (snapshot belongs to user's portfolio)
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.id == snapshot.portfolio_id)
    )
    portfolio = portfolio_result.scalar_one_or_none()

    if not portfolio or portfolio.user_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to view this snapshot")

    # 4. Convert to response model
    return SnapshotDetailResponse(
        id=snapshot.id,
        snapshot_date=snapshot.snapshot_date,
        total_value=float(snapshot.total_value),
        equity_value=float(snapshot.equity_value),
        fixed_income_value=float(snapshot.fixed_income_value),
        cash_value=float(snapshot.cash_value),
        total_change=float(snapshot.total_change) if snapshot.total_change else None,
        total_change_percent=float(snapshot.total_change_percent) if snapshot.total_change_percent else None,
        currency=snapshot.currency,
        account_holder=snapshot.account_holder,
        created_at=snapshot.created_at,
        positions=[
            SnapshotPositionDetail(
                ticker=p.ticker,
                name=p.name,
                quantity=float(p.quantity),
                avg_cost=float(p.avg_cost),
                current_price=float(p.current_price),
                market_value=float(p.market_value),
                unrealized_gain=float(p.unrealized_gain),
                unrealized_gain_percent=float(p.unrealized_gain_percent)
            )
            for p in snapshot.positions
        ]
    )


@router.post("/bulk-upload", response_model=BulkUploadResponse)
async def bulk_upload_files(
    files: List[UploadFile] = File(..., description="Multiple GBM PDF statement files (max 100)"),
    request: Request = None,
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and process multiple PDF files at once (up to 100 files).

    This endpoint:
    - Accepts multiple PDF files simultaneously
    - Processes each file independently
    - Validates duplicates per file
    - Creates snapshots for all valid files
    - Returns detailed results for each file (success/duplicate/error)

    Perfect for uploading historical data organized by year and period.
    """
    # 1. Validate file count
    if len(files) > 100:
        raise HTTPException(
            status_code=400,
            detail=f"Too many files. Maximum allowed: 100, received: {len(files)}"
        )

    if len(files) == 0:
        raise HTTPException(
            status_code=400,
            detail="No files received for processing"
        )

    # 2. Get user from database
    auth0_id = current_user.get("auth0_id")
    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Get user's portfolio
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id).limit(1)
    )
    portfolio = portfolio_result.scalar_one_or_none()

    if not portfolio:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found. Please create one first."
        )

    # 4. Get client IP for tracking
    client_ip = request.client.host if request.client else None

    # 5. Process each file
    results = []
    successful = 0
    duplicates = 0
    errors = 0

    for file in files:
        result = FileUploadResult(
            filename=file.filename or "unknown.pdf",
            status="processing",
            message="Processing..."
        )

        try:
            # Validate file type
            if file.content_type != "application/pdf":
                result.status = "error"
                result.message = "Invalid file type"
                result.error_detail = "Only PDF files are allowed"
                errors += 1
                results.append(result)
                continue

            # Read file content
            try:
                content = await file.read()
            except Exception as e:
                result.status = "error"
                result.message = "Error reading file"
                result.error_detail = str(e)
                errors += 1
                results.append(result)
                continue

            # Parse PDF
            try:
                data = parse_gbm_pdf(content)
            except ValueError as e:
                result.status = "error"
                result.message = "Error parsing PDF"
                result.error_detail = str(e)
                errors += 1
                results.append(result)
                continue
            except Exception as e:
                result.status = "error"
                result.message = "Error processing PDF"
                result.error_detail = str(e)
                errors += 1
                results.append(result)
                continue

            # Check for duplicates
            file_hash = UploadHistory.compute_file_hash(content)
            statement_date = datetime.fromisoformat(data["statement_date"])

            duplicate = await SnapshotService.check_duplicate_upload(
                db=db,
                user_id=user.id,
                file_hash=file_hash,
                statement_date=statement_date
            )

            if duplicate:
                # Extract data immediately to avoid lazy loading issues
                dup_statement_date = duplicate.statement_date
                dup_uploaded_at = duplicate.uploaded_at

                result.status = "duplicate"
                result.message = f"Already exists for {dup_statement_date.strftime('%B %Y')}"
                result.snapshot_date = dup_statement_date.strftime('%Y-%m-%d')
                result.error_detail = f"Uploaded on {dup_uploaded_at.strftime('%m/%d/%Y')}"
                duplicates += 1
                results.append(result)
                continue

            # Create snapshot
            try:
                snapshot = await SnapshotService.create_snapshot(
                    db=db,
                    portfolio_id=portfolio.id,
                    upload_data=data,
                    file_content=content,
                    filename=file.filename or "statement.pdf",
                    user_id=user.id,
                    upload_ip=client_ip
                )

                # Extract data immediately and detach from session
                snapshot_date_str = snapshot.snapshot_date.strftime('%B %Y')
                snapshot_date_iso = snapshot.snapshot_date.strftime('%Y-%m-%d')
                snapshot_id_str = str(snapshot.id)

                # Expunge to detach from session
                db.expunge(snapshot)

                result.status = "success"
                result.message = f"Successfully processed for {snapshot_date_str}"
                result.snapshot_date = snapshot_date_iso
                result.snapshot_id = snapshot_id_str
                successful += 1
                results.append(result)

            except Exception as e:
                # Rollback the transaction to keep session clean for next file
                await db.rollback()
                result.status = "error"
                result.message = "Error saving snapshot"
                result.error_detail = str(e)
                errors += 1
                results.append(result)
                continue

        except Exception as e:
            result.status = "error"
            result.message = "Unexpected error"
            result.error_detail = str(e)
            errors += 1
            results.append(result)

    # 6. Return summary
    return BulkUploadResponse(
        total_files=len(files),
        successful=successful,
        duplicates=duplicates,
        errors=errors,
        results=results
    )
