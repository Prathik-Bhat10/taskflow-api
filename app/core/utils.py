"""Shared utility functions."""
from datetime import datetime, timezone


def _now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)