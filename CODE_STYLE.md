# Code Style Guide - Focus & Flow

## Python Code Style

### Overview

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with the following tools:
- **Black** for code formatting (line length: 88)
- **Pylint** for code analysis (target score: >8.0)
- **Type hints** on all functions
- **Google style** docstrings

### Running Tools

```bash
# Format code with Black
black app/

# Check formatting without changing
black --check app/

# Lint code with Pylint
pylint app/

# Get Pylint score
pylint app/ --exit-zero | grep "rated"
```

## Formatting

### Black

Black is opinionated and non-configurable. Just run it:

```bash
black app/
```

**Key rules:**
- Line length: 88 characters
- String quotes: Double quotes preferred
- Trailing commas: Used for multi-line structures
- Spaces around operators
- 4 spaces for indentation

### Before Committing

Always format before committing:

```bash
# Format all Python files
black app/
black tests/

# Check if formatted correctly
black --check app/ tests/

# Commit only after formatting
git add .
git commit -m "..."
```

## Linting with Pylint

### Configuration

Pylint is configured with sensible defaults. Run:

```bash
pylint app/
```

**Target score: >8.0 out of 10**

### Common Issues

| Issue | Solution |
|-------|----------|
| `missing-docstring` | Add docstring to function/module |
| `line-too-long` | Black will fix automatically |
| `too-many-arguments` | Refactor to use Config class |
| `invalid-name` | Use snake_case for functions, PascalCase for classes |

### Disabling Warnings

Only when justified:

```python
# pylint: disable=line-too-long
long_variable = "This is a really long line that Black formats correctly"

# pylint: disable=too-many-arguments
def process(a, b, c, d, e, f):  # Consider refactoring
    pass
```

## Type Hints

### Always Use Type Hints

```python
# Good
def get_user(user_id: str) -> Optional[User]:
    pass

def process_items(items: List[str]) -> Dict[str, Any]:
    pass

# Bad (no type hints)
def get_user(user_id):
    pass
```

### Typing Imports

```python
from typing import Optional, List, Dict, Any, Tuple, Union
from typing import Callable, Generator, Iterator
```

### Common Patterns

```python
from typing import Optional, Dict, List, Any

# Optional value
def find_user(user_id: str) -> Optional[Dict[str, Any]]:
    pass

# List of items
def get_all_users() -> List[str]:
    pass

# Dictionary
def get_config() -> Dict[str, str]:
    pass

# Union types
def process(value: Union[str, int]) -> Union[str, None]:
    pass

# Callable (function)
def execute_async(callback: Callable[[str], None]) -> None:
    pass

# Generator
def read_lines() -> Generator[str, None, None]:
    pass
```

## Docstrings

### Google Style Format

```python
def calculate_success_rate(
    completed: int,
    total: int,
    period: str = "week"
) -> float:
    """Calculate user success rate for given period.
    
    Computes the percentage of completed objectives/habits
    relative to total for the specified time period.
    
    Args:
        completed: Number of completed items
        total: Total number of items
        period: Time period ('day', 'week', 'month'). Defaults to 'week'
        
    Returns:
        Success rate as float (0.0 to 1.0)
        
    Raises:
        ValueError: If total is 0 or period is invalid
        DatabaseError: If query fails
        
    Example:
        >>> rate = calculate_success_rate(7, 10, 'week')
        >>> print(f"Success: {rate * 100:.1f}%")
        Success: 70.0%
    """
    if total == 0:
        raise ValueError("Total cannot be zero")
    
    if period not in ("day", "week", "month"):
        raise ValueError(f"Invalid period: {period}")
    
    return completed / total
```

### Sections

**Args:**
- Parameter name and type
- Description of what it does
- Default value if applicable

**Returns:**
- Type and description of return value
- Multiple return values if tuple: `tuple: (str, int) - name and age`

**Raises:**
- Exception type and when it's raised
- Multiple exceptions possible

**Example:**
- Show typical usage
- Use `>>>` for Python shell examples
- Include expected output

### Module Docstrings

```python
"""Health check endpoints for system monitoring.

This module provides endpoints to verify system health including:
- API server availability
- Database connectivity
- External service status

Endpoints:
    GET /health: Simple liveness probe
    GET /health/detailed: Full system diagnostics
    
Example:
    >>> from app.routes import health
    >>> status = health.get_health_status()
    >>> print(status['status'])
"""
```

## Naming Conventions

### Variables and Functions

**Use snake_case:**

```python
# Good
user_id = "12345"
completion_rate = 0.85
def get_user_habits(user_id: str) -> List[str]:
    pass

# Bad
userId = "12345"
completionRate = 0.85
def getUserHabits(user_id: str):
    pass
```

### Classes

**Use PascalCase:**

