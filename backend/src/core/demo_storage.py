"""
In-Memory Storage for Demo Mode
Simulates database operations without persisting data
Data is reset on server restart or after session timeout
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
from decimal import Decimal
import uuid

# In-memory storage (resets on server restart)
_demo_data: Dict[str, any] = {
    "users": {},
    "portfolios": {},
    "positions": {},
    "snapshots": {}
}


def init_demo_data():
    """Initialize demo data in memory"""
    # Demo user
    user_id = "demo-user-123"
    _demo_data["users"][user_id] = {
        "id": user_id,
        "auth0_id": "demo|123456789",
        "email": "demo@financial-dashboard.com",
        "name": "Demo User",
        "email_verified": True,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None)
    }

    # Demo portfolio
    portfolio_id = "demo-portfolio-123"
    _demo_data["portfolios"][portfolio_id] = {
        "id": portfolio_id,
        "user_id": user_id,
        "name": "Demo Portfolio",
        "description": "Sample investment portfolio",
        "currency": "MXN",
        "total_net_worth": Decimal("200000.00"),
        "cash_balance": Decimal("50000.00"),
        "invested_value": Decimal("150000.00"),
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None)
    }

    # Demo positions
    positions = [
        {
            "id": str(uuid.uuid4()),
            "portfolio_id": portfolio_id,
            "ticker": "AAPL",
            "description": "Apple Inc.",
            "quantity": Decimal("100"),
            "avg_cost": Decimal("150.00"),
            "current_price": Decimal("175.00"),
            "market_value": Decimal("17500.00"),
            "asset_type": "equity"
        },
        {
            "id": str(uuid.uuid4()),
            "portfolio_id": portfolio_id,
            "ticker": "MSFT",
            "description": "Microsoft Corporation",
            "quantity": Decimal("80"),
            "avg_cost": Decimal("250.00"),
            "current_price": Decimal("300.00"),
            "market_value": Decimal("24000.00"),
            "asset_type": "equity"
        },
        {
            "id": str(uuid.uuid4()),
            "portfolio_id": portfolio_id,
            "ticker": "GOOGL",
            "description": "Alphabet Inc.",
            "quantity": Decimal("50"),
            "avg_cost": Decimal("100.00"),
            "current_price": Decimal("120.00"),
            "market_value": Decimal("6000.00"),
            "asset_type": "equity"
        },
        {
            "id": str(uuid.uuid4()),
            "portfolio_id": portfolio_id,
            "ticker": "CETES",
            "description": "CETES 28 días",
            "quantity": Decimal("1000"),
            "avg_cost": Decimal("100.00"),
            "current_price": Decimal("102.50"),
            "market_value": Decimal("102500.00"),
            "asset_type": "fixed_income"
        }
    ]

    for pos in positions:
        _demo_data["positions"][pos["id"]] = pos

    # Demo snapshots (historical data)
    snapshots = [
        {
            "id": str(uuid.uuid4()),
            "portfolio_id": portfolio_id,
            "user_id": user_id,
            "snapshot_date": datetime(2024, 10, 31, tzinfo=timezone.utc).replace(tzinfo=None),
            "equity_value": Decimal("35000.00"),
            "fixed_income_value": Decimal("95000.00"),
            "cash_balance": Decimal("45000.00"),
            "total_value": Decimal("175000.00")
        },
        {
            "id": str(uuid.uuid4()),
            "portfolio_id": portfolio_id,
            "user_id": user_id,
            "snapshot_date": datetime(2024, 11, 30, tzinfo=timezone.utc).replace(tzinfo=None),
            "equity_value": Decimal("42000.00"),
            "fixed_income_value": Decimal("100000.00"),
            "cash_balance": Decimal("48000.00"),
            "total_value": Decimal("190000.00")
        },
        {
            "id": str(uuid.uuid4()),
            "portfolio_id": portfolio_id,
            "user_id": user_id,
            "snapshot_date": datetime(2024, 12, 31, tzinfo=timezone.utc).replace(tzinfo=None),
            "equity_value": Decimal("47500.00"),
            "fixed_income_value": Decimal("102500.00"),
            "cash_balance": Decimal("50000.00"),
            "total_value": Decimal("200000.00")
        }
    ]

    for snap in snapshots:
        _demo_data["snapshots"][snap["id"]] = snap


def get_demo_user():
    """Get demo user from memory"""
    if not _demo_data["users"]:
        init_demo_data()
    return list(_demo_data["users"].values())[0]


def get_demo_portfolio():
    """Get demo portfolio from memory"""
    if not _demo_data["portfolios"]:
        init_demo_data()
    return list(_demo_data["portfolios"].values())[0]


def get_demo_positions() -> List[Dict]:
    """Get demo positions from memory"""
    if not _demo_data["positions"]:
        init_demo_data()
    return list(_demo_data["positions"].values())


def get_demo_snapshots() -> List[Dict]:
    """Get demo snapshots from memory"""
    if not _demo_data["snapshots"]:
        init_demo_data()
    return list(_demo_data["snapshots"].values())


def reset_demo_data():
    """Reset all demo data (called on server restart or manually)"""
    _demo_data.clear()
    _demo_data.update({
        "users": {},
        "portfolios": {},
        "positions": {},
        "snapshots": {}
    })
    init_demo_data()


# Initialize on module load
init_demo_data()
