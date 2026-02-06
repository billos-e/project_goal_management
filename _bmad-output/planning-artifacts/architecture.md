---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-02-05'
inputDocuments:
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad-output/planning-artifacts/product-brief-project_goal_management-2026-02-04.md'
project_name: 'project_goal_management'
user_name: 'Billux'
date: '2026-02-05'
---

# Architecture Decision Document - Focus & Flow

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

---

## Project Context Analysis

### Requirements Overview

**Functional Requirements (17 total):**

Le système Focus & Flow est structuré autour de 5 domaines fonctionnels :

1. **Gestion de Données (FR1, FR2, FR12-15)** : CRUD complet pour Habitudes (avec fréquences personnalisées) et Objectifs (avec deadlines). Support de la modification, suppression, complétion partielle et marquage manuel.

2. **Intelligence Artificielle (FR3, FR11)** : NLU via Google Gemini-1.5-Flash pour identifier automatiquement les intentions et sentiments dans les messages utilisateur. Templates de réponses avec ton humoristique/analytique configurable (style TARS).

3. **Automatisation Proactive (FR4, FR6, FR7)** : Système de rappels adaptatifs avec forçage en cas d'échéance critique. Cooling Algorithm pour désengagement progressif basé sur l'inactivité. Séquence de résurrection sur 3 jours après 30 jours de sommeil (post-MVP).

4. **Analytics & Insights (FR9-10)** : Consultation du taux de complétion Micro-Win et du nombre de Success Days sur période donnée.

5. **Souveraineté Utilisateur (FR5, FR8, FR17)** : Mode Pause/Vacances, commande /self_test pour diagnostic technique, export complet des données au format JSON.

**Non-Functional Requirements:**

- **NFR1 (Zero Cost)** : Contrainte architecturale majeure - tout le système doit fonctionner avec les offres gratuites (Supabase 500MB, Gemini 1M tokens/mois, GitHub Actions 2000 min/mois). Cette contrainte détermine toutes les décisions technologiques.

- **NFR2 (Robustesse à 100%)** : Le système doit répondre avec un template fallback dans 100% des cas d'échec API Gemini, sans interruption de service. Impose une architecture à double stratégie.

- **NFR3 (Confidentialité Totale)** : Instance privée mono-utilisateur, aucune donnée partagée avec des tiers. Simplifie l'architecture (pas de multi-tenancy) mais impose une souveraineté des données.

- **NFR4 (Latence)** : Temps de réponse NLU ≤ 5 secondes (P95) pour interactions chaudes. Latence jusqu'à 60 secondes acceptable pour cold starts avec feedback UX approprié.

- **NFR5 (Précision Temporelle)** : Rappels déclenchés avec précision de ±2 minutes. Impose des mécanismes de scheduling fiables.

**Scale & Complexity:**

- **Primary domain:** Backend conversationnel + Automation (Event-Driven)
- **Complexity level:** Moyenne
- **Estimated architectural components:** 5 composants principaux
  - Bot Telegram (interface conversationnelle)
  - Backend Python (FastAPI/Flask sur Render)
  - NLU Engine (Gemini + fallback templates)
  - Database Layer (Supabase PostgreSQL)
  - CRON Scheduler (GitHub Actions)

### Technical Constraints & Dependencies

**Hard Constraints:**

