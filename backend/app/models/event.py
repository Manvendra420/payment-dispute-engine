"""Event models for audit log."""

from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Types of events in dispute lifecycle."""
    DISPUTE_CREATED = "dispute_created"
    STATUS_CHANGED = "status_changed"
    EVIDENCE_UPLOADED = "evidence_uploaded"
    NOTE_ADDED = "note_added"
    SLA_APPROACHING = "sla_approaching"
    SLA_BREACHED = "sla_breached"
    ASSIGNEE_CHANGED = "assignee_changed"
    DECISION_MADE = "decision_made"


class DisputeEvent(BaseModel):
    """Audit event for dispute activity."""
    id: Optional[str] = None
    dispute_id: str
    event_type: EventType
    actor_id: str
    actor_type: str  # system, user, api
    details: dict = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None

    class Config:
        use_enum_values = False
