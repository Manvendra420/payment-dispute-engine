# Payment Dispute Engine - Implementation Guide

## Overview

This document provides detailed information about the implementation of the Payment Dispute Engine, explaining the architecture, design decisions, and code organization.

---

## Architecture Overview

### System Design
The Payment Dispute Engine is built on an **event-driven, long-running workflow** architecture. It manages the complete lifecycle of payment disputes from creation to resolution.

**Core Principles:**
- State machine-based workflow for guaranteed valid transitions
- Rule-based decision engine for automated dispute resolution
- SLA enforcement with automatic deadline tracking
- Audit-safe event logging for compliance
- API-first design for system integration

---

## Component Breakdown

### 1. Data Models (`backend/app/models/`)

#### **dispute.py** - Core Dispute Domain

**What was built:**
- `DisputeType` Enum: Categorizes disputes into 4 types
  - CHARGEBACK: Customer disputes a transaction
  - RETRIEVAL_REQUEST: Initial customer inquiry
  - REPRESENTMENT: Response to chargeback
  - PRE_ARBITRATION: Arbitration-level dispute

- `DisputeStatus` Enum: 10-state lifecycle
  - Progression: OPEN → UNDER_REVIEW → ASSIGNED → AWAITING_EVIDENCE → EVIDENCE_SUBMITTED → ARBITRATION → WON/LOST/SETTLED → CLOSED
  - Each status represents a stage in dispute resolution

- `Dispute` Model: Main domain object
  - Tracks transaction details, merchant info, amounts
  - Stores case metadata and SLA deadlines
  - Maintains evidence collection
  - Records state change timestamps

- `Evidence` Model: Supporting documentation tracking
  - Links evidence to disputes
  - Tracks file metadata and timestamps
  - Categorizes evidence types (invoice, receipt, contract, etc.)

**Design Rationale:**
- Pydantic models ensure type safety and automatic validation
- Enum-based statuses prevent invalid state combinations
- Immutable transaction data preserves integrity
- Evidence as separate model allows flexible attachment

#### **event.py** - Audit Logging

**What was built:**
- `EventType` Enum: 8 audit event categories
  - DISPUTE_CREATED: Initial dispute entry
  - STATUS_CHANGED: Workflow transitions
  - EVIDENCE_UPLOADED: Document submission
  - SLA_APPROACHING/SLA_BREACHED: Deadline events
  - etc.

- `DisputeEvent` Model: Compliance-safe audit trail
  - Captures actor (user/system/API)
  - Records timestamp and details
  - Stores IP address for security

**Design Rationale:**
- Immutable event log for regulatory compliance
- Separation of events from disputes enables independent queries
- Actor tracking supports role-based responsibility

#### **schemas.py** - Request/Response Validation

**What was built:**
- Input validation schemas (CreateDisputeRequest, UploadEvidenceRequest)
- Output schemas with automatic serialization
- Metrics models for analytics responses

**Design Rationale:**
- Pydantic validators catch invalid data at API boundary
- Separate schemas enable API versioning
- Type hints improve IDE support

---

### 2. Business Logic (`backend/app/core/`)

#### **engine.py** - Dispute Workflow & Rules Engine

**DisputeEngine Class - Workflow Management:**

What was built:
- `SLA_CONFIG` Dict: Predefined SLA hours per dispute type
  - CHARGEBACK: 45 hours
  - RETRIEVAL_REQUEST: 30 hours
  - REPRESENTMENT: 60 hours
  - PRE_ARBITRATION: 120 hours

- `VALID_TRANSITIONS` Dict: State machine definition
  - Each status maps to permissible next statuses
  - Prevents invalid workflow paths (e.g., OPEN → CLOSED)
  - Enforces business rules through structure

- **calculate_sla_deadline()**: Computes SLA expiration
  - Uses dispute type to determine hours
  - Adds buffer time automatically
  - Returns future deadline datetime

