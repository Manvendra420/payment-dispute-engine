"""Dispute API endpoints."""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..models.dispute import (
    Dispute,
    DisputeCreate,
    DisputeUpdate,
    DisputeStatus,
    Evidence,
)
from ..core.engine import DisputeEngine, DisputeRulesEngine

router = APIRouter(prefix="/api/v1/disputes", tags=["disputes"])

# In-memory store (replace with DB later)
disputes_db: dict = {}
dispute_counter = 1000


class DisputeResponse(BaseModel):
    """Response model for dispute."""
    id: str
    card_last_four: str
    amount_cents: int
    currency: str
    dispute_type: str
    status: str
    merchant_id: str
    transaction_id: str
    reason_code: str
    sla_deadline: datetime
    sla_breached: bool
    sla_approaching: bool
    recommendation: Optional[str] = None


@router.post("", response_model=dict)
async def create_dispute(dispute_create: DisputeCreate):
    """Create a new dispute."""
    global dispute_counter
    
    dispute_id = f"DSP-{dispute_counter}"
    dispute_counter += 1
    
    sla_deadline = DisputeEngine.calculate_sla_deadline(
        dispute_create.dispute_type,
        dispute_create.dispute_filed_date
    )
    
    dispute = Dispute(
        id=dispute_id,
        **dispute_create.model_dump(),
        sla_deadline=sla_deadline,
    )
    
    disputes_db[dispute_id] = dispute
    
    return {
        "success": True,
        "dispute_id": dispute_id,
        "message": f"Dispute {dispute_id} created successfully"
    }


@router.get("/{dispute_id}", response_model=DisputeResponse)
async def get_dispute(dispute_id: str):
    """Retrieve a specific dispute."""
    if dispute_id not in disputes_db:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    dispute = disputes_db[dispute_id]
    recommendation = DisputeRulesEngine.recommend_action(dispute)
    
    return DisputeResponse(
        id=dispute.id,
        card_last_four=dispute.card_last_four,
        amount_cents=dispute.amount_cents,
        currency=dispute.currency,
        dispute_type=dispute.dispute_type.value,
        status=dispute.status.value,
        merchant_id=dispute.merchant_id,
        transaction_id=dispute.transaction_id,
        reason_code=dispute.reason_code,
        sla_deadline=dispute.sla_deadline,
        sla_breached=DisputeEngine.is_sla_breached(dispute),
        sla_approaching=DisputeEngine.is_sla_approaching(dispute),
        recommendation=recommendation,
    )


@router.get("", response_model=dict)
async def list_disputes(
    status: Optional[str] = Query(None),
    merchant_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List all disputes with optional filtering."""
    disputes = list(disputes_db.values())
    
    if status:
        disputes = [d for d in disputes if d.status.value == status]
    
    if merchant_id:
        disputes = [d for d in disputes if d.merchant_id == merchant_id]
    
    total = len(disputes)
    disputes = disputes[offset : offset + limit]
    
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "disputes": [
            {
                "id": d.id,
                "status": d.status.value,
                "amount_cents": d.amount_cents,
                "merchant_id": d.merchant_id,
                "created_at": d.created_at,
            }
            for d in disputes
        ]
    }


@router.patch("/{dispute_id}", response_model=dict)
async def update_dispute(dispute_id: str, update: DisputeUpdate):
    """Update a dispute status or details."""
    if dispute_id not in disputes_db:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    dispute = disputes_db[dispute_id]
    
    if update.status:
        if not DisputeEngine.can_transition(dispute.status, update.status):
            raise HTTPException(
                status_code=400,
                detail=f"Cannot transition from {dispute.status.value} to {update.status.value}"
            )
        dispute.status = update.status
        dispute.stage_updated_at = datetime.utcnow()
    
    if update.description:
        dispute.description = update.description
    
    dispute.updated_at = datetime.utcnow()
    
    return {
        "success": True,
        "message": f"Dispute {dispute_id} updated successfully",
        "status": dispute.status.value
    }


@router.post("/{dispute_id}/evidence", response_model=dict)
async def upload_evidence(dispute_id: str, evidence: Evidence):
    """Upload evidence for a dispute."""
    if dispute_id not in disputes_db:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    dispute = disputes_db[dispute_id]
    evidence.id = f"EVD-{len(dispute.evidence_documents) + 1}"
    dispute.evidence_documents.append(evidence)
    
    return {
        "success": True,
        "evidence_id": evidence.id,
        "message": "Evidence uploaded successfully"
    }


@router.get("/{dispute_id}/valid-transitions", response_model=dict)
async def get_valid_transitions(dispute_id: str):
    """Get valid status transitions for a dispute."""
    if dispute_id not in disputes_db:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    dispute = disputes_db[dispute_id]
    valid_statuses = DisputeEngine.get_next_valid_statuses(dispute.status)
    
    return {
        "current_status": dispute.status.value,
        "valid_next_statuses": [s.value for s in valid_statuses]
    }


@router.get("/{dispute_id}/sla-status", response_model=dict)
async def get_sla_status(dispute_id: str):
    """Get SLA status for a dispute."""
    if dispute_id not in disputes_db:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    dispute = disputes_db[dispute_id]
    time_remaining = (dispute.sla_deadline - datetime.utcnow()).total_seconds() / 3600
    
    return {
        "dispute_id": dispute_id,
        "sla_deadline": dispute.sla_deadline,
        "hours_remaining": max(0, time_remaining),
        "breached": DisputeEngine.is_sla_breached(dispute),
        "approaching_warning": DisputeEngine.is_sla_approaching(dispute),
    }
