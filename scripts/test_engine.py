#!/usr/bin/env python
"""
Test the dispute engine rules and transitions.
Run: python scripts/test_engine.py
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.models.dispute import Dispute, DisputeType, DisputeStatus
from app.core.engine import DisputeEngine, DisputeRulesEngine

print("Testing Dispute Engine")
print("=" * 60)
print()

# Test 1: SLA Calculation
print("Test 1: SLA Deadline Calculation")
print("-" * 60)
now = datetime.utcnow()
for dispute_type in DisputeType:
    deadline = DisputeEngine.calculate_sla_deadline(dispute_type, now)
    hours_diff = (deadline - now).total_seconds() / 3600
    print(f"  {dispute_type.value.upper():20} -> {hours_diff:6.0f} hours SLA")
print()

# Test 2: Valid Transitions
print("Test 2: Valid Status Transitions")
print("-" * 60)
test_transitions = [
    (DisputeStatus.OPEN, DisputeStatus.ASSIGNED, True),
    (DisputeStatus.OPEN, DisputeStatus.CLOSED, False),
    (DisputeStatus.ASSIGNED, DisputeStatus.AWAITING_EVIDENCE, True),
    (DisputeStatus.CLOSED, DisputeStatus.OPEN, False),
]

for current, target, expected in test_transitions:
    result = DisputeEngine.can_transition(current, target)
    status = "✓" if result == expected else "✗"
    print(f"  {status} {current.value} → {target.value}: {result}")
print()

# Test 3: Rules Engine
print("Test 3: Rules Engine - Auto-Win Detection")
print("-" * 60)

# Create test dispute
dispute = Dispute(
    id="DSP-TEST-001",
    card_last_four="1234",
    amount_cents=10000,
    currency="USD",
    dispute_type=DisputeType.CHARGEBACK,
    status=DisputeStatus.OPEN,
    merchant_id="MCH-TEST",
    transaction_id="TXN-TEST",
    transaction_date=datetime.utcnow(),
    dispute_filed_date=datetime.utcnow(),
    reason_code="00",  # Auto-win code
    sla_deadline=datetime.utcnow() + timedelta(hours=48),
)

auto_win = DisputeRulesEngine.auto_win_scenarios(dispute)
auto_lose = DisputeRulesEngine.auto_lose_scenarios(dispute)
recommendation = DisputeRulesEngine.recommend_action(dispute)

print(f"  Dispute: {dispute.id}")
print(f"  Reason Code: {dispute.reason_code}")
print(f"  Auto-Win: {auto_win}")
print(f"  Auto-Lose: {auto_lose}")
print(f"  Recommendation: {recommendation or 'None'}")
print()

# Test 4: SLA Warnings
print("Test 4: SLA Approaching Detection")
print("-" * 60)
upcoming_deadline = datetime.utcnow() + timedelta(hours=20)
approaching_dispute = Dispute(
    id="DSP-APPROACHING",
    card_last_four="5678",
    amount_cents=15000,
    currency="USD",
    dispute_type=DisputeType.RETRIEVAL_REQUEST,
    status=DisputeStatus.AWAITING_EVIDENCE,
    merchant_id="MCH-TEST",
    transaction_id="TXN-TEST",
    transaction_date=datetime.utcnow(),
    dispute_filed_date=datetime.utcnow(),
    reason_code="05",
    sla_deadline=upcoming_deadline,
)

approaching = DisputeEngine.is_sla_approaching(approaching_dispute)
breached = DisputeEngine.is_sla_breached(approaching_dispute)
hours_left = (approaching_dispute.sla_deadline - datetime.utcnow()).total_seconds() / 3600

print(f"  Dispute: {approaching_dispute.id}")
print(f"  Hours until SLA: {hours_left:.1f}")
print(f"  SLA Approaching (within 24h): {approaching}")
print(f"  SLA Breached: {breached}")
print()

print("All tests completed!")
