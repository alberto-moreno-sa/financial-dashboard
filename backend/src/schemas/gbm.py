from typing import List
from pydantic import BaseModel

class FinancialPositionRaw(BaseModel):
    """
    Raw financial position data (legacy schema - kept for backward compatibility).
    Note: This schema is currently unused but kept for potential future use.
    """
    symbol: str
    description: str
    quantity: float
    avg_cost: float
    current_price: float
    market_value: float

    class Config:
        extra = "ignore"

class FinancialPortfolioRaw(BaseModel):
    """
    Raw financial portfolio data (legacy schema - kept for backward compatibility).
    Note: This schema is currently unused but kept for potential future use.
    """
    contract_id: str
    cash_balance: float
    positions: List[FinancialPositionRaw]
