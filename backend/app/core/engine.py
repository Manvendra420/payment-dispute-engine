"""Dispute workflow engine - handles lifecycle transitions and rules."""

from datetime import datetime, timedelta
from typing import Dict, Optional
from enum import Enum

from ..models.dispute import Dispute, DisputeStatus, DisputeType
from ..models.event import DisputeEvent, EventType


class DisputeEngine:
    """Workflow engine for managing dispute lifecycle and state transitions."""
    
    # SLA times in hours based on dispute type
    SLA_CONFIG = {
        DisputeType.CHARGEBACK: 45,
        DisputeType.RETRIEVAL_REQUEST: 30,
        DisputeType.REPRESENTMENT: 60,
        DisputeType.PRE_ARBITRATION: 120,
    }
    
    # Valid state transitions
    VALID_TRANSITIONS = {
        DisputeStatus.OPEN: [DisputeStatus.UNDER_REVIEW, DisputeStatus.ASSIGNED],
        DisputeStatus.UNDER_REVIEW: [
            DisputeStatus.ASSIGNED,
            DisputeStatus.AWAITING_EVIDENCE,
            DisputeStatus.CLOSED,
        ],
        DisputeStatus.ASSIGNED: [
            DisputeStatus.AWAITING_EVIDENCE,
            DisputeStatus.EVIDENCE_SUBMITTED,
            DisputeStatus.CLOSED,
        ],
        DisputeStatus.AWAITING_EVIDENCE: [
            DisputeStatus.EVIDENCE_SUBMITTED,
            DisputeStatus.CLOSED,
        ],
        DisputeStatus.EVIDENCE_SUBMITTED: [
            DisputeStatus.ARBITRATION,
            DisputeStatus.WON,
            DisputeStatus.LOST,
            DisputeStatus.SETTLED,
        ],
        DisputeStatus.ARBITRATION: [
            DisputeStatus.WON,
            DisputeStatus.LOST,
            DisputeStatus.SETTLED,
        ],
        DisputeStatus.WON: [DisputeStatus.CLOSED],
        DisputeStatus.LOST: [DisputeStatus.CLOSED],
        DisputeStatus.SETTLED: [DisputeStatus.CLOSED],
        DisputeStatus.CLOSED: [],
    }
    
    @staticmethod
    def calculate_sla_deadline(
        dispute_type: DisputeType,
        filed_date: datetime
    ) -> datetime:
        """Calculate SLA deadline for a dispute."""
        sla_hours = DisputeEngine.SLA_CONFIG.get(
            dispute_type,
            72  # default 3 days
        )
        return filed_date + timedelta(hours=sla_hours)
    
    @staticmethod
    def can_transition(
        current_status: DisputeStatus,
        target_status: DisputeStatus
    ) -> bool:
        """Check if a status transition is valid."""
        valid_targets = DisputeEngine.VALID_TRANSITIONS.get(
            current_status,
            []
        )
        return target_status in valid_targets
    
    @staticmethod
    def is_sla_breached(dispute: Dispute) -> bool:
        """Check if dispute has breached SLA."""
        return datetime.utcnow() > dispute.sla_deadline
    
    @staticmethod
    def is_sla_approaching(
        dispute: Dispute,
        warning_hours: int = 24
    ) -> bool:
        """Check if SLA deadline is approaching."""
        time_until_sla = dispute.sla_deadline - datetime.utcnow()
        return timedelta(0) < time_until_sla <= timedelta(hours=warning_hours)
    
    @staticmethod
    def get_next_valid_statuses(current_status: DisputeStatus) -> list:
        """Get list of valid next statuses."""
        return DisputeEngine.VALID_TRANSITIONS.get(current_status, [])


class DisputeRulesEngine:
    """Rules engine for decision making."""
    
    @staticmethod
    def auto_win_scenarios(dispute: Dispute) -> bool:
        """Check if dispute should auto-win based on rules."""
        # Rule 1: No evidence required for certain reason codes
        auto_win_codes = ["00", "01", "02"]  # Example reason codes
        if dispute.reason_code in auto_win_codes:
            return True
        return False
    
    @staticmethod
    def auto_lose_scenarios(dispute: Dispute) -> bool:
        """Check if dispute should auto-lose based on rules."""
        # Rule 1: Missing critical evidence
        if dispute.status == DisputeStatus.EVIDENCE_SUBMITTED:
            if len(dispute.evidence_documents) == 0:
                return True
        return False
    
    @staticmethod
    def recommend_action(dispute: Dispute) -> Optional[str]:
        """Recommend next action based on current state."""
        if DisputeRulesEngine.auto_win_scenarios(dispute):
            return "AUTO_WIN"
        if DisputeRulesEngine.auto_lose_scenarios(dispute):
            return "AUTO_LOSE"
        
        # Recommend evidence submission if awaiting
        if dispute.status == DisputeStatus.AWAITING_EVIDENCE:
            return "REQUEST_EVIDENCE_SUBMISSION"
        
        return None
