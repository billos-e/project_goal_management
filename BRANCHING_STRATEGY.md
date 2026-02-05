# Git Branching Strategy - Focus & Flow

## Overview

We use **Git Flow** branching model for organized development workflow.

### Branch Types

```
main ────────────────────── Production-ready releases
    ↑
develop ──────────────────── Integration & testing branch
    ↑
feature/story-* ─────────── New features for each story
bugfix/issue-* ──────────── Bug fixes
hotfix/issue-* ──────────── Urgent production fixes
release/vX.Y.Z ──────────── Release preparation
```

---

## Branch Naming Convention

### Feature Branches

**Format:** `feature/story-<EPIC>-<STORY>-<description>`

```bash
# Story 1.1: Infrastructure
feature/story-1-1-infrastructure

# Story 1.2: Telegram Webhook
feature/story-1-2-telegram-webhook

# Story 2.1: Habits CRUD
feature/story-2-1-habits-crud

# Story 5.2: Export Data
feature/story-5-2-export-data
```

### Bug Fix Branches

**Format:** `bugfix/issue-<NUMBER>-<description>`

```bash
bugfix/issue-42-health-check-timeout
bugfix/issue-123-database-connection-leak
```

### Hotfix Branches

**Format:** `hotfix/issue-<NUMBER>-<description>`

```bash
hotfix/issue-456-production-crash
hotfix/issue-789-security-vulnerability
```

### Release Branches

**Format:** `release/v<MAJOR>.<MINOR>.<PATCH>`

```bash
release/v1.0.0
release/v1.1.0
release/v2.0.0-beta.1
```

---

## Workflow for Story Development

### Phase 1: Create Feature Branch

```bash
# Ensure develop is up to date
git checkout develop
git pull origin develop

# Create feature branch for Story 1.1
git checkout -b feature/story-1-1-infrastructure

# Push to GitHub to enable CI/CD
git push -u origin feature/story-1-1-infrastructure
```

### Phase 2: Development with Commits

**Make changes and commit with Conventional Commits format:**

```bash
# First commit: Project structure
git add app/
git commit -m "feat(infrastructure): initialize FastAPI application

- Create app package with __init__.py
- Add main.py as FastAPI entry point
- Configure uvicorn ASGI server
- Add structured logging setup

Relates to Story 1.1"

# Second commit: Configuration
git add app/config.py
git commit -m "feat(infrastructure): add Pydantic-based configuration

- Support .env file loading
- Define all required environment variables
- Support development and production modes
- Add type hints and validation

Relates to Story 1.1"

# Third commit: Database connection
git add app/services/database.py
git commit -m "feat(database): add Supabase connection setup

- Initialize Supabase client with connection pooling
- Add connection health check query
- Implement exponential backoff retry strategy
- Handle connection errors gracefully

Relates to Story 1.1"

# Fourth commit: Health check endpoints
git add app/routes/health.py
git commit -m "feat(health): add health check endpoints

- Implement GET /health for liveness probe
- Implement GET /health/detailed with component status
- Include database connectivity check
- Add proper error handling and response format

Relates to Story 1.1"

# Fifth commit: Tests
git add tests/
git commit -m "test(health): add comprehensive health check tests

- Test /health endpoint returns correct status
- Test /health/detailed includes all components
- Mock database failures and verify fallback
- Add fixtures for reusable test data

Relates to Story 1.1"

# Push commits as you go
git push origin feature/story-1-1-infrastructure
```

### Phase 3: Prepare for Pull Request

```bash
# Ensure your branch is up to date with develop
git fetch origin
git rebase origin/develop

# If conflicts occur, resolve them:
# 1. Fix conflicts in files
# 2. Stage resolved files: git add <file>
# 3. Continue rebase: git rebase --continue

# Push (may need force push after rebase)
git push origin feature/story-1-1-infrastructure
```

### Phase 4: Create Pull Request

**On GitHub:**

1. Go to repository homepage
2. Click "Compare & pull request" on the feature branch banner
3. Or navigate to Pull Requests → New Pull Request

**Configuration:**
- **Base:** `develop` (integration branch)
- **Compare:** `feature/story-1-1-infrastructure` (your feature)
- **Title:** Story 1.1: Initialisation de l'infrastructure & Cœur FastAPI
- **Description:** Fill the template

**PR Template:**

