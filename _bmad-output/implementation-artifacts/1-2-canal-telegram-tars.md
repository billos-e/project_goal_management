# Story 1.2: Canal Telegram & Echo Persona (TARS)

**Status:** ready-for-dev  
**Story ID:** 1.2  
**Story Key:** 1-2-canal-telegram-tars  
**Created:** 2026-02-06

---

## Story Foundation

### User Story
As a user,  
I want to interact with TARS through Telegram and receive a response in his specific tone,  
So that I can validate the communication channel and the persona consistency.

### Acceptance Criteria

**Given** a Telegram Bot Token and a Webhook configured  
**When** I send a message to the bot  
**Then** TARS must respond with a message in his humorous/analytical tone  
**And** the request must be validated using the Secret Token (ADR-002).

### Business Context

This story validates the first user-facing interaction channel. It proves that the Telegram webhook is secure, that cold-start UX is acceptable, and that the TARS persona can respond consistently.

---

## Developer Context Section

### 🏗️ Architecture Overview for This Story

**Story 1.2 focuses on:**
1. Secure Telegram webhook validation (ADR-002)
2. Handling incoming messages and sending a TARS-styled response
3. Cold-start UX: send typing indicator within 2 seconds (ADR-006)
4. Basic user identification via Telegram ID

**System Architecture Context:**
```
Telegram Bot API
        ↓
    [Webhook]
        ↓
Render (Python/FastAPI)
        ↓
Supabase (PostgreSQL)
```

**Key Architectural Decisions Affecting This Story:**
- **ADR-002: Authentication** - Telegram ID + Header Secret Token
- **ADR-006: Cold-Start UX** - typing indicator within 2s
- **ADR-001: Mono-user Private Instance** - no multi-tenant complexity

---

## Technical Requirements

### Core Deliverables

#### 1. Telegram Webhook Security (ADR-002)
- Validate `X-Telegram-Bot-Api-Secret-Token` header
- Reject requests with missing/invalid secret (HTTP 401)
- Log validation failures with structured logs

#### 2. TARS Persona Response
- Respond to user messages with a basic static TARS-style template
- Keep tone: humorous / analytical
- No NLU in this story (NLU begins in Story 1.3)

#### 3. Cold-Start UX
- Send typing indicator within 2 seconds of webhook call
- If the message processing exceeds 2 seconds, still send typing indicator first

#### 4. Minimal User Tracking
- Extract `telegram_id` from incoming message
- Store or update the `users` table (if exists)
- Do not implement full CRUD (Epic 2)

---

## API Endpoints

### POST `/telegram/webhook/{bot_token}`
- Validate secret header
- Parse incoming Telegram update
- Send typing indicator
- Send a basic TARS response
- Return 200 OK

---

## Testing Requirements

### Unit Tests
- Valid secret token returns 200 OK
- Missing/invalid secret returns 401
- TARS response is sent for a valid message
- Typing indicator is triggered

---

## Dependencies

### Environment Variables
```
TELEGRAM_BOT_TOKEN=[bot token]
TELEGRAM_WEBHOOK_SECRET=[secret token]
TELEGRAM_WEBHOOK_URL=[webhook url]
```

---

## Notes

- Story 1.2 focuses on communication channel validation only.
- NLU pipeline and intent detection will be implemented in Story 1.3.
