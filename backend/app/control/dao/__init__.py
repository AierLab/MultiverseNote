# app/dao/__init__.py

from .historyDataManager import HistoryManager
from .vectorDataManager import VectorEmbeddingManager
from .configDataManager import ConfigManager

# Optional: Initialize dao connection here if necessary
# This could be a setup for a SQLAlchemy dao engine or similar

# Export the dao classes for easy import elsewhere in your application
__all__ = ['HistoryManager', 'VectorEmbeddingManager']