```markdown
## 📋 Description

Implements **Story 1.1: Initialisation de l'infrastructure & Cœur FastAPI** from Epic 1.

This PR sets up the FastAPI project structure with:
- FastAPI application initialization
- Supabase database connection
- Health check endpoints for monitoring
- Production-ready project structure
- Render deployment configuration

## 🔧 Type of Change

- [x] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactor
- [ ] Performance improvement

## ✅ Testing Performed

- [x] Unit tests: `pytest` (all tests pass)
- [x] Manual testing on local machine
- [x] Tested with Render free tier
- [x] Verified Supabase connection
- [x] Health check endpoints functional

## 📊 Code Quality

- [x] Code formatted with Black: `black app/`
- [x] Linting passes: `pylint app/` (score >8.0)
- [x] Type hints on all functions
- [x] Docstrings on all public functions
- [x] No unused imports
- [x] No secrets in code

## 📝 Related Issue

Closes #1 (Story 1.1)

## 🚀 Deployment Notes

- Environment variables: See `.env.example`
- Render: Push to `main` branch to trigger production deploy
- Database: Supabase project configured and tested
- Python 3.11 required

## 📋 Checklist

- [x] README updated (if applicable)
- [x] Documentation updated (if applicable)
- [x] Tests written and passing
- [x] No breaking changes
- [x] Conventional commit messages used
- [x] Code review requested
```

### Phase 5: Address Review Feedback

```bash
# If reviewer requests changes:

# 1. Make changes on your branch
vim app/main.py

# 2. Commit the fix
git add app/main.py
git commit -m "fix(infrastructure): handle database timeout in health check

Respond to review feedback: Add timeout handling with
exponential backoff instead of failing immediately.

Review: PR#42, comment on line 123"

# 3. Push the new commit
git push origin feature/story-1-1-infrastructure

# GitHub will automatically update the PR
# Do NOT force push (keeps review history intact)
```

### Phase 6: Merge to Develop

**After PR approval:**

```bash
# Option A: Merge via GitHub (recommended)
# Click "Merge pull request" on GitHub web interface
# Choose merge strategy: "Create a merge commit"

# Option B: Merge locally
git checkout develop
git pull origin develop
git merge --no-ff feature/story-1-1-infrastructure
git push origin develop

# Option C: Squash commits before merge (if preferred)
git merge --squash feature/story-1-1-infrastructure
git commit -m "feat: implement story 1.1 infrastructure

Merged PR#42: Initialisation de l'infrastructure & Cœur FastAPI"
git push origin develop
```

### Phase 7: Cleanup

```bash
# Delete feature branch locally
git branch -d feature/story-1-1-infrastructure

# Delete feature branch on GitHub
git push origin --delete feature/story-1-1-infrastructure

# Update local develop branch
git checkout develop
git pull origin develop
```

---

## Commit Message Format

### Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Components

**Type** (required): Category of change
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting only (no code change)
- `refactor`: Code refactor (no functionality change)
- `perf`: Performance improvement
- `test`: Test changes
- `chore`: Dependencies, build tools, etc.
- `ci`: CI/CD configuration

**Scope** (required): What part of code is affected
- `infrastructure`: Project setup, FastAPI
- `database`: Supabase connection
- `deployment`: Render config
- `telegram`: Telegram bot
- `nlu`: NLU/AI features
- `health`: Health checks
- `auth`: Authentication/security
- `api`: API endpoints
- `models`: Data models
- `tests`: Testing infrastructure

**Subject** (required): Brief description
- Imperative mood ("add" not "added")
- Lowercase first letter
- No period at end
- Max 50 characters

### Examples

#### Example 1: Feature Implementation

```
feat(infrastructure): initialize FastAPI application structure

Create production-ready FastAPI project with:
- Main app entry point with Uvicorn server
- Environment-based configuration using Pydantic Settings
- Structured logging with JSON format output
- Support for both development and production modes

The application is ready for database connection and
Render deployment in subsequent stories.

Relates to Story 1.1
```

#### Example 2: Bug Fix

```
fix(database): handle Supabase connection timeout

The health check endpoint was failing when Supabase took
too long to respond. Now implements exponential backoff
retry strategy with max 3 attempts.

- First retry after 100ms
- Second retry after 500ms  
- Third retry after 2s
- Report unhealthy if all retries fail

Closes #42
```

#### Example 3: Documentation

```
docs(readme): add development setup instructions

Include comprehensive setup guide with:
- Virtual environment creation
- Dependency installation
- Configuration with .env file
- Running tests locally
- Deploying to Render

This helps new contributors get started quickly.
```

#### Example 4: Tests

```
test(health): add comprehensive health endpoint tests

Add tests for:
- GET /health returns 200 with correct structure
- GET /health/detailed includes all components
- Database failure detected correctly
- Component status reported accurately
- Error handling for connection issues

Use pytest fixtures to mock database and services.
Target coverage >90% on health module.

Relates to Story 1.1
```

#### Example 5: Refactor

