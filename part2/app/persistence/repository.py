"""
In-memory repository implementation for storing and managing objects.
This will be replaced with a database-backed solution in Part 3.
"""


class InMemoryRepository:
    """
    In-memory storage for entities.
    Provides basic CRUD operations for objects.
    """

    def __init__(self):
        """Initialize the repository with an empty storage dictionary."""
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the repository.

        Args:
            obj: Object with an 'id' attribute to be stored
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id: The unique identifier of the object

        Returns:
            The object if found, None otherwise
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Retrieve all objects from the repository.

        Returns:
            List of all stored objects
        """
        return list(self._storage.values())

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
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
        return obj

    def delete(self, obj_id):
        """
        Delete an object from the repository.

        Args:
            obj_id: The unique identifier of the object

        Returns:
            True if the object was deleted, False otherwise
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
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
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
