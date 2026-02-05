# GitHub Repository Setup Guide - Focus & Flow

**Project:** project_goal_management (Focus & Flow)  
**Date:** 2026-02-06  
**Status:** Implementation Guide

---

## Overview

This guide establishes GitHub repository setup with professional development practices including:
- Repository initialization and structure
- Branching strategy (Git Flow)
- Commit conventions
- Code documentation standards
- CI/CD foundation
- Team workflow

---

## Step 1: Initialize GitHub Repository

### 1.1 Create Repository on GitHub

**Repository Settings:**
```
Name: project_goal_management
Description: Focus & Flow - Telegram-based productivity bot with AI coaching
Visibility: Public (or Private if preferred)
Initialize with:
  ☑ README.md
  ☑ .gitignore (Python template)
  ☐ License (MIT recommended)
```

### 1.2 Clone to Local Machine

```bash
cd ~/Documents/Projects
git clone https://github.com/[YOUR_USERNAME]/project_goal_management.git
cd project_goal_management
```

### 1.3 Verify Repository

```bash
git status
git branch -a
```

---

## Step 2: Repository Structure & Initial Files

### 2.1 Project Root Structure

```
project_goal_management/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI/CD pipeline
│   │   └── tests.yml           # Automated testing
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── app/                        # Application code
├── tests/                      # Test suite
├── docs/                       # Documentation
├── .gitignore                  # Git ignore rules
├── .gitattributes              # Git line endings
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Dev dependencies
├── Procfile                    # Render deployment
├── render.yaml                 # Render configuration
├── pyproject.toml              # Python project config
├── README.md                   # Project overview
├── CONTRIBUTING.md             # Contribution guide
├── CODE_STYLE.md               # Code style guide
└── BRANCHING_STRATEGY.md       # Git strategy document
```

### 2.2 Create .gitignore (Python + Environment)

```bash
# Create: .gitignore
```

```
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
Thumbs.db
```

### 2.3 Create .gitattributes (Line Endings)

```bash
# Create: .gitattributes
```

```
# Auto detect text files and normalize line endings to LF
* text=auto

# Python files
*.py text eol=lf
*.pyx text eol=lf
*.pxd text eol=lf
*.pxi text eol=lf

# Shell scripts
*.sh text eol=lf
*.bash text eol=lf

# Windows files
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# Documentation
*.md text eol=lf
*.rst text eol=lf
*.txt text eol=lf

# YAML
*.yaml text eol=lf
*.yml text eol=lf

# JSON
*.json text eol=lf
```

### 2.4 Create .env.example

```bash
# Create: .env.example
# Commit this file - DO NOT commit .env itself
```

```env
# Supabase Configuration
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_KEY=[anon-public-key]
SUPABASE_SERVICE_ROLE_KEY=[service-role-key]

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=[will-be-set-in-story-1.2]
TELEGRAM_WEBHOOK_SECRET=[will-be-set-in-story-1.2]

# Application Configuration
APP_NAME=focus-flow
ENVIRONMENT=production
LOG_LEVEL=INFO
TIMEZONE=Europe/Paris

# Render Configuration
PYTHON_VERSION=3.11
```

---

## Step 3: Branching Strategy (Git Flow)

### 3.1 Git Flow Overview

**Branch Structure:**

```
main (production-ready)
  ├── release/v1.0.0 (release candidate)
  ├── hotfix/issue-123 (urgent fixes)
  └── ← merged PRs from develop

develop (integration branch)
  ├── feature/story-1.1-infrastructure
  ├── feature/story-1.2-telegram-webhook
  ├── feature/story-1.3-nlu-pipeline
  └── bugfix/fix-health-check-endpoint
```

### 3.2 Create Initial Branches

```bash
# From main, create develop branch
git checkout -b develop
git push -u origin develop

# Set develop as default branch in GitHub Settings
# Settings → Branches → Default branch → develop
```

### 3.3 Protection Rules

**Configure Branch Protection on GitHub:**

**For `main` branch:**
- Require pull request reviews (minimum 1 approval)
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Dismiss stale pull request approvals
- Require code owner reviews

**For `develop` branch:**
- Require pull request reviews (minimum 1 approval)
- Require status checks to pass before merging

