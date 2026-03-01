"""Request/Response validation schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class CreateDisputeRequest(BaseModel):
    """Request to create a new dispute."""
    card_last_four: str = Field(..., min_length=4, max_length=4)
    amount_cents: int = Field(..., gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    dispute_type: str
    merchant_id: str = Field(..., min_length=5)
    transaction_id: str = Field(..., min_length=5)
    transaction_date: datetime
    reason_code: str = Field(..., min_length=2, max_length=2)
    description: Optional[str] = None

    @validator('reason_code')
    def validate_reason_code(cls, v):
        if not v.isdigit():
            raise ValueError('reason_code must be numeric')
        return v


class UploadEvidenceRequest(BaseModel):
    """Request to upload evidence."""
    evidence_type: str = Field(..., min_length=3)
    file_path: str = Field(..., min_length=5)
    description: Optional[str] = None
    file_size_bytes: int = Field(..., gt=0)


class UpdateDisputeStatusRequest(BaseModel):
    """Request to update dispute status."""
    status: str = Field(..., min_length=3)
    comment: Optional[str] = None


class MetricsResponse(BaseModel):
    """Metrics response model."""
    total_disputes: int
    open_disputes: int
    sla_breached_count: int
    average_resolution_time_hours: float
    win_rate_percent: float
    auto_decided_count: int