```python
# Good
class UserCheckIn:
    pass

class HealthStatus:
    pass

# Bad
class user_check_in:
    pass

class healthStatus:
    pass
```

### Constants

**Use UPPER_CASE:**

```python
# Good
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
API_RATE_LIMIT = 1000

# Bad
max_retries = 3
defaultTimeout = 30
api_rate_limit = 1000
```

### Private Functions/Variables

**Prefix with underscore:**

```python
class User:
    def __init__(self, user_id: str):
        self._user_id = user_id  # Private
        
    def _validate_user_id(self) -> bool:  # Private method
        pass
    
    def get_id(self) -> str:  # Public
        return self._user_id
```

## Imports

### Organization

```python
# 1. Standard library imports
import os
import json
from datetime import datetime
from typing import Optional, Dict, List

# 2. Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from supabase import create_client

# 3. Local/application imports
from app.config import settings
from app.models.user import User
from app.services.database import get_supabase_client
```

### Rules

- Group imports by category
- Alphabetical order within groups
- One import per line (exceptions: `from ... import a, b, c` if related)
- Blank line between groups

### Avoid

```python
# Bad: unused imports
import os  # Never used

# Bad: wildcard imports
from app.models import *

# Bad: circular imports (refactor if needed)
# app/models.py imports from app/services.py
# app/services.py imports from app/models.py
```

## Functions

### Keep Functions Focused

```python
# Good: Single responsibility
def validate_email(email: str) -> bool:
    """Check if email format is valid."""
    return "@" in email and "." in email.split("@")[1]

def send_email(to: str, subject: str, body: str) -> bool:
    """Send email and return success status."""
    pass

# Bad: Too many responsibilities
def validate_and_send_email(email: str, subject: str, body: str) -> bool:
    """Validate email AND send it AND log result."""
    pass
```

### Function Length

- Prefer functions under 50 lines
- Break large functions into smaller ones
- Extract complex logic into helper functions

### Error Handling

```python
# Good: Specific exceptions
def get_user_habits(user_id: str) -> List[str]:
    """Get user's habits.
    
    Raises:
        ValueError: If user_id is empty
        DatabaseError: If database query fails
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")
    
    try:
        habits = db.query_habits(user_id)
        return habits
    except Exception as e:
        raise DatabaseError(f"Failed to get habits: {e}") from e

# Bad: Generic exception
def get_user_habits(user_id):
    try:
        return db.query_habits(user_id)
    except Exception:
        return []
```

## Comments

### Use Comments Sparingly

Comments should explain **WHY**, not **WHAT**:

```python
# Good: Explains the reason
# Render free tier spins down after 15 min inactivity.
# Use exponential backoff to avoid waking up the instance repeatedly.
def retry_with_backoff(max_retries: int = 3) -> bool:
    pass

# Bad: Restates the code
# Increment retry count
retry_count += 1

# Bad: Obvious from code
# Check if user exists
if user is None:
    pass
```

### Complex Logic

For complex algorithms, add brief comments:

```python
def calculate_cooling_score(days_inactive: int) -> float:
    """Calculate cooling algorithm score.
    
    Cooling prevents notification fatigue. Score increases
    with inactivity: 0 (active) to 1.0 (full cooling).
    
    Formula: score = days_inactive / 30 (capped at 1.0)
    """
    return min(days_inactive / 30, 1.0)
```

## Code Organization

### Module Structure

```python
"""Module docstring at top."""

# Imports
from typing import Optional
from fastapi import FastAPI

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Private functions (if any)
def _helper_function() -> None:
    pass

# Public classes
class User:
    pass

# Public functions
def get_user(user_id: str) -> Optional[User]:
    pass

# Main entry point (if applicable)
if __name__ == "__main__":
    pass
```

### Class Structure

```python
class HealthStatus:
    """System health check result."""
    
    # Class variables
    DEFAULT_TIMEOUT = 5
    
    def __init__(self, status: str):
        # Instance variables
        self.status = status
        self._created_at = datetime.now()
    
    def __str__(self) -> str:
        """String representation."""
        return f"HealthStatus({self.status})"
    
    # Public methods
    def is_healthy(self) -> bool:
        """Check if system is healthy."""
        return self.status == "healthy"
    
    # Private methods
    def _validate_status(self) -> bool:
        """Validate status value."""
        pass
```

## Checklist Before Commit

- [ ] Code formatted: `black app/`
- [ ] Linting passes: `pylint app/` (>8.0)
- [ ] All tests pass: `pytest`
- [ ] Type hints on functions: ✓
- [ ] Docstrings on public functions: ✓
- [ ] No unused imports: ✓
- [ ] No commented code: ✓
- [ ] Commit message conventional: ✓
- [ ] No secrets in code: ✓

---

Questions? Check [CONTRIBUTING.md](./CONTRIBUTING.md) or [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md)
