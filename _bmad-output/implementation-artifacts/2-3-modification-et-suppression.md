# Story 2.3: Modification et Suppression

**Status:** ready-for-dev  
**Story ID:** 2.3  
**Story Key:** 2-3-modification-et-suppression  
**Created:** 2026-02-06

---

## Story Foundation

### User Story
As a user,  
I want to modify or delete an existing habit or objective,  
So that I can keep my commitment list up-to-date (FR12, FR13).

### Acceptance Criteria

**Given** an existing habit or objective  
**When** I send "delete habit: Drink water" or "update goal: Finish report to next Friday"  
**Then** TARS updates or deletes the corresponding record in the database  
**And** confirms the change.

### Business Context

Cette story complète l’Epic 2 en apportant la gestion de modification/suppression (FR12, FR13). Elle garantit la maintenabilité des engagements utilisateur.

---

## Developer Context Section

### 🏗️ Architecture Overview for This Story

**Story 2.3 focuses on:**
1. Routage des commandes Telegram pour modification/suppression
2. Mise à jour/suppression relationnelle stricte (ADR-003)
3. Réponses TARS cohérentes

**Key Architectural Decisions Affecting This Story:**
- **ADR-003: Pure Relational Schema (No JSONB)**
- **Service-Layer Pattern** → routes délèguent à un service (`HabitService`, `ObjectiveService`)
- **Pydantic v2** → validation stricte des entrées/sorties

---

## Technical Requirements

### Core Deliverables

#### 1. Command Routing (Telegram)
- Intercepter explicitement (avant NLU) :
  - `delete habit:` / `delete goal:`
  - `update habit:` / `update goal:`
- Laisser la NLU gérer le reste.
- En cas d’échec parsing, répondre avec un message TARS demandant une reformulation.

#### 2. Update/Delete CRUD
- Ajouter dans les services :
  - `update_habit`, `delete_habit` (soft delete si nécessaire)
  - `update_objective`, `delete_objective`
- Utiliser `telegram_id` pour sécuriser l’accès aux ressources.

#### 3. Response Formatting
- Confirmation claire des changements (TARS style)

---

## Tasks / Subtasks

- [ ] Command parsing Telegram (AC: 1)
  - [ ] Détecter `delete habit/goal` et `update habit/goal`
  - [ ] Extraire cible et nouvelle valeur
- [ ] Habit update/delete (AC: 1)
  - [ ] Ajouter `update_habit`
  - [ ] Ajouter `delete_habit`
- [ ] Objective update/delete (AC: 1)
  - [ ] Ajouter `update_objective`
  - [ ] Ajouter `delete_objective`
- [ ] Réponses TARS (AC: 1)
  - [ ] Confirmation update
  - [ ] Confirmation delete
- [ ] Tests (AC: 1)
  - [ ] Ajout tests webhook pour update/delete

---

## Dev Notes

### Data Model (ADR-003)
- `habits` : `title`, `frequency_type`, `active`
- `objectives` : `title`, `deadline`, `status`

### Suggested File Touch Points
- `app/routes/telegram_webhook.py`
- `app/services/habits.py`
- `app/services/objectives.py`
- `app/services/database.py`
- `tests/test_telegram_webhook.py`

---

## References

- _bmad-output/planning-artifacts/epics.md (Epic 2 / Story 2.3)
- _bmad-output/planning-artifacts/prd.md (FR12, FR13)
- _bmad-output/planning-artifacts/architecture.md (ADR-003)

---

## Dev Agent Record

### Agent Model Used
GPT-5.2-Codex

### Debug Log References

### Completion Notes List

### File List