- **can_transition()**: Validates state changes
  - Prevents invalid workflow states
  - Called before updating dispute status
  - Ensures business rule compliance

- **is_sla_breached()**: Deadline monitoring
  - Checks if current time exceeds SLA deadline
  - Used for escalation alerts
  - Triggers breach workflows

- **is_sla_approaching()**: Warning system
  - Detects disputes within 24-hour window
  - Enables proactive notifications
  - Customizable warning window

**DisputeRulesEngine Class - Automated Decision Making:**

What was built:
- **auto_win_scenarios()**: Auto-approval logic
  - Checks reason codes (00, 01, 02)
  - Returns true for auto-win candidates
  - Eliminates manual review overhead

- **auto_lose_scenarios()**: Auto-rejection logic
  - Detects missing critical evidence
  - Prevents pursing unwinnable cases
  - Saves resources on hopeless disputes

- **recommend_action()**: Decision support
  - Suggests next action based on state
  - Supports manual reviewer decision-making
  - Returns: AUTO_WIN, AUTO_LOSE, REQUEST_EVIDENCE_SUBMISSION, or None

**Design Rationale:**
- State machine pattern prevents invalid transitions
- SLA calculation centralized for consistency
- Rules engine separable for easy rule updates
- Decision recommendations support human-in-loop workflow

#### **config.py** - Configuration Management

**What was built:**
- `Settings` class using pydantic-settings
- Environment-based configuration
- Defaults for local development
- Support for Azure cloud services

**Design Rationale:**
- Centralized config reduces bugs
- Environment-based supports CI/CD pipelines
- Clear defaults unblock development

#### **logging.py** - Request/Response Logging & Error Handling

**What was built:**
- **LoggingMiddleware**: Tracks all requests/responses
  - Logs method, path, status code
  - Includes request-ID for tracing
  - Captures error details

- **ErrorHandlingMiddleware**: Centralized error handling
  - Catches ValueError for validation errors (422 status)
  - Catches Exception for server errors (500 status)
  - Returns consistent error JSON format

- **get_logger()**: Logger factory
  - Creates named loggers for modules
  - Enables filtering by component

**Design Rationale:**
- Middleware-based logging captures all requests automatically
- Request IDs enable request tracing through logs
- Centralized error handling prevents response inconsistencies

#### **database.py** - Database Abstraction

**What was built:**
- **DatabaseSession** mock class
  - Placeholder for SQLAlchemy sessions
  - Methods: save(), delete(), commit(), rollback()
  - Enables dependency injection

- **get_db()** dependency
  - FastAPI dependency for session injection
  - Ensures cleanup even on errors
  - Ready for PostgreSQL integration

**Design Rationale:**
- Mock enables development without database
- Abstraction layer eases future DB migration
- Dependency injection pattern enables testing

---

### 3. API Endpoints (`backend/app/api/`)

#### **routes.py** - Dispute Management API

