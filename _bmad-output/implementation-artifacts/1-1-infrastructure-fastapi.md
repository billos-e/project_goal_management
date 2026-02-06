# Story 1.1: Initialisation de l'infrastructure & Cœur FastAPI

**Status:** ready-for-dev  
**Story ID:** 1.1  
**Story Key:** 1-1-infrastructure-fastapi  
**Created:** 2026-02-05

---

## Story Foundation

### User Story
As a developer,  
I want to set up the FastAPI project structure and connect it to Supabase and Render,  
So that the system has a solid functional foundation.

### Acceptance Criteria

**Given** a new FastAPI project based on the Production-Ready starter  
**When** I configure the environment variables and deploy to Render  
**Then** the `/health` or `/docs` endpoint must be accessible  
**And** the connection to Supabase must be validated by a simple query  
**And** the project is deployed successfully on Render Free Tier  
**And** cold start feedback UX is in place (typing indicator within 2s of webhook call)

### Business Context

This is the **foundational story for Epic 1: Fondations & Cerveau TARS** - the "Always-On" assistant infrastructure layer.

**Why This Story Matters:**
- Establishes the technical foundation for all subsequent stories (1.2, 1.3, 1.4)
- Sets up the communication bridge between Telegram and the backend
- Validates infrastructure readiness for NFR1 (Zero Cost) and NFR4 (Latency) constraints
- Enables the team to understand cold-start behavior and UX implications before feature development

**Epic 1 Objectives:**
- Mise en place de l'infrastructure (FastAPI/Render/Supabase)
- Établir le canal de communication Telegram avec le persona TARS
- Valider la cascade de résilience NLU pour 100% d'uptime

---

## Developer Context Section

### 🏗️ Architecture Overview for This Story

**Story 1.1 focuses on:**
1. FastAPI project initialization with production-ready structure
2. Supabase connection setup and basic database validation
3. Render deployment configuration (free tier with cold-start handling)
4. Telegram webhook setup (will be fully configured in Story 1.2)
5. Health check endpoint for infrastructure validation

**System Architecture Context:**
```
Telegram Bot API
        ↓
    [Webhook]
        ↓
Render (Python/FastAPI) ← Your responsibility in this story
        ↓
Supabase (PostgreSQL)
        ↓
GitHub Actions (CRON scheduling - future)
```

**Key Architectural Decisions Affecting This Story:**
- **ADR-001: Mono-user Private Instance** - No multi-tenant complexity needed
- **ADR-002: Authentication** - Telegram ID + Header Secret Token (setup skeleton in this story, full implementation in 1.2)
- **ADR-003: Relational Schema** - Strict PostgreSQL schema (NO JSONB), prepared statements for security
- **ADR-005: Timezone Handling** - All times stored in UTC, displayed in 'Europe/Paris'
- **ADR-006: Cold-Start UX** - Render free tier spins down after 15 min inactivity. Feedback needed within 2s via Telegram typing indicator.

---

## Technical Requirements

### Core Deliverables

#### 1. FastAPI Project Structure
**Standard production-ready structure to implement:**

```
project_goal_management/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration & environment variables
│   ├── models/
│   │   ├── __init__.py
│   │   ├── domain.py           # Pydantic models for User, Habit, Objective, CheckIn
│   │   └── schemas.py          # API request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py         # Supabase connection & queries
│   │   └── telegram.py         # Telegram API utilities (skeleton)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py           # Health check endpoints
│   │   └── telegram_webhook.py # Telegram webhook endpoint (skeleton)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py           # Logging configuration
│   └── middleware/
│       ├── __init__.py
│       └── error_handler.py    # Global error handling
├── tests/
│   ├── __init__.py
│   ├── test_health.py          # Health endpoint tests
│   └── conftest.py             # Pytest fixtures
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
├── render.yaml                 # Render infrastructure config
└── README.md                   # Setup and deployment instructions
```

#### 2. Environment Variables Setup

**Required in `.env` or Render dashboard:**

```env
# Supabase
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_KEY=[anon-public-key]
SUPABASE_SERVICE_ROLE_KEY=[service-role-key]

# Telegram (skeleton - full values in Story 1.2)
TELEGRAM_BOT_TOKEN=[will-be-set-in-1.2]
TELEGRAM_WEBHOOK_SECRET=[will-be-set-in-1.2]
TELEGRAM_WEBHOOK_URL=[will-be-set-after-deployment]

# Application
APP_NAME=focus-flow
ENVIRONMENT=production
LOG_LEVEL=INFO
TIMEZONE=Europe/Paris

# Render
PYTHON_VERSION=3.11
```

