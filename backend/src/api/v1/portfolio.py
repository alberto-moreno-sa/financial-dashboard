from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from src.core.database import get_db
from src.core.auth0 import get_current_user_from_token
from src.services.parser import PortfolioParser
from src.services.analytics import PortfolioAnalytics
from src.services.snapshot_service import SnapshotService
from src.models.portfolio import Portfolio
from src.models.user import User
from src.models.snapshot import PortfolioSnapshot
from src.schemas.dashboard import StatsResponse, ChartResponse, HoldingsResponse

router = APIRouter()

@router.post("/upload")
async def upload_portfolio(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """Upload portfolio data. Requires Auth0 authentication."""
    raw = await PortfolioParser.parse_json(file)
    analytics = PortfolioAnalytics(raw)

    # Get user from DB using auth0_id
    auth0_id = current_user.get("auth0_id")
    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please sync your account first.")

    p_id = await analytics.save_to_db(db, user.id)
    return {"status": "success", "data": {"portfolioId": p_id}}

# Helper to fetch from DB
async def get_portfolio_data(id: str, db: AsyncSession):
    res = await db.execute(
        select(Portfolio).options(selectinload(Portfolio.positions)).where(Portfolio.id == id)
    )
    p = res.scalar_one_or_none()
    if not p: raise HTTPException(404, "Portfolio not found")
    return p

@router.get("/dashboard/stats", response_model=StatsResponse)
async def get_stats(
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Get portfolio statistics for the authenticated user.
    Now reads from the latest snapshot instead of the portfolio table.
    """
    # Get user from DB using auth0_id
    auth0_id = current_user.get("auth0_id")
    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please sync your account first.")

    # Get user's portfolio
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id).limit(1)
    )
    portfolio = portfolio_result.scalar_one_or_none()

    if not portfolio:
        # Return empty stats if no portfolio yet
        return StatsResponse(
            netWorth={"value": 0.0, "label": "Net Worth"},
            cash={"value": 0.0, "label": "Cash"},
            investments={"value": 0.0, "label": "Invested"},
            performance={"dailyChange": 0.0, "dailyChangePercentage": 0.0, "trend": "neutral"}
        )

    # Get latest snapshot for this portfolio
    latest_snapshot = await SnapshotService.get_latest_snapshot(db, portfolio.id)

    if not latest_snapshot:
        # Return empty stats if no snapshots yet
        return StatsResponse(
            netWorth={"value": 0.0, "label": "Net Worth"},
            cash={"value": 0.0, "label": "Cash"},
            investments={"value": 0.0, "label": "Invested"},
            performance={"dailyChange": 0.0, "dailyChangePercentage": 0.0, "trend": "neutral"}
        )

    # Calculate performance metrics from snapshot changes
    daily_change = float(latest_snapshot.total_change) if latest_snapshot.total_change else 0.0
    daily_change_pct = float(latest_snapshot.total_change_percent) if latest_snapshot.total_change_percent else 0.0
    trend = "up" if daily_change > 0 else "down" if daily_change < 0 else "neutral"

    return StatsResponse(
        netWorth={"value": float(latest_snapshot.total_value), "label": "Valor Total"},
        cash={"value": float(latest_snapshot.cash_value), "label": "Efectivo"},
        investments={"value": float(latest_snapshot.equity_value + latest_snapshot.fixed_income_value), "label": "Invertido"},
        performance={"dailyChange": daily_change, "dailyChangePercentage": daily_change_pct, "trend": trend}
    )

@router.get("/transactions", response_model=HoldingsResponse)
async def get_transactions(
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Get holdings/positions for the authenticated user.
    Now reads from the latest snapshot instead of the positions table.
    """
    # Get user from DB using auth0_id
    auth0_id = current_user.get("auth0_id")
    if not auth0_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_result = await db.execute(select(User).where(User.auth0_id == auth0_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please sync your account first.")

    # Get user's portfolio
    portfolio_result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id).limit(1)
    )
    portfolio = portfolio_result.scalar_one_or_none()

    if not portfolio:
        # Return empty list if no portfolio yet
        return HoldingsResponse(count=0, items=[])

    # Get latest snapshot with positions
    latest_snapshot = await SnapshotService.get_latest_snapshot(db, portfolio.id)

    if not latest_snapshot or not latest_snapshot.positions:
        # Return empty list if no snapshots or no positions
        return HoldingsResponse(count=0, items=[])

    # Convert snapshot positions to holdings format
    items = []
    for position in latest_snapshot.positions:
        items.append({
            "id": str(position.id),
            "ticker": position.ticker,
            "name": position.name,
            "type": position.asset_type or "Stock",
            "details": {
                "quantity": float(position.quantity),
                "avgCost": float(position.avg_cost),
                "currentPrice": float(position.current_price),
            },
            "financials": {
                "totalValue": float(position.market_value),
                "unrealizedGain": float(position.unrealized_gain),
                "unrealizedGainPercent": float(position.unrealized_gain_percent),
            }
        })

    return HoldingsResponse(count=len(items), items=items)