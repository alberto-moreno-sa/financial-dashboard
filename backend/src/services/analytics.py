import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.portfolio import Portfolio, Position
from src.schemas.dashboard import StatsResponse, ChartResponse, HoldingsResponse, ChartSegment, HoldingItem

class PortfolioAnalytics:
    def __init__(self, raw_data: dict):
        self.cash = float(raw_data.get("efectivo", 0))
        self.positions = raw_data.get("posiciones", [])
        self.df = pd.DataFrame(self.positions)
        self._standardize_df()

    def _standardize_df(self):
        map_cols = {
            "emisora": "ticker", "descripcion": "name", "titulos": "qty",
            "costo_promedio": "avg_cost", "ultimo_precio": "price", "valor_mercado": "value"
        }
        self.df.rename(columns=map_cols, inplace=True)
        if "value" not in self.df.columns:
            self.df["value"] = self.df["qty"] * self.df["price"]
        self.df["type"] = self.df["name"].apply(lambda x: "ETF" if "VANGUARD" in x.upper() else "Stock")

    async def save_to_db(self, db: AsyncSession, user_id: str) -> str:
        """Save portfolio data to database. Requires user_id for multi-tenancy."""
        invested = self.df["value"].sum()
        portfolio = Portfolio(
            user_id=user_id,
            name="Mi Portafolio",
            total_net_worth=self.cash + invested,
            cash_balance=self.cash,
            invested_value=invested
        )
        db.add(portfolio)
        await db.flush()
        
        for _, row in self.df.iterrows():
            db.add(Position(
                portfolio_id=portfolio.id,
                ticker=row["ticker"],
                name=row["name"],
                asset_type=row["type"],
                quantity=row["qty"],
                avg_cost=row["avg_cost"],
                current_price=row["price"],
                market_value=row["value"]
            ))
        await db.commit()
        return portfolio.id

    # ... Aquí irían los métodos calculate_stats(), calculate_allocation() 
    # idénticos a la versión anterior, pero usando self.df