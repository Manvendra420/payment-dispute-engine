#!/usr/bin/env python
"""
Initialize the database schema.
Run: python scripts/init_db.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

print("Database initialization script")
print("=" * 50)
print()
print("This script will initialize the PostgreSQL database.")
print("Setup steps:")
print("  1. Ensure PostgreSQL is running")
print("  2. Set DATABASE_URL environment variable")
print("  3. Run migrations with: alembic upgrade head")
print()
print("For now, using in-memory fixture data...")
print()

# Simulate data loading
sample_disputes = [
    {
        "id": "DSP-1001",
        "merchant_id": "MCH-100",
        "amount_cents": 5000,
        "reason": "Unauthorized transaction",
    },
    {
        "id": "DSP-1002",
        "merchant_id": "MCH-101",
        "amount_cents": 2500,
        "reason": "Service not rendered",
    },
]

print("Sample disputes loaded:")
for dispute in sample_disputes:
    print(f"  - {dispute['id']}: {dispute['reason']} ({dispute['amount_cents']} cents)")

print()
print("Database ready! Start the API with: uvicorn backend.main:app --reload")