---

## Step 4: Commit Conventions (Conventional Commits)

### 4.1 Commit Message Format

**Standard:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Example:**
```
feat(health): add detailed health check endpoint

Add /health/detailed endpoint that checks:
- API server status
- Database connectivity
- Service dependencies

Closes #42
```

### 4.2 Commit Types

```
feat:     A new feature
fix:      A bug fix
docs:     Documentation only
style:    Changes that don't affect code meaning (formatting, whitespace)
refactor: Code change that neither fixes a bug nor adds a feature
perf:     Code change that improves performance
test:     Adding or updating tests
chore:    Changes to build process, dependencies, tools
ci:       Changes to CI/CD configuration
```

### 4.3 Scope Examples

```
Infrastructure scope:
  feat(infrastructure): FastAPI app initialization
  feat(database): Supabase connection setup
  feat(deployment): Render configuration

Feature scope:
  feat(telegram): webhook handler
  feat(nlu): Gemini integration
  feat(health): health check endpoints

Non-code:
  docs(readme): update setup instructions
  chore(deps): update FastAPI to 0.104.1
  ci(tests): add pytest configuration
```

### 4.4 Body Guidelines

- Explain WHAT changed and WHY, not HOW
- Keep lines under 72 characters
- Separate from subject with blank line
- Use bullet points for multiple changes
- Reference issues: "Fixes #123" or "Relates to #456"

### 4.5 Footer Guidelines

```
Closes #123
Fixes #456
Relates to #789
BREAKING CHANGE: description of what broke
```

---

## Step 5: Feature Branch Workflow for Story 1.1

### 5.1 Create Feature Branch

```bash
# Start from develop and ensure it's up to date
git checkout develop
git pull origin develop

# Create feature branch for Story 1.1
git checkout -b feature/story-1.1-infrastructure

# Push to GitHub
git push -u origin feature/story-1.1-infrastructure
```

### 5.2 Development Workflow

**During development:**

```bash
# Make changes to code
# Example:
touch app/__init__.py
touch app/main.py
touch app/config.py
# ... etc

# Stage and commit changes
git add app/
git commit -m "feat(infrastructure): initialize FastAPI application structure

- Create app package with main.py entry point
- Add config.py with Pydantic Settings for environment variables
- Configure logging with structured JSON format
- Support both development and production environments

Relates to #1 Story 1.1"

# Continue with more commits
git add tests/
git commit -m "test(health): add health check endpoint tests

- Test GET /health returns 200 with correct structure
- Test GET /health/detailed includes component status
- Add pytest fixtures for database mocking

Relates to #1 Story 1.1"

# Push commits regularly
git push origin feature/story-1.1-infrastructure
```

### 5.3 Create Pull Request

**On GitHub:**

1. Go to repository
2. Click "Compare & pull request"
3. Set:
   - **Base:** develop
   - **Compare:** feature/story-1.1-infrastructure
4. Fill PR template:

```markdown
## Description
Implements Story 1.1: Initialisation de l'infrastructure & Cœur FastAPI

This PR sets up the FastAPI project structure with Supabase connection and Render deployment configuration.

## Type of Change
- [ ] New feature
- [x] Bug fix
- [ ] Documentation
- [ ] Refactor
- [ ] Performance improvement

## Related Issue
Closes #1 Story 1.1

## Testing
- [x] Unit tests added
- [x] Integration tests manual
- [x] Tested on Render free tier

## Checklist
- [x] Code follows project style guide
- [x] Documentation updated
- [x] Comments added for complex logic
- [x] No breaking changes
- [x] Tests pass locally

## Deployment Notes
- Environment variables: See .env.example
- Render deployment: Push to main to trigger deploy
```

### 5.4 Merge to Develop

After approval:

```bash
# GitHub will automatically merge when approved
# Or manually:

git checkout develop
git pull origin develop
git merge --no-ff feature/story-1.1-infrastructure
git push origin develop

# Delete feature branch locally and remotely
git branch -d feature/story-1.1-infrastructure
git push origin --delete feature/story-1.1-infrastructure
```

---

## Step 6: Code Documentation Standards