```
refactor(models): simplify user data model

Extract common fields into base model:
- Remove duplication across User, Habit, Objective models
- Create BaseModel with created_at, updated_at
- Use inheritance for consistency
- No functional changes, improves maintainability
```

---

## Branch Protection Rules

### For `develop` Branch

Settings → Branches → Add protection rule:

- ✅ Require a pull request before merging
- ✅ Require status checks to pass
  - `Tests` workflow must pass
  - `Lint` checks must pass
- ✅ Require branches to be up to date before merging
- ✅ Dismiss stale pull request approvals
- Require 1+ approval before merge

### For `main` Branch

- ✅ Require a pull request before merging
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Dismiss stale PR approvals
- Require 2+ approvals before merge (production safety)
- ✅ Include administrators (enforce for everyone)

---

## Common Git Commands

### Setup

```bash
# Clone repository
git clone https://github.com/username/project_goal_management.git
cd project_goal_management

# Configure Git
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Feature Branch Work

```bash
# Create and switch to feature branch
git checkout -b feature/story-1-1-infrastructure

# Or: Create from remote develop
git fetch origin
git checkout --track origin/develop -b feature/story-1-1-infrastructure

# View current branch
git branch

# List all branches (local and remote)
git branch -a

# Switch to different branch
git checkout develop

# Rename current branch
git branch -m feature/old-name feature/new-name

# Delete branch locally
git branch -d feature/story-1-1-infrastructure

# Delete branch on GitHub
git push origin --delete feature/story-1-1-infrastructure
```

### Commits

```bash
# See status
git status

# Stage files for commit
git add app/
git add tests/
git add .  # Stage all changes

# Commit changes
git commit -m "feat(feature): description"

# View commit history
git log
git log --oneline
git log --oneline --graph --all

# Show specific commit
git show abc1234

# Amend last commit (before push)
git commit --amend

# Unstage file
git restore --staged filename.py

# Discard changes in file
git restore filename.py
```

### Syncing with Remote

```bash
# Fetch latest from remote (doesn't merge)
git fetch origin

# Pull latest from current branch
git pull origin develop

# Pull with rebase (cleaner history)
git pull --rebase origin develop

# Push to remote
git push origin feature/story-1-1-infrastructure

# Push with new upstream
git push -u origin feature/story-1-1-infrastructure

# Force push (use cautiously, only before review)
git push --force origin feature/story-1-1-infrastructure
```

### Rebase (Keep Clean History)

```bash
# Rebase current branch on develop
git rebase origin/develop

# If conflicts occur:
# 1. Fix conflicts in files
# 2. Stage resolved files
git add .
# 3. Continue rebase
git rebase --continue

# Or abort rebase
git rebase --abort

# Rebase and squash commits
git rebase -i origin/develop
# Select 'squash' for commits to combine
```

### Merge

```bash
# Merge feature branch into current branch
git merge feature/story-1-1-infrastructure

# Merge with merge commit (preferred for features)
git merge --no-ff feature/story-1-1-infrastructure

# Merge with squash (combine all commits)
git merge --squash feature/story-1-1-infrastructure
```

---

## Workflow Checklist for Story 1.1

- [ ] Create feature branch: `feature/story-1-1-infrastructure`
- [ ] Make code changes following CODE_STYLE.md
- [ ] Commit changes with conventional commits
- [ ] Write tests with >80% coverage
- [ ] Format code: `black app/`
- [ ] Lint code: `pylint app/` (>8.0)
- [ ] All tests pass: `pytest`
- [ ] Push branch to GitHub
- [ ] Create Pull Request to `develop`
- [ ] Request code review
- [ ] Address review feedback
- [ ] Merge after approval
- [ ] Delete feature branch
- [ ] Update sprint-status.yaml
- [ ] Proceed to next story

---

## Git Flow Diagram

```
main (production)
  ↑
  │ (merge release/PR)
  │
release/v1.0.0 ──────→ Tag v1.0.0
  ↑
  │ (create from develop)
  │
develop (integration) ──────────────┐
  ↑                                 │
  │ (merge feature/PR)              │ (merge back after release)
  │                                 │
feature/story-1-1-infrastructure    │
feature/story-1-2-telegram          │
feature/story-2-1-habits            ↓
  ...                          main (updated)


hotfix branches:
main (production) 
  ↑
  │ (urgent fix)
hotfix/issue-789 
  │ (PR to main + develop)
  ↓
main ✓
develop ✓
```

---

For more information, see:
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines
- [CODE_STYLE.md](./CODE_STYLE.md) - Python style standards
- [GitHub Docs](https://docs.github.com/en/get-started) - Official Git/GitHub docs
