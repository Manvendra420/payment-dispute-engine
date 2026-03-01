"""Dispute models for the payment dispute engine."""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class DisputeType(str, Enum):
    """Types of disputes."""
    CHARGEBACK = "chargeback"
    RETRIEVAL_REQUEST = "retrieval_request"
    REPRESENTMENT = "representment"
    PRE_ARBITRATION = "pre_arbitration"


class DisputeStatus(str, Enum):
    """Dispute lifecycle statuses."""
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    ASSIGNED = "assigned"
    AWAITING_EVIDENCE = "awaiting_evidence"
    EVIDENCE_SUBMITTED = "evidence_submitted"
    ARBITRATION = "arbitration"
    WON = "won"
    LOST = "lost"
    SETTLED = "settled"
    CLOSED = "closed"


class Evidence(BaseModel):
    """Evidence submitted for a dispute."""
    id: Optional[str] = None
    dispute_id: str
    evidence_type: str  # invoice, receipt, contract, communication, etc.
    file_path: str
    description: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    file_size_bytes: int


class Dispute(BaseModel):
    """Payment dispute model."""
    id: str
    card_last_four: str
    amount_cents: int
    currency: str = "USD"
    dispute_type: DisputeType
    status: DisputeStatus = DisputeStatus.OPEN
    merchant_id: str
    transaction_id: str
    transaction_date: datetime
    dispute_filed_date: datetime
    reason_code: str
    description: Optional[str] = None
    sla_deadline: datetime
    evidence_documents: List[Evidence] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    stage_updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""
        use_enum_values = False


class DisputeCreate(BaseModel):
    """Request model to create a dispute."""
    card_last_four: str
    amount_cents: int
    currency: str = "USD"
    dispute_type: DisputeType
    merchant_id: str
    transaction_id: str
    transaction_date: datetime
    reason_code: str
    description: Optional[str] = None


class DisputeUpdate(BaseModel):
    """Request model to update a dispute."""
    status: Optional[DisputeStatus] = None
    description: Optional[str] = None
