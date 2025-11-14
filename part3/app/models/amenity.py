"""
Amenity model for the HBnB application.
"""
import uuid
from datetime import datetime


class Amenity:
    """
    Amenity entity representing an amenity that can be associated with places.
    """

    def __init__(self, name):
        """
        Initialize a new Amenity.

        Args:
            name (str): The name of the amenity
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def validate(self):
        """
        Validate amenity attributes.

        Raises:
            ValueError: If validation fails
        """
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Amenity name is required")
        if len(self.name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")

    def update(self, data):
        """
        Update amenity attributes.

        Args:
            data (dict): Dictionary containing attributes to update
        """
        if 'name' in data:
            self.name = data['name']

        self.updated_at = datetime.utcnow()
        self.validate()

    def to_dict(self):
        """
        Convert amenity to dictionary representation.

        Returns:
            dict: Dictionary representation of the amenity
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
