"""Tests for dispute engine."""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from app.models.dispute import Dispute, DisputeType, DisputeStatus
from app.models.event import DisputeEvent, EventType
from app.core.engine import DisputeEngine, DisputeRulesEngine


def test_sla_calculation():
    """Test SLA deadline calculation for different dispute types."""
    now = datetime.utcnow()
    
    # Test CHARGEBACK - 45 hours
    deadline = DisputeEngine.calculate_sla_deadline(DisputeType.CHARGEBACK, now)
    expected_hours = 45
    actual_hours = (deadline - now).total_seconds() / 3600
    assert abs(actual_hours - expected_hours) < 1, f"CHARGEBACK SLA should be ~{expected_hours}h, got {actual_hours}h"
    
    # Test RETRIEVAL_REQUEST - 30 hours
    deadline = DisputeEngine.calculate_sla_deadline(DisputeType.RETRIEVAL_REQUEST, now)
    expected_hours = 30
    actual_hours = (deadline - now).total_seconds() / 3600
    assert abs(actual_hours - expected_hours) < 1, f"RETRIEVAL_REQUEST SLA should be ~{expected_hours}h, got {actual_hours}h"
    
    print("✓ SLA calculation test passed")


def test_valid_transitions():
    """Test status transition validation."""
    # Valid transitions
    assert DisputeEngine.can_transition(DisputeStatus.OPEN, DisputeStatus.ASSIGNED), "OPEN → ASSIGNED should be valid"
    assert DisputeEngine.can_transition(DisputeStatus.ASSIGNED, DisputeStatus.AWAITING_EVIDENCE), "ASSIGNED → AWAITING_EVIDENCE should be valid"
    assert DisputeEngine.can_transition(DisputeStatus.EVIDENCE_SUBMITTED, DisputeStatus.WON), "EVIDENCE_SUBMITTED → WON should be valid"
    
    # Invalid transitions
    assert not DisputeEngine.can_transition(DisputeStatus.OPEN, DisputeStatus.CLOSED), "OPEN → CLOSED should be invalid"
    assert not DisputeEngine.can_transition(DisputeStatus.CLOSED, DisputeStatus.OPEN), "CLOSED → OPEN should be invalid"
    assert not DisputeEngine.can_transition(DisputeStatus.WON, DisputeStatus.LOST), "WON → LOST should be invalid"
    
    print("✓ Status transition validation test passed")


def test_sla_breach_detection():
    """Test SLA breach detection."""
    # Create a dispute with SLA already breached
    past_deadline = datetime.utcnow() - timedelta(hours=5)
    breached_dispute = Dispute(
        id="TEST-001",
        card_last_four="1234",
        amount_cents=10000,
        currency="USD",
        dispute_type=DisputeType.CHARGEBACK,
        status=DisputeStatus.OPEN,
        merchant_id="MCH-001",
        transaction_id="TXN-001",
        transaction_date=datetime.utcnow(),
        dispute_filed_date=datetime.utcnow(),
        reason_code="00",
        sla_deadline=past_deadline,
    )
    
    assert DisputeEngine.is_sla_breached(breached_dispute), "Dispute should be marked as SLA breached"
    
    # Create a dispute with upcoming SLA
    future_deadline = datetime.utcnow() + timedelta(hours=100)
    valid_dispute = Dispute(
        id="TEST-002",
        card_last_four="5678",
        amount_cents=5000,
        currency="USD",
        dispute_type=DisputeType.CHARGEBACK,
        status=DisputeStatus.OPEN,
        merchant_id="MCH-002",
        transaction_id="TXN-002",
        transaction_date=datetime.utcnow(),
        dispute_filed_date=datetime.utcnow(),
        reason_code="01",
        sla_deadline=future_deadline,
    )
    
    assert not DisputeEngine.is_sla_breached(valid_dispute), "Dispute should not be marked as SLA breached"
    
    print("✓ SLA breach detection test passed")


def test_sla_approaching_warning():
    """Test SLA approaching warning."""
    # Create a dispute with SLA approaching (within 24 hours)
    approaching_deadline = datetime.utcnow() + timedelta(hours=20)
    approaching_dispute = Dispute(
        id="TEST-003",
        card_last_four="9999",
        amount_cents=7500,
        currency="USD",
        dispute_type=DisputeType.RETRIEVAL_REQUEST,
        status=DisputeStatus.AWAITING_EVIDENCE,
        merchant_id="MCH-003",
        transaction_id="TXN-003",
        transaction_date=datetime.utcnow(),
        dispute_filed_date=datetime.utcnow(),
        reason_code="02",
        sla_deadline=approaching_deadline,
    )
    
    assert DisputeEngine.is_sla_approaching(approaching_dispute), "Dispute should trigger SLA approaching warning"
    
    # Create a dispute with SLA far away
    distant_deadline = datetime.utcnow() + timedelta(hours=72)
    safe_dispute = Dispute(
        id="TEST-004",
        card_last_four="1111",
        amount_cents=3000,
        currency="USD",
        dispute_type=DisputeType.REPRESENTMENT,
        status=DisputeStatus.OPEN,
        merchant_id="MCH-004",
        transaction_id="TXN-004",
        transaction_date=datetime.utcnow(),
        dispute_filed_date=datetime.utcnow(),
        reason_code="03",
        sla_deadline=distant_deadline,
    )
    
    assert not DisputeEngine.is_sla_approaching(safe_dispute), "Dispute should not trigger SLA approaching warning"
    
    print("✓ SLA approaching warning test passed")


def test_rules_engine_auto_win():
    """Test auto-win scenario detection."""
    dispute = Dispute(
        id="TEST-WIN",
        card_last_four="2222",
        amount_cents=10000,
        currency="USD",
        dispute_type=DisputeType.CHARGEBACK,
        status=DisputeStatus.OPEN,
        merchant_id="MCH-005",
        transaction_id="TXN-005",
        transaction_date=datetime.utcnow(),
        dispute_filed_date=datetime.utcnow(),
        reason_code="00",  # Auto-win reason code
        sla_deadline=datetime.utcnow() + timedelta(hours=48),
    )
    
    assert DisputeRulesEngine.auto_win_scenarios(dispute), "Reason code 00 should trigger auto-win"
    
    print("✓ Rules engine auto-win detection test passed")


def test_get_next_valid_statuses():
    """Test getting valid next statuses."""
    open_actions = DisputeEngine.get_next_valid_statuses(DisputeStatus.OPEN)
    assert DisputeStatus.ASSIGNED in open_actions, "ASSIGNED should be valid from OPEN"
    assert DisputeStatus.UNDER_REVIEW in open_actions, "UNDER_REVIEW should be valid from OPEN"
    
    closed_actions = DisputeEngine.get_next_valid_statuses(DisputeStatus.CLOSED)
    assert len(closed_actions) == 0, "CLOSED status should have no valid next statuses"
    
    print("✓ Valid status retrieval test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Running Dispute Engine Tests")
    print("=" * 60 + "\n")
    
    test_sla_calculation()
    test_valid_transitions()
    test_sla_breach_detection()
    test_sla_approaching_warning()
    test_rules_engine_auto_win()
    test_get_next_valid_statuses()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()
