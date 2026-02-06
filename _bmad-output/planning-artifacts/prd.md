---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish', 'step-12-complete']
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief-project_goal_management-2026-02-05.md
  - Resumé projet suivi.md
workflowType: 'prd'
briefCount: 1
researchCount: 0
brainstormingCount: 0
projectDocsCount: 0
classification:
  projectType: "Bot-Driven Productivity Tool (Telegram)"
  domain: "Personal Development & AI Coaching"
  complexity: "Medium"
  projectContext: "Greenfield"
---

# Product Requirements Document - Focus & Flow

**Author:** Billux
**Date:** 2026-02-05

## Executive Summary
Focus & Flow est un assistant de productivité personnel sous forme de bot Telegram. Conçu pour lutter contre la désorganisation, il utilise une approche psychologique unique basée sur le renforcement positif (Micro-Wins), la redevabilité (Success Days) et un persona humoristique/analytique (style TARS). Le système se distingue par son "Cooling Algorithm" qui respecte le bien-être mental de l'utilisateur en réduisant les notifications lors de périodes d'inactivité prolongées.

## Success Criteria

### User Success
*   **Micro-Win Quotidien :** Saisie obligatoire d'un élément positif pour maintenir l'élan psychologique (Cible : 90% de complétion).
*   **Status "Success Day" :** Atteindre 100% des objectifs critiques (Cible : 3 jours/semaine après 1 mois).
*   **Réduction de la Charge Mentale :** Sentiment de clarté et automatisation de la discipline.

### Technical Success
*   **Fiabilité NLU :** Moins de 5% d'erreurs d'interprétation via Google Gemini-1.5-Flash.
*   **Latence Réduite :** Délai de réponse maximum de 5 secondes.
*   **Précision des Rappels :** Déclenchement rigoureux à +/- 2 minutes près.

## Product Scope & Roadmap

### MVP (Phase 1: Core Utility)
- **Gestion des Tâches** : Distinction stricte entre Habitudes (récurrences) et Objectifs (deadlines).
- **Interface** : Bot Telegram natif (Inline Keyboards).
- **IA** : NLU via Gemini-1.5-Flash (Free tier) + templates de secours.
- **Cooling** : Système à 2 états (Actif / Repos).

### Growth (Phase 2: Robustesse)
- **Intelligence** : Routage multi-IA (Groq, HuggingFace).
- **Expérience** : Cooling complet à 4 états (🔥⚠️😴💤).
- **Outils** : Espace Admin Web basique et documentation de déploiement tiers.

### Vision (Phase 3: Assistant Audio)
- **Modalités** : Interaction Vocale (Audio Input/Output).
- **Souveraineté** : Migration optionnelle vers des modèles locaux (Ollama).

## User Journeys (TARS Personality)

### 1. La Planification (Dimanche soir)
L'utilisateur configure 3 objectifs. TARS analyse : *"Probabilité de succès augmentée de 15%. Je serai ton assistant ou ton tortionnaire amical."*

### 2. Le Success Day
En fin de journée, après 100% de complétion : *"Ne t'habitue pas trop aux compliments, c'est mauvais pour ton ego."*

### 3. Le Décrochage (Silence Radio)
Après 24h d'inactivité, TARS envoie un unique message : *"Silence radio détecté. Je repasse en veille. Demain est un nouveau jour."*

## Technical Specifications

### Architecture
- **Backend** : Instance personnelle mono-utilisateur.
- **Base de données** : Supabase (PostgreSQL).
- **Automation** : GitHub Actions pour les CRON jobs (rappels quotidiens).

### Data Model Concept
- **User** : `telegram_id` (PK), `timezone`, `preferences` (JSON), `status` (active/pause/cooling).
- **Habit** : `id` (UUID), `user_id` (FK), `title`, `frequency_config` (CRON-like JSON), `created_at`, `active` (BOOL).
- **Objective** : `id` (UUID), `user_id` (FK), `title`, `deadline` (TIMESTAMPTZ), `status` (pending/completed/failed).
- **CheckIn** : `id` (UUID), `user_id` (FK), `ref_id` (FK to Habit/Objective), `type` (habit/objective), `value` (BOOL/INT), `sentiment` (TEXT), `created_at`.
- **DailyStats** : `date` (DATE), `user_id` (FK), `completion_rate` (FLOAT), `is_success_day` (BOOL), `micro_win_count` (INT).

### Security & Privacy
- **Souveraineté** : Instance privée, authentification via 'telegram_id' uniquement.
- **Stockage** : Clés API gérées par variables d'environnement.

## Functional Requirements

### Core Capabilities
- **FR1** : Création d'Habitudes avec fréquences personnalisées.
- **FR2** : Création d'Objectifs avec échéances (deadlines).
- **FR3** : Identification automatique des intentions et sentiments via NLU.
- **FR4** : Système de rappels adaptatifs et forçage en cas d'échéance critique.
- **FR5** : Mode "Pause/Vacances" pour suspendre les notifications.
- **FR9** : Consultation du taux de complétion Micro-Win sur une période donnée (Statistiques).
- **FR10** : Consultation du nombre de Success Days sur une période donnée.
- **FR11** : Utilisation de templates de réponses avec un ton humoristique/analytique configurable (Style TARS).

### Data Lifecycle Capabilities (Detailed)
- **FR12** : Modification des paramètres d'une Habitude existante.
- **FR13** : Suppression d'une Habitude ou d'un Objectif.
- **FR14** : Saisie d'un check-in sans rappel préalable (mode proactif).
- **FR15** : Marquage manuel d'un Objectif comme "Achevé".
- **FR16** : Support de la complétion partielle pour les Habitudes quantifiables.
- **FR17** : Export complet des données utilisateur au format JSON.

### Specialized Logic
- **FR6** : "Cooling Algorithm" pour le désengagement progressif.
- **FR7 (Post-MVP - v1.5)** : Séquence de résurrection daily sur 3 jours après 30 jours de sommeil.
- **FR8** : Commande /self_test pour diagnostic technique immédiat.

## Non-Functional Requirements
- **NFR1 (Zero Cost)** : Le système fonctionne entièrement via les offres gratuites de Supabase (500MB), Google AI Studio (1M tokens/mois) et GitHub Actions (2000 min/mois).
- **NFR2 (Robustesse)** : Le système répond avec un template fallback dans 100% des cas où l'API Gemini échoue, sans interruption de service.
- **NFR3 (Confidentialité)** : Aucune donnée utilisateur n'est partagée avec des tiers ; toutes les données sont stockées dans l'instance Supabase personnelle.
- **NFR4 (Latence)** : Temps de réponse NLU ≤ 5 secondes (P95) pour maintenir la fluidité.
- **NFR5 (Précision)** : Rappels déclenchés avec une précision de ±2 minutes par rapport à l'heure configurée.