**What was built:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/disputes` | POST | Create new dispute with auto-calculated SLA |
| `/api/v1/disputes` | GET | List disputes with filtering (status, merchant_id) |
| `/api/v1/disputes/{id}` | GET | Retrieve dispute details with recommendations |
| `/api/v1/disputes/{id}` | PATCH | Update status (with transition validation) |
| `/api/v1/disputes/{id}/evidence` | POST | Upload supporting documentation |
| `/api/v1/disputes/{id}/valid-transitions` | GET | Show allowed next statuses |
| `/api/v1/disputes/{id}/sla-status` | GET | Check deadline and breach status |

**Request/Response Handling:**
- Request validation via Pydantic schemas
- HTTP exception handling for invalid requests
- Consistent JSON response format
- HTTP status codes follow REST conventions

**In-Memory Storage (Development):**
- `disputes_db` dict: Stores dispute objects by ID
- `dispute_counter`: Generates sequential IDs (DSP-1000, DSP-1001, etc.)
- Ready for database swap without code changes

**Design Rationale:**
- Comprehensive CRUD + workflow operations
- Validation at API boundary prevents invalid data
- In-memory allows development without database
- Clear separation of concerns per endpoint

#### **metrics.py** - Analytics & Business Intelligence

**What was built:**

**Dashboard Metrics** (`GET /api/v1/metrics/dashboard`):
- Overall summary (total, open, won, lost disputes)
- Status breakdown across all workflows
- Performance metrics (win rate, avg resolution time, SLA compliance)
- Top merchants with win rates

**Type-Based Metrics** (`GET /api/v1/metrics/by-type`):
- Metrics for each dispute type separately
- Type-specific win rates and resolution times
- Type comparison for process improvement

**SLA Metrics** (`GET /api/v1/metrics/sla-status`):
- Compliance percentage
- Breached dispute list with hours overdue
- Approaching-deadline alerts with hours remaining

**Auto-Decision Metrics** (`GET /api/v1/metrics/auto-decisions`):
- Count of auto-decided disputes
- Auto-win vs auto-lose breakdown
- Recent auto-decisions with reasoning

**Design Rationale:**
- Multiple metric views for different use cases
- Answers key business questions
- Supports dashboards and reporting
- Mock data ready for database integration

---

### 4. Scripts (`scripts/`)

#### **init_db.py** - Database Initialization

**What was built:**
- Guides user through database setup steps
- Lists prerequisites (PostgreSQL, DATABASE_URL env var)
- Ready for Alembic migrations integration

#### **seed_data.py** - Sample Data Generation

**What was built:**
- Generates 5 sample disputes with realistic data
  - Different dispute types
  - Various statuses
  - Realistic amounts and dates
  - SLA deadline calculation

- Exports disputes to `sample_disputes.json`
- Useful for testing without manual creation

#### **test_engine.py** - Engine Unit Tests

**What was built:**

| Test | Validates |
|------|-----------|
| `test_sla_calculation()` | Each dispute type calculates correct SLA hours |
| `test_valid_transitions()` | State machine enforces valid transitions |
| `test_sla_breach_detection()` | Correctly identifies breached vs valid SLAs |
| `test_sla_approaching_warning()` | 24-hour warning threshold works |
| `test_rules_engine_auto_win()` | Auto-win rules trigger correctly |
| `test_get_next_valid_statuses()` | Valid transition lookup accurate |

**Design Rationale:**
- Comprehensive coverage of core business logic
- Runnable without database
- Documents expected behavior
- Detects regressions

---

### 5. Testing Infrastructure (`backend/tests/`)

#### **test_engine.py** - Comprehensive Test Suite

**What was built:**
- 6 independent test functions
- Each tests specific engine behavior
- Clear assertions with helpful error messages
- All tests runnable without database

**Test Coverage:**
- SLA calculations across all dispute types
- State machine transition validation
- Deadline monitoring and warnings
- Rules engine decision logic

**Design Rationale:**
- Tests document expected behavior
- Enable confident refactoring
- Catch breaking changes early

---

### 6. Configuration & Deployment

#### **requirements.txt** - Python Dependencies

**What was built:**
- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- SQLAlchemy: ORM (for future DB)
- Azure libraries: Cloud integration
- Testing tools: pytest, httpx

#### **docker-compose.yml** - Local Development Environment

**What was built:**
- FastAPI service container
  - Mounts code for live reload
  - Exposes port 8000
  - Configured with dev environment
  
- Comments for PostgreSQL/Redis (ready to uncomment)
- Custom network for service communication

**Design Rationale:**
- Single command startup: `docker-compose up`
- Live reload for development
- Ready for database addition

#### **Dockerfile** - Container Image

**What was built:**
- Python 3.11 slim base image
- System dependencies installation
- Python requirements
- Exposed port 8000
- Uvicorn startup command

**Design Rationale:**
- Slim base reduces image size
- All dependencies baked in
- Clear entrypoint

#### **.env.example** - Configuration Template

**What was built:**
- All available configuration options
- Reasonable defaults
- Comments explaining each setting
- Copy-to-.env pattern

#### **.gitignore** - Version Control

**What was built:**
- Python artifacts (\_\_pycache\_\_, .egg-info)
- Virtual environments
- IDE files (.vscode, .idea)
- Environment files (.env)
- Database files
- Logs and coverage reports

---

## Workflow Examples

### Creating a Dispute
1. API receives POST with dispute data
2. Pydantic validates input
3. System calculates SLA deadline based on type
4. Dispute created with OPEN status
5. Event logged for audit trail
6. Response includes dispute ID

### Processing Evidence
1. Evidence uploaded to endpoint
2. Linked to dispute ID
3. File metadata captured
4. EVIDENCE_UPLOADED event created
5. Event recorded in audit log

### Status Transition
1. User requests status change
2. Engine validates transition is allowed
3. If invalid, 400 error with valid options
4. If valid, status updated with timestamp
5. STATE_CHANGED event logged
6. SLA monitoring continues

---

## Design Patterns Used

### 1. **State Machine Pattern** (`DisputeEngine.VALID_TRANSITIONS`)
- Enforces valid workflows
- Prevents invalid state combinations
- Centralizes business rules

### 2. **Strategy Pattern** (`DisputeRulesEngine`)
- Different decision strategies
- Easily add new rules
- Single responsibility

### 3. **Middleware Pattern** (Logging, Error Handling)
- Centralized cross-cutting concerns
- Automatic behavior for all requests
- Decorative enhancement

### 4. **Dependency Injection** (`get_db()`)
- Decouples components
- Enables testing with mocks
- FastAPI built-in support

### 5. **Repository Pattern** (`database.py`)
- Abstracts data persistence
- Can swap implementations
- Enables testing

---

## Code Organization Principles

1. **Separation of Concerns**
   - Models: Data structure & validation
   - Core: Business logic & rules
   - API: HTTP interface & routing
   - Scripts: Utilities & admin tasks

2. **Testability**
   - Business logic decoupled from FastAPI
   - Mock database enables testing
   - Pure functions where possible

3. **Extensibility**
   - Rules engine easily expands
   - New metrics endpoints added without core changes
   - API versioning support (`/api/v1/`)

4. **Maintainability**
   - Type hints throughout
   - Clear naming conventions
   - Docstrings on complex logic
   - Centralized configuration

---

## Future Enhancements

### Phase 2: Database Integration
- Replace in-memory storage with PostgreSQL
- Alembic migrations for schema versioning
- Transaction management

### Phase 3: Event Queue
- Azure Service Bus integration
- Async task processing
- Cross-system workflows

### Phase 4: Frontend
- Next.js React application
- Dashboard for dispute management
- Evidence portal

### Phase 5: Advanced Features
- Machine learning for predictions
- Batch processing for bulk operations
- Advanced analytics & reporting
- External API integrations

---

## Quick Reference

### Running Tests
```bash
python backend/tests/test_engine.py
```

### Generating Sample Data
```bash
python scripts/seed_data.py
```

### Starting Development Server
```bash
uvicorn backend.main:app --reload
```

### API Documentation
http://localhost:8000/docs

---

## Key Decisions & Trade-offs

| Decision | Rationale |
|----------|-----------|
| In-memory storage initially | Fast development, no DB setup needed |
| State machine pattern | Guarantees valid workflows |
| Pydantic for validation | Type safety + automatic docs |
| FastAPI framework | Async support, OpenAPI docs |
| Scripts before database | Demonstrate logic independently |
| Centralized logging | Trace requests across system |

---

This implementation provides a solid foundation with clear separation of concerns, comprehensive validation, and business logic that's well-tested and documented.