#### 3. Supabase Connection & Validation

**Database connection implementation:**

```python
# app/services/database.py
# Must use: supabase-py client library
# Connection string: SUPABASE_URL + SUPABASE_KEY (anon) or SERVICE_ROLE_KEY

# Implement:
# - Connection pooling for efficiency on free tier
# - Async support where possible (or sync if simpler)
# - Prepared statements to prevent SQL injection
# - Test query: Simple SELECT to verify connectivity

# Do NOT implement:
# - ORM at this stage (keep it simple for MVP)
# - Migration tools (Alembic) - manually create schema or use Supabase UI
# - Complex query builders

# Validation approach:
# create_test_table() function that:
# 1. Attempts to query a marker table or system catalog
# 2. Returns True if successful, False if connection fails
# 3. This will be called by health endpoint
```

#### 4. Render Deployment Configuration

**Files to create:**

- **Procfile**: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **render.yaml**: Infrastructure-as-code for automatic deployment
- **Build command**: `pip install -r requirements.txt`
- **Start command**: As above (Procfile)

**Render Setup:**
- Free tier selection (750 hrs/month = always-on within limits)
- Post-deployment hook: Auto-set environment variables
- Deploy branch: main (or your feature branch for testing)

#### 5. Health Check Endpoints

**Implement two endpoints:**

**GET `/health`** - Simple liveness probe
```json
Response: {"status": "ok", "timestamp": "2026-02-05T14:30:00Z"}
```

**GET `/health/detailed`** - Full system diagnostics
```json
Response: {
  "status": "healthy|degraded|unhealthy",
  "components": {
    "api": "ok",
    "database": "ok|failed",
    "database_error": null,
    "timestamp": "2026-02-05T14:30:00Z"
  }
}
```

#### 6. Telegram Webhook Skeleton

**Setup skeleton (full implementation in Story 1.2):**

```python
# app/routes/telegram_webhook.py
# POST /telegram/webhook/{bot_token}

# At this stage:
# 1. Verify TELEGRAM_WEBHOOK_SECRET header
# 2. Accept and acknowledge the webhook (return 200 OK)
# 3. Log incoming updates (don't process yet)
# 4. This proves communication channel is working
# 5. Actual message processing happens in Story 1.3

# Do NOT:
# - Process NLU or send responses
# - Make database queries based on message content
```

#### 7. Logging & Monitoring

**Implement simple structured logging:**

```python
# app/utils/logger.py
import logging
import json
from datetime import datetime

# Use structured logging (JSON format for Render logs)
# Include: timestamp, level, message, context
# Example: {"timestamp": "...", "level": "ERROR", "component": "database", "message": "..."}
```

---

## Architecture Compliance

### Database Schema (Epic-Level Design - Don't Create Full Schema Yet)

**Story 1.1 focuses on proving connection. Use this schema for the health check query:**

```sql
-- Minimal schema for Story 1.1 validation
-- Full schema created in separate migration or DB setup script

CREATE TABLE IF NOT EXISTS _system_health (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  check_timestamp TIMESTAMPTZ DEFAULT NOW(),
  component VARCHAR(50),
  status VARCHAR(20)
);

-- This table is ONLY for health checks
-- Story 1.1 validates by: INSERT INTO _system_health(...) then SELECT
```

**Complete Database Schema Reference (for context - implement gradually):**

| Table | Purpose | Story |
|-------|---------|-------|
| `users` | User data with timezone preferences | 1.1 (setup only, actual data in 2.1) |
| `habits` | Habit definitions with frequency config | 2.1 |
| `objectives` | Goal definitions with deadlines | 2.2 |
| `checkins` | Completion records | 3.1 |
| `daily_stats` | Daily aggregated metrics | 5.1 |

