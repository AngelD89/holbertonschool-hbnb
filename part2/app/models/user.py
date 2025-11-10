"""
User model for the HBnB application.
"""
import uuid
from datetime import datetime
import re


class User:
    """
    User entity representing a user in the system.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User.

        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email address
            is_admin (bool): Whether the user is an administrator
        """
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.places = []  # List of places owned by this user
        self.reviews = []  # List of reviews written by this user

    def validate(self):
        """
        Validate user attributes.

        Raises:
            ValueError: If validation fails
        """
        if not self.first_name or len(self.first_name.strip()) == 0:
            raise ValueError("First name is required")
        if len(self.first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")

        if not self.last_name or len(self.last_name.strip()) == 0:
            raise ValueError("Last name is required")
        if len(self.last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")

        if not self.email or len(self.email.strip()) == 0:
            raise ValueError("Email is required")

        # Basic email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")

    def update(self, data):
        """
        Update user attributes.

        Args:
            data (dict): Dictionary containing attributes to update
        """
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'email' in data:
            self.email = data['email']

        self.updated_at = datetime.utcnow()
        self.validate()

    def add_place(self, place):
        """Add a place to the user's owned places."""
        self.places.append(place)

    def add_review(self, review):
        """Add a review to the user's reviews."""
        self.reviews.append(review)

    def to_dict(self):
        """
        Convert user to dictionary representation.

        Returns:
            dict: Dictionary representation of the user
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
