# Python Rules

## Code Style

1. Follow PEP 8 style guidelines
2. Use type hints for function parameters and return values
3. Maximum line length: 100 characters
4. Use f-strings for string formatting

## Type Hints

```python
# ✅ Good - full type hints
from typing import Optional, List, Dict

def get_user(user_id: int) -> Optional[User]:
    """Fetch a user by ID."""
    pass

def process_items(items: List[str]) -> Dict[str, int]:
    """Process items and return counts."""
    return {item: len(item) for item in items}

# ❌ Bad - no type hints
def get_user(user_id):
    pass
```

## Project Structure

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Error Handling

```python
# ✅ Good - specific exceptions, logging
import logging

logger = logging.getLogger(__name__)

def process_data(data: dict) -> Result:
    try:
        validated = validate(data)
        return Result(success=True, data=validated)
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        return Result(success=False, error=str(e))
    except Exception as e:
        logger.exception("Unexpected error in process_data")
        raise

# ❌ Bad - bare except, no logging
def process_data(data):
    try:
        return validate(data)
    except:
        return None
```

## Documentation

```python
def calculate_score(
    attempts: int,
    time_seconds: float,
    multiplier: float = 1.0
) -> int:
    """
    Calculate the final score based on game performance.
    
    Args:
        attempts: Number of attempts made
        time_seconds: Time taken in seconds
        multiplier: Score multiplier (default 1.0)
    
    Returns:
        The calculated score as an integer
    
    Raises:
        ValueError: If attempts is negative or time_seconds is zero
    
    Example:
        >>> calculate_score(3, 45.5, 1.5)
        1250
    """
    pass
```

## Imports

```python
# Standard library
import os
import json
from pathlib import Path
from typing import Optional, List

# Third-party
import requests
from pydantic import BaseModel

# Local
from .models import User
from .utils import format_date
```
