#!/usr/bin/env python
"""
Seed sample data for testing.
Run: python scripts/seed_data.py
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.models.dispute import Dispute, DisputeType, DisputeStatus
from app.core.engine import DisputeEngine

print("Seeding sample dispute data")
print("=" * 50)
print()

disputes = []

# Create sample disputes
for i in range(5):
    dispute_type = list(DisputeType)[i % len(DisputeType)]
    filed_date = datetime.utcnow() - timedelta(days=i)
    sla_deadline = DisputeEngine.calculate_sla_deadline(dispute_type, filed_date)
    
    dispute = Dispute(
        id=f"DSP-{1000 + i}",
        card_last_four=f"{1234 + i}",
        amount_cents=(i + 1) * 5000,
        currency="USD",
        dispute_type=dispute_type,
        status=DisputeStatus.OPEN if i % 2 == 0 else DisputeStatus.AWAITING_EVIDENCE,
        merchant_id=f"MCH-{100 + i}",
        transaction_id=f"TXN-{5000 + i}",
        transaction_date=filed_date,
        dispute_filed_date=filed_date,
        reason_code=f"{i:02d}",
        description=f"Sample dispute #{i+1}",
        sla_deadline=sla_deadline,
    )
    disputes.append(dispute)

print(f"Created {len(disputes)} sample disputes:\n")
for dispute in disputes:
    print(f"  ID: {dispute.id}")
    print(f"    Status: {dispute.status.value}")
    print(f"    Type: {dispute.dispute_type.value}")
    print(f"    Amount: ${dispute.amount_cents / 100:.2f}")
    print(f"    SLA: {dispute.sla_deadline.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"    SLA Breached: {DisputeEngine.is_sla_breached(dispute)}")
    print()

# Export sample data
output_file = Path(__file__).parent.parent / "sample_disputes.json"
disputes_json = [json.loads(d.model_dump_json()) for d in disputes]

with open(output_file, "w") as f:
    json.dump(disputes_json, f, indent=2, default=str)

print(f"Sample data exported to: {output_file}")
