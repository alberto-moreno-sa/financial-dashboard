from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class PositionBreakdown(BaseModel):
    """Individual position in the portfolio"""
    ticker: str
    name: str
    quantity: int
    avg_cost: float
    current_price: float
    market_value: float
    unrealized_gain: float
    unrealized_gain_percent: float


class PortfolioSummary(BaseModel):
    """Portfolio summary extracted from statement"""
    equity_value: float  # RENTA VARIABLE
    fixed_income_value: float  # DEUDA
    cash_value: float  # EFECTIVO
    total_value: float  # Total calculated or extracted


class Metadata(BaseModel):
    """Metadata about the uploaded file"""
    filename: str
    detected_date: str  # ISO format: "2021-12-31"
    account_holder: str
    currency: str  # "MXN"


class PortfolioSnapshotResponse(BaseModel):
    """Complete response for upload endpoint matching uploadspec.md"""
    status: str
    metadata: Metadata
    portfolio: PortfolioSummary
    breakdown: List[PositionBreakdown]


class SaveSnapshotRequest(BaseModel):
    """Request to save a confirmed snapshot to database"""
    snapshot_data: dict  # The full parsed data from PDF
    file_hash: str  # SHA256 hash of the original file


class SnapshotSummary(BaseModel):
    """Summary of a saved snapshot for history list"""
    id: str
    snapshot_date: datetime
    total_value: float
    equity_value: float
    fixed_income_value: float
    cash_value: float
    total_change: Optional[float] = None
    total_change_percent: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SnapshotPositionDetail(BaseModel):
    """Position detail in a snapshot"""
    ticker: str
    name: str
    quantity: float
    avg_cost: float
    current_price: float
    market_value: float
    unrealized_gain: float
    unrealized_gain_percent: float

    class Config:
        from_attributes = True


class SnapshotDetailResponse(BaseModel):
    """Detailed snapshot with all positions"""
    id: str
    snapshot_date: datetime
    total_value: float
    equity_value: float
    fixed_income_value: float
    cash_value: float
    total_change: Optional[float] = None
    total_change_percent: Optional[float] = None
    currency: str
    account_holder: Optional[str] = None
    created_at: datetime
    positions: List[SnapshotPositionDetail]

    class Config:
        from_attributes = True


class SnapshotHistoryResponse(BaseModel):
    """Response containing list of historical snapshots"""
    snapshots: List[SnapshotSummary]
    total_count: int


class FileUploadResult(BaseModel):
    """Result of processing a single file in bulk upload"""
    filename: str
    status: str  # "success", "duplicate", "error"
    message: str
    snapshot_date: Optional[str] = None
    snapshot_id: Optional[str] = None
    error_detail: Optional[str] = None


class BulkUploadResponse(BaseModel):
    """Response for bulk file upload"""
    total_files: int
    successful: int
    duplicates: int
    errors: int
    results: List[FileUploadResult]
