"""Compatibility entry point for ``uvicorn app:app``."""

from expense_tracker.main import app

__all__ = ["app"]
