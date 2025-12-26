from typing import List, Literal
from pydantic import BaseModel

class FinancialValue(BaseModel):
    value: float
    label: str
    percentageOfTotal: float = 0.0

class StatsResponse(BaseModel):
    currency: str = "MXN"
    netWorth: FinancialValue
    cash: FinancialValue
    investments: FinancialValue
    performance: dict

class ChartSegment(BaseModel):
    id: str; label: str; value: float; percentage: float; color: str

class ChartResponse(BaseModel):
    chartTitle: str; totalValue: float; segments: List[ChartSegment]

class HoldingItem(BaseModel):
    id: str; ticker: str; name: str; type: str
    details: dict; financials: dict

class HoldingsResponse(BaseModel):
    count: int; items: List[HoldingItem]