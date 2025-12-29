"""
Demo data seeder for Financial Dashboard
Creates sample users and portfolio data for demonstration
"""
import asyncio
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.src.core.database import AsyncSessionLocal
from backend.src.models.user import User
from backend.src.models.portfolio import Portfolio
from backend.src.models.snapshot import PortfolioSnapshot
from backend.src.models.position import Position


async def seed_demo_data():
    """Seed database with demo data"""
    async with AsyncSessionLocal() as session:
        # Check if demo user exists
        result = await session.execute(
            select(User).where(User.email == "demo@financial-dashboard.com")
        )
        demo_user = result.scalar_one_or_none()

        if demo_user:
            print("Demo user already exists. Skipping seed.")
            return

        # Create demo user
        demo_user = User(
            auth0_id="demo|123456789",
            email="demo@financial-dashboard.com",
            name="Demo User",
            email_verified=True
        )
        session.add(demo_user)
        await session.flush()

        # Create demo portfolio
        portfolio = Portfolio(
            user_id=demo_user.id,
            name="Demo Portfolio",
            description="Sample investment portfolio for demonstration",
            currency="MXN",
            total_net_worth=Decimal("500000.00"),
            cash_balance=Decimal("50000.00"),
            invested_value=Decimal("450000.00")
        )
        session.add(portfolio)
        await session.flush()

        # Create demo positions
        positions_data = [
            {
                "ticker": "AAPL",
                "description": "Apple Inc.",
                "quantity": Decimal("100"),
                "avg_cost": Decimal("150.00"),
                "current_price": Decimal("175.00"),
                "market_value": Decimal("17500.00"),
                "asset_type": "equity"
            },
            {
                "ticker": "MSFT",
                "description": "Microsoft Corporation",
                "quantity": Decimal("80"),
                "avg_cost": Decimal("250.00"),
                "current_price": Decimal("300.00"),
                "market_value": Decimal("24000.00"),
                "asset_type": "equity"
            },
            {
                "ticker": "GOOGL",
                "description": "Alphabet Inc.",
                "quantity": Decimal("50"),
                "avg_cost": Decimal("100.00"),
                "current_price": Decimal("120.00"),
                "market_value": Decimal("6000.00"),
                "asset_type": "equity"
            },
            {
                "ticker": "CETES",
                "description": "CETES 28 días",
                "quantity": Decimal("1000"),
                "avg_cost": Decimal("100.00"),
                "current_price": Decimal("102.50"),
                "market_value": Decimal("102500.00"),
                "asset_type": "fixed_income"
            },
        ]

        for pos_data in positions_data:
            position = Position(
                portfolio_id=portfolio.id,
                **pos_data
            )
            session.add(position)

        # Create demo snapshots (historical data)
        snapshots_data = [
            {
                "snapshot_date": datetime(2024, 10, 31, tzinfo=timezone.utc).replace(tzinfo=None),
                "equity_value": Decimal("35000.00"),
                "fixed_income_value": Decimal("95000.00"),
                "cash_balance": Decimal("45000.00"),
                "total_value": Decimal("175000.00")
            },
            {
                "snapshot_date": datetime(2024, 11, 30, tzinfo=timezone.utc).replace(tzinfo=None),
                "equity_value": Decimal("42000.00"),
                "fixed_income_value": Decimal("100000.00"),
                "cash_balance": Decimal("48000.00"),
                "total_value": Decimal("190000.00")
            },
            {
                "snapshot_date": datetime(2024, 12, 31, tzinfo=timezone.utc).replace(tzinfo=None),
                "equity_value": Decimal("47500.00"),
                "fixed_income_value": Decimal("102500.00"),
                "cash_balance": Decimal("50000.00"),
                "total_value": Decimal("200000.00")
            },
        ]

        for snap_data in snapshots_data:
            snapshot = PortfolioSnapshot(
                portfolio_id=portfolio.id,
                user_id=demo_user.id,
                **snap_data
            )
            session.add(snapshot)

        await session.commit()
        print("✅ Demo data seeded successfully!")
        print(f"  - Demo user: {demo_user.email}")
        print(f"  - Portfolio: {portfolio.name}")
        print(f"  - Positions: {len(positions_data)}")
        print(f"  - Snapshots: {len(snapshots_data)}")


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