- **Plateforme:** Telegram Bot API (point d'entrée unique)
- **Coût:** Free tiers obligatoire pour tous les services
  - Render: 750h/mois (spin down après 15 min inactivité)
  - Supabase: 500MB storage
  - Gemini: 1M tokens/mois
  - GitHub Actions: 2000 min/mois
- **Utilisateur:** Instance mono-utilisateur (pas de système d'authentification complexe)
- **Latence:** Cold start de 30-60s acceptable avec feedback UX

**Technology Stack:**

- **Backend:** Python (FastAPI ou Flask) sur Render free tier
- **Database:** Supabase PostgreSQL
- **IA:** Google Gemini-1.5-Flash via AI Studio API (free tier)
- **Automation:** GitHub Actions pour CRON jobs (rappels quotidiens)
- **Interface:** Telegram Bot API avec webhooks

### Cross-Cutting Concerns Identified

1. **Gestion d'État Distribuée** : Le système a un état partagé entre le bot Telegram (réactif) et les GitHub Actions (proactif). La base de données Supabase est la source de vérité unique.

2. **Résilience et Fallbacks** : L'exigence de 100% de réponse impose une architecture défensive avec templates de secours, gestion des erreurs réseau, et retry logic pour les APIs externes.

3. **Cold Start Management** : Render free tier spin down après 15 minutes d'inactivité. Solution : Feedback UX immédiat via Telegram (messages temporaires, typing indicators) pour masquer la latence de 30-60s lors des cold starts.

4. **Observabilité** : La commande /self_test (FR8) impose un système de health checks et de diagnostics intégré dès la conception pour vérifier l'état de tous les composants.

5. **Cohérence du Persona** : Le ton TARS doit être cohérent entre les réponses générées par l'IA et les templates fallback. Nécessite une stratégie de prompt engineering et de template design alignée.

6. **Timezone Handling** : Les rappels et statistiques dépendent du fuseau horaire de l'utilisateur. Doit être stocké en DB et respecté dans tous les calculs temporels (CRON, statistiques, Success Days).

7. **Data Lifecycle** : Export JSON (FR17) impose une structure de données propre et documentée dès le départ pour faciliter la portabilité et la souveraineté des données.

---

## Architecture Decision: Backend Hosting Strategy

### Context

Le PRD mentionne une "instance personnelle mono-utilisateur" sans préciser l'hébergement. Cette décision est critique car elle impacte directement NFR1 (Zero Cost), NFR4 (Latence), et la complexité de maintenance.

### Options Evaluated

#### Option A: VPS Backend Traditionnel
- **Composants:** Telegram Bot → VPS (DigitalOcean/Hetzner) → Supabase
- **Coût:** 5-10€/mois
- **Latence:** Constante <2s
- **Disponibilité:** 99.9%+
- **Complexité:** Moyenne (gestion serveur, déploiement, monitoring)
- **Verdict:** ❌ Viole NFR1 (Zero Cost)

#### Option B: Supabase Edge Functions
- **Composants:** Telegram Bot → Edge Functions (TypeScript) → Supabase
- **Coût:** 0€ (500K invocations/mois gratuit)
- **Latence:** <2s (cold start 1-2s)
- **Disponibilité:** 99.95%+
- **Complexité:** Faible (serverless, auto-scale)
- **Scheduling:** pg_cron natif dans PostgreSQL
- **Verdict:** ⚠️ Nécessite apprentissage TypeScript, complexité perçue sur RLS policies

#### Option C: Python Backend sur Render Free Tier (CHOIX FINAL)
- **Composants:** Telegram Bot → Render (Python) → Supabase
- **Coût:** 0€
- **Latence:** 
  - Serveur chaud: <2s
  - Cold start: 30-60s (après 15 min inactivité)
- **Disponibilité:** Acceptable pour usage personnel
- **Complexité:** Faible (Python familier, déploiement git-based)
- **Scheduling:** GitHub Actions pour CRON
- **Verdict:** ✅ Optimal pour MVP

### Decision Rationale

**Choix Final: Python/Render + GitHub Actions (sans keepalive)**

**Justification via First Principles Analysis:**

1. **Le cold start de 30-60s n'est PAS critique car:**
   - **Rappels proactifs (80% des interactions):** Le cold start se produit AVANT l'envoi de la notification. L'utilisateur ne le voit jamais.
   - **Messages utilisateur (20% des interactions):** Nature asynchrone du coaching. Un délai de 30-60s est socialement acceptable dans une conversation Telegram.
   - **Fréquence limitée:** Maximum 2-3 cold starts/jour en pratique (matin, après-midi si inactif).

2. **Feedback UX masque complètement la latence:**
   ```python
   # Réponse instantanée
   temp_msg = await bot.send_message(chat_id, "🤖 TARS analyse... Un instant.")
   
   # Traitement (30-60s si cold start)
   result = await process_with_gemini(message)
   
   # Remplacement du message temporaire
   await bot.edit_message_text(chat_id, temp_msg.message_id, text=result)
   ```

3. **Pas de keepalive nécessaire:**
   - ❌ Rejeté: Keepalive via GitHub Actions (73 pings/jour = 1,095 min/mois)
   - ✅ Accepté: Cold starts avec feedback UX approprié
   - **Raison:** Simplicité architecturale, budget libéré (1,700+ min/mois disponibles pour features futures)

4. **Alignement avec les contraintes:**
   - ✅ NFR1 (Zero Cost): Respecté à 100%
   - ✅ NFR2 (Robustesse): Templates fallback + retry logic
   - ✅ NFR3 (Confidentialité): Instance privée
   - ✅ NFR4 (Latence): <5s serveur chaud, <60s cold start avec UX
   - ✅ NFR5 (Précision): GitHub Actions CRON suffisant pour ±2 min

5. **Avantages stratégiques:**
   - Python familier → développement rapide
   - Architecture simple → moins de bugs
   - Migration future possible → Edge Functions ou VPS payant si besoins évoluent
   - Focus sur le MVP, pas sur l'optimisation prématurée

### Architecture Simplifiée

```
┌─────────────────┐
│  Telegram API   │
│   (Webhooks)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│   Backend Python/Render     │
│   - FastAPI/Flask           │
│   - Spin down après 15 min  │
│   - Cold start: 30-60s      │
│   - Feedback UX immédiat    │
└──────┬──────────────┬───────┘
       │              │
       ▼              ▼
┌─────────────┐  ┌──────────────────┐
│  Supabase   │  │  Gemini API      │
│  PostgreSQL │  │  (NLU + fallback)│
│  (État)     │  │                  │
└─────────────┘  └──────────────────┘
       ▲
       │
┌──────────────────┐
│ GitHub Actions   │
│ (CRON Rappels)   │
│ - 3-5 jobs/jour  │
│ - ~200-400 min/  │
│   mois utilisés  │
└──────────────────┘
```

### Budget Allocation

| Service | Limite Free Tier | Usage Estimé | Marge |
|---------|------------------|--------------|-------|
| Render | 750h/mois | 744h (31j) | ✅ OK |
| GitHub Actions | 2000 min/mois | 200-400 min | ✅ 1600+ min libres |
| Supabase | 500 MB | <50 MB | ✅ Très confortable |
| Gemini | 1M tokens/mois | <100K tokens | ✅ Très confortable |

### Risks & Mitigations

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Render restart inopiné | Service indisponible 2-5 min | Faible | Retry logic côté GitHub Actions |
| GitHub Actions CRON délais | Rappels retardés de 3-15 min | Moyenne | Acceptable pour ±2 min NFR5 |
| Gemini API rate limit | Pas de NLU temporaire | Faible | Templates fallback (NFR2) |
| Cold start frustrant | UX dégradée | Faible | Feedback immédiat masque latence |
| **Inaccessibilité Backend** | **Zéro réponse utilisateur** | **Faible** | **Gestion des timeouts webhooks & notifications manuelles** |

### Specialized Logic: Cooling & Maintenance

#### Daily Maintenance Script ("The Sweeper")
Pour pallier l'absence de serveur persistant, un job de maintenance quotidien est mis en place :
- **Déclencheur** : GitHub Action à minuit UTC.
- **Action** : Appelle l'endpoint `/daily-maintenance` sur Render.
- **Rôle** : 
    1. Calcule la nouvelle "température" (🔥⚠️😴💤) basée sur `last_interaction_at`.
    2. Met à jour le `status` de l'utilisateur.
    3. Génère les lignes de statistiques `daily_stats` pour la journée écoulée.
    4. Nettoie les jobs de rappels obsolètes.

#### Cooling Algorithm Trigger
La logique de refroidissement est double :
- **Proactive (Sweeper)** : Le job de minuit ajuste l'état global.
- **Réactive (Push)** : Avant chaque rappel envoyé par le CRON, le backend vérifie le `status` actuel. Si l'état est `😴 Repos` ou `💤 Sommeil`, le rappel est soit annulé, soit remplacé par un message de veille discret, respectant ainsi le bien-être mental de l'utilisateur.

---

## Starter Template Evaluation

### Primary Technology Domain
**Backend API / Bot Framework** (Traitement asynchrone et orchestrateur de services).

### Selected Starter: FastAPI Production-Ready Structure

**Rationale for Selection:**
- **Asynchronisme natif** : Indispensable pour gérer les délais de réponse de l'IA (Gemini) sans bloquer les autres webhooks.
- **Typage Fort (Type Hints)** : Utilisation de Pydantic pour valider les données de Supabase et de Telegram, garantissant une base de code propre et maintenable.
- **Auto-Documentation** : Accès à Swagger UI (`/docs`) pour tester manuellement les endpoints métier et le diagnostic (/self_test).
- **Performance Free Tier** : Utilisation optimale des ressources limitées de Render via `uvicorn`.

**Initialization Command:**
```bash
# Setup initial de l'environnement
mkdir focus_flow && cd focus_flow
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn supabase google-generativeai pydantic python-dotenv httpx
```

**Architectural Decisions Provided by Starter:**

- **Language & Runtime** : Python 3.10+ avec Type Hints obligatoires pour la logique métier.
- **Structure de Dossiers** :
    - `app/api/endpoints/` : Pour séparer le webhook Telegram du script de maintenance et du self-test.
    - `app/schemas/` : Modèles Pydantic reflétant exactement le schéma de la base de données Supabase.
    - `app/services/` : Encapsulation de l'intelligence (TARS persona engine, Gemini wrapper, Cooling logic).
    - `app/core/` : Gestion des variables d'environnement et de la configuration globale.
- **Build Tooling** : Standard `requirements.txt` et `Dockerfile` optimisé pour Render.

---

## Starter Template Evaluation

### Primary Technology Domain
**Backend API / Bot Framework** (Traitement asynchrone et orchestrateur de services).

### Selected Starter: FastAPI Production-Ready Structure

**Rationale for Selection:**
- **Asynchronisme natif** : Indispensable pour gérer les délais de réponse de l'IA (Gemini) sans bloquer les autres webhooks.
- **Typage Fort (Type Hints)** : Utilisation de Pydantic pour valider les données de Supabase et de Telegram, garantissant une base de code propre et maintenable.
- **Auto-Documentation** : Accès à Swagger UI (`/docs`) pour tester manuellement les endpoints métier et le diagnostic (/self_test).
- **Performance Free Tier** : Utilisation optimale des ressources limitées de Render via `uvicorn`.

**Initialization Command:**
```bash
# Setup initial de l'environnement
mkdir focus_flow && cd focus_flow
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn supabase google-generativeai pydantic python-dotenv httpx
```

**Architectural Decisions Provided by Starter:**

- **Language & Runtime** : Python 3.10+ avec Type Hints obligatoires pour la logique métier.
- **Structure de Dossiers** :
    - `app/api/endpoints/` : Pour séparer le webhook Telegram du script de maintenance et du self-test.
    - `app/schemas/` : Modèles Pydantic reflétant exactement le schéma de la base de données Supabase.
    - `app/services/` : Encapsulation de l'intelligence (TARS persona engine, Gemini wrapper, Cooling logic).
    - `app/core/` : Gestion des variables d'environnement et de la configuration globale.
- **Build Tooling** : Standard `requirements.txt` et `Dockerfile` optimisé pour Render.

---

## Core Architectural Decisions

### Data Architecture
- **Validation** : Modèles **Pydantic v2** pour une validation stricte des entrées/sorties.
- **Data Access** : **Supabase-py** (Client asynchrone) utilisé directement dans les services FastAPI.
- **Migrations** : Gestion manuelle via le SQL Editor de Supabase (stratégie validée pour sa simplicité et sa rareté).

### Security & Compliance
- **Secrets** : Utilisation de **python-dotenv** et **Pydantic-Settings**.
- **Auth Proxy** : Webhook secret token Telegram obligatoire pour chaque requête entrante.
- **Privacy** : Aucune donnée sensible (PII) n'est envoyée à Gemini, uniquement les messages de coaching.

### API & Error Handling
- **Pattern** : Service-Layer Pattern. Les contrôleurs FastAPI délèguent à des services (`HabitService`, `AIService`).
- **Resilience** : Implémentation de la cascade NLU (ADR-004) et gestion des retries HTTP exponentiels pour les appels Gemini.
- **Logging** : Utilisation du module `logging` standard de Python, orienté vers la console pour capturer les logs Render.

### Infrastructure & Deployment
- **Hébergement** : Render Web Service (Free Tier).
- **Automation** : GitHub Actions pour les rappels et la maintenance quotidien (The Sweeper).
- **CI/CD** : Les développeurs poussent directement sur GitHub (`develop` ou branches features). Render surveille la branche `main` pour déploiement automatique en production. Pas d'intermédiaire manuel.
- **Diagnostic** : Endpoint `/api/v1/self_test` pour valider l'intégrité de la pile technique en un clic.

---

## Architecture Decision Records (ADRs)

### ADR-001: Backend Hosting on Render Free Tier Without Keepalive

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Le système nécessite un backend pour gérer les webhooks Telegram, appeler l'API Gemini, et interagir avec Supabase. La contrainte NFR1 (Zero Cost) limite les options d'hébergement. Trois approches ont été évaluées.

**Decision:**

Utiliser Python (FastAPI ou Flask) hébergé sur Render free tier, SANS système de keepalive, en acceptant les cold starts de 30-60s avec feedback UX approprié.

**Alternatives Considered:**

1. **VPS Payant (DigitalOcean/Hetzner)** : 5-10€/mois, latence constante <2s, mais viole NFR1 (Zero Cost). ❌ Rejeté.

2. **Supabase Edge Functions** : 0€, latence 1-2s, serverless natif avec pg_cron, mais nécessite apprentissage TypeScript et perçu comme complexe pour RLS policies. ⚠️ Différé à Phase 2.

3. **Render + Keepalive GitHub Actions** : 0€, maintient le serveur chaud avec 73 pings/jour (1,095 min/mois), mais complexité accrue, consommation réseau inutile, et dépendance sur la fiabilité des CRON. ❌ Rejeté pour simplicité.

**Rationale:**

Via First Principles Analysis, nous avons déconstruit l'hypothèse que "le cold start est un problème" :

- **Rappels proactifs (80% interactions)** : Le cold start se produit AVANT l'envoi de la notification Telegram. L'utilisateur ne le voit jamais.
- **Messages utilisateur (20% interactions)** : La nature asynchrone du coaching rend acceptable un délai de 30-60s. Telegram montre "typing..." pendant le traitement.
- **Fréquence limitée** : Maximum 2-3 cold starts/jour (matin, après-midi si inactif).
- **UX masque la latence** : Messages temporaires ("🤖 TARS analyse... Un instant.") édités ensuite avec la réponse finale.

L'utilisateur a explicitement confirmé : "Je ne suis pas à la minute près" et "1 min de délai ne me pose aucun problème".

**Consequences:**

✅ **Positives:**
- Simplicité architecturale maximale (5 composants au lieu de 6 avec keepalive)
- Python familier = développement rapide du MVP
- Budget GitHub Actions libéré : 1,600+ min/mois disponibles pour features futures
- Zero maintenance du keepalive
- Architecture écologique (serveur ne consomme que quand utilisé)

⚠️ **Négatives:**
- Latence variable (2s chaud, 30-60s froid)
- Pas de SLA sur Render free tier (acceptable pour usage personnel)
- Dépendance sur la fiabilité de Render (peut redémarrer sans prévenir)

**Compliance:**
- ✅ NFR1 (Zero Cost): Respecté à 100%
- ✅ NFR2 (Robustesse): Templates fallback garantissent 100% réponse
- ✅ NFR3 (Confidentialité): Instance privée mono-utilisateur
- ✅ NFR4 (Latence): <5s serveur chaud, <60s cold start avec UX acceptable
- ✅ NFR5 (Précision): GitHub Actions CRON suffisant pour ±2 min

**Notes:**
Migration vers Edge Functions reste une option documentée pour Phase 2 si les besoins évoluent.

---

### ADR-002: Authentication via Telegram ID Only

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Le système doit identifier l'utilisateur pour toutes les opérations. Étant une instance mono-utilisateur, la complexité d'authentification doit être minimisée sans compromettre la sécurité.

**Decision:**

Utiliser uniquement le `telegram_id` comme identifiant utilisateur, avec vérification de la signature des webhooks Telegram via le secret token.

**Alternatives Considered:**

1. **OAuth 2.0** : Standard industrie, mais overkill pour mono-utilisateur. Ajouterait complexité sans bénéfice. ❌ Rejeté.

2. **JWT Tokens** : Génération et validation de tokens, mais inutile quand Telegram gère déjà l'authentification. ❌ Rejeté.

3. **Password-based auth** : Nécessiterait un système de login séparé, violant l'objectif de "friction minimale". ❌ Rejeté.

**Rationale:**

- Telegram vérifie l'authentification côté serveur. Impossible de forger un `update` Telegram avec un faux `user_id`.
- Le webhook est signé avec un secret token (vérifié par le backend).
- Instance mono-utilisateur = pas de risque de collision d'identifiants.
- Simplicité maximale : zéro code d'authentification à maintenir.

**Implementation Details:**

```python
# Vérification signature webhook
def verify_telegram_webhook(request):
    secret_token = os.getenv('TELEGRAM_SECRET_TOKEN')
    provided_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    return hmac.compare_digest(secret_token, provided_token)

# Extraction user_id
user_id = update['message']['from']['id']
```

**Consequences:**

✅ **Positives:**
- Architecture simple sans couche auth complexe
- Zero overhead de performance
- Sécurité garantie par Telegram
- Code minimal à maintenir

⚠️ **Négatives:**
- Dépendance complète sur la sécurité de Telegram (acceptable car Telegram est un système robuste)
- Migration difficile si passage multi-utilisateur futur (mais hors scope)

**Security Measures:**
- Secret token stocké en variable d'environnement Render (jamais dans le code)
- Vérification systématique de la signature sur chaque webhook
- Logging des tentatives d'accès non autorisées

---

### ADR-003: Pure Relational Database Schema (No JSONB)

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Le modèle de données du PRD mentionne `preferences` (JSON) et `frequency_config` (CRON-like JSON). Débat entre utiliser JSONB pour flexibilité vs colonnes strictes pour validation.

**Decision:**

Utiliser un schéma relationnel strict avec colonnes typées, SANS JSONB. Les habitudes et préférences sont modélisées comme des lignes dans des tables dédiées, pas comme des colonnes dans `users`.

**Alternatives Considered:**

1. **Hybrid (Colonnes + JSONB pour flexibilité)** : Colonnes pour données core + `preferences JSONB` et `frequency_config JSONB`. Flexible mais perd la validation PostgreSQL. ❌ Rejeté.

2. **Entity-Attribute-Value (EAV)** : Table `user_preferences` avec (key, value) pour éviter migrations. Flexible mais perte totale de typage, requêtes complexes, 4x plus de storage. ❌ Rejeté.

3. **Pure Relationnel (CHOISI)** : Colonnes strictes pour préférences, table `habit_schedules` pour fréquences. Simple, performant, validé par PostgreSQL. ✅ Accepté.

**Rationale:**

**Débat d'experts - Points clés :**

- **Validation automatique** : PostgreSQL valide les types (INTEGER, BOOLEAN, TIME). Avec JSONB, tout est TEXT, bugs silencieux possibles.
- **Performance** : Requêtes simples avec colonnes vs requêtes complexes avec opérateurs JSONB (`->`, `@>`).
- **Storage efficiency** : Colonnes typées = 100 bytes vs JSONB = 400 bytes pour même données (4x plus efficace).
- **Debugging** : `SELECT timezone FROM users` vs `SELECT preferences->>'timezone' FROM users` - lequel préférez-vous à 23h ?

**Malentendu clarifié :**

L'utilisateur pensait que chaque habitude nécessiterait une nouvelle colonne (migration). FAUX. Les habitudes sont des LIGNES dans la table `habits`. Ajouter une habitude = INSERT (requête normale), pas ALTER TABLE (migration).

**Migrations réelles (rares) :**

- Ajout d'une nouvelle colonne à `users` (ex: `preferred_language`) : 2-3 fois/an maximum
- Création d'une nouvelle table (ex: `user_achievements`) : 1 fois tous les 6 mois
- Ces opérations prennent 3 secondes avec Supabase SQL Editor

**Schema Design:**

```sql
-- Users : Colonnes strictes pour préférences
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  telegram_id BIGINT UNIQUE NOT NULL,
  timezone TEXT NOT NULL DEFAULT 'UTC',
  humor_level INTEGER CHECK (humor_level BETWEEN 1 AND 10) DEFAULT 8,
  cooling_enabled BOOLEAN DEFAULT true,
  notification_start TIME DEFAULT '06:00',
  notification_end TIME DEFAULT '23:00',
  status TEXT CHECK (status IN ('active', 'pause', 'cooling')) DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habits : Lignes dynamiques (pas de colonnes par habitude)
CREATE TABLE habits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  frequency_type TEXT CHECK (frequency_type IN ('daily', 'weekly', 'custom')) NOT NULL,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habit Schedules : Récurrences flexibles
CREATE TABLE habit_schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  habit_id UUID REFERENCES habits(id) ON DELETE CASCADE,
  day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),  -- NULL pour daily
  time_of_day TIME NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(habit_id, day_of_week, time_of_day)
);

-- Objectives
CREATE TABLE objectives (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  deadline TIMESTAMPTZ NOT NULL,
  status TEXT CHECK (status IN ('pending', 'completed', 'failed')) DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Check-ins : Traçabilité des actions
CREATE TABLE check_ins (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  ref_id UUID NOT NULL,
  ref_type TEXT CHECK (ref_type IN ('habit', 'objective')) NOT NULL,
  value INTEGER,  -- Pour quantités (verres d'eau, pompes)
  completed BOOLEAN DEFAULT false,
  sentiment TEXT,  -- Ressenti court
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Daily Stats : Agrégations quotidiennes
CREATE TABLE daily_stats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  completion_rate FLOAT CHECK (completion_rate BETWEEN 0 AND 100),
  is_success_day BOOLEAN DEFAULT false,
  micro_win_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date)
);
```

**Usage Examples:**

```sql
-- Ajouter habitude "Lecture" (requête normale, PAS migration)
INSERT INTO habits (user_id, title, frequency_type) 
VALUES ('billux-uuid', 'Lecture', 'daily');

-- Changer Sport de 3x/semaine à 5x/semaine (requêtes normales)
DELETE FROM habit_schedules WHERE habit_id = 'sport-uuid';
INSERT INTO habit_schedules (habit_id, day_of_week, time_of_day) VALUES
  ('sport-uuid', 0, '07:00'),  -- Lundi
  ('sport-uuid', 2, '07:00'),  -- Mercredi
  ('sport-uuid', 3, '07:00'),  -- Jeudi
  ('sport-uuid', 4, '07:00'),  -- Vendredi
  ('sport-uuid', 6, '07:00');  -- Dimanche
```

**Consequences:**

✅ **Positives:**
- Validation stricte par PostgreSQL (prévient bugs silencieux)
- Requêtes SQL simples et performantes
- Storage optimal (colonnes typées < JSONB)
- Debugging facile (colonnes explicites)
- Ajout/suppression illimités d'habitudes sans migrations
- Indexes efficaces sur toutes les colonnes

⚠️ **Négatives:**
- Nouvelles préférences système = migration DB (mais 2-3 fois/an max, 3 secondes avec Supabase)

**Indexes (Phase 2):**
```sql
CREATE INDEX idx_habits_user ON habits(user_id) WHERE active = true;
CREATE INDEX idx_schedules_time ON habit_schedules(time_of_day);
CREATE INDEX idx_checkins_date ON check_ins(created_at);
CREATE INDEX idx_daily_stats_date ON daily_stats(user_id, date);
```

---

### ADR-004: NLU Cascade with 3-Second Timeout

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

NFR2 exige "100% de réponse" même en cas d'échec API Gemini. NFR4 exige latence <5s pour serveur chaud. Besoin d'une stratégie de fallback robuste.

**Decision:**

Implémenter une cascade à 3 niveaux avec timeout strict :

1. **Gemini API** (3 secondes max) → Compréhension NLU complète
2. **Templates TARS** (fallback immédiat) → Réponses pré-écrites avec persona
3. **Hardcoded Response** (dernier recours) → Message d'erreur gracieux

**Architecture:**

```python
async def process_user_message(message: str) -> str:
    try:
        # Niveau 1 : Gemini avec timeout strict
        response = await asyncio.wait_for(
            gemini_api.generate(message),
            timeout=3.0
        )
        log_success('gemini', message)
        return response
        
    except asyncio.TimeoutError:
        log_fallback('gemini_timeout', message)
        # Niveau 2 : Templates TARS
        return get_tars_template_response(message)
        
    except Exception as e:
        log_fallback('gemini_error', message, error=e)
        # Niveau 2 : Templates TARS
        try:
            return get_tars_template_response(message)
        except Exception:
            # Niveau 3 : Hardcoded
            return "Mon cerveau positronique a un hoquet. Essaie /help ou reformule."
```

**Templates TARS Strategy:**

Templates doivent matcher le ton humoristique/analytique pour cohérence du persona :

```python
TARS_TEMPLATES = {
    'check_in_sport': [
        "Sport enregistré. Ne t'habitue pas trop aux compliments.",
        "Compris. Ton corps te remercie. Ton esprit aussi, même s'il ne l'admet pas.",
        "✅ Sport comptabilisé. Streak : {streak} jours. Impressionnant pour un humain."
    ],
    'check_in_water': [
        "Hydratation notée. Continue comme ça, tu n'es pas un cactus.",
        "{count} verres aujourd'hui. Objectif : 8. Mathématiques simples."
    ],
    'cooling_mode': [
        "Silence radio détecté. Je repasse en veille. Demain est un nouveau jour.",
        "Inactivité prolongée. Je respecte ton espace. Reviens quand tu es prêt."
    ],
    'error_graceful': [
        "Mon cerveau positronique a un hoquet. Essaie /help.",
        "Erreur temporaire. Je ne suis pas parfait. Toi non plus. On fait avec."
    ]
}
```

**Logging & Monitoring:**

Tous les fallbacks sont loggés pour détecter les patterns :

```python
# Si >10% des requêtes fallback, alerte
fallback_rate = fallback_count / total_requests
if fallback_rate > 0.10:
    send_alert("High fallback rate: {}%".format(fallback_rate * 100))
```

**Rationale:**

- **3 secondes Gemini** : Laisse 2s de marge pour autres opérations DB et reste <5s total
- **Templates TARS** : Maintient la cohérence du persona même en fallback
- **Hardcoded** : Garantit TOUJOURS une réponse (NFR2 à 100%)
- **Logging** : Permet de détecter dégradations de service Gemini

**Consequences:**

✅ **Positives:**
- Garantie 100% de réponse (NFR2 respecté)
- Latence <5s même en fallback (NFR4 respecté)
- Persona cohérent TARS maintenu
- Observabilité complète via logs

⚠️ **Négatives:**
- Maintenance de templates nécessaire (mais rare)
- Expérience légèrement dégradée en fallback (acceptable temporairement)

**Monitoring Thresholds:**
- Fallback rate >5% : Warning log
- Fallback rate >10% : Alert (vérifier quota Gemini ou connectivité)
- Fallback rate >25% : Critical (Gemini API probablement down)

---

### ADR-005: UTC Storage with Timezone Conversion

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Les rappels via GitHub Actions CRON s'exécutent en UTC. L'utilisateur est en Europe/Paris (UTC+1/+2 selon DST). Les "Success Days" dépendent du jour local de l'utilisateur.

**Decision:**

- Stocker le timezone utilisateur en DB (`users.timezone`)
- Stocker TOUS les timestamps en UTC (`TIMESTAMPTZ` PostgreSQL)
- Convertir à la présentation et lors des calculs de Success Days

**Implementation Pattern:**

```python
from datetime import datetime
import pytz

# Récupération user timezone
user_tz = pytz.timezone(user.timezone)  # 'Europe/Paris'

# Stockage en UTC
created_at = datetime.utcnow()  # Toujours UTC
db.insert(check_in, created_at=created_at)

# Présentation en timezone local
local_time = created_at.astimezone(user_tz)
message = f"Check-in enregistré à {local_time.strftime('%H:%M')}"

# Calcul Success Day (selon jour local)
local_date = datetime.now(user_tz).date()
stats = db.query(daily_stats).filter(date=local_date).first()
```

**GitHub Actions CRON Conversion:**

```yaml
# Rappel "Micro-Win" à 6h heure locale (Europe/Paris)
# Paris = UTC+1 (hiver) ou UTC+2 (été)

# Hiver (Nov-Mars) : 6h Paris = 5h UTC
- cron: '0 5 * * *'

# Été (Avr-Oct) : 6h Paris = 4h UTC  
- cron: '0 4 * * *'

# Alternative : Calcul dynamique en Python
reminder_time_utc = datetime.now(user_tz).replace(hour=6, minute=0)
                            .astimezone(pytz.UTC)
```

**Success Day Logic:**

```python
def calculate_success_day(user_id: str, date: datetime.date) -> bool:
    """
    Success Day = 100% des objectifs critiques complétés
    Calculé selon le jour LOCAL de l'utilisateur
    """
    user = db.get_user(user_id)
    user_tz = pytz.timezone(user.timezone)
    
    # Début et fin du jour en heure locale
    day_start = user_tz.localize(datetime.combine(date, time.min))
    day_end = user_tz.localize(datetime.combine(date, time.max))
    
    # Conversion en UTC pour requête DB
    day_start_utc = day_start.astimezone(pytz.UTC)
    day_end_utc = day_end.astimezone(pytz.UTC)
    
    # Check-ins du jour (selon timezone local)
    checkins = db.query(check_ins).filter(
        created_at >= day_start_utc,
        created_at <= day_end_utc
    ).all()
    
    # Logique Success Day
    completion_rate = calculate_completion(checkins)
    return completion_rate >= 1.0  # 100%
```

**Edge Cases Handled:**

1. **Check-in à 23h59 vs 00h01** : Compté dans le bon jour local
2. **Changement d'heure DST** : pytz gère automatiquement
3. **Voyage/changement timezone** : L'utilisateur peut UPDATE `users.timezone`, stats recalculées correctement
4. **CRON en UTC** : Conversion faite au moment du scheduling

**Rationale:**

- **Standard industrie** : Stocker en UTC, afficher en local
- **Évite les bugs DST** : PostgreSQL TIMESTAMPTZ + pytz gèrent automatiquement
- **Success Days corrects** : Calculés selon jour civil local, pas UTC
- **CRON fiables** : GitHub Actions en UTC, conversion explicite

**Consequences:**

✅ **Positives:**
- Timestamps non ambigus (UTC universel)
- Success Days calculés correctement selon jour local
- Support DST automatique
- Pattern standard bien documenté

⚠️ **Négatives:**
- Nécessite conversion explicite à chaque présentation (mais pattern simple)
- CRON doivent être ajustés manuellement pour DST (ou calculés dynamiquement)

**Testing Strategy:**
```python
def test_success_day_across_timezones():
    # Check-in à 23h59 Paris le 5 février
    checkin_time = datetime(2026, 2, 5, 22, 59, tzinfo=pytz.UTC)  # 23h59 Paris
    
    # Doit compter pour le 5 février, pas le 6
    assert get_checkin_date(checkin_time, 'Europe/Paris') == date(2026, 2, 5)
    
    # Check-in à 00h01 Paris le 6 février  
    checkin_time = datetime(2026, 2, 5, 23, 1, tzinfo=pytz.UTC)  # 00h01 Paris
    
    # Doit compter pour le 6 février
    assert get_checkin_date(checkin_time, 'Europe/Paris') == date(2026, 2, 6)
```

---

## Implementation Patterns & Consistency Rules

Pour garantir la pérennité du projet "Focus & Flow" et éviter les conflits lors de l'intervention de multiples agents IA, les standards suivants sont obligatoires :

### 📏 Conventions de Nommage & Structure
*   **Case Convention** :
    *   **Python/DB/API JSON** : Strict `snake_case` (variables, fonctions, colonnes, champs JSON).
    *   **Classes & Types Pydantic** : `PascalCase`.
*   **Service-Layer Architecture (Atomic Services)** :
    *   `app/api/` : Les routes valident les entrées (Pydantic) et délèguent immédiatement aux services.
    *   `app/services/` : Les services sont **atomiques** (ne s'appellent pas entre eux). La coordination transverse s'effectue dans un **Orchestrateur** ou directement dans la route API.
    *   `app/schemas/` : Centralise tous les modèles Pydantic pour éviter les redéfinitions.

### 🛡️ Gestion des Erreurs & Réponses
*   **Unified Response Format** :
    ```json
    {
      "success": true,
      "data": { ... },
      "meta": { "tars_tone": "analytical", "update_id": 12345 }
    }
    ```
*   **TARS Middleware** : Un middleware global intercepte les exceptions imprévues pour s'assurer que l'utilisateur reçoit toujours un message de désolation du bot au lieu d'un silence radio.

### 🕒 Types, Dates & Validation
*   **Strict ISO 8601** : Toutes les dates échangées via l'API doivent être des chaînes ISO 8601 avec le suffixe `Z` (UTC).
*   **Pydantic strict** : Utilisation systématique de `ConfigDict(from_attributes=True)` pour valider les données issues de Supabase.

### 🤖 TARS Persona Engine
*   **Prompt Centralization** : La logique "âme" de TARS et l'assemblage des prompts Gemini résident exclusivement dans `app/core/personality.py`. Aucun "hardcoding" de prompt n'est autorisé dans les services métier.

### 📋 Observabilité
*   **Correlation ID** : L'ID de l'update Telegram (`update_id`) doit être injecté dans le contexte de logging de chaque requête pour permettre un traçage complet (API → Service → DB → IA).

---

## Project Structure & Boundaries

La structure physique du projet est conçue pour être "Lean" (légère pour les ressources Render et la compréhension IA) tout en étant "Pro" (rigoureuse sur le versioning et la sécurité).

### 🏆 Arborescence de Synthèse (Lean-Pro)

```text
focus_flow/
├── app/
│   ├── api/                       <-- Routes (préfixées /api/v1 dans le code)
│   │   ├── bot.py                 <-- Webhook Telegram (NLU + Orchestration)
│   │   ├── maintenance.py         <-- Rappels, Sweeper, Healthchecks
│   │   └── crud.py                <-- Endpoints techniques (User, Stats)
│   ├── core/
│   │   ├── config.py              <-- Secrets & Settings
│   │   ├── security.py            <-- 🛡️ Centralisation de la vérification des tokens
│   │   └── personality.py         <-- L'âme de TARS (Prompts Gemini)
│   ├── db/
│   │   ├── client.py              <-- Connexion Supabase
│   │   └── migrations/            <-- 📜 RIGUEUR : Historique du schéma SQL
│   │       ├── 001_initial.sql
│   │       └── 002_add_timezone.sql
│   ├── schemas/                   <-- 🧱 RIGUEUR : Un fichier par domaine
│   │   ├── habit.py
│   │   ├── user.py
│   │   └── objective.py
│   ├── services/                  <-- Les "Cerveaux" consolidés
│   │   ├── ai_engine.py           <-- Gemini integration & Anonymisation
│   │   └── habit_manager.py       <-- Logique métier (Données & Calculs)
│   └── main.py                    <-- Point d'entrée principal FastAPI
├── .github/workflows/             <-- 🤖 Automatisation (Rappels/Sweeper)
│   ├── deploy.yml
│   └── cron_tasks.yml
├── .gitignore                     <-- 🛡️ Exclusion stricte (.env, venv, etc.)
├── Dockerfile                     <-- Déploiement Render
├── requirements.txt               <-- Dépendances consolidées
└── .env.example                   <-- Template de configuration
```

### 📋 Directives de Cohérence pour les Développeurs (IA)

1.  **Versioning des Données** : Tout changement de structure SQL DOIT être consigné dans `app/db/migrations/` avec un fichier numéroté.
2.  **API Prefixing** : Toutes les instances `APIRouter` doivent être montées sous le préfixe `/api/v1`.
3.  **Habilitations & Sécurité** :
    *   Aucune route n'est accessible sans validation du secret token via `app/core/security.py`.
    *   Interdiction de logguer toute donnée sensible ou header HTTP (PII-Scrubbing).
4.  **Isolation des Services** : Utiliser le pattern "Atomic Services" défini à l'Étape 5. Pas d'appels circulaires entre services.
5.  **Git Workflow** : Les développeurs poussent leurs modifications directement sur GitHub (branches `feature/*`). Pull Requests vers `develop` requises. Merge vers `main` déclenche le déploiement automatique sur Render (pas d'intervention manuelle).

---

## Architecture Validation Summary

L'architecture de **Focus & Flow** a été soumise à une revue complète de cohérence et de couverture.

### ✅ État de la Validation
*   **Cohérence Interne** : PASS (Aucun conflit identifié entre FastAPI, Supabase et Gemini).
*   **Couverture Fonctionnelle** : 100% (Les 17 FR sont mappés à des composants spécifiques).
*   **Respect des NFR** : 100% (Stratégies "Zero-Cost", "Offline-Resilience" et "Persona-Consistency" validées).
*   **Précision des Patterns** : PASS (Règles de nommage, Atomic Services et Security Middleware définis).

### 🎯 Prochaines Étapes critiques pour l'implémentation
1.  **Initialisation DB** : Exécuter `001_initial.sql` dans l'éditeur SQL de Supabase.
2.  **Health Check** : Développer l'endpoint `/api/v1/self_test` en premier pour valider la connectivité globale.
3.  **TARS Core** : Stabiliser `app/core/personality.py` avant de déléguer la création des services à d'autres agents.

---

### ADR-007: Git Workflow & Autonomous Deployment with Approval Gates

**Status:** ✅ Accepted  
**Date:** 2026-02-06  
**Deciders:** Billux + Architect (Winston)

**Context:**

Le projet nécessite un workflow Git clair pour coordonner le travail de plusieurs agents IA développeurs tout en maintenant la qualité du code et la stabilité de la production. La documentation existante (BRANCHING_STRATEGY.md, GITHUB_SETUP.md, CODE_STYLE.md) définit des pratiques, mais elles doivent être consolidées dans une ADR pour garantir leur respect strict.

**Decision:**

Adopter un workflow Git Flow avec déploiement automatique sur Render, incluant des **gates d'approbation obligatoires** avant tout push.

**Workflow Standard:**

1. **Développement sur branches features** :
   - Format : `feature/story-X-Y-description`
   - Créées depuis `develop`
   - Commits suivant Conventional Commits (feat, fix, docs, etc.)

2. **Pull Request obligatoire** :
   - Toute modification doit passer par une PR vers `develop`
   - ⚠️ **GATE 1** : Les développeurs (agents IA) DOIVENT demander l'approbation de Billux avant de créer la PR
   - Review requise (minimum 1 approbation)
   - Tests CI/CD doivent passer (GitHub Actions)

3. **Merge vers develop** :
   - Après approbation de la PR
   - ⚠️ **GATE 2** : Confirmation explicite de Billux avant le merge

4. **Déploiement production** :
   - Merge de `develop` vers `main` déclenche automatiquement le déploiement sur Render
   - ⚠️ **GATE 3** : Billux valide explicitement le merge vers `main` (déploiement production)

**Rationale:**

- **Contrôle qualité** : Les gates d'approbation garantissent que Billux valide chaque changement avant intégration et déploiement.
- **Traçabilité** : Tout le code est versionné sur GitHub avec historique complet.
- **Automatisation sécurisée** : Le déploiement reste automatique (pas de manipulation manuelle sur Render) mais contrôlé par le workflow Git.
- **Collaboration IA** : Les agents développeurs respectent un processus uniforme et ne peuvent pas pousser sans autorisation.

**Consequences:**

✅ **Positives:**
- Aucun code non validé ne peut atteindre la production
- Historique Git complet pour audit et rollback
- Déploiement automatique (pas de tâches manuelles post-merge)
- Protection contre les erreurs d'agents IA autonomes

⚠️ **Négatives:**
- Billux doit être disponible pour valider chaque PR (délai potentiel)
- Processus légèrement plus long qu'un push direct

**Implementation Details:**

Les agents développeurs doivent systématiquement :
1. Annoncer leur intention de créer une PR avec résumé des changements
2. Attendre la réponse "Approved" de Billux avant `git push`
3. Ne jamais forcer un push (`git push --force`) sans autorisation explicite
4. Respecter les templates de PR (description, checklist, tests)

**Compliance:**
- ✅ Aligne avec BRANCHING_STRATEGY.md (Git Flow)
- ✅ Aligne avec GITHUB_SETUP.md (PR process)
- ✅ Aligne avec CODE_STYLE.md (Conventional Commits)

---

### Future Evolution Path

**Phase 1 (MVP):** Python/Render + GitHub Actions (actuel)
**Phase 2 (Si cold starts deviennent problématiques):** 
- Migration vers Supabase Edge Functions (TypeScript)
- Ou VPS payant 5€/mois si Python préféré
**Phase 3 (Production robuste):**
- Monitoring (Uptime Robot gratuit)
- Alerting (email sur failures)
- Backup automatisé Supabase

---

### ADR-006: Backend Inaccessibility Handling (Offline Strategy)

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Dans une architecture serverless/PaaS gratuite (Render), il existe un risque (faible mais réel) que le backend Python soit totalement inaccessible :
1. Panne complète de Render.
2. Épuisement des 750h gratuites (si mal géré).
3. Erreur critique lors d'un déploiement automatique.

**Decision:**

Implémenter une stratégie de résilience à deux niveaux pour éviter l'effet "trou noir" où l'utilisateur n'obtient aucune réponse.

**Level 1: Telegram Webhook Timeouts**
Telegram réessaie d'envoyer les webhooks pendant 24h si le serveur renvoie une erreur (5xx) ou est injoignable.
- **Action** : Le bot "récupérera" les messages manqués dès que Render sera de nouveau en ligne.

**Level 2: User Communication (Graceful Degradation)**
En cas d'échec de connexion prolongé vers Render (détecté par les GitHub Actions de rappels) :
- **Action** : Envoyer une notification directe via une GitHub Action de secours (qui n'utilise pas le backend Render) pour prévenir l'utilisateur que TARS est en maintenance.

**Rationale:**

- Garantir que l'utilisateur n'est pas ignoré, même en cas de crash infrastructure.
- S'appuyer sur la résilience native de Telegram (retries automatiques).
- Utiliser la séparation des services (GitHub Actions vs Render) comme un avantage de disponibilité.

**Consequences:**

✅ **Positives:**
- Pas de perte de données (Telegram stocke les messages non délivrés temporairement).
- Transparence vis-à-vis de l'utilisateur.
- Respect de la philosophie "robuste" du projet.

⚠️ **Négatives:**
- Le "typing indicator" peut tourner dans le vide si le serveur est totalement down avant l'envoi du message de statut.

**Compliance:**
- ✅ NFR2 (Robustesse): Assure la continuité de service même en cas de défaillance majeure.

---

## Architecture Decision Records (ADRs)

### ADR-001: Backend Hosting on Render Free Tier Without Keepalive

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Le système nécessite un backend pour gérer les webhooks Telegram, appeler l'API Gemini, et interagir avec Supabase. La contrainte NFR1 (Zero Cost) limite les options d'hébergement. Trois approches ont été évaluées.

**Decision:**

Utiliser Python (FastAPI ou Flask) hébergé sur Render free tier, SANS système de keepalive, en acceptant les cold starts de 30-60s avec feedback UX approprié.

**Alternatives Considered:**

1. **VPS Payant (DigitalOcean/Hetzner)** : 5-10€/mois, latence constante <2s, mais viole NFR1 (Zero Cost). ❌ Rejeté.

2. **Supabase Edge Functions** : 0€, latence 1-2s, serverless natif avec pg_cron, mais nécessite apprentissage TypeScript et perçu comme complexe pour RLS policies. ⚠️ Différé à Phase 2.

3. **Render + Keepalive GitHub Actions** : 0€, maintient le serveur chaud avec 73 pings/jour (1,095 min/mois), mais complexité accrue, consommation réseau inutile, et dépendance sur la fiabilité des CRON. ❌ Rejeté pour simplicité.

**Rationale:**

Via First Principles Analysis, nous avons déconstruit l'hypothèse que "le cold start est un problème" :

- **Rappels proactifs (80% interactions)** : Le cold start se produit AVANT l'envoi de la notification Telegram. L'utilisateur ne le voit jamais.
- **Messages utilisateur (20% interactions)** : La nature asynchrone du coaching rend acceptable un délai de 30-60s. Telegram montre "typing..." pendant le traitement.
- **Fréquence limitée** : Maximum 2-3 cold starts/jour (matin, après-midi si inactif).
- **UX masque la latence** : Messages temporaires ("🤖 TARS analyse... Un instant.") édités ensuite avec la réponse finale.

L'utilisateur a explicitement confirmé : "Je ne suis pas à la minute près" et "1 min de délai ne me pose aucun problème".

**Consequences:**

✅ **Positives:**
- Simplicité architecturale maximale (5 composants au lieu de 6 avec keepalive)
- Python familier = développement rapide du MVP
- Budget GitHub Actions libéré : 1,600+ min/mois disponibles pour features futures
- Zero maintenance du keepalive
- Architecture écologique (serveur ne consomme que quand utilisé)

⚠️ **Négatives:**
- Latence variable (2s chaud, 30-60s froid)
- Pas de SLA sur Render free tier (acceptable pour usage personnel)
- Dépendance sur la fiabilité de Render (peut redémarrer sans prévenir)

**Compliance:**
- ✅ NFR1 (Zero Cost): Respecté à 100%
- ✅ NFR2 (Robustesse): Templates fallback garantissent 100% réponse
- ✅ NFR3 (Confidentialité): Instance privée mono-utilisateur
- ✅ NFR4 (Latence): <5s serveur chaud, <60s cold start avec UX acceptable
- ✅ NFR5 (Précision): GitHub Actions CRON suffisant pour ±2 min

**Notes:**
Migration vers Edge Functions reste une option documentée pour Phase 2 si les besoins évoluent.

---

### ADR-002: Authentication via Telegram ID Only

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Le système doit identifier l'utilisateur pour toutes les opérations. Étant une instance mono-utilisateur, la complexité d'authentification doit être minimisée sans compromettre la sécurité.

**Decision:**

Utiliser uniquement le `telegram_id` comme identifiant utilisateur, avec vérification de la signature des webhooks Telegram via le secret token.

**Alternatives Considered:**

1. **OAuth 2.0** : Standard industrie, mais overkill pour mono-utilisateur. Ajouterait complexité sans bénéfice. ❌ Rejeté.

2. **JWT Tokens** : Génération et validation de tokens, mais inutile quand Telegram gère déjà l'authentification. ❌ Rejeté.

3. **Password-based auth** : Nécessiterait un système de login séparé, violant l'objectif de "friction minimale". ❌ Rejeté.

**Rationale:**

- Telegram vérifie l'authentification côté serveur. Impossible de forger un `update` Telegram avec un faux `user_id`.
- Le webhook est signé avec un secret token (vérifié par le backend).
- Instance mono-utilisateur = pas de risque de collision d'identifiants.
- Simplicité maximale : zéro code d'authentification à maintenir.

**Implementation Details:**

```python
# Vérification signature webhook
def verify_telegram_webhook(request):
    secret_token = os.getenv('TELEGRAM_SECRET_TOKEN')
    provided_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    return hmac.compare_digest(secret_token, provided_token)

# Extraction user_id
user_id = update['message']['from']['id']
```

**Consequences:**

✅ **Positives:**
- Architecture simple sans couche auth complexe
- Zero overhead de performance
- Sécurité garantie par Telegram
- Code minimal à maintenir

⚠️ **Négatives:**
- Dépendance complète sur la sécurité de Telegram (acceptable car Telegram est un système robuste)
- Migration difficile si passage multi-utilisateur futur (mais hors scope)

**Security Measures:**
- Secret token stocké en variable d'environnement Render (jamais dans le code)
- Vérification systématique de la signature sur chaque webhook
- Logging des tentatives d'accès non autorisées

---

### ADR-003: Pure Relational Database Schema (No JSONB)

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Le modèle de données du PRD mentionne `preferences` (JSON) et `frequency_config` (CRON-like JSON). Débat entre utiliser JSONB pour flexibilité vs colonnes strictes pour validation.

**Decision:**

Utiliser un schéma relationnel strict avec colonnes typées, SANS JSONB. Les habitudes et préférences sont modélisées comme des lignes dans des tables dédiées, pas comme des colonnes dans `users`.

**Alternatives Considered:**

1. **Hybrid (Colonnes + JSONB pour flexibilité)** : Colonnes pour données core + `preferences JSONB` et `frequency_config JSONB`. Flexible mais perd la validation PostgreSQL. ❌ Rejeté.

2. **Entity-Attribute-Value (EAV)** : Table `user_preferences` avec (key, value) pour éviter migrations. Flexible mais perte totale de typage, requêtes complexes, 4x plus de storage. ❌ Rejeté.

3. **Pure Relationnel (CHOISI)** : Colonnes strictes pour préférences, table `habit_schedules` pour fréquences. Simple, performant, validé par PostgreSQL. ✅ Accepté.

**Rationale:**

**Débat d'experts - Points clés :**

- **Validation automatique** : PostgreSQL valide les types (INTEGER, BOOLEAN, TIME). Avec JSONB, tout est TEXT, bugs silencieux possibles.
- **Performance** : Requêtes simples avec colonnes vs requêtes complexes avec opérateurs JSONB (`->`, `@>`).
- **Storage efficiency** : Colonnes typées = 100 bytes vs JSONB = 400 bytes pour même données (4x plus efficace).
- **Debugging** : `SELECT timezone FROM users` vs `SELECT preferences->>'timezone' FROM users` - lequel préférez-vous à 23h ?

**Malentendu clarifié :**

L'utilisateur pensait que chaque habitude nécessiterait une nouvelle colonne (migration). FAUX. Les habitudes sont des LIGNES dans la table `habits`. Ajouter une habitude = INSERT (requête normale), pas ALTER TABLE (migration).

**Migrations réelles (rares) :**

- Ajout d'une nouvelle colonne à `users` (ex: `preferred_language`) : 2-3 fois/an maximum
- Création d'une nouvelle table (ex: `user_achievements`) : 1 fois tous les 6 mois
- Ces opérations prennent 3 secondes avec Supabase SQL Editor

**Schema Design:**

```sql
-- Users : Colonnes strictes pour préférences
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  telegram_id BIGINT UNIQUE NOT NULL,
  timezone TEXT NOT NULL DEFAULT 'UTC',
  humor_level INTEGER CHECK (humor_level BETWEEN 1 AND 10) DEFAULT 8,
  cooling_enabled BOOLEAN DEFAULT true,
  notification_start TIME DEFAULT '06:00',
  notification_end TIME DEFAULT '23:00',
  status TEXT CHECK (status IN ('active', 'pause', 'cooling')) DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habits : Lignes dynamiques (pas de colonnes par habitude)
CREATE TABLE habits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  frequency_type TEXT CHECK (frequency_type IN ('daily', 'weekly', 'custom')) NOT NULL,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habit Schedules : Récurrences flexibles
CREATE TABLE habit_schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  habit_id UUID REFERENCES habits(id) ON DELETE CASCADE,
  day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),  -- NULL pour daily
  time_of_day TIME NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(habit_id, day_of_week, time_of_day)
);

-- Objectives
CREATE TABLE objectives (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  deadline TIMESTAMPTZ NOT NULL,
  status TEXT CHECK (status IN ('pending', 'completed', 'failed')) DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Check-ins : Traçabilité des actions
CREATE TABLE check_ins (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  ref_id UUID NOT NULL,
  ref_type TEXT CHECK (ref_type IN ('habit', 'objective')) NOT NULL,
  value INTEGER,  -- Pour quantités (verres d'eau, pompes)
  completed BOOLEAN DEFAULT false,
  sentiment TEXT,  -- Ressenti court
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Daily Stats : Agrégations quotidiennes
CREATE TABLE daily_stats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  completion_rate FLOAT CHECK (completion_rate BETWEEN 0 AND 100),
  is_success_day BOOLEAN DEFAULT false,
  micro_win_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date)
);
```

**Usage Examples:**

```sql
-- Ajouter habitude "Lecture" (requête normale, PAS migration)
INSERT INTO habits (user_id, title, frequency_type) 
VALUES ('billux-uuid', 'Lecture', 'daily');

-- Changer Sport de 3x/semaine à 5x/semaine (requêtes normales)
DELETE FROM habit_schedules WHERE habit_id = 'sport-uuid';
INSERT INTO habit_schedules (habit_id, day_of_week, time_of_day) VALUES
  ('sport-uuid', 0, '07:00'),  -- Lundi
  ('sport-uuid', 2, '07:00'),  -- Mercredi
  ('sport-uuid', 3, '07:00'),  -- Jeudi
  ('sport-uuid', 4, '07:00'),  -- Vendredi
  ('sport-uuid', 6, '07:00');  -- Dimanche
```

**Consequences:**

✅ **Positives:**
- Validation stricte par PostgreSQL (prévient bugs silencieux)
- Requêtes SQL simples et performantes
- Storage optimal (colonnes typées < JSONB)
- Debugging facile (colonnes explicites)
- Ajout/suppression illimités d'habitudes sans migrations
- Indexes efficaces sur toutes les colonnes

⚠️ **Négatives:**
- Nouvelles préférences système = migration DB (mais 2-3 fois/an max, 3 secondes avec Supabase)

**Indexes (Phase 2):**
```sql
CREATE INDEX idx_habits_user ON habits(user_id) WHERE active = true;
CREATE INDEX idx_schedules_time ON habit_schedules(time_of_day);
CREATE INDEX idx_checkins_date ON check_ins(created_at);
CREATE INDEX idx_daily_stats_date ON daily_stats(user_id, date);
```

---

### ADR-004: NLU Cascade with 3-Second Timeout

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

NFR2 exige "100% de réponse" même en cas d'échec API Gemini. NFR4 exige latence <5s pour serveur chaud. Besoin d'une stratégie de fallback robuste.

**Decision:**

Implémenter une cascade à 3 niveaux avec timeout strict :

1. **Gemini API** (3 secondes max) → Compréhension NLU complète
2. **Templates TARS** (fallback immédiat) → Réponses pré-écrites avec persona
3. **Hardcoded Response** (dernier recours) → Message d'erreur gracieux

**Architecture:**

```python
async def process_user_message(message: str) -> str:
    try:
        # Niveau 1 : Gemini avec timeout strict
        response = await asyncio.wait_for(
            gemini_api.generate(message),
            timeout=3.0
        )
        log_success('gemini', message)
        return response
        
    except asyncio.TimeoutError:
        log_fallback('gemini_timeout', message)
        # Niveau 2 : Templates TARS
        return get_tars_template_response(message)
        
    except Exception as e:
        log_fallback('gemini_error', message, error=e)
        # Niveau 2 : Templates TARS
        try:
            return get_tars_template_response(message)
        except Exception:
            # Niveau 3 : Hardcoded
            return "Mon cerveau positronique a un hoquet. Essaie /help ou reformule."
```

**Templates TARS Strategy:**

Templates doivent matcher le ton humoristique/analytique pour cohérence du persona :

```python
TARS_TEMPLATES = {
    'check_in_sport': [
        "Sport enregistré. Ne t'habitue pas trop aux compliments.",
        "Compris. Ton corps te remercie. Ton esprit aussi, même s'il ne l'admet pas.",
        "✅ Sport comptabilisé. Streak : {streak} jours. Impressionnant pour un humain."
    ],
    'check_in_water': [
        "Hydratation notée. Continue comme ça, tu n'es pas un cactus.",
        "{count} verres aujourd'hui. Objectif : 8. Mathématiques simples."
    ],
    'cooling_mode': [
        "Silence radio détecté. Je repasse en veille. Demain est un nouveau jour.",
        "Inactivité prolongée. Je respecte ton espace. Reviens quand tu es prêt."
    ],
    'error_graceful': [
        "Mon cerveau positronique a un hoquet. Essaie /help.",
        "Erreur temporaire. Je ne suis pas parfait. Toi non plus. On fait avec."
    ]
}
```

**Logging & Monitoring:**

Tous les fallbacks sont loggés pour détecter les patterns :

```python
# Si >10% des requêtes fallback, alerte
fallback_rate = fallback_count / total_requests
if fallback_rate > 0.10:
    send_alert("High fallback rate: {}%".format(fallback_rate * 100))
```

**Rationale:**

- **3 secondes Gemini** : Laisse 2s de marge pour autres opérations DB et reste <5s total
- **Templates TARS** : Maintient la cohérence du persona même en fallback
- **Hardcoded** : Garantit TOUJOURS une réponse (NFR2 à 100%)
- **Logging** : Permet de détecter dégradations de service Gemini

**Consequences:**

✅ **Positives:**
- Garantie 100% de réponse (NFR2 respecté)
- Latence <5s même en fallback (NFR4 respecté)
- Persona cohérent TARS maintenu
- Observabilité complète via logs

⚠️ **Négatives:**
- Maintenance de templates nécessaire (mais rare)
- Expérience légèrement dégradée en fallback (acceptable temporairement)

**Monitoring Thresholds:**
- Fallback rate >5% : Warning log
- Fallback rate >10% : Alert (vérifier quota Gemini ou connectivité)
- Fallback rate >25% : Critical (Gemini API probablement down)

---

### ADR-005: UTC Storage with Timezone Conversion

**Status:** ✅ Accepted  
**Date:** 2026-02-05  
**Deciders:** Billux + Panel d'experts architectes

**Context:**

Les rappels via GitHub Actions CRON s'exécutent en UTC. L'utilisateur est en Europe/Paris (UTC+1/+2 selon DST). Les "Success Days" dépendent du jour local de l'utilisateur.

**Decision:**

- Stocker le timezone utilisateur en DB (`users.timezone`)
- Stocker TOUS les timestamps en UTC (`TIMESTAMPTZ` PostgreSQL)
- Convertir à la présentation et lors des calculs de Success Days

**Implementation Pattern:**

```python
from datetime import datetime
import pytz

# Récupération user timezone
user_tz = pytz.timezone(user.timezone)  # 'Europe/Paris'

# Stockage en UTC
created_at = datetime.utcnow()  # Toujours UTC
db.insert(check_in, created_at=created_at)

# Présentation en timezone local
local_time = created_at.astimezone(user_tz)
message = f"Check-in enregistré à {local_time.strftime('%H:%M')}"

# Calcul Success Day (selon jour local)
local_date = datetime.now(user_tz).date()
stats = db.query(daily_stats).filter(date=local_date).first()
```

**GitHub Actions CRON Conversion:**

```yaml
# Rappel "Micro-Win" à 6h heure locale (Europe/Paris)
# Paris = UTC+1 (hiver) ou UTC+2 (été)

# Hiver (Nov-Mars) : 6h Paris = 5h UTC
- cron: '0 5 * * *'

# Été (Avr-Oct) : 6h Paris = 4h UTC  
- cron: '0 4 * * *'

# Alternative : Calcul dynamique en Python
reminder_time_utc = datetime.now(user_tz).replace(hour=6, minute=0)
                            .astimezone(pytz.UTC)
```

**Success Day Logic:**

```python
def calculate_success_day(user_id: str, date: datetime.date) -> bool:
    """
    Success Day = 100% des objectifs critiques complétés
    Calculé selon le jour LOCAL de l'utilisateur
    """
    user = db.get_user(user_id)
    user_tz = pytz.timezone(user.timezone)
    
    # Début et fin du jour en heure locale
    day_start = user_tz.localize(datetime.combine(date, time.min))
    day_end = user_tz.localize(datetime.combine(date, time.max))
    
    # Conversion en UTC pour requête DB
    day_start_utc = day_start.astimezone(pytz.UTC)
    day_end_utc = day_end.astimezone(pytz.UTC)
    
    # Check-ins du jour (selon timezone local)
    checkins = db.query(check_ins).filter(
        created_at >= day_start_utc,
        created_at <= day_end_utc
    ).all()
    
    # Logique Success Day
    completion_rate = calculate_completion(checkins)
    return completion_rate >= 1.0  # 100%
```

**Edge Cases Handled:**

1. **Check-in à 23h59 vs 00h01** : Compté dans le bon jour local
2. **Changement d'heure DST** : pytz gère automatiquement
3. **Voyage/changement timezone** : L'utilisateur peut UPDATE `users.timezone`, stats recalculées correctement
4. **CRON en UTC** : Conversion faite au moment du scheduling

**Rationale:**

- **Standard industrie** : Stocker en UTC, afficher en local
- **Évite les bugs DST** : PostgreSQL TIMESTAMPTZ + pytz gèrent automatiquement
- **Success Days corrects** : Calculés selon jour civil local, pas UTC
- **CRON fiables** : GitHub Actions en UTC, conversion explicite

**Consequences:**

✅ **Positives:**
- Timestamps non ambigus (UTC universel)
- Success Days calculés correctement selon jour local
- Support DST automatique
- Pattern standard bien documenté

⚠️ **Négatives:**
- Nécessite conversion explicite à chaque présentation (mais pattern simple)
- CRON doivent être ajustés manuellement pour DST (ou calculés dynamiquement)

**Testing Strategy:**
```python
def test_success_day_across_timezones():
    # Check-in à 23h59 Paris le 5 février
    checkin_time = datetime(2026, 2, 5, 22, 59, tzinfo=pytz.UTC)  # 23h59 Paris
    
    # Doit compter pour le 5 février, pas le 6
    assert get_checkin_date(checkin_time, 'Europe/Paris') == date(2026, 2, 5)
    
    # Check-in à 00h01 Paris le 6 février  
    checkin_time = datetime(2026, 2, 5, 23, 1, tzinfo=pytz.UTC)  # 00h01 Paris
    
    # Doit compter pour le 6 février
    assert get_checkin_date(checkin_time, 'Europe/Paris') == date(2026, 2, 6)
```