### 6.1 Python Docstring Format (Google Style)

```python
def get_health_status() -> Dict[str, Any]:
    """Check system health and component status.
    
    Returns a detailed health report including API, database,
    and external service status.
    
    Returns:
        Dict[str, Any]: Health status with structure:
            {
                "status": "healthy|degraded|unhealthy",
                "components": {
                    "api": "ok|error",
                    "database": "ok|error",
                    "timestamp": "2026-02-05T14:30:00Z"
                }
            }
    
    Raises:
        ConnectionError: If database connection fails permanently
    
    Example:
        >>> status = get_health_status()
        >>> if status['status'] == 'healthy':
        ...     print("System operational")
    """
    pass
```

### 6.2 Module Docstrings

```python
"""Health check endpoints for system monitoring.

This module provides endpoints to verify:
- API server availability
- Database connectivity
- External service dependencies

Endpoints:
    GET /health: Simple liveness probe
    GET /health/detailed: Full system diagnostics
"""
```

### 6.3 Inline Comments

```python
# Do: Explain WHY, not WHAT
# The database connection needs time to initialize after
# Render cold start, so we retry up to 3 times
retry_count = 0
max_retries = 3

# Avoid: Stating the obvious
# Increment retry count
retry_count += 1
```

### 6.4 Type Hints

```python
from typing import Optional, Dict, List, Any
from datetime import datetime

def process_checkin(
    user_id: str,
    message: str,
    sentiment: Optional[str] = None
) -> Dict[str, Any]:
    """Process a user check-in message."""
    pass
```

---

## Step 7: README Structure

### 7.1 Main README.md

```markdown
# Focus & Flow

Telegram-based productivity bot with AI coaching.

## Quick Start

### Prerequisites
- Python 3.11+
- Supabase account (free tier)
- Render account (free tier)
- Telegram Bot Token

### Installation

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Configure .env
5. Run locally

### Deployment

Deploy to Render with GitHub integration.

## Development

### Setting Up Development Environment

1. Clone repo
2. Create virtual env: `python -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dev deps: `pip install -r requirements-dev.txt`
5. Run tests: `pytest`

### Git Workflow

See [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md)

### Code Style

See [CODE_STYLE.md](./CODE_STYLE.md)

## Project Structure

```
app/
├── main.py           # FastAPI entry point
├── config.py         # Environment configuration
├── models/           # Data models
├── services/         # Business logic
├── routes/           # API endpoints
└── utils/            # Utilities
```

## Testing

Run tests with pytest:
```bash
pytest
pytest -v              # Verbose
pytest --cov          # With coverage
pytest -k health      # Specific test
```

## Documentation

- [Architecture](./docs/ARCHITECTURE.md)
- [API Reference](./docs/API.md)
- [Database Schema](./docs/DATABASE.md)

## License

MIT License

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)
```

### 7.2 CONTRIBUTING.md

```markdown
# Contributing to Focus & Flow

## Code of Conduct

Be respectful and constructive.

## Getting Started

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes
4. Run tests: `pytest`
5. Commit with conventional commits
6. Push to branch
7. Create Pull Request

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Examples in [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md)

## Pull Request Process

1. Update README if needed
2. Add/update tests
3. Ensure all tests pass
4. Fill PR template completely
5. Request review
6. Address feedback
7. Merge when approved

## Code Style

Run formatters before committing:
```bash
black app/
pylint app/
```

See [CODE_STYLE.md](./CODE_STYLE.md) for details.
```

### 7.3 CODE_STYLE.md

```markdown
# Code Style Guide

## Python

### Formatting
- Use Black (line length: 88)
- Run before commit: `black app/`

### Linting
- Use Pylint
- Target score: >8.0
- Run: `pylint app/`

### Type Hints
- Use type hints on all functions
- Example:
  ```python
  def get_user(user_id: str) -> Optional[User]:
      pass
  ```

### Docstrings
- Use Google style
- Include examples
- Document raises and returns

### Naming
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private: prefix with `_`

### Imports
- Group: stdlib, third-party, local
- Order: alphabetical within groups
- One import per line (with exceptions)

## Git Commits

See [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md)

## Documentation

