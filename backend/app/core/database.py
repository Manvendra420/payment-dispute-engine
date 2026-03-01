"""Database session and connection management."""

from typing import Generator
import logging

# Mock database session for development
# In production, this will be replaced with SQLAlchemy sessions

logger = logging.getLogger(__name__)


class DatabaseSession:
    """Mock database session."""
    
    def __init__(self):
        self.data = {}
    
    def save(self, model):
        """Save a model instance."""
        logger.debug(f"Saving model: {model.id}")
        return model
    
    def delete(self, model):
        """Delete a model instance."""
        logger.debug(f"Deleting model: {model.id}")
    
    def commit(self):
        """Commit changes."""
        logger.debug("Committing changes")
    
    def rollback(self):
        """Rollback changes."""
        logger.debug("Rolling back changes")


def get_db() -> Generator[DatabaseSession, None, None]:
    """Dependency for getting database session."""
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.rollback()
