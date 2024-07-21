# app/database/__init__.py

from .historyStore import HistoryStore
from .vectorStore import VectorStore

# Optional: Initialize database connection here if necessary
# This could be a setup for a SQLAlchemy database engine or similar

# Export the database classes for easy import elsewhere in your application
__all__ = ['HistoryStore', 'VectorStore']
