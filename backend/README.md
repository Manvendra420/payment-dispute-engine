# Payment Dispute Engine - Backend

This is the FastAPI backend service for the Payment Dispute Engine.

## Quick Start

### Without Docker

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

   API will be available at `http://localhost:8000`
   Docs at `http://localhost:8000/docs`

### With Docker

```bash
docker-compose up -d
```

## Scripts

### Initialize Database
```bash
python scripts/init_db.py
```

### Seed Sample Data
```bash
python scripts/seed_data.py
```

### Run Engine Tests
```bash
python scripts/test_engine.py
```

## API Endpoints

### Disputes
- `POST /api/v1/disputes` - Create new dispute
- `GET /api/v1/disputes` - List disputes (with filtering)
- `GET /api/v1/disputes/{dispute_id}` - Get specific dispute
- `PATCH /api/v1/disputes/{dispute_id}` - Update dispute
- `POST /api/v1/disputes/{dispute_id}/evidence` - Upload evidence
- `GET /api/v1/disputes/{dispute_id}/valid-transitions` - Get valid status transitions
- `GET /api/v1/disputes/{dispute_id}/sla-status` - Get SLA status

### System
- `GET /health` - Health check
- `GET /` - API info

## Data Models

### Dispute Types
- CHARGEBACK
- RETRIEVAL_REQUEST
- REPRESENTMENT
- PRE_ARBITRATION

### Dispute Status
- OPEN
- UNDER_REVIEW
- ASSIGNED
- AWAITING_EVIDENCE
- EVIDENCE_SUBMITTED
- ARBITRATION
- WON
- LOST
- SETTLED
- CLOSED

## Features

- **Workflow Engine**: Validates status transitions and SLA enforcement
- **Rules Engine**: Auto-resolution based on configurable rules
- **SLA Management**: Automatic SLA calculation and breach detection
- **Evidence Management**: Upload and track evidence
- **Event Auditing**: Full audit trail of all changes
- **In-Memory Storage**: Currently uses in-memory DB (will migrate to PostgreSQL)

## Environment Variables

See `.env.example` for all available configuration options.

## Testing

Engine tests are available in `scripts/test_engine.py`:
- SLA calculation
- Status transitions
- Rules engine
- SLA warnings
