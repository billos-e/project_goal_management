# Story 2.1: Définition des Habitudes (CRUD)

**Status:** done  
**Story ID:** 2.1  
**Story Key:** 2-1-habitudes-crud  
**Created:** 2026-02-06

---

## Story Foundation

### User Story
As a user,  
I want to define, list, and view my habits with custom frequencies,  
So that TARS knows what I am committed to on a recurring basis.

### Acceptance Criteria

**Given** I am an identified user  
**When** I send "new habit: Drink water 8 times a day" or "show habits"  
**Then** TARS creates or displays the habit in the `habits` and `habit_schedules` tables (ADR-003)  
**And** confirms the action.

### Business Context

Cette story lance le cœur de **l’Epic 2 - Gestion des Engagements**, en activant le CRUD des habitudes (FR1, FR12, FR13). Elle pose les fondations pour :
- le suivi quotidien (Epic 3),
- les rappels (Epic 4),
- les stats (Epic 5).

---

## Developer Context Section

### 🏗️ Architecture Overview for This Story

**Story 2.1 focuses on:**
1. Routage des commandes Telegram liées aux habitudes (création, liste, lecture)
2. Persistence dans Supabase selon schéma relationnel strict (ADR-003)
3. Formats de fréquence et création des schedules (table `habit_schedules`)
4. Réponses TARS cohérentes (ton humoristique/analytique)

**Key Architectural Decisions Affecting This Story:**
- **ADR-003: Pure Relational Schema (No JSONB)** → `habits` + `habit_schedules`, colonnes typées
- **Service-Layer Pattern** → les routes délèguent à un service (`HabitService`)
- **Pydantic v2** → validation stricte des entrées/sorties
- **Mono-user instance** → auth basée sur `telegram_id`

---

## Technical Requirements

### Core Deliverables

#### 1. Command Routing (Telegram)
- Intercepter explicitement (avant NLU) les intents suivants :
  - `new habit:` → création d’habitude
  - `show habits` / `list habits` → listing
- Laisser la NLU gérer le reste.
- En cas d’échec parsing, répondre avec un message TARS demandant une reformulation.

#### 2. Habit CRUD (Create + Read)
- Ajouter un **HabitService** (ex: `app/services/habits.py`) ou étendre `DatabaseService`.
- Actions minimales requises pour ce story :
  - `create_habit(telegram_id, title, frequency_type, schedules)`
  - `list_habits(telegram_id)`
- Récupérer l’utilisateur via `telegram_id` pour obtenir `user_id` et préférences (ex: `notification_start`).

#### 3. Schema Constraints (ADR-003)
- Utiliser les tables **`habits`** et **`habit_schedules`** (pas de JSONB).
- `habit_schedules.time_of_day` est **NOT NULL** → prévoir une valeur par défaut si l’utilisateur ne fournit pas d’heure.
- `frequency_type` doit être l’une des valeurs: `daily | weekly | custom`.

#### 4. Pydantic Models
- Ajouter des schémas pour les habitudes (ex: `HabitCreate`, `HabitScheduleCreate`, `HabitListItem`).
- Aligner les champs avec le schéma Supabase.

#### 5. Response Formatting
- Confirmation de création : phrase TARS + résumé de la fréquence.
- Listing : format compact, numéroté, envoie 1 message.

---

## Tasks / Subtasks

- [x] Command parsing Telegram (AC: 1)
  - [x] Détecter `new habit:` et `show habits`
  - [x] Extraire `title` et `frequency_type` basique (daily/weekly/custom)
- [x] HabitService + DB access (AC: 1)
  - [x] Ajouter `get_user_by_telegram_id`
  - [x] Ajouter `create_habit` + insertion `habit_schedules`
  - [x] Ajouter `list_habits` (filtre `active=true`)
- [x] Schémas Pydantic (AC: 1)
  - [x] Ajouter modèles habit/schedule
- [x] Réponses TARS (AC: 1)
  - [x] Confirmation création
  - [x] Listing lisible
- [x] Tests (AC: 1)
  - [x] Ajout tests sur webhook pour `new habit:`
  - [x] Ajout tests sur webhook pour `show habits`

---

## Dev Notes

### Data Model (ADR-003)
- `habits`: `id`, `user_id`, `title`, `frequency_type`, `active`, `created_at`, `updated_at`
- `habit_schedules`: `habit_id`, `day_of_week`, `time_of_day`
- Pas de JSONB. Pas de colonne dynamique.

### Suggested File Touch Points
- `app/routes/telegram_webhook.py` → routing des commandes
- `app/services/database.py` → méthodes CRUD habits
- `app/services/habits.py` (optionnel) → logique métier isolée
- `app/models/schemas.py` → Pydantic models
- `tests/test_telegram_webhook.py` → nouveaux tests de commandes

### Constraints & Guardrails
- **No JSONB** (ADR-003)
- **Mono-user** → auth via `telegram_id`
- **Service-layer** obligatoire
- **Pydantic v2** strict

---

## Open Questions / Assumptions

1. Si l’utilisateur ne fournit pas d’heure, utiliser `users.notification_start` comme `time_of_day` par défaut ?
2. Pour la phrase "8 times a day", la quantité doit-elle être stockée (ex: futur champ `target_value`) ou conservée uniquement dans `title` ?

---

## References

- _bmad-output/planning-artifacts/epics.md (Epic 2 / Story 2.1)
- _bmad-output/planning-artifacts/prd.md (FR1, FR12, FR13)
- _bmad-output/planning-artifacts/architecture.md (ADR-003 + Schema Design)

---

## Dev Agent Record

### Agent Model Used
GPT-5.2-Codex

### Debug Log References

- Tests: `pytest`

### Completion Notes List

- Routage Telegram pour `new habit:` et `show habits` avec contournement NLU.
- Ajout du service `HabitService` + CRUD minimal (création, listing) et schedules.
- Ajout des schémas Pydantic pour habitudes.
- Tests webhook ajoutés et suite complète passée.
- Correction review: rollback si création des schedules échoue.
- Correction review: normalisation de `time_of_day`.
- Correction review: commande `show habits` plus tolérante.

### File List

- app/models/schemas.py
- app/routes/telegram_webhook.py
- app/services/__init__.py
- app/services/database.py
- app/services/habits.py
- tests/test_telegram_webhook.py
- _bmad-output/implementation-artifacts/sprint-status.yaml

### Change Log

- 2026-02-06: Implémentation CRUD minimal Habitudes + tests webhook.
- 2026-02-06: Fixes review (rollback schedules, time normalization, matching).
