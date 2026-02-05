# Contributing to Focus & Flow

Thank you for your interest in contributing to Focus & Flow! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites
- Python 3.11+
- Git
- GitHub account

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork locally:**
   ```bash
   git clone https://github.com/[YOUR_USERNAME]/project_goal_management.git
   cd project_goal_management
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Create a feature branch:**
   ```bash
   git checkout -b feature/story-X-Y-description
   ```

## Making Changes

### Commit Message Format

Use **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only
- `style`: Changes that don't affect code meaning (formatting, whitespace)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Code change that improves performance
- `test`: Adding or updating tests
- `chore`: Changes to build process, dependencies, tools
- `ci`: Changes to CI/CD configuration

### Commit Scope Examples
- `infrastructure` - Project setup, FastAPI app
- `database` - Supabase connection
- `deployment` - Render configuration
- `telegram` - Telegram bot integration
- `nlu` - NLU/AI pipeline
- `health` - Health check endpoints
- `auth` - Authentication/security
- `api` - API endpoints

### Commit Examples

```bash
# Good: Clear type, scope, and descriptive message
git commit -m "feat(infrastructure): initialize FastAPI application structure

- Create app package with main.py entry point
- Add config.py with Pydantic Settings
- Configure structured logging with JSON format
- Support both development and production environments

Relates to Story 1.1"

git commit -m "test(health): add health check endpoint tests

- Test GET /health returns 200 with correct structure
- Test GET /health/detailed includes component status
- Add pytest fixtures for mocking

Relates to Story 1.1"

git commit -m "fix(database): handle connection timeout gracefully

The connection timeout was causing health checks to fail.
Now implements exponential backoff retry strategy with
max 3 attempts before reporting unhealthy status.

Closes #42"

git commit -m "docs(readme): update development setup instructions

Include sections for:
- Virtual environment creation
- Dependency installation
- Running tests locally
- Deploying to Render"
```

## Code Style

### Python Code Style

Run formatters **before committing**:

```bash
# Format with Black (line length: 88)
black app/

# Check with Pylint (target score: >8.0)
pylint app/
```

See [CODE_STYLE.md](./CODE_STYLE.md) for detailed guidelines.

### Type Hints

Always use type hints on function signatures:

```python
from typing import Optional, Dict, Any

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID.
    
    Args:
        user_id: The user's Telegram ID
        
    Returns:
        User data or None if not found
    """
    pass
```

### Docstrings

Use Google style docstrings:

```python
def process_checkin(
    user_id: str,
    message: str,
    sentiment: Optional[str] = None
) -> Dict[str, Any]:
    """Process a user check-in message.
    
    Parses the message for intent and sentiment, then
    records the check-in in the database.
    
    Args:
        user_id: User's Telegram ID
        message: The check-in message text
        sentiment: Optional sentiment override
        
    Returns:
        Response dictionary with:
            - success: bool
            - check_in_id: str
            - message: str (response message)
            
    Raises:
        ValueError: If message is empty
        DatabaseError: If database insert fails
        
    Example:
        >>> result = process_checkin("12345", "30min workout done")
        >>> print(result['message'])
    """
    pass
```

## Testing

### Write Tests

Create tests in `tests/` directory:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_health.py

# Run specific test
pytest tests/test_health.py::test_health_endpoint
```

### Test Coverage

Aim for >80% coverage on critical paths:
- Database operations
- API endpoints
- Configuration loading
- Error handling

## Pull Request Process

### Before Creating PR

- [ ] Branch is up to date with `develop`
- [ ] All tests pass: `pytest`
- [ ] Code formatted: `black app/`
- [ ] Linting passes: `pylint app/` (score >8.0)
- [ ] Commits use conventional format
- [ ] No secrets or `.env` in commits
- [ ] README updated (if needed)
- [ ] Type hints on all new functions
- [ ] Docstrings on all new functions

### Create Pull Request

1. **Push your branch:**
   ```bash
   git push -u origin feature/story-X-Y-description
   ```

2. **Go to GitHub and create PR:**
   - Base: `develop`
   - Compare: `feature/story-X-Y-description`

3. **Fill PR template:**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] New feature
   - [ ] Bug fix
   - [ ] Documentation
   - [ ] Refactor
   
   ## Related Issue
   Closes #123
   
   ## Testing
   - [ ] Unit tests added
   - [ ] Manual testing done
   
   ## Checklist
   - [ ] Code follows style guide
   - [ ] Documentation updated
   - [ ] Tests pass
   - [ ] No breaking changes
   ```

4. **Address review feedback:**
   - Make changes on your branch
   - Push new commits
   - Don't force push (keeps review history)

5. **Merge after approval:**
   - Maintainer will merge PR
   - Feature branch can be deleted

## Git Workflow Summary

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/story-1.1-infrastructure

# 2. Make changes and commit
git add app/
git commit -m "feat(infrastructure): description"

# 3. Push to GitHub
git push -u origin feature/story-1.1-infrastructure

# 4. Create PR on GitHub (from web interface)

# 5. After approval, maintainer merges
# 6. Update local develop
git checkout develop
git pull origin develop

# 7. Delete local feature branch
git branch -d feature/story-1.1-infrastructure
```

## Questions?

- Check [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md) for detailed Git flow
- Check [CODE_STYLE.md](./CODE_STYLE.md) for code standards
- Open an issue for questions or concerns

Thank you for contributing! 🚀
