"""Metrics and analytics endpoints."""

from typing import Optional
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])


@router.get("/dashboard", response_model=dict)
async def get_dashboard_metrics():
    """Get overall dispute dashboard metrics."""
    # In production, these would query the database
    return {
        "summary": {
            "total_disputes": 42,
            "open_disputes": 8,
            "won_disputes": 22,
            "lost_disputes": 12,
        },
        "by_status": {
            "open": 8,
            "under_review": 3,
            "assigned": 5,
            "awaiting_evidence": 6,
            "evidence_submitted": 4,
            "arbitration": 2,
            "won": 22,
            "lost": 12,
            "settled": 2,
            "closed": 36,
        },
        "performance": {
            "win_rate_percent": 64.7,
            "average_resolution_days": 12.3,
            "sla_breach_count": 2,
            "sla_compliance_percent": 95.2,
        },
        "by_merchant_top_5": [
            {"merchant_id": "MCH-100", "total": 15, "win_rate": 73.3},
            {"merchant_id": "MCH-101", "total": 12, "win_rate": 66.7},
            {"merchant_id": "MCH-102", "total": 8, "win_rate": 62.5},
            {"merchant_id": "MCH-103", "total": 4, "win_rate": 50.0},
            {"merchant_id": "MCH-104", "total": 3, "win_rate": 66.7},
        ],
    }


@router.get("/by-type", response_model=dict)
async def get_metrics_by_type():
    """Get metrics grouped by dispute type."""
    return {
        "CHARGEBACK": {
            "total": 18,
            "won": 12,
            "lost": 4,
            "settled": 2,
            "win_rate_percent": 66.7,
            "avg_resolution_days": 11.5,
        },
        "RETRIEVAL_REQUEST": {
            "total": 12,
            "won": 8,
            "lost": 3,
            "settled": 1,
            "win_rate_percent": 66.7,
            "avg_resolution_days": 8.2,
        },
        "REPRESENTMENT": {
            "total": 8,
            "won": 5,
            "lost": 3,
            "settled": 0,
            "win_rate_percent": 62.5,
            "avg_resolution_days": 15.1,
        },
        "PRE_ARBITRATION": {
            "total": 4,
            "won": 2,
            "lost": 2,
            "settled": 0,
            "win_rate_percent": 50.0,
            "avg_resolution_days": 18.7,
        },
    }


@router.get("/sla-status", response_model=dict)
async def get_sla_metrics():
    """Get SLA compliance metrics."""
    return {
        "total_active_disputes": 28,
        "sla_compliant": 26,
        "sla_breached": 2,
        "sla_approaching_warning": 5,
        "sla_compliance_percent": 92.9,
        "breached_disputes": [
            {"dispute_id": "DSP-1001", "hours_overdue": 4.5},
            {"dispute_id": "DSP-1002", "hours_overdue": 2.1},
        ],
        "approaching_disputes": [
            {"dispute_id": "DSP-1003", "hours_remaining": 18.5},
            {"dispute_id": "DSP-1004", "hours_remaining": 12.3},
            {"dispute_id": "DSP-1005", "hours_remaining": 8.7},
            {"dispute_id": "DSP-1006", "hours_remaining": 5.2},
            {"dispute_id": "DSP-1007", "hours_remaining": 3.1},
        ],
    }


@router.get("/auto-decisions", response_model=dict)
async def get_auto_decision_metrics():
    """Get metrics on auto-decided disputes."""
    return {
        "auto_decided_total": 8,
        "auto_win": 5,
        "auto_lose": 3,
        "auto_win_rate_percent": 62.5,
        "recent_auto_decisions": [
            {
                "dispute_id": "DSP-1020",
                "decided_at": "2026-03-01T10:30:00Z",
                "decision": "AUTO_WIN",
                "reason": "Reason code in auto-win list",
            },
            {
                "dispute_id": "DSP-1019",
                "decided_at": "2026-03-01T09:15:00Z",
                "decision": "AUTO_LOSE",
                "reason": "Missing critical evidence",
            },
            {
                "dispute_id": "DSP-1018",
                "decided_at": "2026-02-28T16:45:00Z",
                "decision": "AUTO_WIN",
                "reason": "Reason code in auto-win list",
            },
        ],
    }
