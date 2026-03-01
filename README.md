# Payment Dispute Engine

A comprehensive workflow-driven system to manage card payment disputes, chargebacks, evidence submission, arbitration, and analytics.

## 🚀 Quick Start

### Option 1: Run Locally (Recommended for Development)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload
```

API Documentation: http://localhost:8000/docs

### Option 2: Run with Docker

```bash
docker-compose up
```

## 📋 Core Features

- ✅ **Dispute Lifecycle Engine** - State machine with validated transitions
- ✅ **SLA & Deadline Enforcement** - Automatic SLA calculation and breach detection
- ✅ **Evidence Management** - Upload and track supporting documentation
- ✅ **Rules-Based Decision Engine** - Auto-resolution based on configurable rules
- ✅ **Audit-Safe Event Log** - Full history of all changes
- ✅ **API-First Design** - RESTful endpoints with OpenAPI docs

## 🏗️ Architecture

Event-driven, long-running workflows with:
- FastAPI backend (REST API)
- In-memory storage (migration to PostgreSQL ready)
- Dispute workflow engine
- Rules engine for automated decisions
- SLA management system

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **API Docs**: OpenAPI (Swagger UI)
- **Storage**: PostgreSQL (ready, not required to start)
- **Task Queue**: Azure Service Bus (optional)
- **Cloud Storage**: Azure Blob Storage (optional)
- **Frontend**: Next.js (planned)
- **Containerization**: Docker & Docker Compose

## 📚 Scripts

```bash
# Test the engine logic
python scripts/test_engine.py

# Generate sample data
python scripts/seed_data.py

# Prepare database (when PostgreSQL is added)
python scripts/init_db.py
```

## 🎯 Next Steps

- [ ] Integrate PostgreSQL database
- [ ] Add event queue (Azure Service Bus)
- [ ] Implement document storage (Azure Blob)
- [ ] Build React/Next.js frontend
- [ ] Add authentication & authorization
- [ ] Implement batch processing
- [ ] Add analytics & reporting
