# Story 1.4: Diagnostic Système (/self_test)

**Status:** ready-for-dev  
**Story ID:** 1.4  
**Story Key:** 1-4-diagnostic-self-test  
**Created:** 2026-02-06

---

## Story Foundation

### User Story
As a user,  
I want to run a diagnostic command,  
So that I can verify that all components (DB, AI, Webhooks) are working correctly.

### Acceptance Criteria

**Given** TARS is active  
**When** I send the command /self_test  
**Then** TARS must perform a check of the Supabase connection and Gemini API  
**And** return a status report (FR8).

### Business Context

This story provides operational visibility and quick diagnostics for system health, allowing the user to validate core infrastructure.

---

## Developer Context Section

### 🏗️ Architecture Overview for This Story

**Story 1.4 focuses on:**
1. Command routing for /self_test
2. Supabase connectivity check
3. Gemini API connectivity check
4. Consolidated status response

**Key Architectural Decisions Affecting This Story:**
- **FR8: /self_test** - immediate diagnostic command
- **ADR-004: NLU Cascade** - ensure AI component is reachable

---

## Technical Requirements

### Core Deliverables

#### 1. Command Handling
- Recognize `/self_test` command in Telegram updates
- Bypass NLU for this command

#### 2. Health Checks
- Validate Supabase connectivity (simple query)
- Validate Gemini connectivity (lightweight request)

#### 3. Status Report
- Return a structured message with component status
- Format for readability in Telegram

---

## Testing Requirements

### Unit Tests
- `/self_test` returns status when all components are healthy
- Failure in DB returns degraded status
- Failure in AI returns degraded status

---

## Notes

- This story depends on Story 1.2 and 1.3.
- Keep responses concise and user-friendly.
