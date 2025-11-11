"""
Review model for the HBnB application.
"""
import uuid
from datetime import datetime


class Review:
    """
    Review entity representing a review of a place by a user.
    """

    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review.

        Args:
            text (str): The review text
            rating (int): Rating from 1 to 5
            place (Place): The place being reviewed
            user (User): The user who wrote the review
        """
        self.id = str(uuid.uuid4())
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def validate(self):
        """
        Validate review attributes.

        Raises:
            ValueError: If validation fails
        """
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Review text is required")

        if self.rating is None:
            raise ValueError("Rating is required")
        if not isinstance(self.rating, int) or self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        if not self.place:
            raise ValueError("Place is required")

        if not self.user:
            raise ValueError("User is required")

    def update(self, data):
        """
        Update review attributes.

        Args:
            data (dict): Dictionary containing attributes to update
        """
        if 'text' in data:
            self.text = data['text']
        if 'rating' in data:
            self.rating = data['rating']

        self.updated_at = datetime.utcnow()
        self.validate()

    def to_dict(self):
        """
        Convert review to dictionary representation.

        Returns:
            dict: Dictionary representation of the review
        """
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
