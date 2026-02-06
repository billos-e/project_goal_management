# Sprint 1 Plan - Focus & Flow

**Goal:** Deliver a functional "Always-On" assistant (TARS) with a solid technical foundation, ready for feature expansion. This sprint focuses on completing Epic 1.

---

## Sprint Backlog

### Epic 1: Fondations & Cerveau TARS (L'Assistant "Always-On")

| Priority | Story ID | Title                                           | Status      |
|----------|----------|-------------------------------------------------|-------------|
| 1        | 1.1      | Initialisation de l'infrastructure & Cœur FastAPI | Not Started |
| 2        | 1.2      | Canal Telegram & Echo Persona (TARS)            | Not Started |
| 3        | 1.3      | Pipeline NLU Gemini & Cascade de Résilience     | Not Started |
| 4        | 1.4      | Diagnostic Système (/self_test)                 | Not Started |

---

### Story Details

#### Story 1.1: Initialisation de l'infrastructure & Cœur FastAPI
**As a** developer,
**I want** to set up the FastAPI project structure and connect it to Supabase and Render,
**So that** the system has a solid functional foundation.

**Acceptance Criteria:**
- **Given** a new FastAPI project based on the Production-Ready starter
- **When** I configure the environment variables and deploy to Render
- **Then** the /docs endpoint must be accessible
- **And** the connection to Supabase must be validated by a simple query.

#### Story 1.2: Canal Telegram & Echo Persona (TARS)
**As a** user,
**I want** to interact with TARS through Telegram and receive a response in his specific tone,
**So that** I can validate the communication channel and the persona consistency.

**Acceptance Criteria:**
- **Given** a Telegram Bot Token and a Webhook configured
- **When** I send a message to the bot
- **Then** TARS must respond with a message in his humorous/analytical tone
- **And** the request must be validated using the Secret Token (ADR-002).

#### Story 1.3: Pipeline NLU Gemini & Cascade de Résilience
**As a** developer,
**I want** to implement the NLU cascade with Gemini and local fallback templates,
**So that** the system always responds even if the AI is slow or unavailable (NFR2/NFR4).

**Acceptance Criteria:**
- **Given** an incoming user message
- **When** the Gemini API is called
- **Then** it must return an identified intention within 3 seconds
- **And** if it fails or times out, a TARS template response must be used (ADR-004).

#### Story 1.4: Diagnostic Système (/self_test)
**As a** user,
**I want** to run a diagnostic command,
**So that** I can verify that all components (DB, AI, Webhooks) are working correctly.

**Acceptance Criteria:**
- **Given** TARS is active
- **When** I send the command /self_test
- **Then** TARS must perform a check of the Supabase connection and Gemini API
- **And** return a status report (FR8).
