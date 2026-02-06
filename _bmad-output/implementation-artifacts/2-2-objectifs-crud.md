# Story 2.2: Gestion des Objectifs à Deadline (CRUD)

**Status:** review  
**Story ID:** 2.2  
**Story Key:** 2-2-objectifs-crud  
**Created:** 2026-02-06

---

## Story Foundation

### User Story
As a user,  
I want to set, view, and list objectives with a specific deadline,  
So that TARS can track my time-sensitive goals.

### Acceptance Criteria

**Given** I am an identified user  
**When** I send "new goal: Finish report by tomorrow 5pm"  
**Then** TARS creates an entry in the `objectives` table with the deadline stored in UTC (ADR-005)  
**And** confirms the deadline back to me in 'Europe/Paris' time.

### Business Context

Cette story complète l’Epic 2 en ajoutant le CRUD minimal des objectifs à échéance (FR2). Elle prépare :
- le cycle de suivi (Epic 3),
- les rappels (Epic 4),
- les statistiques (Epic 5).

---

## Developer Context Section

### 🏗️ Architecture Overview for This Story

**Story 2.2 focuses on:**
1. Routage des commandes Telegram liées aux objectifs (création, liste, lecture)
2. Conversion des deadlines en UTC (ADR-005) et affichage Europe/Paris
3. Persistence relationnelle strictes dans Supabase (`objectives`)
4. Réponses TARS cohérentes (ton humoristique/analytique)

**Key Architectural Decisions Affecting This Story:**
- **ADR-003: Pure Relational Schema (No JSONB)** → table `objectives`
- **ADR-005: Timezone Handling** → stockage UTC, affichage Europe/Paris
- **Service-Layer Pattern** → routes délèguent à un service (`ObjectiveService`)
- **Pydantic v2** → validation stricte des entrées/sorties

---

## Technical Requirements

### Core Deliverables

#### 1. Command Routing (Telegram)
- Intercepter explicitement (avant NLU) :
  - `new goal:` → création d’objectif
  - `show goals` / `list goals` → listing
- Laisser la NLU gérer le reste.
- En cas d’échec parsing, répondre avec un message TARS demandant une reformulation.

#### 2. Objective CRUD (Create + Read)
- Ajouter un **ObjectiveService** (ex: `app/services/objectives.py`) ou étendre `DatabaseService`.
- Actions minimales requises :
  - `create_objective(telegram_id, title, deadline_utc)`
  - `list_objectives(telegram_id)`

#### 3. Deadline Parsing & Timezone
- Interpréter des expressions simples (ex: "tomorrow 5pm")
- Convertir en **UTC** pour stockage (`objectives.deadline`)
- Confirmer en **Europe/Paris** à l’utilisateur

#### 4. Pydantic Models
- Ajouter des schémas pour objectifs (ex: `ObjectiveCreate`, `ObjectiveListItem`).
- Aligner les champs avec le schéma Supabase.

#### 5. Response Formatting
- Confirmation création : phrase TARS + deadline formatée Europe/Paris
- Listing : format compact, numéroté, envoi unique

---

## Tasks / Subtasks

- [x] Command parsing Telegram (AC: 1)
  - [x] Détecter `new goal:` et `show goals`
  - [x] Extraire `title` et `deadline` basique (ex: "tomorrow 5pm")
- [x] ObjectiveService + DB access (AC: 1)
  - [x] Ajouter `create_objective`
  - [x] Ajouter `list_objectives`
- [x] Timezone & parsing (AC: 1)
  - [x] Convertir deadlines en UTC pour stockage
  - [x] Afficher en Europe/Paris dans la réponse
- [x] Schémas Pydantic (AC: 1)
  - [x] Ajouter modèles objective
- [x] Réponses TARS (AC: 1)
  - [x] Confirmation création
  - [x] Listing lisible
- [x] Tests (AC: 1)
  - [x] Ajout tests sur webhook pour `new goal:`
  - [x] Ajout tests sur webhook pour `show goals`

---

## Dev Notes

### Data Model (ADR-003)
- `objectives`: `id`, `user_id`, `title`, `deadline` (TIMESTAMPTZ), `status`, `created_at`, `updated_at`
- `status` ∈ (`pending`, `completed`, `failed`)

### Timezone (ADR-005)
- Stocker en UTC
- Afficher `Europe/Paris`

### Suggested File Touch Points
- `app/routes/telegram_webhook.py` → routing des commandes
- `app/services/database.py` → méthodes CRUD objectives
- `app/services/objectives.py` (optionnel) → logique métier isolée
- `app/models/schemas.py` → Pydantic models
- `tests/test_telegram_webhook.py` → nouveaux tests de commandes

---

## Open Questions / Assumptions

1. Parser minimal: accepte-t-on seulement "tomorrow 5pm" / "demain 17h" ?
2. Doit-on introduire une dépendance de parsing (ex: dateparser) ou rester minimal ?

---

## References

- _bmad-output/planning-artifacts/epics.md (Epic 2 / Story 2.2)
- _bmad-output/planning-artifacts/prd.md (FR2)
- _bmad-output/planning-artifacts/architecture.md (ADR-003 + ADR-005)

---

## Dev Agent Record

### Agent Model Used
GPT-5.2-Codex

### Debug Log References

- Tests: `pytest`

### Completion Notes List

- Routage Telegram pour `new goal:` et `show goals` avec contournement NLU.
- Ajout du service `ObjectiveService` + CRUD minimal et parsing deadline.
- Conversion timezone UTC/Europe-Paris pour les deadlines.
- Schémas Pydantic objectifs ajoutés.
- Tests webhook ajoutés et suite complète passée.

### File List

- app/models/schemas.py
- app/routes/telegram_webhook.py
- app/services/__init__.py
- app/services/database.py
- app/services/objectives.py
- tests/test_telegram_webhook.py
- _bmad-output/implementation-artifacts/sprint-status.yaml

### Change Log

- 2026-02-06: Implémentation CRUD minimal Objectifs + tests webhook.