**For Story 1.1:**
- Create minimal `users` table with just `telegram_id` (PK), `timezone`, `created_at`
- Do NOT populate with data (that's Story 1.2+)
- Just prove connection works

---

## Library & Framework Requirements

### Python Version & Package Manager
- **Python:** 3.11+ (Render supports up to 3.11)
- **Package Manager:** pip (standard)
- **Virtual Environment:** venv (included with Python)

### Core Dependencies

**FastAPI Stack:**
```
fastapi==0.104.1                # Web framework
uvicorn==0.24.0                 # ASGI server
pydantic==2.5.0                 # Data validation
pydantic-settings==2.1.0        # Environment variable management
python-dotenv==1.0.0            # .env file support
```

**Database:**
```
supabase==2.3.4                 # Supabase Python client
# Alternative: postgrest-py, psycopg2-binary if raw SQL preferred
# Recommendation: Use supabase client - it handles connection pooling
```

**Utilities:**
```
python-telegram-bot==20.3       # Will be used in 1.2, add now for consistency
httpx==0.25.2                   # Async HTTP client (optional, if using async)
```

**Development & Testing:**
```
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.12.0
pylint==3.0.3
```

### Dependencies File Structure

**requirements.txt** - Include:
- All dependencies listed above
- Pin exact versions for production stability
- Comment with purpose

**requirements-dev.txt** - Additional for development:
- pytest, black, pylint, etc.

**Installation in Render:**
- Render reads `requirements.txt` automatically
- Ensure pip is up to date: `pip install --upgrade pip`

---

## File Structure & Code Organization

### Path Conventions
- **All paths relative to:** `app/`
- **Naming:** snake_case for files and functions
- **Modules:** Organized by responsibility (models, services, routes)
- **No:** Relative imports across modules (use absolute: `from app.services import ...`)

### Import Patterns
```python
# Good: Absolute imports
from app.services.database import get_supabase_client
from app.config import settings

# Avoid: Relative imports
from ..services.database import ...

# Group imports: stdlib, third-party, local
import os
import json
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import settings
```

### Configuration Pattern
**Use Pydantic Settings for environment variables:**

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    telegram_bot_token: Optional[str] = None
    timezone: str = "Europe/Paris"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## Testing Requirements

### Unit Tests for Story 1.1

**test_health.py:**
```python
# Test endpoints:
# 1. GET /health returns 200 with correct structure
# 2. GET /health/detailed returns 200 with component status
# 3. Database health check correctly detects connection success/failure
# 4. Each test is independent (use fixtures)
```

**Test Framework:**
- pytest with asyncio support
- Use fixtures for test data and mocking
- Aim for >80% code coverage on critical paths (database, health checks)

### Integration Test (Manual, Document in README)
1. Deploy to Render
2. Curl `/health` endpoint
3. Verify 200 response with correct structure
4. Document Render logs output in debugging section

---

## Previous Story Intelligence

**N/A** - This is Story 1.1, the first story in Epic 1. No prior stories to learn from.

---

## Git Intelligence Summary

**This is a new repository.** 

**Code patterns to establish in this story:**
- ✅ Python 3.11+ compatibility
- ✅ Async/await patterns where beneficial (FastAPI routes)
- ✅ Type hints on all function signatures
- ✅ Structured logging with JSON format
- ✅ Pydantic for validation
- ✅ Environment-based configuration (12-factor app)

**No previous commits to analyze - establishing baseline.**

---

## Latest Technical Information

### FastAPI Best Practices (Feb 2026)
- FastAPI 0.104.1 is current stable; use it
- Uvicorn 0.24.0 supports HTTP/2 and WebSockets natively
- Pydantic v2 introduces breaking changes - ensure all code uses v2 patterns (field_validator, not validator)

### Supabase Client Library
- **Current Version:** supabase-py 2.3.4
- **Key Features:**
  - Connection pooling built-in
  - Async support via `AsyncClient` (optional for MVP)
  - Automatic JWT handling for RLS
  - Free tier includes: 500MB storage, 1GB bandwidth, 50k API calls/month
- **Gotchas:**
  - Use `SUPABASE_KEY` (anon) for client; service role key only for backend
  - RLS (Row-Level Security) policies are NOT enforced in this story (mono-user)

### Render Deployment (Feb 2026)
- **Free Tier Details:**
  - 750 hours/month (barely enough for always-on)
  - Spins down after 15 min inactivity
  - Cold start: 30-60 seconds typical
  - ✅ Supports Git-based deployment (GitHub, GitLab)
  - ✅ Automatic `Procfile` detection
  - ✅ Environment variable management via dashboard
- **Deploying Python Apps:**
  - Must have `Procfile` or `render.yaml`
  - Auto-detects Python via `requirements.txt`
  - Port binding: Read `$PORT` environment variable

### Telegram Webhook Security (Feb 2026)
- Telegram sends webhooks as HTTPS POST to your URL
- **Validation:** Check `X-Telegram-Bot-Api-Secret-Hash` header
- Formula: `HMAC-SHA256(TELEGRAM_BOT_TOKEN, request.body) == header_value`
- Story 1.2 implements full validation; Story 1.1 prepares the skeleton

---

## Project Context Reference

### Project Goals
**Focus & Flow** is a Telegram-based productivity bot with AI coaching. The system emphasizes psychological well-being through positive reinforcement (Micro-Wins), accountability (Success Days), and a humorous/analytical persona (TARS).

### Key Constraints Affecting Story 1.1
1. **NFR1 - Zero Cost:** All services on free tiers
   - ✅ Render free tier acceptable
   - ✅ Supabase free tier acceptable
   - ✅ Gemini free tier (1M tokens/month) - used in Story 1.3

2. **NFR4 - Latency:** ≤5s NLU response (P95)
   - Cold start of 30-60s is acceptable for proactive reminders
   - Must show typing indicator within 2s for reactive messages

3. **NFR2 - Robustness (100%):** System must never be unavailable
   - Fallback templates if Gemini fails (Story 1.3)
   - Health checks to monitor system state (this story)

4. **NFR5 - Precision:** Reminders ±2 min accuracy
   - GitHub Actions scheduling precision (Story 4.1)
   - Timezone conversion critical (UTC→Europe/Paris)

### Document References
- **PRD:** `_bmad-output/planning-artifacts/prd.md` (Success criteria, Requirements)
- **Architecture:** `_bmad-output/planning-artifacts/architecture.md` (Full technical decisions)
- **Epics:** `_bmad-output/planning-artifacts/epics.md` (User story definitions)
- **Implementation Readiness:** `_bmad-output/planning-artifacts/implementation-readiness-report-2026-02-05.md`

---

## Dev Agent Record

### Completion Checklist

Before marking story as "done" (after development), verify:

**Code:**
- ✅ FastAPI app initializes without errors
- ✅ All environment variables properly loaded from .env or Render dashboard
- ✅ `/health` endpoint returns 200 with correct JSON structure
- ✅ `/health/detailed` endpoint includes database connectivity check
- ✅ Supabase connection successfully queries test table
- ✅ Telegram webhook skeleton accepts POST, validates secret header
- ✅ All code passes pylint checks (score >8.0)
- ✅ Code formatted with black

**Testing:**
- ✅ pytest passes all tests in `tests/` directory
- ✅ >80% coverage on core modules (database, health, config)
- ✅ Manual curl tests documented in README

**Deployment:**
- ✅ `Procfile` correctly configured for Render
- ✅ `requirements.txt` includes all dependencies
- ✅ Deployed to Render and `/health` is accessible publicly
- ✅ Environment variables set in Render dashboard
- ✅ Logs visible in Render dashboard

**Documentation:**
- ✅ README.md includes setup instructions
- ✅ .env.example shows all required variables
- ✅ Comments explain non-obvious code sections
- ✅ Git commits have clear messages

### Debug Log References

When developing, capture:
1. Render build logs (check for dependency errors)
2. Render runtime logs (check for startup errors)
3. pytest output (all tests passing)
4. curl responses from deployed endpoint

### Next Story Dependencies

**Story 1.2 (Telegram Webhook & TARS Persona)** depends on:
- ✅ FastAPI infrastructure working
- ✅ Supabase connected
- ✅ Render deployment functional
- ✅ Webhook skeleton in place (receives requests, validates header)

**Story 1.3 (NLU Pipeline)** depends on:
- ✅ Telegram webhook fully processing messages (from 1.2)
- ✅ TARS persona consistent in responses

---

## Story Completion Status

**Current Status:** ready-for-dev

This story is ready for the developer agent to implement. All context, constraints, and technical requirements have been thoroughly analyzed. The developer should:

1. Set up the FastAPI project structure as described
2. Configure Supabase connection with proper error handling
3. Deploy to Render and validate `/health` endpoint
4. Document setup process in README
5. Create minimal tests for health checks
6. Mark story as "done" in sprint-status.yaml when development is complete

---

**End of Story 1.1 Context Document**

*Generated by BMAD Ultimate Context Engine - Comprehensive Developer Guide*  
*Story created: 2026-02-05 by /bmad-bmm-create-story workflow*
