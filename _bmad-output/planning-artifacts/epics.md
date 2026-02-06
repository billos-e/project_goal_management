---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics']
inputDocuments:
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad-output/planning-artifacts/architecture.md'
  - '_bmad-output/planning-artifacts/product-brief-project_goal_management-2026-02-04.md'
---

# Focus & Flow - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Focus & Flow, decomposing the requirements from the PRD, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Création d'Habitudes avec fréquences personnalisées.
FR2: Création d'Objectifs avec échéances (deadlines).
FR3: Identification automatique des intentions et sentiments via NLU.
FR4: Système de rappels adaptatifs et forçage en cas d'échéance critique.
FR5: Mode "Pause/Vacances" pour suspendre les notifications.
FR6: "Cooling Algorithm" pour le désengagement progressif.
FR7: Séquence de résurrection daily sur 3 jours après 30 jours de sommeil (Post-MVP).
FR8: Commande /self_test pour diagnostic technique immédiat.
FR9: Consultation du taux de complétion Micro-Win sur une période donnée (Statistiques).
FR10: Consultation du nombre de Success Days sur une période donnée.
FR11: Utilisation de templates de réponses avec un ton humoristique/analytique configurable (Style TARS).
FR12: Modification des paramètres d'une Habitude existante.
FR13: Suppression d'une Habitude ou d'un Objectif.
FR14: Saisie d'un check-in sans rappel préalable (mode proactif).
FR15: Marquage manuel d'un Objectif comme "Achevé".
FR16: Support de la complétion partielle pour les Habitudes quantifiables.
FR17: Export complet des données utilisateur au format JSON.

### NonFunctional Requirements

NFR1: (Zero Cost) Système sur offres gratuites uniquement (Supabase, Gemini, GitHub Actions).
NFR2: (Robustesse) Réponse avec template fallback dans 100% des cas d'échec Gemini.
NFR3: (Confidentialité) Instance privée mono-utilisateur, aucune donnée partagée.
NFR4: (Latence) Temps de réponse NLU ≤ 5 secondes (P95).
NFR5: (Précision) Rappels déclenchés à ±2 minutes.

### Additional Requirements

- **Starter Template**: FastAPI Production-Ready Structure.
- **Backend**: Python (FastAPI/Uvicorn) on Render (Free Tier), accepting 30-60s cold start with UX feedback.
- **Database**: Supabase PostgreSQL with strict relational schema (no JSONB) as per ADR-003.
- **NLU Strategy**: ADR-004 NLU Cascade with 3-second timeout for Gemini, then TARS templates.
- **Time Management**: ADR-005 UTC storage with conversion to 'Europe/Paris' for display and Success Days.
- **Maintenance**: "The Sweeper" GitHub Action for daily stats and cooling logic (ADR-001/ADR-003).
- **Security**: ADR-002 Authentication via Telegram ID + Header Secret Token validation.
- **Resilience**: ADR-006 Offline strategy via GitHub Actions notifications if Render is down.
- **Implementation Patterns**: Atomic Services, Pydantic v2, Service-Layer Pattern, snake_case convention.

### FR Coverage Map

FR1: Epic 2 - Création d'Habitudes
FR2: Epic 2 - Création d'Objectifs
FR3: Epic 1 - Intelligence NLU & Persona
FR4: Epic 4 - Rappels & Discipline
FR5: Epic 4 - Mode Pause
FR6: Epic 4 - Cooling Algorithm
FR7: Post-MVP - Séquence de résurrection
FR8: Epic 1 - Diagnostic /self_test
FR9: Epic 5 - Statistiques Micro-Wins
FR10: Epic 5 - Statistiques Success Days
FR11: Epic 1 - Ton Persona TARS
FR12: Epic 2 - Modification Habitudes
FR13: Epic 2 - Suppression Habitudes/Objectifs
FR14: Epic 3 - Saisie proactive check-in
FR15: Epic 3 - Marquage Objectif achevé
FR16: Epic 3 - Complétion partielle
FR17: Epic 5 - Export JSON

## Epic List

