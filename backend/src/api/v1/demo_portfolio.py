"""
Demo Portfolio Endpoints - In-Memory Data Only
All data is stored in memory and resets on browser close/server restart
No database persistence
"""
from fastapi import APIRouter, Depends
from src.core.auth0 import get_current_user_from_token
from src.core.demo_auth import is_demo_mode
from src.core.demo_storage import get_demo_portfolio, get_demo_positions, get_demo_snapshots
from src.core.config import settings
from src.schemas.dashboard import StatsResponse, HoldingsResponse
from decimal import Decimal

router = APIRouter()


@router.get("/dashboard/stats", response_model=StatsResponse)
async def get_demo_stats(
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Get demo portfolio statistics from in-memory storage.
    No database access.
    """
    # Only works in demo mode
    if not is_demo_mode(settings.AUTH0_DOMAIN):
        return {"error": "Demo mode not enabled"}

    portfolio = get_demo_portfolio()
    snapshots = get_demo_snapshots()

    # Get latest snapshot
    latest_snapshot = max(snapshots, key=lambda x: x["snapshot_date"])

    # Calculate performance from last two snapshots
    if len(snapshots) >= 2:
        sorted_snapshots = sorted(snapshots, key=lambda x: x["snapshot_date"], reverse=True)
        current = sorted_snapshots[0]
        previous = sorted_snapshots[1]

        change = float(current["total_value"] - previous["total_value"])
        change_pct = (change / float(previous["total_value"])) * 100 if previous["total_value"] > 0 else 0.0
        trend = "up" if change > 0 else "down" if change < 0 else "neutral"
    else:
        change = 0.0
        change_pct = 0.0
        trend = "neutral"

    return StatsResponse(
        netWorth={"value": float(latest_snapshot["total_value"]), "label": "Total Value"},
        cash={"value": float(latest_snapshot["cash_balance"]), "label": "Cash"},
        investments={
            "value": float(latest_snapshot["equity_value"] + latest_snapshot["fixed_income_value"]),
            "label": "Invested"
        },
        performance={
            "dailyChange": change,
            "dailyChangePercentage": change_pct,
            "trend": trend
        }
    )


@router.get("/transactions", response_model=HoldingsResponse)
async def get_demo_transactions(
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Get demo holdings/positions from in-memory storage.
    No database access.
    """
    # Only works in demo mode
    if not is_demo_mode(settings.AUTH0_DOMAIN):
        return {"error": "Demo mode not enabled"}

    positions = get_demo_positions()

    items = []
    for idx, position in enumerate(positions):
        gain_loss = float(position["market_value"] - (position["avg_cost"] * position["quantity"]))
        gain_loss_pct = (gain_loss / float(position["avg_cost"] * position["quantity"])) * 100 if position["avg_cost"] > 0 else 0.0

        items.append({
            "id": f"holding-{idx+1}",
            "ticker": position["ticker"],
            "name": position["description"],
            "type": position["asset_type"],
            "details": {
                "quantity": float(position["quantity"]),
                "avgCost": float(position["avg_cost"]),
                "currentPrice": float(position["current_price"])
            },
            "financials": {
                "marketValue": float(position["market_value"]),
                "gainLoss": gain_loss,
                "gainLossPercent": gain_loss_pct
            }
        })

    return HoldingsResponse(count=len(items), items=items)


@router.get("/snapshots")
async def get_demo_snapshots_endpoint(
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Get demo snapshot history from in-memory storage.
    No database access.
    """
    # Only works in demo mode
    if not is_demo_mode(settings.AUTH0_DOMAIN):
        return {"error": "Demo mode not enabled"}

    snapshots = get_demo_snapshots()

    # Sort by date
    sorted_snapshots = sorted(snapshots, key=lambda x: x["snapshot_date"])

    items = []
    for snap in sorted_snapshots:
        items.append({
            "id": snap["id"],
            "snapshot_date": snap["snapshot_date"].isoformat(),
            "equity_value": float(snap["equity_value"]),
            "fixed_income_value": float(snap["fixed_income_value"]),
            "cash_value": float(snap["cash_balance"]),
            "total_value": float(snap["total_value"])
        })

    return {"count": len(items), "snapshots": items}
