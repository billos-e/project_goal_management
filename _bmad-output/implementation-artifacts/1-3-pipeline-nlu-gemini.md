# Story 1.3: Pipeline NLU Gemini & Cascade de Résilience

**Status:** ready-for-dev  
**Story ID:** 1.3  
**Story Key:** 1-3-pipeline-nlu-gemini  
**Created:** 2026-02-06

---

## Story Foundation

### User Story
As a developer,  
I want to implement the NLU cascade with Gemini and local fallback templates,  
So that the system always responds even if the AI is slow or unavailable (NFR2/NFR4).

### Acceptance Criteria

**Given** an incoming user message  
**When** the Gemini API is called  
**Then** it must return an identified intention within 3 seconds  
**And** if it fails or times out, a TARS template response must be used (ADR-004).

### Business Context

This story ensures NFR2 (robustness) and NFR4 (latency) by implementing a resilient NLU cascade. It is the foundation for reliable conversational behavior.

---

## Developer Context Section

### 🏗️ Architecture Overview for This Story

**Story 1.3 focuses on:**
1. Gemini API integration for NLU intent detection
2. Timeout handling (3 seconds)
3. Fallback response templates (TARS tone)
4. Centralized NLU service layer

**Key Architectural Decisions Affecting This Story:**
- **ADR-004: NLU Cascade** - Gemini first, fallback templates on failure
- **NFR2: Robustness** - 100% response guarantee
- **NFR4: Latency** - ≤5s response (P95)

---

## Technical Requirements

### Core Deliverables

#### 1. Gemini API Integration
- Call Gemini (1.5-Flash) for intent detection
- Parse and normalize intent output

#### 2. Timeout Management
- Enforce 3-second timeout for Gemini call
- If timeout or error, use fallback templates

#### 3. Fallback Templates
- Provide 3–5 TARS-styled fallback responses
- Ensure always-on response behavior

#### 4. NLU Service Layer
- `app/services/nlu.py` service with `identify_intent()`
- Returns normalized intent or fallback template

---

## Testing Requirements

### Unit Tests
- Gemini call success returns intent
- Timeout triggers fallback response
- Errors trigger fallback response

---

## Dependencies

### Environment Variables
```
GEMINI_API_KEY=[gemini key]
GEMINI_MODEL=gemini-1.5-flash
```

---

## Notes

- Focus on resilience, not accuracy tuning.
- Intent taxonomy will be refined in later stories.
