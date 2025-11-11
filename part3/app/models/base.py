"""
Base model for all database entities.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


class BaseModel(db.Model):
    """
    Base model class that provides common fields and methods for all entities.
    """
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Save the current instance to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance from the database."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """
        Update instance attributes with provided data.

        Args:
            data (dict): Dictionary containing attributes to update
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