- Use Markdown
- Include code examples
- Keep line length at 80 chars for .md files
```

### 7.4 BRANCHING_STRATEGY.md

```markdown
# Git Branching Strategy

## Overview

We use Git Flow branching model:

```
main (production)
  ↑ PR from release/develop
develop (integration)
  ↑ PR from feature/bugfix
feature/* (development)
release/* (release prep)
hotfix/* (urgent fixes)
```

## Branch Naming

- `feature/story-X-Y-description` - New features
- `bugfix/issue-123-description` - Bug fixes
- `hotfix/issue-456-description` - Urgent fixes
- `release/vX.Y.Z` - Release preparation

## Workflow

### Feature Development

1. Create feature branch from `develop`
2. Make changes and commits
3. Create Pull Request to `develop`
4. Request review
5. Address feedback
6. Merge when approved
7. Delete feature branch

### Commit Messages

Use Conventional Commits format.

Examples:
- `feat(health): add detailed health check`
- `fix(database): handle connection timeout`
- `docs(readme): update setup instructions`
- `test(api): add endpoint tests`

### Pull Request Process

1. Base: `develop`
2. Compare: `feature/...`
3. Fill PR template
4. Request review
5. CI must pass
6. Require 1+ approval
7. Merge with "Squash and merge" for features

## Release Process

1. Create `release/vX.Y.Z` from `develop`
2. Update version in code
3. Create PR to `main`
4. Tag merge commit: `vX.Y.Z`
5. Merge back to `develop`

## Hotfix Process

1. Create `hotfix/issue-id` from `main`
2. Fix issue with conventional commit
3. Create PR to both `main` and `develop`
4. Tag merge to `main`
5. Merge to `develop`
```

---

## Step 8: CI/CD Setup

### 8.1 GitHub Actions Workflows

**Create: `.github/workflows/tests.yml`**

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Lint with pylint
      run: pylint app/ --fail-under=8.0
    
    - name: Format check with black
      run: black --check app/
    
    - name: Run tests with pytest
      run: pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## Step 9: Initial Repository Commit

### 9.1 Create All Documentation Files

```bash
git checkout develop

# Create files as documented above
touch .gitignore .gitattributes .env.example
touch CONTRIBUTING.md CODE_STYLE.md BRANCHING_STRATEGY.md
mkdir -p .github/workflows
touch .github/workflows/tests.yml
```

### 9.2 Initial Commit

```bash
git add .

git commit -m "chore: initialize repository with git workflow and documentation

- Add .gitignore for Python and environment
- Add .gitattributes for consistent line endings
- Add .env.example with configuration template
- Add GitHub Actions CI/CD workflow
- Add contribution guidelines
- Add code style documentation
- Add branching strategy documentation
- Add .github workflow templates

This establishes professional development practices before
feature development begins."

git push origin develop
```

---

## Step 10: Ready for Development

After completing the above setup:

1. ✅ Repository initialized on GitHub
2. ✅ Git Flow branching structure in place
3. ✅ Conventional Commits conventions documented
4. ✅ Code style standards established
5. ✅ CI/CD pipeline configured
6. ✅ Documentation templates created
7. ✅ Branch protection rules enabled

**Developer can now:**
- Create feature branch for Story 1.1
- Follow commit conventions
- Write properly documented code
- Use PR workflow for code review
- Automated tests on every commit

---

## Quick Reference Commands

```bash
# Clone repo
git clone https://github.com/[USERNAME]/project_goal_management.git

# Create feature branch
git checkout -b feature/story-1.1-infrastructure

# Commit with conventional format
git commit -m "feat(infrastructure): initialize FastAPI app

Description here"

# Push branch
git push -u origin feature/story-1.1-infrastructure

# Update from develop
git fetch origin
git rebase origin/develop

# Create PR
# Go to GitHub and create PR from feature branch to develop

# Switch branches
git checkout develop
git checkout feature/story-1.1-infrastructure

# Delete branch
git branch -d feature/story-1.1-infrastructure
git push origin --delete feature/story-1.1-infrastructure

# View commit history
git log --oneline --graph --all

# Check status
git status
git diff
```

---

**✅ Repository Setup Complete - Ready for Story 1.1 Development**