### Epic 1: Fondations & Cerveau TARS (L'Assistant "Always-On")
Mise en place de l'infrastructure (FastAPI/Render/Supabase) et du canal de communication Telegram avec le persona TARS.
**FRs covered:** FR3, FR8, FR11, NFR1, NFR2, NFR4.

### Epic 2: Gestion des Engagements (Habitudes & Objectifs)
Permettre à l'utilisateur de définir ce qu'il veut suivre. Mise en place du CRUD pour les habitudes et les objectifs.
**FRs covered:** FR1, FR2, FR12, FR13.

### Epic 3: Cycle de Suivi & Micro-Wins (Le Quotidien)
L'interaction quotidienne. Enregistrement des progrès (check-ins), gestion de la complétion partielle et saisie proactive.
**FRs covered:** FR14, FR15, FR16.

### Epic 4: Discipline Adaptive & Cooling (Le Coach Intelligent)
Automatisation de la discipline. Système de rappels adaptatifs et algorithme de "Cooling".
**FRs covered:** FR4, FR5, FR6, NFR5.

### Epic 5: Bilan, Analytics & Souveraineté (Le Débrief)
Visualisation des performances (Success Days, Micro-Wins) et export des données.
**FRs covered:** FR9, FR10, FR17.

## Epic 1: Fondations & Cerveau TARS (L'Assistant "Always-On")
Mise en place de l'infrastructure (FastAPI/Render/Supabase) et du canal de communication Telegram avec le persona TARS.

### Story 1.1: Initialisation de l'infrastructure & Cœur FastAPI
As a developer,
I want to set up the FastAPI project structure and connect it to Supabase and Render,
So that the system has a solid functional foundation.

**Acceptance Criteria:**
**Given** a new FastAPI project based on the Production-Ready starter
**When** I configure the environment variables and deploy to Render
**Then** the /health or /docs endpoint must be accessible
**And** the connection to Supabase must be validated by a simple query.

### Story 1.2: Canal Telegram & Echo Persona (TARS)
As a user,
I want to interact with TARS through Telegram and receive a response in his specific tone,
So that I can validate the communication channel and the persona consistency.

**Acceptance Criteria:**
**Given** a Telegram Bot Token and a Webhook configured
**When** I send a message to the bot
**Then** TARS must respond with a message in his humorous/analytical tone
**And** the request must be validated using the Secret Token (ADR-002).

### Story 1.3: Pipeline NLU Gemini & Cascade de Résilience
As a developer,
I want to implement the NLU cascade with Gemini and local fallback templates,
So that the system always responds even if the AI is slow or unavailable (NFR2/NFR4).

**Acceptance Criteria:**
**Given** an incoming user message
**When** the Gemini API is called
**Then** it must return an identified intention within 3 seconds
**And** if it fails or times out, a TARS template response must be used (ADR-004).

### Story 1.4: Diagnostic Système (/self_test)
As a user,
I want to run a diagnostic command,
So that I can verify that all components (DB, AI, Webhooks) are working correctly.

**Acceptance Criteria:**
**Given** TARS is active
**When** I send the command /self_test
**Then** TARS must perform a check of the Supabase connection and Gemini API
**And** return a status report (FR8).


## Epic 2: Gestion des Engagements (Habitudes & Objectifs)
Permettre à l'utilisateur de définir ce qu'il veut suivre. Mise en place du CRUD pour les habitudes et les objectifs.

### Story 2.1: Définition des Habitudes (CRUD)
As a user,
I want to define, list, and view my habits with custom frequencies,
So that TARS knows what I am committed to on a recurring basis.

**Acceptance Criteria:**
**Given** I am an identified user
**When** I send "new habit: Drink water 8 times a day" or "show habits"
**Then** TARS creates or displays the habit in the  and  tables (ADR-003)
**And** confirms the action.

### Story 2.2: Gestion des Objectifs à Deadline (CRUD)
As a user,
I want to set, view, and list objectives with a specific deadline,
So that TARS can track my time-sensitive goals.

