"""
Database models package.

This package contains all the SQLAlchemy ORM models.
Import all models here for easier access.
"""

from app.models.user import User
from app.models.saved_route import SavedRoute

__all__ = ["User", "SavedRoute"]
