"""
SQLAlchemy repository implementation for database persistence.
"""
from app.models.base import db


class SQLAlchemyRepository:
    """
    Repository class for database operations using SQLAlchemy.
    """

    def __init__(self, model):
        """
        Initialize the repository with a specific model.

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    def add(self, obj):
        """
        Add an object to the database.

        Args:
            obj: Object to be stored
        """
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id: The unique identifier of the object

        Returns:
            The object if found, None otherwise
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """
        Retrieve all objects from the database.

        Returns:
            List of all stored objects
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        Update an object with new data.

        Args:
            obj_id: The unique identifier of the object
            data: Dictionary containing the attributes to update

        Returns:
            The updated object if found, None otherwise
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    def delete(self, obj_id):
        """
        Delete an object from the database.

        Args:
            obj_id: The unique identifier of the object

        Returns:
            True if the object was deleted, False otherwise
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute value.

        Args:
            attr_name: The name of the attribute to search by
            attr_value: The value to match

        Returns:
            The first object that matches, None otherwise
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