**Acceptance Criteria:**
**Given** I am an identified user
**When** I send "new goal: Finish report by tomorrow 5pm"
**Then** TARS creates an entry in the  table with the deadline stored in UTC (ADR-005)
**And** confirms the deadline back to me in 'Europe/Paris' time.

### Story 2.3: Modification et Suppression
As a user,
I want to modify or delete an existing habit or objective,
So that I can keep my commitment list up-to-date (FR12, FR13).

**Acceptance Criteria:**
**Given** an existing habit or objective
**When** I send "delete habit: Drink water" or "update goal: Finish report to next Friday"
**Then** TARS updates or deletes the corresponding record in the database
**And** confirms the change.

## Epic 3: Cycle de Suivi & Micro-Wins (Le Quotidien)
L'interaction quotidienne. Enregistrement des progrès (check-ins), gestion de la complétion partielle et saisie proactive.

### Story 3.1: Check-in Proactif
As a user,
I want to log the completion of a task without being prompted,
So that I can track my progress proactively (FR14).

**Acceptance Criteria:**
**Given** an existing habit or objective
**When** I send a message like "done: 30min workout"
**Then** TARS identifies the corresponding item and creates a  record
**And** replies with a cynical-yet-encouraging TARS-like message.

### Story 3.2: Engagement Partiel & Quantifiable
As a user,
I want to log partial completion for a quantifiable habit,
So that my effort is tracked even if I don't fully meet the target (FR16).

**Acceptance Criteria:**
**Given** a habit like "Drink 8 glasses of water"
**When** I send "I drank 2 glasses of water"
**Then** TARS updates the  record with the value '2'
**And** confirms how much is left to reach the daily goal.

### Story 3.3: Marquage Manuel d'un Objectif
As a user,
I want to manually mark an objective as completed,
So that I can close out long-term goals (FR15).

**Acceptance Criteria:**
**Given** an existing objective
**When** I send "mark goal 'Submit application' as done"
**Then** TARS updates the status of the objective to 'completed'
**And** provides a congratulatory (but still TARS-like) message.


## Epic 4: Discipline Adaptive & Cooling (Le Coach Intelligent)
Automatisation de la discipline. Système de rappels adaptatifs et algorithme de "Cooling".

### Story 4.1: Planificateur de Rappels (CRON)
As a developer,
I want to implement a reliable scheduling system using GitHub Actions,
So that TARS can send proactive reminders for habits and objectives.

**Acceptance Criteria:**
**Given** a habit scheduled for 9am 'Europe/Paris'
**When** the corresponding UTC time is reached
**Then** a GitHub Action workflow is triggered
**And** it calls a specific endpoint on the FastAPI backend to send the notification (NFR5).

### Story 4.2: Logique de "Cooling" & Mode Pause
As a user,
I want the system to reduce notifications when I'm inactive and allow me to pause them manually,
So that TARS respects my availability and energy levels (FR5, FR6).

**Acceptance Criteria:**
**Given** no user interaction for more than 3 days
**When** the daily "Sweeper" script runs
**Then** the user's status is updated to 'cooling' and reminder frequency is reduced.
**And** when I send "/pause", all non-critical notifications are suspended until I send "/resume".

## Epic 5: Bilan, Analytics & Souveraineté (Le Débrief)
Visualisation des performances (Success Days, Micro-Wins) et export des données.

### Story 5.1: Calcul des "Success Days" & Stats
As a user,
I want to be able to query my performance statistics,
So that I can get an objective overview of my progress.

**Acceptance Criteria:**
**Given** data exists in the  table
**When** the daily "Sweeper" script runs at midnight
**Then** it calculates the previous day's stats and populates the  table.
**And** when I ask "show my stats for this week", TARS returns the number of Success Days and Micro-Win rate (FR9, FR10).

### Story 5.2: Export des Données (Souveraineté)
As a user,
I want to be able to export all my data,
So that I remain in full control of my information (FR17).

**Acceptance Criteria:**
**Given** I am an identified user
**When** I send the command "/export_data"
**Then** TARS provides a secure link to download a JSON file containing all my habits, objectives, and check-ins.

