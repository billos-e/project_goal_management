# Development Standards - Focus & Flow

**Last Updated:** 2026-02-06  
**Effective From:** Step 1.1 Implementation  
**Audience:** AI Developers (Agents) & Technical Team

---

## Overview

Ce document consolide toutes les pratiques de développement validées par l'équipe technique pour Focus & Flow. **Une source unique de vérité** pour tous les agents développeurs.

---

## 1. Commit Message Format

### Rule: Ultra-Concise Conventional Commits

**Structure:**
```
<type>(<scope>): <subject>

<body (1-2 sentences max)>

<footer (if applicable)>
```

**Example (Good):**
```
feat(schemas): add humor_level (1-10) to User model

Enables FR-11: TARS tone customization per user preference.

Migration: 003_add_humor_level | Dependencies: None | Breaking: No
```

**Constraints:**
- Subject line: ≤50 characters
- Body: 1-2 sentences max, explain the *why* not the *what*
- No rambling or philosophical discussions in commit messages
- Footer required ONLY if touching `app/db/migrations/`

### Commit Types
- `feat` : New feature
- `fix` : Bug fix
- `docs` : Documentation only
- `style` : Code formatting (no logic change)
- `refactor` : Code reorganization (no functionality change)
- `test` : Test additions or fixes
- `chore` : Build, CI/CD, dependencies

### Migration Footer Format (DB changes only)
```
Migration: NNN_description
Dependencies: None | (or: Story X.Y description)
Breaking: Yes | No
```

---

## 2. Git Workflow (Git Flow)

### Branch Naming
- **Features:** `feature/story-X-Y-description`
- **Bugfixes:** `bugfix/issue-ID-description`
- **Hotfixes:** `hotfix/issue-ID-description`

### Workflow Steps

1. **Create feature branch from `develop`**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/story-1-1-infrastructure
   ```

2. **Develop & commit locally**
   - Follow Conventional Commits rules
   - Test locally before pushing
   - Push regularly to avoid long-lived local branches

3. **Push branch to GitHub**
   ```bash
   git push -u origin feature/story-1-1-infrastructure
   ```

4. **Create Pull Request (PR)**
   - Base: `develop`
   - **WAIT**: Announce PR to Billux and request approval before pushing
   - Once approved by Billux → proceed to merge
   - Never force-push without explicit authorization

5. **Merge to `develop` (after Billux approval)**
   - Merge via GitHub UI (recommended)
   - Delete feature branch locally & remotely after merge

6. **Merge `develop` → `main` (production deploy)**
   - Requires Billux validation
   - Triggers automatic Render deployment

### Important
- **No merging without approval** (ADR-007)
- **No force pushes** (`git push --force`) unless explicitly authorized
- **Tests must pass** in GitHub Actions before any merge

---

## 3. Code Style & Testing

### Python Code Style
- Use **Black** for formatting (line length: 88 chars)
- Use **Pylint** for linting (minimum score: 8.0)
- Type hints **mandatory** for all function signatures
- Docstrings: Google-style format for public functions

### Testing
- **GitHub Actions CI/CD** runs automatically on every push
- Tests must pass 100% before PR can be merged
- If tests fail:
  - Fix locally
  - Commit fix with message format: `fix(test): description`
  - Push new commit (do NOT force-push)
  - GitHub will re-run CI/CD automatically

### Pre-commit Hooks
- **NOT mandatory**
- Optional for local development to catch issues early
- CI/CD pipeline is the authoritative validation

---

## 4. Pull Request Process

### Before Creating PR
1. Ensure all commits follow Conventional Commits format
2. Run local tests (if possible)
3. Verify code follows style guidelines

### PR Title & Description
**Format:**
```
Story X.Y: Description

## Description
Implements [Story/Epic/Feature description]

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactor

## Related Issue
Closes #X (if applicable)

## Testing
- [ ] Unit tests added/updated
- [ ] All tests pass
- [x] Tested locally

## Checklist
- [x] Code follows style guide
- [x] Documentation updated
- [x] No breaking changes (unless intentional)
```

### Review & Approval
- Billux reviews complete PR
- If changes requested: make commits, push, CI/CD re-runs
- If approved: Billux merges
- Delete feature branch after merge

---

## 5. Database Migrations (ADR-003)

### File Location
All migrations in: `app/db/migrations/NNN_description.sql`

### Naming Convention
```
001_initial_schema.sql
002_add_timezone_to_users.sql
003_add_humor_level.sql
```

### Migration Footers in Commits
Every commit touching migrations MUST include:
```
Migration: NNN_description
Dependencies: None | (or specific Story/Epic)
Breaking: Yes | No
```

### Examples
**Backward compatible migration:**
```
feat(db): add optional habit_notes column

Enables FR-12: Users can add notes to habits.

Migration: 005_add_habit_notes | Dependencies: None | Breaking: No
```

**Migration with dependencies:**
```
feat(db): rename column user_status to cooling_status

Aligns schema with ADR-005 naming conventions.

Migration: 006_rename_user_status | Dependencies: Story 4.2 | Breaking: Yes
```

---

## 6. Approval Gates (ADR-007)

### Gate 1: Before Push
- Agent announces intention to create PR
- Billux approves concept
- Agent proceeds to push

### Gate 2: PR Review
- Agent creates PR on GitHub
- Billux reviews complete PR
- Feedback or approval

### Gate 3: Merge
- If approved: Billux merges to `develop`
- If feedback: Agent makes fixes, pushes new commits, Billux re-reviews

### Gate 4: Production Deploy
- Merge `develop` → `main` requires Billux validation
- Automatic Render deployment follows

---

## 7. Documentation Requirements

### Inline Code Documentation
- **Public functions:** Google-style docstrings mandatory
- **Private functions:** Docstrings recommended
- **Complex logic:** Inline comments explaining *why* not *what*
- **API endpoints:** FastAPI automatically generates Swagger docs

### Story/Feature Documentation
- Link to related Story/Epic in commit messages
- Update README if adding user-facing features
- Update CONTRIBUTING.md if changing development process

---

## 8. Common Workflows

### Sync with `develop`
```bash
git fetch origin
git rebase origin/develop
# If conflicts: resolve, then git rebase --continue
git push origin feature/story-X-Y
```

### Undo Last Commit (before push)
```bash
git reset --soft HEAD~1
# Make changes
git commit -m "corrected message"
```

### Fix Commit Message (before push)
```bash
git commit --amend -m "new message"
```

### After PR Merge
```bash
git checkout develop
git pull origin develop
git branch -d feature/story-X-Y
git push origin --delete feature/story-X-Y
```

---

## 9. Troubleshooting

### Tests Fail in GitHub Actions
1. Check the GitHub Actions output for error details
2. Reproduce locally
3. Fix code or tests
4. Commit with `fix(...)` prefix
5. Push new commit
6. GitHub Actions re-runs automatically

### Merge Conflicts
1. Sync feature branch: `git rebase origin/develop`
2. Resolve conflicts in files
3. `git add .` resolved files
4. `git rebase --continue`
5. `git push origin feature/story-X-Y` (may need force after rebase, ask Billux)

### Need to Rollback Production
1. Identify commit that caused issue
2. `git revert COMMIT_SHA` on `main`
3. Push to `main`
4. Render automatically deploys revert

---

## 10. Questions & Support

- **Git workflow questions:** See BRANCHING_STRATEGY.md
- **Code style questions:** See CODE_STYLE.md
- **Architecture questions:** See architecture.md
- **Contributing guidelines:** See CONTRIBUTING.md

---

**Last Review:** 2026-02-06  
**Next Review:** Post-Story-1.1 (Sprint 1)
